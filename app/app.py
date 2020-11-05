import logging

from flask import jsonify
from werkzeug.exceptions import HTTPException
from marshmallow.exceptions import ValidationError

from app import create_app


# app = create_app()


# @app.errorhandler(Exception)
# def handle_exception(e):
#     """Handle all application's exceptions."""
#     if isinstance(e, ValidationError):
#         logging.exception(e)
#         return jsonify(message='Invalid request data.', error_info=e.messages), 400     #
#
#     if isinstance(e, HTTPException):
#         logging.exception(e)
#         return jsonify(message=e.description,
#                        error_info=e.response.data if e.response else {}
#                        ), e.code
#
#     logging.exception(e)
#     return jsonify(message='Internal Server Error.'), 500
