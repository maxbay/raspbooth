import os
import sys
from twilio.rest import TwilioRestClient



# put your own credentials here
ACCOUNT_SID = "AC3f2b66d925a5c2564818587acdcb197e"
AUTH_TOKEN = "335daf929a903ef7309962f996c728ce"

ACCOUNT = "+13478686098"
ALINE = "+15625878814"
MAX = "+13152436255"

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

client.messages.create(
    to= MAX,
    from_= ACCOUNT,
    #body="Hey Bb! Good luck on the bar exam!",
    media_url="http://farm2.static.flickr.com/1075/1404618563_3ed9a44a3a.jpg",
)

