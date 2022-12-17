from __future__ import annotations

import pygame
from pygame.surface import Surface

from .displayable import Image


def loadImage(path: str) -> Image:
    """Loads an image from disk

    Args:
        path: the file path to the image

    Returns:
        Image: the resulting image displayable
    """
    image = pygame.image.load(path)
    if _hasAlphaChannel(image):
        image = image.convert_alpha()
    else:
        image = image.convert()
    return Image(image)


def _hasAlphaChannel(surface: Surface) -> bool:
    """Returns whether a provided surface has an alpha channel"""

    return (surface.get_flags() & pygame.SRCALPHA) != 0
