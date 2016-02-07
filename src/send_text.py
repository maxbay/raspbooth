import os
import sys
from twilio.rest import TwilioRestClient

class sendText():

    def __init__(self,number,img_path):

        self.number = number

        self.send()

    def send(self):
        # put your own credentials here
        config = ConfigParser.ConfigParser()
        config.read('auth.ini')

        ACCOUNT_SID = config.get('twillo_credentials', 'ACCOUNT_SID')
        AUTH_TOKEN = config.get('twillo_credentials','AUTH_TOKEN')
        account = config.get('twillo_credentials','ACCOUNT')

        ALINE = "+15625878814"
        MAX = "+13152436255"
        SAMSON = "+15012831068"

        client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

        client.messages.create(
            to = MAX,
            from_ = account,
            body ="Hi beebz! Look what I did!",
            media_url = "http://i.imgur.com/N6CT5HF.png",
        )

    @staticmethod
    def cleanupNumber(number):
        #TODO: Make system for formatting numbers
        pass







