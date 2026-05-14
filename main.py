from fastapi import FastAPI, APIRouter, Request, status
from fastapi.exceptions import FastAPIError, RequestValidationError
from fastapi.responses import JSONResponse
from api.v1.responses.error import ErrorResponse, ValidationErrorResponse
from api.v1.utils.database import Base, engine
from api.v1.routes import version_one
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHttpException
from sqlalchemy.exc import InvalidRequestError

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevLedger",
    docs_url="/docs",
    redoc_url=None,
    description="Our Application provides Invoicing an History"
)

app.include_router(version_one)

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    :param request: HTTP request object
    :param exc: HTTP exception
    :returns JSONResponse
    """

    errors = []
    for error in exc.errors():
        errors.append(
            {
                "field": error.get("loc")[-1],
                "message": error.get("msg"),
            }
        )
    response = ValidationErrorResponse(errors=errors)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content=response.model_dump()
    )

@app.exception_handler(StarletteHttpException)
async def http_exception_handler(request: Request, exc: StarletteHttpException):
    """
    :param request: HTTP request object
    :param exc: HTTP exception
    :returns JSONResponse
    """

    response = ErrorResponse(status_code=exc.status_code, message=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=response.model_dump())


@app.exception_handler(InvalidRequestError)
async def http_exception_handler(request: Request, exc: InvalidRequestError):
    """
    :param request: HTTP request object
    :param exc: HTTP exception
    :returns JSONResponse
    """

    response = ErrorResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=exc._message()
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response.model_dump()
    )

@app.exception_handler(FastAPIError)
async def http_exception_handler(request: Request, exc: FastAPIError):
    """
    :param request: HTTP request object
    :param exc: HTTP exception
    :returns JSONResponse
    """

    response = ErrorResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=exc.detail
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response.model_dump()
    )

@app.get("/check")
def healthcheck():
    return JSONResponse({"message" : "Healthy"})