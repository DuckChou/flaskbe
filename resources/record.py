import json

from flask import jsonify,make_response
from flask.views import MethodView

from flask_smorest import Blueprint, abort

from schemas import RecordSchema, RecordPostSchema,RecordGetSchema

from db import RecordModel, db

from flask_jwt_extended import jwt_required

blp = Blueprint("records", __name__, description="Operations on users")


@blp.route("/record")
class Login(MethodView):

    @jwt_required()
    @blp.arguments(RecordPostSchema)
    def post(self, record_data):
        record = RecordModel(
            description = record_data["description"],
            user_id = record_data["user_id"],
            date = record_data["date"],
            start_time = record_data["start_time"],
            duration = record_data["duration"]
        )

        db.session.add(record)
        db.session.flush()
        record_id = record.record_id
        db.session.commit()

        res = make_response(jsonify({"mes":"record added","record_id":record_id}))
        res.status = '201'
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'

        return res

        # return {"mes":"record added","record_id":record_id}, 201

    @jwt_required()
    @blp.arguments(RecordGetSchema)
    def get(self,date_data):
        records = RecordModel.query.filter(
            RecordModel.date == date_data["date"],
            RecordModel.user_id == date_data["user_id"]
        ).all()

        result = []
        for record in records:
            result.append(record.to_json())

        # dump_data = RecordSchema.dump(records)
        res = make_response(jsonify(result))
        res.status = '200'
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'

        return res


        # return result

        # return {"mes":"ok"}

    @jwt_required()
    @blp.arguments(RecordSchema)
    def delete(self,date_data):
        record = RecordModel.query.get_or_404(date_data["record_id"])
        db.session.delete(record)
        db.session.commit()

        res = make_response(jsonify({"mes": "record deleted"}))
        res.status = '200'
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'

        return res

        # return {"mes": "record deleted"}, 200
