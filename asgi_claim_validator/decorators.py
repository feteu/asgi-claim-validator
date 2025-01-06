import logging
from collections.abc import Callable
from jsonschema import validate
from jsonschema.exceptions import SchemaError, ValidationError
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
        def wrapper(self, *args, **kwargs) -> Callable:
            claims = getattr(self, 'claims_callable', _DEFAULT_CLAIMS_CALLABLE)
            if not isinstance(claims, Callable):
                raise InvalidClaimsConfigurationException()
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def validate_secured() -> Callable:
    def decorator(func) -> Callable:
        def wrapper(self, *args, **kwargs) -> Callable:
            secured = getattr(self, 'secured', None)
            try:
                validate(instance=secured, schema=_DEFAULT_SECURED_JSON_SCHEMA)
            except (SchemaError, ValidationError) as e:
                log.error(e)
                raise InvalidSecuredConfigurationException()
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def validate_skipped() -> Callable:
    def decorator(func) -> Callable:
        def wrapper(self, *args, **kwargs) -> Callable:
            skipped = getattr(self, 'skipped', None)
            try:
                validate(instance=skipped, schema=_DEFAULT_SKIPPED_JSON_SCHEMA)
            except (SchemaError, ValidationError) as e:
                log.error(e)
                raise InvalidSkippedConfigurationException()
            return func(self, *args, **kwargs)
        return wrapper
    return decorator