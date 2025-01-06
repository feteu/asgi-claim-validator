import pytest
from asgi_claim_validator.exceptions import (
    ClaimValidatorException,
    UnspecifiedMethodAuthenticationException,
    UnspecifiedPathAuthenticationException,
    UnauthenticatedRequestException,
    MissingEssentialClaimException,
    InvalidClaimValueException,
    InvalidClaimsTypeException,
    InvalidClaimsConfigurationException,
)

def test_claim_validator_exception() -> None:
    with pytest.raises(ClaimValidatorException) as exc_info:
        raise ClaimValidatorException("Test error")
    exception = exc_info.value
    assert exception.status == 400
    assert exception.title == "Bad Request"
    assert str(exception) == "Test error"

def test_unspecified_method_authentication_exception() -> None:
    with pytest.raises(UnspecifiedMethodAuthenticationException) as exc_info:
        raise UnspecifiedMethodAuthenticationException("GET", "/test")
    exception = exc_info.value
    assert exception.method == "GET"
    assert exception.path == "/test"
    assert exception.status == 401
    assert exception.title == "Unauthorized"

def test_unspecified_path_authentication_exception() -> None:
    with pytest.raises(UnspecifiedPathAuthenticationException) as exc_info:
        raise UnspecifiedPathAuthenticationException("GET", "/test")
    exception = exc_info.value
    assert exception.method == "GET"
    assert exception.path == "/test"
    assert exception.status == 401
    assert exception.title == "Unauthorized"

def test_unauthenticated_request_exception() -> None:
    with pytest.raises(UnauthenticatedRequestException) as exc_info:
        raise UnauthenticatedRequestException("/test", "GET")
    exception = exc_info.value
    assert exception.path == "/test"
    assert exception.method == "GET"
    assert exception.status == 401
    assert exception.title == "Unauthorized"

def test_missing_essential_claim_exception() -> None:
    with pytest.raises(MissingEssentialClaimException) as exc_info:
        raise MissingEssentialClaimException("/test", "GET", "claims")
    exception = exc_info.value
    assert exception.path == "/test"
    assert exception.method == "GET"
    assert exception.claims == "claims"
    assert exception.status == 403
    assert exception.title == "Forbidden"

def test_invalid_claim_value_exception() -> None:
    with pytest.raises(InvalidClaimValueException) as exc_info:
        raise InvalidClaimValueException("/test", "GET", "claims")
    exception = exc_info.value
    assert exception.path == "/test"
    assert exception.method == "GET"
    assert exception.claims == "claims"
    assert exception.status == 403
    assert exception.title == "Forbidden"

def test_invalid_claims_type_exception() -> None:
    with pytest.raises(InvalidClaimsTypeException) as exc_info:
        raise InvalidClaimsTypeException("/test", "GET", "str", "dict")
    exception = exc_info.value
    assert exception.path == "/test"
    assert exception.method == "GET"
    assert exception.type_received == "str"
    assert exception.type_expected == "dict"
    assert exception.status == 400
    assert exception.title == "Bad Request"

def test_invalid_claims_configuration_exception() -> None:
    with pytest.raises(InvalidClaimsConfigurationException) as exc_info:
        raise InvalidClaimsConfigurationException()
    exception = exc_info.value
    assert exception.status == 500
    assert exception.title == "Internal Server Error"