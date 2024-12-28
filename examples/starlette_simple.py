import uvicorn
from asgi_claim_validator import ClaimValidatorMiddleware
from starlette.applications import Starlette
from starlette.responses import JSONResponse

app = Starlette()

@app.route('/')
async def homepage(request) -> JSONResponse:
    return JSONResponse({'message': 'Hello, world!'})

claim_validator_config = {
    "^/$": {
        "GET": [
            {
                "sub" : {
                    "essential": True,
                    "allow_blank": False,
                    "values": ["admin", "user"],
                }
            }
        ]
    } 
}

app.add_middleware(ClaimValidatorMiddleware, config=claim_validator_config)

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)