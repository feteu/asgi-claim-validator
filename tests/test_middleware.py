import pytest
from httpx import AsyncClient, ASGITransport
from starlette.applications import Starlette
from asgi_claim_validator.middleware import ClaimValidatorMiddleware
from asgi_claim_validator.exceptions import (
    InvalidClaimsTypeException,
    InvalidClaimValueException,
    MissingEssentialClaimException,
    UnauthenticatedRequestException,
    UnspecifiedMethodAuthenticationException,
    UnspecifiedPathAuthenticationException,
)

async def test_secured_endpoint(app: Starlette) -> None:
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/secured")
        assert response.status_code == 200
        assert response.json() == {"message": "secured"}

async def test_skipped_endpoint(app: Starlette) -> None:
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/skipped")
        assert response.status_code == 200
        assert response.json() == {"message": "skipped"}

async def test_blocked_endpoint(app: Starlette) -> None:
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/blocked")
        assert response.status_code == 500
        assert response.text == "Internal Server Error"

async def test_unspecified_path_exception(app: Starlette) -> None:
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        with pytest.raises(UnspecifiedPathAuthenticationException):
            await client.get("/blocked")

# async def test_unauthenticated_endpoint(app: Starlette) -> None:
#     # TODO: change the request subject to a empty dictionary
#     assert print(app.user_middleware[0]) == {}
#     transport = ASGITransport(app=app, raise_app_exceptions=False)
#     async with AsyncClient(transport=transport, base_url="http://testserver") as client:
#         response = await client.get("/secured")
#         assert response.status_code == 500
#         assert response.text == "Internal Server Error"

# async def test_unauthenticated_exception(app: Starlette) -> None:
#     # TODO: change the request subject to a empty dictionary
#     transport = ASGITransport(app=app, raise_app_exceptions=True)
#     async with AsyncClient(transport=transport, base_url="http://testserver") as client:
#         with pytest.raises(UnauthenticatedRequestException):
#             await client.get("/secured")

# def test_unauthenticated_request(client: TestClient) -> None:
#     client.app.middleware_stack.middleware[0].claims_callable = lambda: {}
#     with pytest.raises(UnauthenticatedRequestException):
#         client.get("/secured")

# def test_invalid_claims_type(client):
#     client.app.middleware_stack.middleware[0].claims_callable = lambda: "invalid_claims"
#     with pytest.raises(InvalidClaimsTypeException):
#         client.get("/secured")

# def test_missing_essential_claim(client):
#     client.app.middleware_stack.middleware[0].claims_callable = lambda: {
#         "sub": "admin",
#         "iss": "https://wrong-issuer.com",
#     }
#     with pytest.raises(MissingEssentialClaimException):
#         client.get("/secured")

# def test_invalid_claim_value(client):
#     client.app.middleware_stack.middleware[0].claims_callable = lambda: {
#         "sub": "user",
#         "iss": "https://example.com",
#     }
#     with pytest.raises(InvalidClaimValueException):
#         client.get("/secured")

# def test_unspecified_method(client):
#     client.app.middleware_stack.middleware[0].secured = {
#         "^/secured$": {
#             "POST": {
#                 "sub": {
#                     "essential": True,
#                     "allow_blank": False,
#                     "values": ["admin"],
#                 },
#             }
#         }
#     }
#     with pytest.raises(UnspecifiedMethodAuthenticationException):
#         client.get("/secured")
