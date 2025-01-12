from collections.abc import Callable
from jsonschema import validate
from jsonschema.exceptions import SchemaError, ValidationError
from logging import getLogger
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

log = getLogger(__name__)

def validate_claims_callable() -> Callable:
    """
    Decorator to validate the claims_callable attribute of a class.

    Raises:
        InvalidClaimsConfigurationException: If claims_callable is not a callable.
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(self, *args, **kwargs) -> Callable:
            claims = getattr(self, 'claims_callable', _DEFAULT_CLAIMS_CALLABLE)
            if not isinstance(claims, Callable):
                raise InvalidClaimsConfigurationException()
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def validate_secured() -> Callable:
    """
    Decorator to validate the secured attribute of a class against a JSON schema.

    Raises:
        InvalidSecuredConfigurationException: If the secured attribute does not conform to the schema.
    """
    def decorator(func: Callable) -> Callable:
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
    """
    Decorator to validate the skipped attribute of a class against a JSON schema.

    Raises:
        InvalidSkippedConfigurationException: If the skipped attribute does not conform to the schema.
    """
    def decorator(func: Callable) -> Callable:
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