import pytest
from httpx import AsyncClient, ASGITransport
from starlette.applications import Starlette
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
        assert response.status_code == 401
        assert response.json() == {"error": "Unauthorized"}

async def test_invalid_claims_type_endpoint(app: Starlette) -> None:
    app.user_middleware[0].kwargs["claims_callable"] = lambda _: "not_a_dict"
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/secured")
        assert response.status_code == 400
        assert response.json() == {"error": "Bad Request"}

async def test_invalid_claims_type_exception(app: Starlette) -> None:
    app.user_middleware[0].kwargs["claims_callable"] = lambda _: "not_a_dict"
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        with pytest.raises(InvalidClaimsTypeException):
            await client.get("/secured")

async def test_unauthenticated_endpoint(app: Starlette) -> None:
    app.user_middleware[0].kwargs["claims_callable"] = lambda _: {}
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/secured")
        assert response.status_code == 401
        assert response.json() == {"error": "Unauthorized"}

async def test_unauthenticated_exception(app: Starlette) -> None:
    app.user_middleware[0].kwargs["claims_callable"] = lambda _: {}
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        with pytest.raises(UnauthenticatedRequestException):
            await client.get("/secured")

async def test_unspecified_path_authentication_endpoint(app: Starlette) -> None:
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/unspecified")
        assert response.status_code == 401
        assert response.json() == {"error": "Unauthorized"}

async def test_unspecified_path_authentication_exception(app: Starlette) -> None:
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        with pytest.raises(UnspecifiedPathAuthenticationException):
            await client.get("/unspecified")

async def test_unspecified_method_authentication_endpoint(app: Starlette) -> None:
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.delete("/secured")
        assert response.status_code == 401
        assert response.json() == {"error": "Unauthorized"}

async def test_unspecified_method_authentication_exception(app: Starlette) -> None:
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        with pytest.raises(UnspecifiedMethodAuthenticationException):
            await client.delete("/secured")

async def test_missing_essential_claim_endpoint(app: Starlette) -> None:
    app.user_middleware[0].kwargs["claims_callable"] = lambda _: {
        "sub": "admin",
    }
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/secured")
        assert response.status_code == 403
        assert response.json() == {"error": "Forbidden"}
 
async def test_missing_essential_claim_exception(app: Starlette) -> None:
    app.user_middleware[0].kwargs["claims_callable"] = lambda _: {
        "sub": "admin",
    }
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        with pytest.raises(MissingEssentialClaimException):
            await client.get("/secured")

async def test_invalid_claim_value_endpoint(app: Starlette) -> None:
    app.user_middleware[0].kwargs["claims_callable"] = lambda _: {
        "sub": "admin",
        "iss": "https://wrong-example.com",
    }
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/secured")
        assert response.status_code == 403
        assert response.json() == {"error": "Forbidden"}
 
async def test_invalid_claim_value_exception(app: Starlette) -> None:
    app.user_middleware[0].kwargs["claims_callable"] = lambda _: {
        "sub": "admin",
        "iss": "https://wrong-example.com",
    }
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        with pytest.raises(InvalidClaimValueException):
            await client.get("/secured")