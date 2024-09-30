<!-- SPDX-License-Identifier: zlib-acknowledgement -->

app = Flask(__name__, static_folder='build', static_url_path='/')

@app.route('/')
def index():
  return app.send_static_file('index.html')


# install heroku cli

heroku container:login
heroku create <name-for-your-app>
# https://<name-for-your-app>.herokuapp.com/
heroku container:push web --app <name-for-your-app>
heroku container:release web --app <name-for-your-app>
