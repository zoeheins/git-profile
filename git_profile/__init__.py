from flask import Flask


app = Flask(__name__)
app.config.from_object('config')
from git_profile import views
app.register_blueprint(views.profiles)
