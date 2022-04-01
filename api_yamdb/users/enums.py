from enum import Enum


class ChoiceEnum(Enum):

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Role(ChoiceEnum):
    """Class Role(enum)."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
