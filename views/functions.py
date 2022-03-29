import calendar
import datetime
import hashlib

import jwt
from flask import request, abort
# import hmac
# import base64
JWT_ALGO = 'HS256'
JWT_SECRET = 's3cR$eT'

# def password_check(password_hash, other_password, salt, algo):
#     return hmac.compare_digest(
#         password_hash,
#         hashlib.pbkdf2_hmac(algo, generate_password(other_password), salt, 1000)
#         #hashlib.pbkdf2_hmac(algo, other_password.encode('utf-8'), salt, 1000)
#     )

def generate_password(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()
    # h = hashlib.pbkdf2_hmac( # получим бинарные данные из пароля и соли
    #     'sha256',
    #     password.encode('utf-8'),
    #     salt,
    #     1000
    # )
    # return base64.b64encode(h) # закодируем бинарные данные в строку

# получаем токен доступа на 30 мин
def generate_token(data):
    min30 = datetime.datetime.utcnow()+datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)
    return access_token

# проверим его валидность
def check_token(token):
    try:
        jwt.decode(token,JWT_SECRET, algorithms=[JWT_ALGO])
        return True
    except Exception:
        return False

def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        except Exception as e:
            print(f"JWT.decode auth Exception: {e}")
            abort(401)
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        role = None
        try:
            user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
            role = user.get("role")
        except Exception as e:
            print("JWT Decode admin Exception", e)
            abort(401)
        if role != "admin":
            abort(403)
        return func(*args, **kwargs)
    return wrapper
