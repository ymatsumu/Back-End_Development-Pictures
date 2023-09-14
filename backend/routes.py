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
    return (jsonify(dict(status="OK")), 200)


######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################

@app.route("/count")
def count():
    """return length of data"""
    if data:
        return (jsonify(length=len(data)), 200)

    return ({"message": "Internal server error"}, 500)


######################################################################
# GET ALL PICTURES
######################################################################

@app.route("/picture", methods=["GET"])
def get_pictures():
    return (jsonify(data), 200)


######################################################################
# GET A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if 0 <= id < len(data):
        urlOfPicture = data[id]
        return (jsonify({"url": urlOfPicture, "id": id}), 200)
    else:
        errorMessage = {"message": "Picture not found"}
        return (jsonify(errorMessage), 404)


######################################################################
# CREATE A PICTURE
######################################################################

@app.route("/picture", methods=["POST"])
def create_picture():
    newPicture = request.json

    idExist = False
    for picture in data:
        if picture["id"] == newPicture["id"]:
            idExist = True
            return ({"Message":f"picture with id {picture['id']} already present"}, 302)

    if idExist is False:
        data.append(newPicture)
        return (newPicture, 201)


######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pictureData = request.json

    picExists = False
    for idx, picture in enumerate(data):
        if picture["id"] == id:
            data[idx] = pictureData # update with the incoming request
            picExists = True
            return (picture, 201)
            
    if picExists is False:
        return ({"Message":"picture not found"}, 404)


######################################################################
# DELETE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return ("", 204)

    return ({"message":"picture not found"}, 404)