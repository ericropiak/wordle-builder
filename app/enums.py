import enum


class LoginAttemptResult(enum.Enum):
    SUCCESS = 'Success'
    INCORRECT_PASSCODE = 'Incorrect passcode'
