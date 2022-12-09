ColorRGB = tuple[int, int, int]
"""A color represented by a (red, green, blue) tuple"""
ColorRGBA = tuple[int, int, int, int]
"""A color represented by a (red, green, blue, alpha) tuple"""
Color = (ColorRGB | ColorRGBA)

Point = tuple[int, int]
"""An (x, y) coordinate pair"""
Vector = tuple[int, int]
"""A 2-tuple meant to represent a direction"""
