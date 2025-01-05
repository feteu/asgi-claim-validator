import logging
from collections.abc import Callable
from jsonschema import validate
from asgi_claim_validator.constants import (
    _DEFAULT_CLAIMS_CALLABLE, 
    _DEFAULT_SECURED_JSON_SCHEMA,
    _DEFAULT_SKIPPED_JSON_SCHEMA,
)
from asgi_claim_validator.exceptions import (
    InvalidClaimsConfigurationException, 
    InvalidSecuredConfigurationException,
    InvalidSkippedConfigurationException,
)

log = logging.getLogger(__name__)

def validate_claims_callable() -> Callable:
    def decorator(func) -> Callable:
        def wrapper(*args, **kwargs) -> Callable:
            claims = kwargs.get('claims', _DEFAULT_CLAIMS_CALLABLE)
            if not isinstance(claims, Callable):
                raise InvalidClaimsConfigurationException()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def validate_secured() -> Callable:
    def decorator(func) -> Callable:
        def wrapper(*args, **kwargs) -> Callable:
            secured = kwargs.get('secured')
            try:
                validate.schema(secured, _DEFAULT_SECURED_JSON_SCHEMA)
            except Exception as e:
                log.error(e)
                raise InvalidSecuredConfigurationException()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def validate_skipped() -> Callable:
    def decorator(func) -> Callable:
        def wrapper(*args, **kwargs) -> Callable:
            skipped = kwargs.get('skipped')
            try:
                validate.schema(skipped, _DEFAULT_SKIPPED_JSON_SCHEMA)
            except Exception as e:
                log.error(e)
                raise InvalidSkippedConfigurationException()
            return func(*args, **kwargs)
        return wrapper
    return decorator