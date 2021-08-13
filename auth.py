import json
from flask import Response
from flask import Blueprint, request
from services.auth import register_service
from constants import AUTH_RESULT

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/register', methods=('POST',))
def register():
	username = request.form['username']
	password = request.form['password']
	register_result = register_service(username, password)

	resp = Response(json.dumps({'result': register_result}))
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp
