#!/usr/bin/python
#
# python-v4l2capture
#
# 2009, 2010 Fredrik Portstrom
#
# I, the copyright holder of this file, hereby release it into the
# public domain. This applies worldwide. In case this is not legally
# possible: I grant anyone the right to use this work for any
# purpose, without any conditions, unless such conditions are
# required by law.

import os
import v4l2capture
file_names = [x for x in os.listdir("/dev") if x.startswith("video")]
file_names.sort()
for file_name in file_names:
    path = "/dev/" + file_name
    print(path)
    try:
        video = v4l2capture.Video_device(path)
        driver, card, bus_info, capabilities = video.get_info()
        print("driver:\t\t{driver}\ncard:\t\t{card}"  \
              "\nbus info:\t\t{bus_info}"  \
              "\ncapabilities: {capabilities}".format(driver=driver,
                                                      card=card,
                                                      bus_info=bus_info,
                                                      capabilities=", ".join(capabilities)))
        video.close()
    except IOError, e:
        print("    " + str(e))
