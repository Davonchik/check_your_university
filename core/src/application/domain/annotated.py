from fastapi import Header
from typing_extensions import Annotated

TokenAnnotated = Annotated[
    str,
    Header(
        alias='X-Auth-Token',
    )
]