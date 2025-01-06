import pytest
from collections.abc import Callable
from asgi_claim_validator.decorators import validate_claims_callable
from asgi_claim_validator.exceptions import InvalidClaimsConfigurationException

@validate_claims_callable()
def test_function(*args, **kwargs) -> bool:
    return True

def test_validate_claims_callable_with_valid_callable(claims_callable: Callable) -> None:
    result = test_function(claims=claims_callable)
    assert result == True

def test_validate_claims_callable_with_invalid_callable() -> None:
    with pytest.raises(InvalidClaimsConfigurationException):
        test_function(claims=False)

def test_validate_claims_callable_with_default_callable() -> None:
    result = test_function()
    assert result == True