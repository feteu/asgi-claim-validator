import json
import time
import uvicorn
from connexion import AsyncApp, RestyResolver
from connexion.exceptions import OAuthProblem
from connexion.lifecycle import ConnexionRequest, ConnexionResponse
from connexion.middleware import MiddlewarePosition
from asgi_claim_validator import ClaimValidatorMiddleware, MissingEssentialClaimException, UnspecifiedPathAuthenticationException

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
        "^/api/1/ui/?$": ["get"],
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

def claim_validator_401(request: ConnexionRequest, exc: Exception) -> None:
    raise OAuthProblem()

def claim_validator_403(request: ConnexionRequest, exc: Exception) -> ConnexionResponse:
    return ConnexionResponse(status_code=403, body=json.dumps({"error": "Forbidden"}), content_type="application/json")

app = AsyncApp(__name__, specification_dir="spec")
app.add_api("openapi.yaml", resolver=RestyResolver("api"))
app.add_middleware(ClaimValidatorMiddleware, MiddlewarePosition.BEFORE_SWAGGER, **claim_validation_config)
app.add_error_handler(MissingEssentialClaimException, claim_validator_401)
app.add_error_handler(UnspecifiedPathAuthenticationException, claim_validator_403)


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)