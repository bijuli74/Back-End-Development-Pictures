from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for, redirect
import sys
print(sys.path)

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((pic for pic in data if pic["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    else:
        abort(404)

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    try:
        new_picture = request.get_json()
        existing_picture = next((pic for pic in data if pic["id"] == new_picture["id"]), None)
        if existing_picture:
            response = make_response(jsonify(Message=f"picture with id {new_picture['id']} already present"), 302)
            response.headers["Location"] = url_for("get_picture_by_id", id=new_picture["id"])
            return response
        else:
            if "id" not in new_picture:
                new_picture["id"] = max([pic["id"] for pic in data]) + 1
            data.append(new_picture)
            return jsonify(new_picture), 201
    except Exception as e:
        print(e)
        abort(500)

######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = next((pic for pic in data if pic["id"] == id), None)
    if picture:
        updated_picture = request.get_json()
        picture.update(updated_picture)
        return jsonify(picture), 200
    else:
        abort({"message": "picture not found"}, 404)

######################################################################
# DELETE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    picture = next((pic for pic in data if pic["id"] == id), None)
    if picture:
        data.remove(picture)
        return "", 204
    else:
        abort(404)
