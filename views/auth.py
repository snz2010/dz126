from flask import request, abort
from flask_restx import Resource, Namespace
from models import User, UserSchema
from setup_db import db
import calendar
import datetime
import jwt
import hashlib

auth_ns = Namespace('auth')
secret = 's3cR$eT'
algo = 'HS256'


@auth_ns.route('/')
class AuthView(Resource):
    # При POST-запросе на адрес /auth/ возвращается словарь с access_token и refresh token
    def post(self):
        req_json = request.json
        # Если в теле запроса отсутствуют поля username или password -> ответ с кодом 400
        username = req_json.get("username", None)
        password = req_json.get("password", None)
        if None in [username, password]:
            abort(400)
        # запрос к БД - по имени пользователя
        user = db.session.query(User).filter(User.username == username).first()
        # Если такой пользователь отсутствует в базе или пароль неверный :
        if user is None:
            return {"error": "Неверные учётные данные - user is None"}, 401
        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()

        if password_hash != user.password:
            return {"error": "Неверные учётные данные - password_hash != user.password"}, 401
        # выявление Имени и Группы пользователя
        data = {
            "username": user.username,
            "role": user.role
        }
        # генерация access_token
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)
        # генерация refresh_token
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)
        tokens = {"username": data["username"], "role": data["role"], "access_token": access_token,
                  "refresh_token": refresh_token, "EXP": data["exp"]}
        return tokens, 201

    # При PUT запросе (запрос должен содержать refresh token) на адрес /auth/
    # возвращается словарь с access_token и refresh token.
    # {
    #    "refresh_token": "refresh_token"
    # }
    def put(self):
        req_json = request.json
        refresh_token = req_json.get("refresh_token")
        # Если refresh_token отсутствует в запросе возвращать код 400
        if refresh_token is None:
            abort(400)
        try:
            data = jwt.decode(jwt=refresh_token, key=secret, algorithms=[algo])
        except Exception as e:
            abort(400)

        username = data.get("username")

        user = db.session.query(User).filter(User.username == username).first()

        data = {
            "username": user.username,
            "role": user.role
        }
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens, 201
