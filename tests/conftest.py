import pytest
from asgi_claim_validator.exceptions import ClaimValidatorException
from asgi_claim_validator.middleware import ClaimValidatorMiddleware
from collections.abc import Callable
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from time import time

@pytest.fixture
def claims_callable() -> Callable:
    """Fixture for providing mock JWT claims callable."""
    return lambda _: {
        "sub": "admin",
        "iss": "https://example.com",
        "aud": "https://example.com",
        "exp": int(time() + 3600),
        "iat": int(time()),
        "nbf": int(time()),
    }

@pytest.fixture
def app(claims_callable: Callable) -> Starlette:

    async def blocked_endpoint(request: Request) -> JSONResponse:
        return JSONResponse({"message": "blocked"})

    async def secured_endpoint(request: Request) -> JSONResponse:
        return JSONResponse({"message": "secured"})

    async def skipped_endpoint(request: Request) -> JSONResponse:
        return JSONResponse({"message": "skipped"})

async def claim_validator_error_handler(request: Request, exc: ClaimValidatorException) -> JSONResponse:
    return JSONResponse({"error": f"{exc.title}"}, status_code=exc.status)

    routes = [
        Route("/blocked", blocked_endpoint, methods=["GET", "DELETE"]),
        Route("/secured", secured_endpoint, methods=["GET", "DELETE"]),
        Route("/skipped", skipped_endpoint, methods=["GET", "DELETE"]),
    ]
    app = Starlette(routes=routes, exception_handlers={Exception: claim_validator_error_handler})
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
            },
        },
        skipped={
            "^/skipped$": ["GET"],
        },
    )
    return app

@pytest.fixture
def valid_secured_configs_01() -> dict:
    # default config
    return {
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
        },
    }

@pytest.fixture
def valid_secured_configs_02() -> dict:
    # lowercased method, non essential claim, allow blank claim
    return {
        "^/secured$": {
            "post": {
                "aud": {
                    "essential": False,
                    "allow_blank": True,
                    "values": [],
                },
            },
        },
    }

@pytest.fixture
def valid_secured_configs_03() -> dict:
    # cover all methods
    return {
        "^/secured$": {
            "*": {
                "sub": {
                    "essential": True,
                    "allow_blank": False,
                    "values": ["admin"],
                },
            },            
        },
    }

@pytest.fixture
def valid_secured_configs_04() -> dict:
    # covery all path and methods
    return {
        "^/.+$": {
            "*": {
                "sub": {
                    "essential": True,
                    "allow_blank": False,
                    "values": ["admin"],
                },
            },            
        },
    }

@pytest.fixture
def invalid_secured_configs_01() -> dict:
    return {
        "^/secured$": {
            "GET": {},
        },
    }

@pytest.fixture
def invalid_secured_configs_02() -> dict:
    return {
        "^/secured$": {
            "GET_": {
                "sub": {
                    "essential": True,
                    "allow_blank": False,
                    "values": ["admin"],
                },
            },
        },
    }

@pytest.fixture
def valid_skipped_configs_01() -> dict:
    return {
        "^/skipped$": ["get"],
    }

@pytest.fixture
def valid_skipped_configs_02() -> dict:
    return {
        "^/skipped$": ["*"],
    }

@pytest.fixture
def valid_skipped_configs_03() -> dict:
    return {
        "^/skipped$": ["GET", "POST"],
    }

@pytest.fixture
def valid_skipped_configs_04() -> dict:
    return {
        "^/$": ["GET", "POST"],
        "^/skipped$": ["*"],
    }

@pytest.fixture
def invalid_skipped_configs_01() -> dict:
    # invalid method
    return {
        "^/skipped$": ["GET_"],
    }

@pytest.fixture
def invalid_skipped_configs_02() -> dict:
    # invalid path
    return {
        "": ["GET"],
    }

@pytest.fixture
def invalid_skipped_configs_03() -> dict:
    # invalid method object
    return {
        "^/skipped$": False,
    }
