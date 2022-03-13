import enum


class LoginAttemptResult(enum.Enum):
    SUCCESS = 'Success'
    INCORRECT_PASSCODE = 'Incorrect passcode'


class GuessingGameFacetType(enum.Enum):
    INTEGER = 'Integer'
    ENUM = 'Enum'
    BOOLEAN = 'Boolean'


class GuessingGameFacetPropertyType(enum.Enum):
    DEGREES_OF_CLOSENESS = 'Degrees Of Closeness'
