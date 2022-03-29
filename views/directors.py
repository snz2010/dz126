from flask import request
from flask_restx import Resource, Namespace
from views.functions import admin_required, auth_required
from models import Director, DirectorSchema
from setup_db import db

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = db.session.query(Director).all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        ent = Director(**req_json)

        db.session.add(ent)
        db.session.commit()
        return "", 201, {"location": f"/directors/{ent.id}"}

@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_required
    def get(self, rid):
        r = db.session.query(Director).get(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, bid):
        user = db.session.query(Director).get(bid)
        req_json = request.json
        user.name = req_json.get("name")
        db.session.add(user)
        db.session.commit()
        return "", 204

    @admin_required
    def delete(self, bid):
        user = db.session.query(Director).get(bid)
        db.session.delete(user)
        db.session.commit()
        return "", 204