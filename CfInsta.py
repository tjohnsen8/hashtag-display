from InstagramAPI import InstagramAPI
from credentials import instagram_client_id, instagram_client_secret
from os import remove
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def get_largest_image(candidates):
	candidate = {}
	pixels = 0
	for cand in candidates:
		# pick the highest resolution one
		res = cand['height']*cand['width']
		if res > pixels:
			pixels = res
			candidate = cand

	return candidate


def get_caption(item):
	caption = ''
	if 'caption' in item.keys():
		if 'text' in item['caption'].keys():
			caption = item['caption']['text']
	return caption


class CfInstagram:
	def __init__(self):
		self.already_tweeted = []
		self.get_already_tweeted()
		self.api = InstagramAPI(instagram_client_id, instagram_client_secret)
		self.api.login()


	def get_already_tweeted(self):
		try:
			with open('twig.txt', 'r') as file:
				lines = file.readlines()
				for line in lines:
					self.already_tweeted.append(line.rstrip('\n'))
		except:
			print('error in file handling')


	def add_already_tweeted_to_file(self, id):
		try:
			with open('twig.txt', 'a') as file:
				file.write('{}\n'.format(str(id)))
		except:
			print('error in file handling')


	def save_image_from_candidate(self, url):
		response = requests.get(url)
		filename = url.split("/")[-1].split('?')[0]
		if response.status_code == 200 and not filename in self.already_tweeted:
			with open('static/images/' + filename, 'wb') as f:
				f.write(response.content)
			self.add_already_tweeted_to_file(filename)
			self.already_tweeted.append(filename)
		else:
			print('already tweeted')
			#remove(filename)
			filename = ''
		return filename
	

	def get_images_from_hashtag(self, hashtag, num_images, view_debug=False):
		images = []
		get_hashtag = self.api.getHashtagFeed(hashtag)

		if get_hashtag == False:
			return images

		for item in self.api.LastJson['items']:
			if 'image_versions2' in item.keys():
				candidate = get_largest_image(item['image_versions2']['candidates'])
				# get image 
				filename = self.save_image_from_candidate(candidate['url'])
				if filename != '':
					# get status, save as tuple
					caption = get_caption(item)
					images.append((filename, caption))
				if len(images) > num_images:
					break
				if view_debug:
					try:
						img = mpimg.imread(filename)
						imgplot = plt.imshow(img)
						plt.show()
					except OSError:
						print('not an image')
		return images


	def get_ig_updates(self):
		# get the hashtags from a file
		self.hashtags = []
		try:
			with open('ig_hashtags.txt') as file:
				lines = file.readlines()
				for line in lines:
					self.hashtags.append(line.rstrip('\n'))
		except:
			print('error handling hashtags file')

		updates = []
		for hashtag in self.hashtags:
			images = self.get_images_from_hashtag(hashtag, 3)
			updates.extend(images)
		return updates


if __name__ == '__main__':
	ig = CfInstagram();
	#images = ig.get_images_from_hashtag('healthystepsnutrition', 5)
	updates = ig.get_ig_updates()
	print(updates)
	#print(images)