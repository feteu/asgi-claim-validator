import pytest
from collections.abc import Callable
from asgi_claim_validator.constants import _DEFAULT_CLAIMS_CALLABLE, _DEFAULT_SECURED, _DEFAULT_SKIPPED
from asgi_claim_validator.decorators import validate_claims_callable, validate_secured, validate_skipped
from asgi_claim_validator.exceptions import InvalidClaimsConfigurationException, InvalidSecuredConfigurationException, InvalidSkippedConfigurationException
from asgi_claim_validator.types import SecuredType, SkippedType

class TestClass:
    def __init__(self, claims_callable: Callable = _DEFAULT_CLAIMS_CALLABLE, secured: SecuredType = _DEFAULT_SECURED, skipped: SkippedType = _DEFAULT_SKIPPED) -> None:
        self.claims_callable = claims_callable
        self.secured = secured
        self.skipped = skipped

    @validate_claims_callable()
    def test_validate_claims_callable(self, *args, **kwargs) -> bool:
        return "OK"
    
    @validate_secured()
    def test_validate_secured(self, *args, **kwargs) -> bool:
        return "OK"
    
    @validate_skipped()
    def test_validate_skipped(self, *args, **kwargs) -> bool:
        return "OK"

def test_validate_claims_callable_with_default_callable() -> None:
    TC = TestClass()
    result = TC.test_validate_claims_callable()
    assert result == "OK"

def test_validate_claims_callable_with_valid_callable(claims_callable: Callable) -> None:
    claims_callable = claims_callable
    TC = TestClass(claims_callable=claims_callable)
    result = TC.test_validate_claims_callable()
    assert result == "OK"

def test_validate_claims_callable_with_invalid_callable(claims_callable: Callable) -> None:
    claims_callable = None
    with pytest.raises(InvalidClaimsConfigurationException):
        TC = TestClass(claims_callable=claims_callable)
        TC.test_validate_claims_callable()

def test_validate_secured_with_default_config() -> None:
    TC = TestClass()
    result = TC.test_validate_secured()
    assert result == "OK"

@pytest.mark.parametrize("secured", [f"valid_secured_configs_{i:02d}" for i in range(1, 5)])
def test_validate_secured_with_valid_config(secured: SecuredType, request: pytest.FixtureRequest) -> None:
    secured = request.getfixturevalue(secured)
    TC = TestClass(secured=secured)
    result = TC.test_validate_secured()
    assert result == "OK"

@pytest.mark.parametrize("secured", [f"invalid_secured_configs_{i:02d}" for i in range(1, 3)])
def test_validate_secured_with_invalid_config(secured: SecuredType, request: pytest.FixtureRequest) -> None:
    secured = request.getfixturevalue(secured)
    with pytest.raises(InvalidSecuredConfigurationException):
        TC = TestClass(secured=secured)
        TC.test_validate_secured()

def test_validate_skipped_with_default_config() -> None:
    TC = TestClass()
    result = TC.test_validate_skipped()
    assert result == "OK"

@pytest.mark.parametrize("skipped", [f"valid_skipped_configs_{i:02d}" for i in range(1, 5)])
def test_validate_skipped_with_valid_config(skipped: SkippedType, request: pytest.FixtureRequest) -> None:
    skipped = request.getfixturevalue(skipped)
    TC = TestClass(skipped=skipped)
    result = TC.test_validate_skipped()
    assert result == "OK"

@pytest.mark.parametrize("skipped", [f"invalid_skipped_configs_{i:02d}" for i in range(1, 4)])
def test_validate_skipped_with_invalid_config(skipped: SkippedType, request: pytest.FixtureRequest) -> None:
    skipped = request.getfixturevalue(skipped)
    with pytest.raises(InvalidSkippedConfigurationException):
        TC = TestClass(skipped=skipped)
        TC.test_validate_skipped()