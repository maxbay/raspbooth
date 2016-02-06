
from imgurpython import ImgurClient
from auth import authenticate
import ConfigParser

class Upload():
	def __init__(self,image_path):

		self.image_path = image_path

		self.client = authenticate()
		self.album = Upload.getAlbum('auth.ini')

		self.sendToImgur()


	def sendToImgur(self):

		config = {
			'album': self.album,
			'name':  'Photo',
			'title': 'Booth!',
			'description': 'PB stuff ;)'
		}

		print("Uploading image... ")
		image = self.client.client.upload_from_path(self.image_path, config=config, anon=False)
		print("Done")
		print("You can find it here: {0}".format(image['link']))



	@staticmethod
	def getAlbum(ini_file):
		config = ConfigParser.ConfigParser()
		config.read(ini_file)
		album = config.get('misc', 'album')

		return album