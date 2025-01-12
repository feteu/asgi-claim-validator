from connexion import AsyncApp, RestyResolver
from connexion.exceptions import problem
from connexion.lifecycle import ConnexionRequest, ConnexionResponse
from connexion.middleware import MiddlewarePosition
from joserfc import jwt, jwk
from logging import getLogger
from time import time
from uvicorn import run
from asgi_claim_validator import ClaimValidatorMiddleware
from asgi_claim_validator.exceptions import ClaimValidatorException

log = getLogger("uvicorn.error")

JWT_ALG = "HS256"
JWT_TYP = "JWT"
JWT_TTL = 3600
JWT_SUB = "subject"
JWT_ISS = "local.asgi_claim_validator"
JWT_SEC = "WW91IGZvdW5kIGEgZWFzdGVyIGVnZywgZW5qb3kgdGhlIGRheSE="

def generate_token() -> str:
    timestamp = time()
    header = {
        "alg": JWT_ALG, 
        "typ": JWT_TYP,
    }
    claims = {
        "iss": JWT_ISS,
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_TTL),
        "sub": JWT_SUB,
    }
    key = jwk.OctKey.import_key(JWT_SEC)
    text = jwt.encode(header, claims, key)
    return text

def validate_token(token: str) -> dict:
    text = token
    key = jwk.OctKey.import_key(JWT_SEC)
    token = jwt.decode(text, key)
    return token.claims

claims_callable = lambda scope: scope["extensions"]["connexion_context"]["token_info"]

claim_validation_skipped = {
    "^/api/1/openapi.json$": ["GET"],
    "^/api/1/skipped/?$": ["GET"],
    "^/api/1/ui/?.+$": ["GET"],
}
claim_validation_secured = {
    "^/api/1/secured/?$": {
        "GET": {
            "sub" : {
                "essential": True,
                "allow_blank": False,
                "values": [f"{JWT_SUB}"],
            }, 
            "iss": {
                "essential": True,
                "allow_blank": False,
                "values": [f"{JWT_ISS}"],
            },
        },
    },
}

def claim_validator_error_handler(request: ConnexionRequest, exc: Exception) -> ConnexionResponse:
    return problem(detail=exc.detail, status=exc.status, title=exc.title)

log.info("Generated jwt token to use in the Swagger UI ...")
log.info(generate_token())

app = AsyncApp(__name__, specification_dir="spec")
app.add_api("openapi.yaml", resolver=RestyResolver("api"))
app.add_middleware(ClaimValidatorMiddleware, MiddlewarePosition.BEFORE_VALIDATION, secured=claim_validation_secured, skipped=claim_validation_skipped, claims_callable=claims_callable)
app.add_error_handler(ClaimValidatorException, claim_validator_error_handler)

if __name__ == "__main__":
    run(app, host='127.0.0.1', port=8000)

