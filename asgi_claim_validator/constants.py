from asgi_claim_validator.types import SecuredType, SkippedType, ClaimsCallableType

_DEFAULT_ANY_HTTP_METHOD: str = "*"
_DEFAULT_CLAIMS_CALLABLE: ClaimsCallableType = lambda: dict()
_DEFAULT_RAISE_ON_INVALID_CLAIM: bool = True
_DEFAULT_RAISE_ON_INVALID_CLAIMS_TYPE: bool = True
_DEFAULT_RAISE_ON_MISSING_CLAIM: bool = True
_DEFAULT_RAISE_ON_UNAUTHENTICATED: bool = True
_DEFAULT_RAISE_ON_UNSPECIFIED_METHOD: bool = True
_DEFAULT_RAISE_ON_UNSPECIFIED_PATH: bool = True
_DEFAULT_RE_IGNORECASE: bool = False
_DEFAULT_SECURED: SecuredType = dict()
_DEFAULT_SKIPPED: SkippedType = dict()
_DEFAULT_SKIPPED_JSON_SCHEMA: dict = {
    "title": "Skipped JSON Schema",
    "description": "Schema for validating skipped configuration",
    "type": "object",
    "minProperties": 1,
    "patternProperties": {
        "^(.+)$": {
            "type": "array",
            "items": {
                "oneOf": [
                    {
                        "type": "string",
                        "pattern": "^(?i:DELETE|GET|HEAD|OPTIONS|PATCH|POST|PUT|{_DEFAULT_ANY_HTTP_METHOD})$"
                    },
                    { "type": "null" }
                ]
            }
        }
    },
    "additionalProperties": False,
    "unevaluatedProperties": False
}
_DEFAULT_SECURED_JSON_SCHEMA: dict = {
    "title": "Secured JSON Schema",
    "description": "Schema for validating secured configuration",
    "type": "object",
    "minProperties": 1,
    "patternProperties": {
        "^(.+)$": {
            "type": "object",
            "minProperties": 1,
            "patternProperties": {
                f"^(?i:DELETE|GET|HEAD|OPTIONS|PATCH|POST|PUT|{_DEFAULT_ANY_HTTP_METHOD})$": {
                    "type": "object",
                    "minProperties": 1,
                    "patternProperties": {
                        "^(.+)$": {
                            "type": "object",
                            "minProperties": 1,
                            "properties": {
                                "essential": {
                                    "oneOf": [
                                        {"type": "boolean"}
                                    ]
                                },
                                "allow_blank": {
                                    "oneOf": [
                                        {"type": "boolean"},
                                        {"type": "null"}
                                    ]
                                },
                                "values": {
                                    "type": "array",
                                    "items": {
                                        "oneOf": [
                                            {"type": "boolean"},
                                            {"type": "integer"},
                                            {"type": "string"}
                                        ]
                                    }
                                }
                            },
                            "required": ["essential", "values"],
                            "additionalProperties": False,
                            "unevaluatedProperties": False
                        }
                    },
                    "additionalProperties": False,
                    "unevaluatedProperties": False
                }
            },
            "additionalProperties": False,
            "unevaluatedProperties": False
        }
    },
    "additionalProperties": False,
    "unevaluatedProperties": False
}