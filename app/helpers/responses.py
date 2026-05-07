def success_response(data=None, mensaje="", meta=None):
    response = {
        "ok": True,
        "data": data,
        "mensaje": mensaje
    }

    if meta is not None:
        response["meta"] = meta

    return response

def error_response(mensaje):
    return {
        "ok": False,
        "error": mensaje
    }