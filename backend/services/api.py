from fastapi.responses import JSONResponse

def ApiResponse(message, code=200, **kwargs):
    content = {
        "code": code,
        "message": message,
        **kwargs
    }

    return JSONResponse(content=content, status_code=code)

class ApiException(Exception):
    def __init__(self, code: int, message: str, **kwagrs):
        self.code = code
        self.message = message
        self.data = kwagrs

        super().__init__(message)