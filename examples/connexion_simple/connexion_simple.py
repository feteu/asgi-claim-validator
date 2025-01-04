import json
import time
import uvicorn
from connexion import AsyncApp, RestyResolver
from connexion.exceptions import OAuthProblem, problem
from connexion.lifecycle import ConnexionRequest, ConnexionResponse
from connexion.middleware import MiddlewarePosition
from asgi_claim_validator import ClaimValidatorMiddleware
from asgi_claim_validator.exceptions import MissingEssentialClaimException, UnspecifiedPathAuthenticationException

JWT_LIFETIME_SECONDS = 3600

claim_validation_skipped = {
    "^/api/1/openapi.json$": ["get"],
    "^/api/1/skipped/?$": ["get"],
    "^/api/1/ui/?$": ["get"],
    "^/api/1/ui/.+$": ["get"],
}
claim_validation_secured = {
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
}
claim_validation_claims_callable = lambda: {
    "sub": "admin",
    "iss": "https://example.com",
    "aud": "https://example.com",
    "exp": int(time.time() + JWT_LIFETIME_SECONDS),
    "iat": int(time.time()),
    "nbf": int(time.time()),
}

def claim_validator_401(request: ConnexionRequest, exc: Exception) -> ConnexionResponse:
    return problem(
        detail=exc.detail,
        status=exc.status,
        title=exc.title,
    )

def claim_validator_403(request: ConnexionRequest, exc: Exception) -> ConnexionResponse:
    return ConnexionResponse(status_code=403, body=json.dumps({"error": "Forbidden"}), content_type="application/json")

app = AsyncApp(__name__, specification_dir="spec")
app.add_api("openapi.yaml", resolver=RestyResolver("api"))
app.add_middleware(ClaimValidatorMiddleware, MiddlewarePosition.BEFORE_SWAGGER, secured=claim_validation_secured, skipped=claim_validation_skipped, claims_callable=claim_validation_claims_callable)
app.add_error_handler(MissingEssentialClaimException, claim_validator_401)
app.add_error_handler(UnspecifiedPathAuthenticationException, claim_validator_403)


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)