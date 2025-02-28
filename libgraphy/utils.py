from enum import Enum

# Enum with available image formats (for jupyter)
class _ImgFormat(Enum):
    PNG = 1
    SVG = 2

# A special class to debug graphviz generated code
class _DebugGraphviz():
    source: str = ""
