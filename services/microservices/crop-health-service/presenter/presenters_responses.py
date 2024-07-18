def response_with(response):
    return response

def success_response(data):
    return {
        "status": "success",
        "data": data
    }

def error_response(message):
    return {
        "status": "error",
        "message": message
    }
