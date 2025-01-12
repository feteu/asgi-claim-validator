from connexion import context
from connexion.lifecycle import ConnexionResponse

def search() -> ConnexionResponse:
    data = {
        "status": "secured", 
        "token_info": context.context["token_info"],
        "user": context.context["user"],
    }
    status_code = 200
    headers = {"Content-Type": "application/json"}
    return data, status_code, headers