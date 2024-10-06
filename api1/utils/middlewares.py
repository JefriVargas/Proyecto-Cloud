from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request, status
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

origins = ['*']

def setup_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        custom_messages = {
            401: "Unauthorized",
            403: "Forbidden",
            404: "Resource not found",
            406: "Not accepted",
            408: "Timeout, try again later",
            422: "Unprocessable",
            500: "Internal server error",
        }
        message = custom_messages.get(exc.status_code, "Error")
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "code": exc.status_code, "message": message},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                'success': False,
                'code': 422,
                'message': 'Unprocessable'
            }
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": 500,
                "message": "Internal server error"
            },
        )
