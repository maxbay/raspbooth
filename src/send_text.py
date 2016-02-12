import os
import sys
import ConfigParser
from twilio.rest import TwilioRestClient

class sendText():

    def __init__(self,img_url,number):

        self.img_url = img_url
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
            to = self.number,
            from_ = account,
            body ="Hi beebz! Look what I did!",
            media_url = self.img_url, #"http://i.imgur.com/uhd5uej.png",
        )
        print("Message sent to: {0}".format(self.number))



#if __name__ == '__main__':
#    stxt = sendText('str1','str2')





