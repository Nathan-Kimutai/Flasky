from flask import jsonify

def forbidden(message):
    response = jsonify({"error":"forbidden"})
    response.status_code = 403
    return response
