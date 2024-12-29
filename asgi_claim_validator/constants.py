from joserfc.jwt import ClaimsOption

_DEFAULT_ANY_HTTP_METHOD: str = "*"
_DEFAULT_CLAIMS: callable = lambda: dict()
_DEFAULT_RAISE_ON_INVALID_CLAIM: bool = True
_DEFAULT_RAISE_ON_INVALID_CLAIMS_TYPE: bool = True
_DEFAULT_RAISE_ON_MISSING_CLAIM: bool = True
_DEFAULT_RAISE_ON_UNAUTHENTICATED: bool = True
_DEFAULT_RAISE_ON_UNSPECIFIED_METHOD: bool = True
_DEFAULT_RAISE_ON_UNSPECIFIED_PATH: bool = True
_DEFAULT_RE_IGNORECASE: bool = False
_DEFAULT_SECURED: dict[str, dict[str, dict[str, ClaimsOption]]] = dict()
_DEFAULT_SKIPPED: dict[str, list[str]] = dict()
