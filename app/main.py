from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routers import books

app = FastAPI(title="Library API – Khoa CNTT", version="1.0.0",
              description="API quản lý sách của Thư viện số Khoa CNTT")
app.include_router(books.router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    try:
        error = HTTPStatus(exc.status_code).phrase
    except ValueError:
        error = "Error"
    return JSONResponse(status_code=exc.status_code,
                        content={"error": error, "message": str(exc.detail)})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request,
                                       exc: RequestValidationError):
    details = [f"{'.'.join(str(x) for x in e['loc'])}: {e['msg']}"
               for e in exc.errors()]
    return JSONResponse(status_code=422,
                        content={"error": "Unprocessable Entity",
                                 "message": "; ".join(details)})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500,
                        content={"error": "Internal Server Error",
                                 "message": "Lỗi máy chủ"})


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}