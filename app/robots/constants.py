import enum


class RobotDataFrameType(enum.IntEnum):
    POSITION = 1
    GEO = 2
    HARDWARE = 3


class RobotCommand(enum.Enum):
    AUTO = 'auto'
    IDLE = 'idle'
    ERROR = 'error'
    MANUAL = 'manual'
