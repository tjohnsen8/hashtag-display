import os
from flask import Flask, render_template, request
import CfInsta as cfi


application = Flask(__name__)
#APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@application.route('/', methods=['GET', 'POST'])
def home():
	ig = cfi.CfInstagram()
	media = ig.get_ig_updates() # saves to folder
	images = os.listdir(os.path.join(application.static_folder, "images"))
	images = images[::-1]
	return render_template('index.html', images=images)


if __name__ == '__main__':
	application.secret_key = os.urandom(12)
	application.run(host='0.0.0.0')