from flask import jsonify
from app.helpers import responses

def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(error):
        mensaje = error.description if hasattr(error, "description") else "Solicitud inválida"
        return jsonify(responses.error_response(mensaje)), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        mensaje = error.description if hasattr(error, "description") else "No autorizado"
        return jsonify(responses.error_response(mensaje)), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        mensaje = error.description if hasattr(error, "description") else "Acceso denegado"
        return jsonify(responses.error_response(mensaje)), 403

    @app.errorhandler(404)
    def not_found(error):
        mensaje = error.description if hasattr(error, "description") else "Recurso no encontrado"
        return jsonify(responses.error_response(mensaje)), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify(responses.error_response("Error interno del servidor")), 500