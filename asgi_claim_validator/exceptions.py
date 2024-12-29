class ClaimValidatorException(Exception):
    """Base exception for claim validator-related errors.

    This is the base class for all exceptions raised by the claim validator.
    It provides a common interface for handling errors related to claim validation.

    Attributes:
        description (str): A brief description of the error.
    """
    description: str = "A claim validator error occurred."

    def __init__(self, detail: str = description) -> None:
        self.detail: str = detail
        super().__init__(self.detail)

class UnspecifiedMethodAuthenticationException(ClaimValidatorException):
    """Exception raised when authentication is not specified for a method.

    This exception is used in the ClaimValidatorMiddleware to indicate that 
    the specified HTTP method does not have an associated authentication configuration.
    It is raised when the `raise_on_unspecified_method` flag is set to True and 
    no matching secured method pattern is found for the current request method.

    Attributes:
        method (str): The HTTP method of the request.
        path (str): The path of the request.
        detail (str): A detailed error message.
    """
    description: str = (
        "Authentication configuration missing for the specified method. "
        "Ensure that an appropriate authentication definition is provided "
        "for this method and try again."
    )

    def __init__(self, method: str, path: str, detail: str = description) -> None:
        self.method: str = method
        self.path: str = path
        self.detail: str = detail
        super().__init__(self.detail)

    def __str__(self) -> str:
        return f"Method authentication not specified {self.method} {self.path} ({self.detail})"

class UnspecifiedPathAuthenticationException(ClaimValidatorException):
    """Exception raised when authentication is not specified for a path.

    This exception is used in the ClaimValidatorMiddleware to indicate that 
    the specified path does not have an associated authentication configuration.
    It is raised when the `raise_on_unspecified_path` flag is set to True and 
    no matching secured path pattern is found for the current request path.

    Attributes:
        method (str): The HTTP method of the request.
        path (str): The path of the request.
        detail (str): A detailed error message.
    """
    description: str = (
        "Authentication configuration missing for the specified path. "
        "Ensure that an appropriate authentication definition is provided "
        "for this path and try again."
    )

    def __init__(self, method: str, path: str, detail: str = description) -> None:
        self.method: str = method
        self.path: str = path
        self.detail: str = detail
        super().__init__(self.detail)

    def __str__(self) -> str:
        return f"Path authentication not specified {self.method} {self.path} ({self.detail})"

class UnauthenticatedRequestException(ClaimValidatorException):
    """Exception raised when a request cannot be authenticated.

    This exception is used in the ClaimValidatorMiddleware to indicate that 
    the request could not be authenticated due to missing or invalid claims.
    It is raised when the `raise_on_unauthenticated` flag is set to True and 
    the claims provided are insufficient for authentication.

    Attributes:
        path (str): The path of the request.
        method (str): The HTTP method of the request.
        detail (str): A detailed error message.
    """
    description: str = (
        "The request could not be authenticated. Ensure that the necessary "
        "claims are provided and try again."
    )

    def __init__(self, path: str, method: str, detail: str = description) -> None:
        self.path: str = path
        self.method: str = method
        self.detail: str = detail
        super().__init__(self.detail)

    def __str__(self) -> str:
        return f"Unauthenticated request {self.method} {self.path} ({self.detail})"

class MissingEssentialClaimException(ClaimValidatorException):
    """Exception raised when an essential claim is missing from the request.

    This exception is used in the ClaimValidatorMiddleware to indicate that 
    a required claim is missing from the JWT claims provided in the request.
    It is raised when the `raise_on_missing_claim` flag is set to True and 
    a required claim is not found in the JWT claims.

    Attributes:
        path (str): The path of the request.
        method (str): The HTTP method of the request.
        claim (str): The name of the missing claim.
        detail (str): A detailed error message.
    """
    description: str = (
        "An essential claim is missing from the request. Ensure that the "
        "necessary claims are provided and try again."
    )

    def __init__(self, path: str, method: str, claim: str, detail: str = description) -> None:
        self.path: str = path
        self.method: str = method
        self.claim: str = claim
        self.detail: str = detail
        super().__init__(self.detail)

    def __str__(self) -> str:
        return f"Missing essential claim {self.claim} in request {self.method} {self.path} ({self.detail})"

class InvalidClaimValueException(ClaimValidatorException):
    """Exception raised when a claim has an invalid value.

    This exception is used in the ClaimValidatorMiddleware to indicate that 
    a claim provided in the JWT claims has an invalid value.
    It is raised when the `raise_on_invalid_claim` flag is set to True and 
    a claim is found to have an invalid value during validation.

    Attributes:
        path (str): The path of the request.
        method (str): The HTTP method of the request.
        claim (str): The name of the invalid claim.
        detail (str): A detailed error message.
    """
    description: str = (
        "A claim has an invalid value. Ensure that the claims provided have "
        "valid values and try again."
    )

    def __init__(self, path: str, method: str, claim: str, detail: str = description) -> None:
        self.path: str = path
        self.method: str = method
        self.claim: str = claim
        self.detail: str = detail
        super().__init__(self.detail)

    def __str__(self) -> str:
        return f"Invalid claim value {self.claim} in request {self.method} {self.path} ({self.detail})"
    
class InvalidClaimsTypeException(ClaimValidatorException):
    """Exception raised when the claims provided are not of the expected type.

    This exception is raised when the claims provided to the ClaimValidatorMiddleware
    are not of the expected type. It indicates that the claims should be a dictionary
    but are not.

    Attributes:
        path (str): The path of the request.
        method (str): The HTTP method of the request.
        detail (str): A detailed error message.
    """
    description: str = (
        "The claims provided are not of the expected type. Ensure that the claims are "
        "correctly formatted as a dictionary and try again."
    )

    def __init__(self, path: str, method: str, type_received: str, type_expected: str, detail: str = description) -> None:
        self.path: str = path
        self.method: str = method
        self.type_received: str = type_received
        self.type_expected: str = type_expected
        self.detail: str = detail
        super().__init__(self.detail)

    def __str__(self) -> str:
        return f"Invalid claims type in request {self.method} {self.path} (received: {self.type_received}; expected: {self.type_expected}) ({self.detail})"