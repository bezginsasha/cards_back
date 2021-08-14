from flask import Blueprint, request
from bson import json_util
from services.piles import get_all_piles_service, insert_pile_service, delete_pile_service
from utils.decorators import standard_headers_with_str_response

piles_bp = Blueprint('piles', __name__, url_prefix='/api/piles')


@piles_bp.route('/get_all', methods=['GET'])
@standard_headers_with_str_response
def get_all():
	piles = get_all_piles_service()
	return piles


@piles_bp.route('/add', methods=['POST'])
@standard_headers_with_str_response
def insert_pile():
	insert_pile_service(request.form['pile_name'])
	return json_util.dumps({'result': 'ok'})


@piles_bp.route('/delete', methods=['POST'])
@standard_headers_with_str_response
def delete_pile():
	delete_pile_service(request.form['pile_name'])
	return json_util.dumps({'result': 'ok'})
