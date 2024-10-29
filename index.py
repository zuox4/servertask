from functools import wraps

import flask
from descope import descope_client, DescopeClient
from flask import Flask, request, jsonify, make_response
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models.User import db, User, Categoties
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
  r"/*" : {
   "origins" : "*" ,
   "methods" : [
    "GET" ,
    "POST" ,
    "PUT" ,
    "PATCH" ,
    "DELETE" ,
    "OPTIONS" ,
   ],
   "allow_headers" : [
    "Content-Type" ,
    "Authorization" ,
   ],
  }
}, )
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://default:sncjxh9prwt4@ep-wispy-dream-a48ro2xf.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123123'

admin = Admin(app, name='Добродел')
db.init_app(app)

try:
    descope_client = DescopeClient(project_id='P2msZFI0ktS3dFMvrH4S6l7x9yF5')  # initialize the descope client
except Exception as error:
    print("failed to initialize. Error:")
    print(error)


def token_required(f):  # auth decorator
    @wraps(f)
    def decorator(*args, **kwargs):
        session_token = None

        if 'Authorization' in request.headers:  # check if token in request
            auth_request = request.headers['Authorization']
            session_token = auth_request.replace('Bearer ', '')
        if not session_token:  # throw error
            return make_response(jsonify({"error": "❌ invalid session token!"}), 401)

        try:  # validate token
            jwt_response = descope_client.validate_session(session_token=session_token)
        except:
            return make_response(jsonify({"error": "❌ invalid session token!"}), 401)

        return f(jwt_response, *args, **kwargs)

    return decorator


with app.app_context():
    db.create_all()
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Categoties, db.session))


@app.route('/get_user', methods=['GET'])
@token_required
def get_user(jwt_response):
    try:
        email = jwt_response["email"]
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({'user': {'userName': user.username}}), 200
        else:
            return jsonify({'user': None})
    except:
        return jsonify({'user': None})


@app.route('/create_user', methods=['POST'])
@token_required
def create_user(jwt_response):
    email = jwt_response["email"]
    data = request.json
    username = data.get('username')
    user = User(email=email, username=username)
    db.session.add(user)
    db.session.commit()
    return jsonify({'user': {'userName': user.username, 'email': user.email}})


@app.route('/categories')
@token_required
def get_categories(jwt_response):
    email = jwt_response["email"]
    categories = Categoties.query.all()
    print(categories)
    data = [{'id': i.id, 'name': i.name} for i in categories]
    response = jsonify({'categories': data})
    return response


if __name__ == "__main__":
    app.run(debug=True)
