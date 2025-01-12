from connexion import AsyncApp, RestyResolver
from connexion.exceptions import problem
from connexion.lifecycle import ConnexionRequest, ConnexionResponse
from connexion.middleware import MiddlewarePosition
from json import dumps
from time import time
from uvicorn import run
from asgi_claim_validator import ClaimValidatorMiddleware
from asgi_claim_validator.exceptions import ClaimValidatorException, UnspecifiedPathAuthenticationException

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
claim_validation_claims_callable = lambda _: {
    "sub": "admin",
    "iss": "https://example.com",
    "aud": "https://example.com",
    "exp": int(time() + JWT_LIFETIME_SECONDS),
    "iat": int(time()),
    "nbf": int(time()),
}


def claim_validator_custom_403(request: ConnexionRequest, exc: Exception) -> ConnexionResponse:
    return ConnexionResponse(status_code=403, body=dumps({"error": "Forbidden"}), content_type="application/json")

def claim_validator_error_handler(request: ConnexionRequest, exc: Exception) -> ConnexionResponse:
    return problem(detail=exc.detail, status=exc.status, title=exc.title)

app = AsyncApp(__name__, specification_dir="spec")
app.add_api("openapi.yaml", resolver=RestyResolver("api"))
app.add_middleware(ClaimValidatorMiddleware, MiddlewarePosition.BEFORE_SWAGGER, secured=claim_validation_secured, skipped=claim_validation_skipped, claims_callable=claim_validation_claims_callable)
app.add_error_handler(UnspecifiedPathAuthenticationException, claim_validator_custom_403)
app.add_error_handler(ClaimValidatorException, claim_validator_error_handler)


if __name__ == "__main__":
    run(app, host='127.0.0.1', port=8000)