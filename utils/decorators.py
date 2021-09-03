import traceback

from flask import Response, request, abort
import loguru

loguru.logger.add('logs.txt', format='{time:DD-MM-YY HH:mm:ss} {level} {message}', level='DEBUG')


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


def logger(foo):
    def wrapper():
        loguru.logger.debug(f'url: {request.base_url}')
        loguru.logger.debug(f'method: {request.method}')
        loguru.logger.debug(f'cookies: {dict(request.cookies)}')
        if request.method != 'GET':
            loguru.logger.debug(f'form data: {dict(request.form)}')

        try:
            return foo()
        except Exception as e:
            loguru.logger.error(e)
            loguru.logger.error(traceback.format_exc())
            raise

    wrapper.__name__ = foo.__name__
    return wrapper
