from connexion.lifecycle import ConnexionResponse

def get() -> ConnexionResponse:
    data = {"message": "Hello, World!"}
    status_code = 200
    headers = {"Content-Type": "application/json"}
    return data, status_code, headers