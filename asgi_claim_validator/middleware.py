from dataclasses import dataclass, field
from joserfc.errors import InvalidClaimError, MissingClaimError
from joserfc.jwt import JWTClaimsRegistry
from logging import DEBUG, getLogger
from re import compile, error, IGNORECASE, NOFLAG, Pattern, RegexFlag
from starlette.types import ASGIApp, Receive, Scope, Send
from asgi_claim_validator.constants import (
    _DEFAULT_ANY_HTTP_METHODS,
    _DEFAULT_CLAIMS_CALLABLE,
    _DEFAULT_RAISE_ON_INVALID_CLAIM,
    _DEFAULT_RAISE_ON_INVALID_CLAIMS_TYPE,
    _DEFAULT_RAISE_ON_MISSING_CLAIM,
    _DEFAULT_RAISE_ON_UNAUTHENTICATED,
    _DEFAULT_RAISE_ON_UNSPECIFIED_METHOD,
    _DEFAULT_RAISE_ON_UNSPECIFIED_PATH,
    _DEFAULT_RE_IGNORECASE,
    _DEFAULT_SECURED,
    _DEFAULT_SKIPPED,
)
from asgi_claim_validator.decorators import (
    validate_claims_callable,
    validate_secured,
    validate_skipped,
)
from asgi_claim_validator.exceptions import (
    InvalidClaimsTypeException,
    InvalidClaimValueException,
    MissingEssentialClaimException,
    UnauthenticatedRequestException,
    UnspecifiedMethodAuthenticationException,
    UnspecifiedPathAuthenticationException,
)
from asgi_claim_validator.types import (
    ClaimsCallableType, 
    SecuredCompiledType, 
    SecuredType, 
    SkippedCompiledType, 
    SkippedType,
)

log = getLogger(__name__)

@dataclass
class ClaimValidatorMiddleware:
    """
    Middleware for validating JWT claims in ASGI applications.

    Attributes:
        app (ASGIApp): The ASGI application.
        claims_callable (ClaimsCallableType): A callable that returns the claims.
        raise_on_invalid_claim (bool): Flag to raise an exception on invalid claims.
        raise_on_invalid_claims_type (bool): Flag to raise an exception on invalid claims type.
        raise_on_missing_claim (bool): Flag to raise an exception on missing claims.
        raise_on_unauthenticated (bool): Flag to raise an exception on unauthenticated requests.
        raise_on_unspecified_method (bool): Flag to raise an exception on unspecified methods.
        raise_on_unspecified_path (bool): Flag to raise an exception on unspecified paths.
        re_flags (RegexFlag): Regular expression flags.
        re_ignorecase (bool): Flag to ignore case in regular expressions.
        secured_compiled (SecuredCompiledType): Compiled secured paths and methods.
        secured (SecuredType): Secured paths and methods.
        skipped_compiled (SkippedCompiledType): Compiled skipped paths and methods.
        skipped (SkippedType): Skipped paths and methods.
    """
    app: ASGIApp
    claims_callable: ClaimsCallableType = field(default=_DEFAULT_CLAIMS_CALLABLE)
    raise_on_invalid_claim: bool = field(default=_DEFAULT_RAISE_ON_INVALID_CLAIM)
    raise_on_invalid_claims_type: bool = field(default=_DEFAULT_RAISE_ON_INVALID_CLAIMS_TYPE)
    raise_on_missing_claim: bool = field(default=_DEFAULT_RAISE_ON_MISSING_CLAIM)
    raise_on_unauthenticated: bool = field(default=_DEFAULT_RAISE_ON_UNAUTHENTICATED)
    raise_on_unspecified_method: bool = field(default=_DEFAULT_RAISE_ON_UNSPECIFIED_METHOD)
    raise_on_unspecified_path: bool = field(default=_DEFAULT_RAISE_ON_UNSPECIFIED_PATH)
    re_flags: RegexFlag = field(default=NOFLAG, init=False)
    re_ignorecase: bool = field(default=_DEFAULT_RE_IGNORECASE)
    secured_compiled: SecuredCompiledType = field(default_factory=dict, init=False)
    secured: SecuredType = field(default_factory=lambda: _DEFAULT_SECURED)
    skipped_compiled: SkippedCompiledType = field(default_factory=dict, init=False)
    skipped: SkippedType = field(default_factory=lambda: _DEFAULT_SKIPPED)
  
    @validate_claims_callable()
    @validate_secured()
    @validate_skipped()
    def __post_init__(self) -> None:
        """
        Post-initialization method to compile regular expressions for secured and skipped paths.

        This method is called after the object is initialized. It compiles the regular expressions
        for the paths specified in the `secured` and `skipped` attributes, and associates them with
        their corresponding HTTP methods and claims.

        Attributes:
            re_flags (int): Regular expression flags, set to IGNORECASE if `re_ignorecase` is True, otherwise NOFLAG.
            secured_compiled (dict): A dictionary where keys are compiled regular expressions for secured paths,
                                    and values are dictionaries mapping HTTP methods to their corresponding claims.
            skipped_compiled (dict): A dictionary where keys are compiled regular expressions for skipped paths,
                                    and values are sets of HTTP methods in uppercase.

        Raises:
            ValueError: If there is an invalid regular expression in the `secured` or `skipped` paths.
        """
        try:
            self.re_flags = IGNORECASE if self.re_ignorecase else NOFLAG
            # This code compiles regular expressions for each path in self.secured and associates them with a 
            # dictionary of HTTP methods in uppercase and their corresponding claims.
            self.secured_compiled = {
                compile(path, flags=self.re_flags): { 
                    method.upper(): claims for method, claims in methods.items()
                } for path, methods in self.secured.items()
            }
            # This code compiles regular expressions for each path in self.skipped and associates them with the 
            # corresponding HTTP methods in uppercase.
            self.skipped_compiled = {
                compile(path, flags=self.re_flags): set(
                    method.upper() for method in methods
                ) for path, methods in self.skipped.items()
            }
        except error as e:
            raise ValueError(f"Invalid regular expression in secured or skipped paths: {e}")

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        ASGI application callable to validate JWT claims.

        Args:
            scope (Scope): The ASGI scope.
            receive (Receive): The ASGI receive callable.
            send (Send): The ASGI send callable.

        Raises:
            InvalidClaimValueException: If a claim value is invalid and raise_on_invalid_claim is True.
            MissingEssentialClaimException: If a required claim is missing and raise_on_missing_claim is True.
            UnauthenticatedRequestException: If the request is unauthenticated and raise_on_unauthenticated is True.
            UnspecifiedMethodAuthenticationException: If the method is not specified and raise_on_unspecified_method is True.
            UnspecifiedPathAuthenticationException: If the path is not specified and raise_on_unspecified_path is True.
        """
        if scope["type"] not in ("http",):
            await self.app(scope, receive, send)
            return

        method = scope["method"].upper()
        path = scope["path"]
        claims = self.claims_callable()

        # Check if the request path matches any skipped path patterns and if the request method is allowed for that path.
        # If both conditions are met, forward the request to the next middleware or application.
        for p in self._search_patterns_in_string(path, self.skipped_compiled.keys()):
            if any(sc_method in (method, _DEFAULT_ANY_HTTP_METHODS) for sc_method in self.skipped_compiled[p]):
                await self.app(scope, receive, send)
                return

        if self.raise_on_invalid_claims_type and not isinstance(claims, dict):
            raise InvalidClaimsTypeException(path=path, method=method, type_received=type(claims), type_expected=dict)

        if self.raise_on_unauthenticated and not claims:
            raise UnauthenticatedRequestException(path=path, method=method)

        # This dictionary comprehension filters the secured_compiled dictionary to include only those patterns
        # that match the current URL path. It creates a new dictionary where the keys are the patterns that match the URL path.
        filtered_patterns = {
            p: self.secured_compiled[p] for p in self._search_patterns_in_string(path, self.secured_compiled.keys())    
        }

        if self.raise_on_unspecified_path and not filtered_patterns:
            raise UnspecifiedPathAuthenticationException(path=path, method=method)

        # This dictionary comprehension filters the previously created filtered_patterns dictionary to include only those methods
        # that match the current HTTP method. It creates a new dictionary where the keys are the paths and the values
        # are dictionaries of methods and their corresponding claims that match the current HTTP method.
        filtered_patterns = {
            fp_path: {
                fp_method: fp_claims for fp_method, fp_claims in fp_methods.items() if fp_method in (method, _DEFAULT_ANY_HTTP_METHODS)
            } for fp_path, fp_methods in filtered_patterns.items()
        }

        if self.raise_on_unspecified_method and all(not fp_methods for fp_methods in filtered_patterns.values()):
            raise UnspecifiedMethodAuthenticationException(path=path, method=method)

        # This block iterates over filtered patterns of paths and methods, validates JWT claims for each method,
        # and logs any errors encountered during the validation process.
        for fp_path, fp_methods in filtered_patterns.items():
            for fp_method, fp_claims in fp_methods.items():
                if log.isEnabledFor(DEBUG):
                    log.debug(f"path: {path} | method: {method} | claims: {claims}")
                    log.debug(f"fp_path: {fp_path} | fp_method: {fp_method} | fp_claims: {fp_claims}")
                try:
                    claims_requests = JWTClaimsRegistry(**fp_claims)
                    claims_requests.validate(claims)
                except MissingClaimError as e:
                    log.debug(f"Missing claim: {e}")
                    if self.raise_on_missing_claim:
                        raise MissingEssentialClaimException(path=path, method=method, claims=claims)
                except InvalidClaimError as e:
                    log.debug(f"Invalid claim: {e}")
                    if self.raise_on_invalid_claim:
                        raise InvalidClaimValueException(path=path, method=method, claims=claims)
                except Exception as e:
                    log.error(f"Unexpected error during claim validation: {e}")
                    raise e

        await self.app(scope, receive, send)
        return

    @staticmethod
    def _search_patterns_in_string(s: str, patterns: list[Pattern]) -> list[Pattern]:
        """
        Searches for patterns in a given string and returns the patterns that match.

        This method iterates over a list of compiled regular expression patterns and checks if each pattern matches the given string `s`. 
        The method returns a list of patterns that have at least one match in the string.

        Args:
            s (str): The string to search within.
            patterns (list[Pattern]): A list of compiled regular expression patterns to search for.

        Returns:
            list[Pattern]: A list of patterns that match the string.
        """
        return [p for p in patterns if p.search(s)]