import enum


class BaseEnum(enum.Enum):
    @classmethod
    def choices(cls):
        print('CHOICES', [(choice.name, choice.value) for choice in cls])
        return [(choice.name, choice.value) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return getattr(cls, item)

    def __str__(self):
        return str(self.value)


class LoginAttemptResult(BaseEnum):
    SUCCESS = 'Success'
    INCORRECT_PASSCODE = 'Incorrect passcode'


class GuessingGameFacetType(BaseEnum):
    INTEGER = 'Integer'
    ENUM = 'Enum'
    BOOLEAN = 'Boolean'


class GuessingGameFacetPropertyType(BaseEnum):
    DEGREES_OF_CLOSENESS = 'Degrees Of Closeness'


class GuessingGameFacetComparisonResult(BaseEnum):
    INCORRECT = 'Incorrect'
    CORRECT = 'Correct'
    CLOSE_LOW = 'Close Low'
    CLOSE_HIGH = 'Close High'
    LOW = 'Low'
    HIGH = 'High'
