from collections.abc import Callable
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from time import time
from uvicorn import run
from asgi_claim_validator import ClaimValidatorMiddleware, ClaimValidatorException

JWT_LIFETIME_SECONDS = 3600

def claims_callable() -> Callable:
    return lambda _: {
        "sub": "admin",
        "iss": "https://example.com",
        "aud": "https://example.com",
        "exp": int(time() + JWT_LIFETIME_SECONDS),
        "iat": int(time()),
        "nbf": int(time()),
    }

async def blocked_endpoint(request: Request) -> JSONResponse:
    return JSONResponse({"message": "blocked"})

async def secured_endpoint(request: Request) -> JSONResponse:
    return JSONResponse({"message": "secured"})

async def skipped_endpoint(request: Request) -> JSONResponse:
    return JSONResponse({"message": "skipped"})

async def claim_validator_error_handler(request: Request, exc: ClaimValidatorException) -> JSONResponse:
    return JSONResponse({"error": f"{exc.title}"}, status_code=exc.status)

routes = [
    Route("/blocked", blocked_endpoint, methods=["GET"]),
    Route("/secured", secured_endpoint, methods=["GET"]),
    Route("/skipped", skipped_endpoint, methods=["GET"]),
]

exception_handlers = {
    ClaimValidatorException: claim_validator_error_handler
}

app = Starlette(routes=routes, exception_handlers=exception_handlers)
app.add_middleware(
    ClaimValidatorMiddleware,
    claims_callable=claims_callable,
    secured={
        "^/secured$": {
            "GET": {
                "sub": {
                    "essential": True,
                    "allow_blank": False,
                    "values": ["admin"],
                },
                "iss": {
                    "essential": True,
                    "allow_blank": False,
                    "values": ["https://example.com"],
                },
            },
        }
    },
    skipped={
        "^/skipped$": ["GET"],
    },
)

if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8000)