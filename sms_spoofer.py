import requests
import urllib
import sys
import os.path

ERROR_API = "Error during API call"
ERROR_FILE = "The specified file does not exist"
URL = 'https://api.smsmode.com/http/1.6/'
PATH_SEND_SMS = "sendSMS.do"
PATH_SEND_SMS_BATCH = "sendSMSBatch.do"

"""
*    Function parameters:
*
*    - access_token (required)
*    - message (required)
*    - destinataires (required): Receivers separated by a comma
*    - emetteur (optional): Allows to deal with the sms sender
*    - option_stop (optional): Deal with the STOP sms when marketing send (cf. API HTTP documentation)
*    - batch_file_path (required for batch mode): The path of CSV file for sms in Batch Mode
"""


class ExempleClientHttpApi:

    # send SMS with GET method
    def send_sms_get(self, access_token, message, destinataires, emetteur, option_stop):

        final_url = (
                URL + PATH_SEND_SMS +
                '?accessToken=' + access_token +
                '&message=' + urllib.quote_plus(message.encode('iso-8859-15')) +
                '&numero=' + destinataires +
                '&emetteur=' + emetteur +
                '&stop=' + option_stop
        )
        r = requests.get(final_url)
        if not r:
            return ERROR_API
        return r.text

    # send SMS with POST method
    def send_sms_post(self, access_token, message, destinataires, emetteur, option_stop):

        final_url = URL + PATH_SEND_SMS
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        payload = {
            'accessToken': access_token,
            'message': message,
            'numero': destinataires,
            'emetteur': emetteur,
            'stop': option_stop
        }
        r = requests.post(final_url, data=payload, headers=headers)
        if not r:
            return ERROR_API
        return r.text

    # send SMS with POST method (Batch)
    def send_sms_batch(self, access_token, batch_file_path, option_stop):

        final_url = URL + PATH_SEND_SMS_BATCH + "?accessToken=" + access_token + "&stop=" + option_stop
        if not os.path.isfile(batch_file_path):
            return ERROR_FILE
        r = requests.post(final_url, files={'file': open(batch_file_path, 'rb')})
        if not r:
            return ERROR_API
        return r.text