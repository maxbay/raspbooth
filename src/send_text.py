import os
import sys
from twilio.rest import TwilioRestClient

class sendText():

    def __init__(self,number,img_path):

        self.number = number

        self.send()

    def send(self):
        # put your own credentials here
        ACCOUNT_SID = "AC3f2b66d925a5c2564818587acdcb197e"
        AUTH_TOKEN = "335daf929a903ef7309962f996c728ce"

        ACCOUNT = "+13478686098"
        ALINE = "+15625878814"
        MAX = "+13152436255"
        SAMSON = "+15012831068"

        client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

        client.messages.create(
            to = MAX,
            from_ = ACCOUNT,
            body ="Hi beebz! Look what I did!",
            media_url = "http://i.imgur.com/N6CT5HF.png",
        )

    @staticmethod
    def cleanupNumber(number):
        #TODO: Make system for formatting numbers
        pass

if __name__ == "__main__":
    stxt = sendText('str1','str2')






