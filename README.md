[![PyPI - License](https://img.shields.io/pypi/l/asgi-claim-validator)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI - Version](https://img.shields.io/pypi/v/asgi-claim-validator.svg)](https://pypi.org/project/asgi-claim-validator/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/asgi-claim-validator)](https://pypi.org/project/asgi-claim-validator/)
[![PyPI - Status](https://img.shields.io/pypi/status/asgi-claim-validator)](https://pypi.org/project/asgi-claim-validator/)
[![Dependencies](https://img.shields.io/librariesio/release/pypi/asgi-claim-validator)](https://libraries.io/pypi/asgi-claim-validator)
[![Last Commit](https://img.shields.io/github/last-commit/feteu/asgi-claim-validator)](https://github.com/feteu/asgi-claim-validator/commits/main)
[![Build Status build/testpypi](https://img.shields.io/github/actions/workflow/status/feteu/asgi-claim-validator/publish-testpypi.yaml?label=publish-testpypi)](https://github.com/feteu/asgi-claim-validator/actions/workflows/publish-testpypi.yaml)
[![Build Status build/pypi](https://img.shields.io/github/actions/workflow/status/feteu/asgi-claim-validator/publish-pypi.yaml?label=publish-pypi)](https://github.com/feteu/asgi-claim-validator/actions/workflows/publish-pypi.yaml)
[![Build Status test](https://img.shields.io/github/actions/workflow/status/feteu/asgi-claim-validator/test.yaml?label=test)](https://github.com/feteu/asgi-claim-validator/actions/workflows/test.yaml)

# asgi-claim-validator 🚀

A focused ASGI middleware for validating additional claims within JWT tokens to enhance token-based workflows.

> **Note:** If you find this project useful, please consider giving it a star ⭐ on GitHub. This helps prioritize its maintenance and development. If you encounter any typos, bugs 🐛, or have new feature requests, feel free to open an issue. I will be happy to address them.


## Table of Contents 📑

1. [Overview 📖](#overview-)
    1. [Purpose 🎯](#purpose-)
    2. [Key Features ✨](#key-features-)
    3. [Use Cases 💡](#use-cases-)
    4. [Compatibility 🤝](#compatibility-)
2. [Installation 🛠️](#installation-)
3. [Usage 📚](#usage-)
    1. [Basic Usage 🌟](#basic-usage)
    2. [Configuration ⚙️](#configuration-)
    3. [Error Handlers 🚨](#error-handlers-)
4. [Examples 📝](#examples-)
5. [Testing 🧪](#testing-)
6. [Contributing 🤝](#contributing-)
7. [License 📜](#license-)


## Overview 📖

`asgi-claim-validator` is an ASGI middleware designed to validate additional claims within JWT tokens. Built in addition to the default JWT verification implementation of Connexion, it enhances token-based workflows by ensuring that specific claims are present and meet certain criteria before allowing access to protected endpoints. This middleware allows consumers to validate claims on an endpoint/method level and is compatible with popular ASGI frameworks such as Starlette, FastAPI, and Connexion.

### Purpose 🎯

The primary purpose of `asgi-claim-validator` is to provide an additional layer of security by validating specific claims within JWT tokens. This ensures that only requests with valid and authorized tokens can access protected resources. The middleware is highly configurable, allowing developers to define essential claims, allowed values, and whether blank values are permitted. It also supports path and method filtering, enabling claim validation to be applied selectively based on the request path and HTTP method.

### Key Features ✨

- **Claim Validation**: Validate specific claims within JWT tokens, such as `sub`, `iss`, `aud`, `exp`, `iat`, and `nbf`.
- **Customizable Claims**: Define essential claims, allowed values, and whether blank values are permitted.
- **Path and Method Filtering**: Apply claim validation to specific paths and HTTP methods.
- **Exception Handling**: Integrate with custom exception handlers to provide meaningful error responses.
- **Logging**: Log validation errors for debugging and monitoring purposes.
- **Flexible Configuration**: Easily configure the middleware using a variety of options to suit different use cases.
- **Middleware Positioning**: Integrate the middleware at different positions within the ASGI application stack.
- **Token Extraction**: Extract tokens from various parts of the request, such as headers, cookies, or query parameters.
- **Custom Claim Validators**: Implement custom claim validation logic by providing your own validation functions.
- **Support for Multiple Frameworks**: Compatible with popular ASGI frameworks such as Starlette, FastAPI, and Connexion.
- **Performance Optimization**: Efficiently handle claim validation with minimal impact on request processing time.
- **Extensive Test Coverage**: Comprehensive test suite to ensure reliability and correctness of the middleware.

### Use Cases 💡

- **API Security**: Enhance the security of your API by ensuring that only requests with valid JWT tokens and specific claims can access protected endpoints.
- **Role-Based Access Control**: Implement role-based access control by validating claims that represent user roles and permissions.
- **Compliance**: Ensure compliance with security policies by enforcing the presence and validity of specific claims within JWT tokens.
- **Custom Authentication Logic**: Implement custom authentication logic by providing your own claim validation functions.

### Compatibility 🤝

`asgi-claim-validator` is compatible with popular ASGI frameworks such as Starlette, FastAPI, and Connexion. It can be easily integrated into existing ASGI applications and configured to suit various use cases and requirements.

By using `asgi-claim-validator`, you can enhance the security and flexibility of your token-based authentication workflows, ensuring that only authorized requests can access your protected resources.


## Installation 🛠️

To install the `asgi-claim-validator` package, use the following pip command:

```sh
pip install asgi-claim-validator
```


## Usage 📚

### Basic Usage 🌟

Below is an example of how to integrate `ClaimValidatorMiddleware` with a Connexion application. This middleware validates specific claims within JWT tokens for certain endpoints.

The `ClaimValidatorMiddleware` requires several parameters to function correctly. The `claims_callable` parameter is a callable that extracts token information from the Connexion context. This parameter must be specified and is typically dependent on the framework being used. The `secured` parameter is a dictionary that defines the secured paths and the claims that need to be validated. For instance, in the provided example, the `/secured` path requires the `sub` claim to be `admin` and the `iss` claim to be `https://example.com` for GET requests. The `skipped` parameter is a dictionary that specifies the paths and methods that should be excluded from validation. In the example, the `/skipped` path is skipped for GET requests.

```python
from asgi_claim_validator.middleware import ClaimValidatorMiddleware
from connexion import AsyncApp

# Create a Connexion application
app = AsyncApp(__name__, specification_dir="spec")

# Add the ClaimValidatorMiddleware
app.add_middleware(
    ClaimValidatorMiddleware,
    claims_callable=lambda scope: scope["extensions"]["connexion_context"]["token_info"],
    secured={
        "^/secured/?$": {
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
        },
    },
    skipped={
        "^/skipped/?$": ["GET"],
    },
)
```


### Configuration ⚙️

The `ClaimValidatorMiddleware` requires two main configuration pieces: `secured` and `skipped`. These configurations are validated using JSON schemas to ensure correctness.

> **Note:** The path regex patterns provided in the `secured` and `skipped` parameters will be automatically escaped by the middleware.

#### Secured Configuration

The `secured` configuration is a dictionary that defines the paths and the claims that need to be validated. Each path is associated with a dictionary of HTTP methods, and each method is associated with a dictionary of claims. Each claim can have the following properties:
- `essential`: A boolean indicating whether the claim is essential.
- `allow_blank`: A boolean indicating whether blank values are allowed.
- `values`: A list of allowed values for the claim.

Example:
```python
secured={
    "^/secured/?$": {
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
    },
}
```

#### Skipped Configuration

The `skipped` configuration is a dictionary that defines the paths and methods that should be excluded from validation. Each path is associated with a list of HTTP methods.

Example:
```python
skipped={
    "^/skipped/?$": ["GET"],
}
```

#### JSON Schema Validation

Both `secured` and `skipped` configurations are validated using JSON schemas to ensure their correctness. This validation helps catch configuration errors early and ensures that the middleware behaves as expected.


### Error Handlers 🚨

To handle exceptions raised by this middleware, you can configure your framework (such as Starlette or Connexion) to catch and process them dynamically. For security reasons, the exception messages are kept generic, but you can customize them using the exception parameters.

#### Connexion

```python
from asgi_claim_validator import ClaimValidatorMiddleware, ClaimValidatorException
from connexion import AsyncApp
from connexion.lifecycle import ConnexionRequest, ConnexionResponse

# [...]

def claim_validator_error_handler(request: ConnexionRequest, exc: ClaimValidatorException) -> ConnexionResponse:
    return problem(detail=exc.detail, status=exc.status, title=exc.title)

app = AsyncApp(__name__, specification_dir="spec")
app.add_error_handler(ClaimValidatorException, claim_validator_error_handler)

# [...]
```

#### Starlette

```python
from asgi_claim_validator import ClaimValidatorMiddleware, ClaimValidatorException
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse

# [...]

async def claim_validator_error_handler(request: Request, exc: ClaimValidatorException) -> JSONResponse:
    return JSONResponse({"error": f"{exc.title}"}, status_code=exc.status)

exception_handlers = {
    ClaimValidatorException: claim_validator_error_handler
}

app = Starlette(routes=routes, exception_handlers=exception_handlers)

# [...]
```

## Examples 📝

### Starlette Example
To see a complete example using Starlette, refer to the [app.py](examples/starlette/simple/app.py) file.

### Connexion Example
Check out the [app.py](examples/connexion/simple/app.py) file for a simple example using Connexion. For a comprehensive example that demonstrates automatic extraction and validation of token claims with Connexion, see the [app.py](examples/connexion/complex/app.py) file.

## Testing 🧪
Run the tests using `pytest`:

```sh
poetry run pytest
```

### Scope:

- **Middleware Functionality**: Ensures correct validation of JWT claims and proper handling of secured and skipped paths.
- **Exception Handling**: Verifies that custom exceptions are raised and handled appropriately.
- **Configuration Validation**: Checks the correctness of middleware configuration for secured and skipped paths.
- **Integration with Frameworks**: Confirms seamless integration with ASGI frameworks like Starlette and Connexion.
- **Custom Claim Validators**: Tests the implementation and usage of custom claim validation logic.


## Contributing 🤝
Contributions are welcome! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.


## License 📜
This project is licensed under the GNU GPLv3 License. See the [LICENSE](LICENSE) file for more details.