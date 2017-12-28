import wtforms


class ProfileForm(wtforms.Form):
    first_name = wtforms.StringField('First Name', validators=[wtforms.validators.InputRequired()])
    last_name = wtforms.StringField('Family Name', validators=[wtforms.validators.InputRequired()])
    email = wtforms.StringField('Email', validators=[wtforms.validators.InputRequired(), wtforms.validators.Email()])
