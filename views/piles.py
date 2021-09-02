from flask import Blueprint, request
from bson import json_util
from services.piles import get_all_piles_service, insert_pile_service, delete_pile_service, update_pile_service
from utils.decorators import standard_headers_with_str_response, require_auth
from humps import camelize

piles_bp = Blueprint('piles', __name__, url_prefix='/api/piles')


@piles_bp.route('/get_all', methods=['GET'])
@require_auth
@standard_headers_with_str_response
def get_all():
    username = request.cookies['username']
    piles = get_all_piles_service(username)
    return json_util.dumps(camelize(piles))


@piles_bp.route('/add', methods=['POST'])
@require_auth
@standard_headers_with_str_response
def insert_pile():
    pile_name = request.form[camelize('pile_name')]
    username = request.cookies['username']
    insert_pile_service(pile_name, username)
    return json_util.dumps({'result': 'ok'})


@piles_bp.route('/update', methods=['POST'])
@require_auth
@standard_headers_with_str_response
def update_pile():
    old_pile_name = request.form[camelize('old_pile_name')]
    new_pile_name = request.form[camelize('new_pile_name')]
    username = request.cookies['username']
    update_pile_service(old_pile_name, new_pile_name, username)
    return json_util.dumps({'result': 'ok'})


@piles_bp.route('/delete', methods=['POST'])
@require_auth
@standard_headers_with_str_response
def delete_pile():
    pile_name = request.form[camelize('pile_name')]
    username = request.cookies['username']
    delete_pile_service(pile_name, username)
    return json_util.dumps({'result': 'ok'})
