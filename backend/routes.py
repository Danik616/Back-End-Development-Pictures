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
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for image in data:
        if image["id"] == id:
            return image
        
    return {"message": "Image not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_image = request.json
    if not new_image:
        return {"message": "Invalidinput parameter"}, 422
    
    try:
        for image in data:
            if new_image["id"] == image["id"]:
                return {"Message": f"picture with id {image['id']} already present"}, 302
        
        data.append(new_image)
    except NameError:
        return {"message": "Data not found"}, 500
    
    return new_image, 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    for image in data:
        if image["id"] == id:
            try:
                updated_image = request.get_json()
                if not updated_image:
                    return {"message": "Invalid input parameter"}, 422
            except Exception as e:
                return {"message": "Error parsing input"}, 400

            image.update(updated_image)
            return jsonify(image), 200

    return {"message": "Image not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for index, image in enumerate(data):
        if image["id"] == id:
            data.remove(image)
            return "", 204

    return {"message": "Image not found"}, 404