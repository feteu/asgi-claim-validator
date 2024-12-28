import logging
import re
from dataclasses import dataclass, field
from joserfc import jwt, ClaimsOption
from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

log = logging.getLogger(__name__)

@dataclass
class ClaimValidatorMiddleware:
    app: ASGIApp
    excluded_paths_patterns: list[re.Pattern] = field(init=False)
    excluded_paths: list[str | None] = field(default_factory=list)
    secured_paths_patterns: dict[re.Pattern, dict[str, list[dict[str, ClaimsOption]]]] = field(init=False)
    secured_paths: dict[str, dict[str, list[dict[str, ClaimsOption]]]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.excluded_paths_patterns = [re.compile(path) for path in self.excluded_paths]
        self.secured_paths_patterns = {re.compile(path): config for path, config in self.secured_paths.items()}