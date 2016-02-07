
from imgurpython import ImgurClient
from auth import authenticate
import ConfigParser

class Upload():
	def __init__(self,image_path):

		self.image_path = image_path

		self.client = authenticate()
		
		config = ConfigParser.ConfigParser()
		config.read('auth.ini')
		self.album = config.get('imgur_misc', 'album')

		self.sendToImgur()
		self.link = None


	def sendToImgur(self):

		config = {
			'album': self.album,
			'name':  'Photo',
			'title': 'Booth!',
			'description': 'PB stuff ;)'
		}

		print("Uploading image... ")
		image = self.client.client.upload_from_path(self.image_path, config=config, anon=False)
		self.link = image['link']
		print("Done")
		print("You can find it here: {0}".format(link))
