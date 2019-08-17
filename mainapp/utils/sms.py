import os

import requests
from dateutil import parser
import calendar
import environ
import logging

from mainapp.models import Volunteer, SmsJob

logger = logging.getLogger('send_sms')


def sms_sender(smsjobid, **kwargs):
    smsjob = SmsJob.objects.get(id=smsjobid)
    if smsjob.has_completed is True:
        logger.info('Job already complete')
        return
    root = environ.Path(__file__) - 3
    environ.Env.read_env(root('.env'))

    SMS_API_URL = os.environ.get("SMS_API")
    API_USERNAME = os.environ.get("SMS_USER")
    API_PASSWORD = os.environ.get("SMS_PASSWORD")

    district = kwargs['district']
    type = kwargs['type']
    area = kwargs['area']
    message = kwargs['message']

    logger.info(
        'Starting sms job.\nDistrict: {}, Type: {}, Area: {}, Message: {}'
        .format(district, type, area, message)
    )

    volunteers = Volunteer.objects.filter(district=district, area=area)
    if type != 'consent':
        volunteers.filter(has_consented=True)
    fail_count = 0
    for volunteer in volunteers:
        if type == 'consent':
            timestamp = parser.parse(str(volunteer.joined))
            timestamp = calendar.timegm(timestamp.utctimetuple())
            # Preparing unique URL
            url = 'http://keralarescue.in/c/' + str(volunteer.id) + "/" + str(timestamp)[-4:]
            message = "Thank you for registering as a volunteer on keralarescue. Please click here to confirm. " + url
        payload = {
            'username': API_USERNAME,
            'password': API_PASSWORD,
            'numbers': volunteer.phone,
            'message': message
        }

        response = requests.get(SMS_API_URL, params=payload)
        logger.info("Got {} as response for {} - {}".format(response.text, volunteer.name, volunteer.phone))
        if "402" not in response.text:
            fail_count += 1

    smsjob.failure = "{} sms failed out of {}".format(fail_count, volunteers.count())
    logger.info(smsjob.failure)
    smsjob.has_completed = True
    smsjob.save()


