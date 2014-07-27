from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.json import JSONEncoder


app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RA'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///foo.db"


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        if hasattr(obj,'isoformat'):
            return obj.isoformat()
        else:
            return JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder

app.config.from_object('config')

db = SQLAlchemy(app)

import main
import serveries
import users
import dishdetails
