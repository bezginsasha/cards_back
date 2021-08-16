from flask import Response, request, abort


def add_headers_to_response_object(response):
	response.headers['Access-Control-Allow-Credentials'] = 'true'
	response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
	return response


def standard_headers_with_str_response(foo):
	def wrapper():
		response_str = foo()
		response = Response(response_str)
		response = add_headers_to_response_object(response)
		return response
	wrapper.__name__ = foo.__name__
	return wrapper


def standard_headers_with_response_object(foo):
	def wrapper():
		response = foo()
		response = add_headers_to_response_object(response)
		return response
	wrapper.__name__ = foo.__name__
	return wrapper


def require_auth(foo):
	def wrapper():
		if 'username' in request.cookies:
			return foo()
		else:
			abort(401)
	wrapper.__name__ = foo.__name__
	return wrapper
