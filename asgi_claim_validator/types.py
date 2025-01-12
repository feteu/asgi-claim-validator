from collections.abc import Callable
from joserfc.jwt import ClaimsOption, Claims
from re import Pattern

SecuredCompiledType = dict[Pattern, dict[str, dict[str, ClaimsOption]]]
SecuredType = dict[str, dict[str, dict[str, ClaimsOption]]]
SkippedCompiledType = dict[Pattern, set[str]]
SkippedType = dict[str, list[str]]
ClaimsType = Claims
ClaimsCallableType = Callable[..., Claims]