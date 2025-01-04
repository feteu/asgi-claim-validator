from collections.abc import Callable
from asgi_claim_validator.constants import _DEFAULT_CLAIMS_CALLABLE
from asgi_claim_validator.exceptions import InvalidClaimsConfigurationException

def validate_claims_callable() -> Callable:
    def decorator(func) -> Callable:
        def wrapper(*args, **kwargs) -> Callable:
            claims = kwargs.get('claims', _DEFAULT_CLAIMS_CALLABLE)
            if not isinstance(claims, Callable):
                raise InvalidClaimsConfigurationException()
            return func(*args, **kwargs)
        return wrapper
    return decorator