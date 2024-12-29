import time
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from asgi_claim_validator import ClaimValidatorMiddleware

app = Starlette()

@app.route("/api/1")
async def root_(request) -> JSONResponse:
    return JSONResponse({"message": "Hello, world!"})

@app.route("/api/1/secured")
async def api_1_secured(request) -> JSONResponse:
    return JSONResponse({"status": "secured"})

@app.route("/api/1/skipped")
async def api_1_skipped(request) -> JSONResponse:
    return JSONResponse({"status": "skipped"})

config = {
    "skipped": {
        "^/api/1/skipped$": ["get"],
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
    "claims": lambda: {
        "sub": "admin",
        "iss": "https://example.com",
        "aud": "https://example.com",
        "exp": (int(time.time()) + 3600),
        "iat": (int(time.time()) - 1),
        "nbf": (int(time.time()) - 1),
        "jti": "123456",
    }
}

app.add_middleware(ClaimValidatorMiddleware, **config)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)