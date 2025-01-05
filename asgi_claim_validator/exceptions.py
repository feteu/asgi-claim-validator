class ClaimValidatorException(Exception):
    """Base exception for claim validator-related errors.

    This is the base class for all exceptions raised by the claim validator.
    It provides a common interface for handling errors related to claim validation.

    Attributes:
        description (str): A brief description of the error.
        status (int): The HTTP status code.
        title (str): A short HTTP status message.
    """
    description: str = "A claim validator error occurred."
    status: int = 400
    title: str = "Bad Request"

    def __init__(self, detail: str = description, status: int = status, title: str = title) -> None:
        self.detail: str = detail
        self.status: int = status
        self.title: str = title
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
        status (int): The HTTP status code.
        title (str): A short HTTP status message.
    """
    description: str = (
        "Authentication configuration missing for the specified method. "
        "Ensure that an appropriate authentication definition is provided "
        "for this method and try again."
    )
    status: int = 401
    title: str = "Unauthorized"

    def __init__(self, method: str, path: str, detail: str = description, status: int = status, title: str = title) -> None:
        self.method: str = method
        self.path: str = path
        self.detail: str = detail
        self.status: int = status
        self.title: str = title
        super().__init__(self.detail, self.status, self.title)

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
        status (int): The HTTP status code.
        title (str): A short HTTP status message.
    """
    description: str = (
        "Authentication configuration missing for the specified path. "
        "Ensure that an appropriate authentication definition is provided "
        "for this path and try again."
    )
    status: int = 401
    title: str = "Unauthorized"

    def __init__(self, method: str, path: str, detail: str = description, status: int = status, title: str = title) -> None:
        self.method: str = method
        self.path: str = path
        self.detail: str = detail
        self.status: int = status
        self.title: str = title
        super().__init__(self.detail, self.status, self.title)

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
        status (int): The HTTP status code.
        title (str): A short HTTP status message.
    """
    description: str = (
        "The request could not be authenticated. Ensure that the necessary "
        "claims are provided and try again."
    )
    status: int = 401
    title: str = "Unauthorized"

    def __init__(self, path: str, method: str, detail: str = description, status: int = status, title: str = title) -> None:
        self.path: str = path
        self.method: str = method
        self.detail: str = detail
        self.status: int = status
        self.title: str = title
        super().__init__(self.detail, self.status, self.title)

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
        claims (str): The claims in the request.
        detail (str): A detailed error message.
        status (int): The HTTP status code.
        title (str): A short HTTP status message.
    """
    description: str = (
        "An essential claim is missing from the request. Ensure that the "
        "necessary claims are provided and try again."
    )
    status: int = 403
    title: str = "Forbidden"

    def __init__(self, path: str, method: str, claims: str, detail: str = description, status: int = status, title: str = title) -> None:
        self.path: str = path
        self.method: str = method
        self.claims: str = claims
        self.detail: str = detail
        self.status: int = status
        self.title: str = title
        super().__init__(self.detail, self.status, self.title)

    def __str__(self) -> str:
        return f"Missing essential claims in request {self.method} {self.path} {self.claims} ({self.detail})"

class InvalidClaimValueException(ClaimValidatorException):
    """Exception raised when a claim has an invalid value.

    This exception is used in the ClaimValidatorMiddleware to indicate that 
    a claim provided in the JWT claims has an invalid value.
    It is raised when the `raise_on_invalid_claim` flag is set to True and 
    a claim is found to have an invalid value during validation.

    Attributes:
        path (str): The path of the request.
        method (str): The HTTP method of the request.
        claims (str): The claims in the request.
        detail (str): A detailed error message.
        status (int): The HTTP status code.
        title (str): A short HTTP status message.
    """
    description: str = (
        "A claim has an invalid value. Ensure that the claims provided have "
        "valid values and try again."
    )
    status: int = 403
    title: str = "Forbidden"

    def __init__(self, path: str, method: str, claims: str, detail: str = description, status: int = status, title: str = title) -> None:
        self.path: str = path
        self.method: str = method
        self.claims: str = claims
        self.detail: str = detail
        self.status: int = status
        self.title: str = title
        super().__init__(self.detail, self.status, self.title)

    def __str__(self) -> str:
        return f"Invalid claims value in request {self.method} {self.path} {self.claims} ({self.detail})"
    
class InvalidClaimsTypeException(ClaimValidatorException):
    """Exception raised when the claims provided are not of the expected type.

    This exception is raised when the claims provided to the ClaimValidatorMiddleware
    are not of the expected type. It indicates that the claims should be a dictionary
    but are not.

    Attributes:
        path (str): The path of the request.
        method (str): The HTTP method of the request.
        type_received (str): The type of the claims received.
        type_expected (str): The expected type of the claims.
        detail (str): A detailed error message.
        status (int): The HTTP status code.
        title (str): A short HTTP status message.
    """
    description: str = (
        "The claims provided are not of the expected type. Ensure that the claims are "
        "correctly formatted as a dictionary and try again."
    )
    status: int = 400
    title: str = "Bad Request"

    def __init__(self, path: str, method: str, type_received: str, type_expected: str, detail: str = description, status: int = status, title: str = title) -> None:
        self.path: str = path
        self.method: str = method
        self.type_received: str = type_received
        self.type_expected: str = type_expected
        self.detail: str = detail
        self.status: int = status
        self.title: str = title
        super().__init__(self.detail, self.status, self.title)

    def __str__(self) -> str:
        return f"Invalid claims type in request {self.method} {self.path} (received: {self.type_received}; expected: {self.type_expected}) ({self.detail})"

class InvalidClaimsConfigurationException(ClaimValidatorException):
    """Exception raised when the claims configuration is invalid.

    This exception is used to indicate that the claims callable provided
    does not return an instance of Claims. It is raised during the initialization
    of the ClaimValidatorMiddleware when the `claims` parameter is not callable
    or does not return the expected type.

    Attributes:
        detail (str): A detailed error message.
        status (int): The HTTP status code.
        title (str): A short HTTP status message.
    """
    description: str = (
        "The claims callable must return an instance of Claims. Ensure that the "
        "claims callable is correctly referenced and returns the expected type."
    )
    status: int = 500
    title: str = "Internal Server Error"

    def __init__(self, detail: str = description, status: int = status, title: str = title) -> None:
        self.detail: str = detail
        self.status: int = status
        self.title: str = title
        super().__init__(self.detail, self.status, self.title)

    def __str__(self) -> str:
        return f"Invalid claims callable: {self.detail}"

class InvalidSecuredConfigurationException(ClaimValidatorException):
    """Exception raised when the secured configuration is invalid.

    This exception is used to indicate that the secured dictionary provided
    is not correctly formatted or contains invalid values. It is raised during
    the initialization of the ClaimValidatorMiddleware.

    Attributes:
        detail (str): A detailed error message.
        status (int): The HTTP status code.
        title (str): A short HTTP status message.
    """
    description: str = (
        "The secured configuration is invalid. Ensure that the secured dictionary "
        "is correctly formatted and contains valid values."
    )
    status: int = 500
    title: str = "Internal Server Error"

    def __init__(self, detail: str = description, status: int = status, title: str = title) -> None:
        self.detail: str = detail
        self.status: int = status
        self.title: str = title
        super().__init__(self.detail, self.status, self.title)

    def __str__(self) -> str:
        return f"Invalid secured configuration: {self.detail}"

class InvalidSkippedConfigurationException(ClaimValidatorException):
    """Exception raised when the skipped configuration is invalid.

    This exception is used to indicate that the skipped dictionary provided
    is not correctly formatted or contains invalid values. It is raised during
    the initialization of the ClaimValidatorMiddleware.

    Attributes:
        detail (str): A detailed error message.
        status (int): The HTTP status code.
        title (str): A short HTTP status message.
    """
    description: str = (
        "The skipped configuration is invalid. Ensure that the skipped dictionary "
        "is correctly formatted and contains valid values."
    )
    status: int = 500
    title: str = "Internal Server Error"

    def __init__(self, detail: str = description, status: int = status, title: str = title) -> None:
        self.detail: str = detail
        self.status: int = status
        self.title: str = title
        super().__init__(self.detail, self.status, self.title)

    def __str__(self) -> str:
        return f"Invalid skipped configuration: {self.detail}"