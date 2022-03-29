
from flask import request
from flask_restx import Resource, Namespace

from models import User, UserSchema
from setup_db import db
from views.functions import auth_required, admin_required, generate_password


users_ns = Namespace('users')
#USER_SALT = b"s3cR$eTs3c"



@users_ns.route('/')
class UsersView(Resource):
    def get(self):
        id = request.args.get("id")
        username = request.args.get("username")
        role = request.args.get("role")
        t = db.session.query(User)
        if id is not None:
            t = t.filter(User.id == id)
        if username is not None:
            t = t.filter(User.username == username)
        if role is not None:
            t = t.filter(User.role == role)
        all_users = t.all()
        res = UserSchema(many=True).dump(all_users)
        return res, 200
    # регистрация пользователя
    def post(self):
        req_json = request.json
        ent = User(**req_json)
        # Для пароля применим шифрование
        password = ent.password
        ent.password = generate_password(password)
        print(ent.password)
        db.session.add(ent)
        db.session.commit()
        return "", 201, {"location": f"/users/{ent.id}"}


@users_ns.route('/<int:bid>')
class UserView(Resource):
    def get(self, bid):
        b = db.session.query(User).get(bid)
        sm_d = UserSchema().dump(b)
        return sm_d, 200

    def put(self, bid):
        user = db.session.query(User).get(bid)
        req_json = request.json
        user.username = req_json.get("username")
        user.password = req_json.get("password")
        user.role = req_json.get("role")
        db.session.add(user)
        db.session.commit()
        return "", 204

    @admin_required
    def delete(self, bid):
        user = db.session.query(User).get(bid)
        db.session.delete(user)
        db.session.commit()
        return "", 204
