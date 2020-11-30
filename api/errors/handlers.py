from flask import jsonify, make_response
from flask_babel import gettext
from api.errors import bp

@bp.app_errorhandler(404)
def not_found_error(error):
    return make_response(jsonify({'error': gettext('Not found')}), 404)

@bp.app_errorhandler(500)
def internal_error(error):
    return make_response(jsonify({'error':gettext('Internal error')}), 500)