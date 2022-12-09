from __future__ import annotations

import pygame
from pygame.event import Event
from pygame.rect import Rect
from pygame.surface import Surface

from typedefs import (
    Color,
    ColorRGB,
    Point
)

ERROR = -1
READY = 0
ACTIVE = 1
QUIT = 2


def hasAlphaChannel(surface: Surface) -> bool:
    """Returns whether a provided surface has an alpha channel
    """
    return (surface.get_flags() & pygame.SRCALPHA) != 0


def makeSurface(width: int, height: int, hasAlpha: bool) -> Surface:
    """Generates a new pygame surface

    Args:
        width (int): the desired width of the surface
        height (int): the desired height of the surface
        hasAlpha (bool): whether the surface should support alpha values

    Returns:
        Surface: a newly created surface with the given properties
    """
    surface = Surface((width, height))
    if hasAlpha:
        return surface.convert_alpha()
    return surface.convert()


def loadImage(path: str) -> Image:
    """Loads an image from disk

    Args:
        path (str): the file path to the image

    Returns:
        Image: the resulting image displayable
    """
    image = pygame.image.load(path)
    if hasAlphaChannel(image):
        image = image.convert_alpha()
    else:
        image = image.convert()
    return Image(image)


class Display:
    """Represents a display window that can be updated at a fixed framerate
    """

    def __init__(self,
                 width: int,
                 height: int,
                 frameRate: int = 60,
                 fillColor: ColorRGB = (0, 0, 0)):
        self.width = width
        self.height = height
        self._surface = pygame.display.set_mode((width, height))
        self.fillColor = fillColor

        self.frameRate = frameRate
        self._clock = pygame.time.Clock()

        self._displayables: list[Displayable] = []

        self.state = READY

    def show(self):
        """Causes the display to be shown
        """
        pygame.display.flip()
        self.state = ACTIVE

    def add(self, disp: Displayable, pos: Point, z: int = 0):
        """Adds a displayable to the display

        Args:
            disp (Displayable): the displayable to add
            pos (Point): the screen position at which to render the displayable
            z (int): the displayable's z order. Defaults to 0.
        """
        disp.position = pos
        disp.zOrder = z
        self._displayables.append(disp)
        # Maintain z-order sort
        self._displayables.sort(key=lambda x: x.zOrder)

    def tick(self):
        """Updates the display by one frame
        """
        self._processEvents()

        self._surface.fill(self.fillColor)
        for disp in self._displayables:
            surface = disp.render()
            self._surface.blit(surface, disp.position)

        pygame.display.update()
        self._clock.tick(self.frameRate)

    def _processEvents(self):
        events = pygame.event.get()
        if any(event.type == pygame.QUIT for event in events):
            self.state = QUIT
            return

        for event in events:
            # traverse in reverse z-order
            for child in self._displayables[::-1]:
                # stop once the event has been successfully handled
                if child.handle(event):
                    break

class Displayable:
    """Abstract class for display elements
    """
    position: Point
    zOrder: int

    def render(self) -> Surface:
        """Returns a pygame surface to be displayed
        """
        raise NotImplementedError(
            "Child class does not override render method")

    def handle(self, event: Event) -> bool:
        """Responds to events passed to the displayable

        Args:
            event (Event): the event to respond to

        Returns:
            bool: whether the event was successfully handled
        """
        return False


class Panel(Displayable):
    """A display element that can contain child displayables
    """

    def __init__(self,
                 width: int,
                 height: int,
                 fillColor: Color = (0, 0, 0, 0),
                 background: (Image | None) = None):
        self.fillColor = fillColor

        if background is not None:
            # Scale the image to fit the panel
            self.background = background.scale((width, height))
        else:
            self.background = None

        self._surface = makeSurface(width,
                                    height,
                                    len(self.fillColor) == 4)
        self._children: list[Displayable] = []

    def add(self, disp: Displayable, pos: Point, z: int = 0):
        """Adds a child displayable to the panel

        Args:
            disp (Displayable): the displayable to add
            pos (Point): the position at which to display the child
            z (int, optional): the child's z layer. Defaults to 0.
        """
        disp.position = pos
        disp.zOrder = z
        self._children.append(disp)

    def render(self) -> Surface:
        self._surface.fill(self.fillColor)

        if self.background is not None:
            background = self.background.render()
            self._surface.blit(background, (0, 0))

        for child in sorted(self._children, key=lambda x: x.zOrder):
            surface = child.render()
            self._surface.blit(surface, child.position)

        return self._surface


class Image(Displayable):
    """An image display element
    """

    def __init__(self,
                 source: Surface,
                 area: (Rect | None) = None):
        self._source = source.copy()

        if area is not None:
            self._source = self._source.subsurface(area)

    def render(self) -> Surface:
        return self._source.copy()

    def scale(self, size: tuple[int, int]) -> Image:
        """Returns a scaled version of the original image

        Args:
            size (tuple[int, int]): the (width, height) to scale to

        Returns:
            Image: the resulting scaled image
        """
        scaled = pygame.transform.scale(self._source, size)
        return Image(scaled)

    def crop(self, area: Rect) -> Image:
        """Returns a cropped version of the original image

        Args:
            area (Rect): the area of the image to crop to

        Returns:
            Image: the resulting cropped image
        """
        return Image(self._source, area)

    def size(self) -> Point:
        """Returns the dimensions of the image

        Returns:
            Point: a (width, height) pair
        """
        return self._source.get_size()
