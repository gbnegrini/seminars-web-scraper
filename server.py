from os import environ
import from flask

app = flask.Flask(__name__)
app.run(host= '0.0.0.0', port=environ.get('PORT'))
