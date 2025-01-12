[![PyPI - License](https://img.shields.io/pypi/l/asgi-claim-validator)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI - Version](https://img.shields.io/pypi/v/asgi-claim-validator.svg)](https://pypi.org/project/asgi-claim-validator/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/asgi-claim-validator)](https://pypi.org/project/asgi-claim-validator/)
[![PyPI - Status](https://img.shields.io/pypi/status/asgi-claim-validator)](https://pypi.org/project/asgi-claim-validator/)
[![Dependencies](https://img.shields.io/librariesio/release/pypi/asgi-claim-validator)](https://libraries.io/pypi/asgi-claim-validator)
[![Last Commit](https://img.shields.io/github/last-commit/feteu/asgi-claim-validator)](https://github.com/feteu/asgi-claim-validator/commits/main)
[![Build Status build/testpypi](https://img.shields.io/github/actions/workflow/status/feteu/asgi-claim-validator/publish-testpypi.yaml?label=publish-testpypi)](https://github.com/feteu/asgi-claim-validator/actions/workflows/publish-testpypi.yaml)
[![Build Status build/pypi](https://img.shields.io/github/actions/workflow/status/feteu/asgi-claim-validator/publish-pypi.yaml?label=publish-pypi)](https://github.com/feteu/asgi-claim-validator/actions/workflows/publish-pypi.yaml)
[![Build Status test](https://img.shields.io/github/actions/workflow/status/feteu/asgi-claim-validator/test.yaml?label=test)](https://github.com/feteu/asgi-claim-validator/actions/workflows/test.yaml)

# asgi-claim-validator

A focused ASGI middleware for validating additional claims within JWT tokens to enhance token-based workflows.

## Overview

`asgi-claim-validator` is an ASGI middleware designed to validate additional claims within JWT tokens. Built in addition to the default JWT verification implementation of Connexion, it enhances token-based workflows by ensuring that specific claims are present and meet certain criteria before allowing access to protected endpoints. This middleware allows consumers to validate claims on an endpoint/method level and is compatible with popular ASGI frameworks such as Starlette, FastAPI, and Connexion.

## Features

- **Claim Validation**: Validate specific claims within JWT tokens, such as `sub`, `iss`, `aud`, `exp`, `iat`, and `nbf`.
- **Customizable Claims**: Define essential claims, allowed values, and whether blank values are permitted.
- **Path and Method Filtering**: Apply claim validation to specific paths and HTTP methods.
- **Exception Handling**: Integrate with custom exception handlers to provide meaningful error responses.
- **Logging**: Log validation errors for debugging and monitoring purposes.

## Installation

Install the package using pip:

```sh
pip install asgi-claim-validator
```

## Usage

### Basic Usage

```python
from asgi_claim_validator.middleware import ClaimValidatorMiddleware
from starlette.applications import Starlette

app = Starlette()

# This needs to be specified and is most likely differente dependent on the framework
# it needs to return a already validated decoded token content (dict)
claims_callable = lambda: {
    "sub": "<subject>",
    "iss": "<issuer>",
}

app.add_middleware(
    ClaimValidatorMiddleware,
    claims_callable=claims_callable,
    secured={
        "^/secured$": {
            "GET": {
                "sub": {
                    "essential": True,
                    "allow_blank": False,
                    "values": ["admin"],
                },
                "iss": {
                    "essential": True,
                    "allow_blank": False,
                    "values": ["https://example.com"],
                },
            },
        }
    },
    skipped={
        "^/skipped$": ["GET"],
    },
)
```

## Examples

### Starlette Example
Refer to the [app.py](examples/starlette/simple/app.py) file for a complete example using Starlette.

### Connexion Example
Refer to the [app.py](examples/connexion/simple/app.py) file for a complete example using Connexion.

## Testing
Run the tests using `pytest`:

```sh
poetry run pytest
```

## Contributing
Contributions are welcome! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License
This project is licensed under the GNU GPLv3 License. See the [LICENSE](LICENSE) file for more details.