import io
import os
import base64
import falcon
import qrcode
import jinja2
import requests
from pusher import Pusher

from urllib.parse import urljoin

from falcon_multipart.middleware import MultipartMiddleware

from forms import ProfileForm

VISAGE_URL = os.getenv('VISAGE_URL', 'http://192.168.0.117:8083')
FACIAL_URL = os.getenv('FACIAL_URL', 'http://192.168.0.117:8082')


pusher = Pusher(
    app_id=os.getenv('PUSHER_APP_ID', 'app_id'),
    key=os.getenv('PUSHER_KEY', 'app_key'),
    secret=os.getenv('PUSHER_SECRET', 'secret'),
    cluster=os.getenv('PUSHER_CLUSTER', 'APP_CLUSTER'),
    host=os.getenv('PUSHER_HOST', '192.168.0.117'),
    port=os.getenv('PUSHER_PORT', 8081),
    ssl=False
)


def load_template(name):
    path = os.path.join('templates', name)
    with open(os.path.abspath(path), 'r') as fp:
        return jinja2.Template(fp.read())


def _base64_image(img):
    in_mem_file = io.BytesIO()
    img.save(in_mem_file, format = "PNG")
    # reset file pointer to start
    in_mem_file.seek(0)
    img_bytes = in_mem_file.read()

    base64_encoded_result_bytes = base64.b64encode(img_bytes)
    return 'data:image/png;base64,%s' % base64_encoded_result_bytes.decode('ascii')


def publish(channel, event_name, **kwargs):
    print('publishing to {channel} for event {event_name} {data}'.format(channel=channel, event_name=event_name, data=kwargs))
    pusher.trigger(channels=channel,
                   event_name=event_name,
                   data=kwargs)


class FaceResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = {
            'quote': (
                "I've always been more interested in "
                "the future than in the past."
            ),
            'author': 'Grace Hopper'
        }

        resp.media = quote

    def on_post(self, req, resp):
        """Handles POST requests"""
        resp.content_type = falcon.MEDIA_JSON

        file = req.get_param('file')
        files = {'file': (file.filename, file.file, file.type, {'Expires': '0'})}
        response = requests.post(FACIAL_URL,
                                 files=files)
        if response.ok is False:
            resp.media = {"message": "Could not test image: %s" % response.content}
            publish(channel='home', event_name='new-compliment', **resp.media)
        else:
            data = response.json()

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            if data.get('count', 0) > 0:
                # found at least one a number
                person = data.get('faces', [])[0]
                # order by distance, closest to furthers and pick the closest
                url = urljoin(VISAGE_URL, 'profile', person.get('id'))
                qr.add_data(url)
                qr.make(fit=True)

                resp.media = {
                    'message': 'Hi there %s' % person.get('id'),
                    'url': url,
                    'qr': _base64_image(img=qr.make_image()),
                    'faces': data.get('faces', [])[0]
                }

            else:
                url = urljoin(VISAGE_URL, 'profile')
                qr.add_data(url)
                qr.make(fit=True)

                resp.media = {
                    'message': 'I dont seem to know you, please tell me who you are',
                    'qr': _base64_image(img=qr.make_image()),
                }

            publish(channel='home', event_name='new-compliment', **{'message': resp.media.get('message')})


class ProfileResource:
    def on_get(self, req, resp, id=None):
        """Handles GET requests"""
        template = load_template('profile_form.j2')
        url = urljoin(VISAGE_URL, 'profile', id)
        form = ProfileForm()
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_HTML
        resp.body = template.render(form=form, url=url)

    def on_post(self, req, resp):
        form = ProfileForm(req.POST)
        if form.validate():
            pass

        resp.media = {}

api = falcon.API(middleware=[MultipartMiddleware()])

api.add_route('/', FaceResource())
api.add_route('/profile', ProfileResource())
api.add_route('/profile/{id}', ProfileResource())