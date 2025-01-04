import re
from collections.abc import Callable
from joserfc.jwt import ClaimsOption, Claims

SecuredCompiledType = dict[re.Pattern, dict[str, dict[str, ClaimsOption]]]
SecuredType = dict[str, dict[str, dict[str, ClaimsOption]]]
SkippedCompiledType = dict[re.Pattern, set[str]]
SkippedType = dict[str, list[str]]
ClaimsType = Claims
ClaimsCallableType = Callable[..., Claims]