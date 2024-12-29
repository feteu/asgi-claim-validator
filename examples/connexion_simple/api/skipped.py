from connexion.lifecycle import ConnexionResponse

def search() -> ConnexionResponse:
    data = {"status": "skipped"}
    status_code = 200
    headers = {"Content-Type": "application/json"}
    return data, status_code, headers