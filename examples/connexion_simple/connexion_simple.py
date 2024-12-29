import time
import uvicorn
from connexion import AsyncApp, RestyResolver
from connexion.middleware import MiddlewarePosition
from asgi_claim_validator import ClaimValidatorMiddleware

JWT_LIFETIME_SECONDS = 3600

# Mock claims for testing purposes, ideally this should be fetched from the JWT token.
# usually with connexion the claims are accessible via the state object of connexion.
claims_mock = lambda: {
    "sub": "admin",
    "iss": "https://example.com",
    "aud": "https://example.com",
    "exp": int(time.time() + JWT_LIFETIME_SECONDS),
    "iat": int(time.time()),
    "nbf": int(time.time()),
}

claim_validation_config = {
    "skipped": {
        "^/api/1/openapi.json$": ["get"],
        "^/api/1/skipped/?$": ["get"],
        "^/api/1/ui/?$": ["post"],
        "^/api/1/ui/.+$": ["get"],
    },
    "secured": {
        "^/api/1/secured$": {
            "get": {
                "sub" : {
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
    "claims": claims_mock,
}

app = AsyncApp(__name__, specification_dir="spec")
app.add_api("openapi.yaml", resolver=RestyResolver("api"))
app.add_middleware(ClaimValidatorMiddleware, MiddlewarePosition.BEFORE_SWAGGER, **claim_validation_config)

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)