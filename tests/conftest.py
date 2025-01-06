import pytest
import time
from collections.abc import Callable
from asgi_claim_validator.middleware import ClaimValidatorMiddleware
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

@pytest.fixture
def claims_callable() -> Callable:
    """Fixture for providing mock JWT claims callable."""
    return lambda: {
        "sub": "admin",
        "iss": "https://example.com",
        "aud": "https://example.com",
        "exp": int(time.time() + 3600),
        "iat": int(time.time()),
        "nbf": int(time.time()),
    }

async def blocked_endpoint(request: Request) -> JSONResponse:
    return JSONResponse({"message": "blocked"})

async def secured_endpoint(request: Request) -> JSONResponse:
    return JSONResponse({"message": "secured"})

async def skipped_endpoint(request: Request) -> JSONResponse:
    return JSONResponse({"message": "skipped"})

@pytest.fixture
def app(claims_callable: Callable) -> Starlette:
    routes = [
        Route("/blocked", blocked_endpoint, methods=["GET"]),
        Route("/secured", secured_endpoint, methods=["GET"]),
        Route("/skipped", skipped_endpoint, methods=["GET"]),
    ]
    app = Starlette(routes=routes)
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
    return app