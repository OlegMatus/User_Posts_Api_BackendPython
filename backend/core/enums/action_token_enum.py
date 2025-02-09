from datetime import timedelta
from enum import Enum


class ActionTokenEnum(Enum):
    ACTIVATE = (
        'activate',
        timedelta(hours=1)
    )

    def __init__(self, token_type: str, lifetime: timedelta):
        self.token_type = token_type
        self.lifetime = lifetime
