from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

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
    if not data:
        return {"message": "No pictures found"}, 404
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if not data:
        return {"message": "No pictures found"}, 404 
    
    for picture in data:
        if picture.get("id") == id:
            return jsonify(picture), 200

    return {"message": f"Picture with id {id} not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    if not data:
        return {"Message": "no pictures found"}, 404

    picture = request.get_json()

    if not picture.get("id"):
        return {"Message": "picture must have an 'id'"}, 400

    for existing_picture in data:
        if existing_picture.get("id") == picture.get("id"):
            return {"Message": f"picture with id {picture.get('id')} already present"}, 302

    data.append(picture)
    return jsonify(picture), 201
######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    if not data:
        return {"Message": "no pictures found"}, 404

    picture = request.get_json()

    for index, existing_picture in enumerate(data):
        if existing_picture.get("id") == id:
 
            data[index].update(picture)
            return jsonify(data[index]), 204

    return {"message": "picture not found"}
######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if not data:
        return {"Message": "no pictures found"}, 404

    for index, existing_picture in enumerate(data):
        if existing_picture.get("id") == id:
            data.pop(index)
            return '', 204
    
    return {"message": "picture not found"}, 404