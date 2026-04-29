from enum import Enum, auto

# Enum with available image formats (for jupyter)
class _ImgFormat(Enum):
    PNG = 1
    SVG = 2

# A special class to debug graphviz generated code
class _DebugGraphviz():
    source: str = ""

# Enum with available formats for duplicate edge handling during conversion
class EdgeOverrideMode(Enum):
    MINIMUM = auto()
    MAXIMUM = auto()
    AVERAGE = auto()
    IGNORE = auto()
    EXCEPTION = auto()