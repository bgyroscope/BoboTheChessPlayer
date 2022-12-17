from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, Sequence

import pygame
from pygame.event import Event
from pygame.rect import Rect
from pygame.surface import Surface

from typedefs import (
    Color,
    Coord,
    Size
)


def makeSurface(width: int, height: int, hasAlpha: bool) -> Surface:
    """Generates a new pygame surface

    Args:
        width: the desired width of the surface
        height: the desired height of the surface
        hasAlpha: whether the surface should support alpha values

    Returns:
        a newly created surface with the given properties
    """
    surface = Surface((width, height))
    if hasAlpha:
        return surface.convert_alpha()
    return surface.convert()


def getBounds(disp: Displayable) -> Rect:
    """Determines the bounding rectanble for the given displayable"""

    position = disp.getTopLeft()
    if disp.parent is not None:
        parentBounds = getBounds(disp.parent)
        position = (position[0] + parentBounds.x,
                    position[1] + parentBounds.y)
    return Rect(position, disp.size)


class Displayable(ABC):
    """Abstract class for display elements"""

    localPosition: Coord
    pivot: tuple[float, float]
    zOrder: int
    parent: (Displayable | None)

    def __init__(self):
        self.localPosition = (0, 0)
        self.pivot = (0.0, 0.0)
        self.zOrder = 0
        self.parent = None

    def getTopLeft(self) -> Coord:
        """Returns the coordinates of the top-left corner of the displayable"""

        x, y = self.localPosition
        pivotX, pivotY = self.pivot
        width, height = self.size
        position = (round(x - width * pivotX),
                    round(y - height * pivotY))
        return position

    @property
    @abstractmethod
    def size(self) -> Size:
        """The dimensions of the displayable"""

    @abstractmethod
    def render(self) -> Surface:
        """Returns a pygame surface to be displayed"""

    def handle(self, event: Event) -> bool:
        """Responds to events passed to the displayable

        Args:
            event: the event to respond to

        Returns:
            whether the event was successfully handled
        """
        return False


class Container(Displayable):
    """Abstract class for displayables that contain other displayables"""

    _children: list[Displayable]

    def __init__(self):
        super().__init__()

        self._children = []

    def _addChild(self, disp: Displayable):
        """Adds a child displayable to the container"""

        disp.parent = self
        self._children.append(disp)
        # Maintain z-order sort
        self._children.sort(key=lambda x: x.zOrder)

    def clearChildren(self):
        """Removes all children from the container"""

        self._children = []

    def render(self) -> Surface:
        width, height = self.size
        surface = makeSurface(width, height, True)
        surface.fill((0, 0, 0, 0))

        for child in self._children:
            childSurface = child.render()
            position = child.getTopLeft()
            surface.blit(childSurface, position)

        return surface

    def handle(self, event: Event) -> bool:
        # Traverse in reverse z-order
        for child in self._children[::-1]:
            if child.handle(event):
                return True

        return super().handle(event)


class Solid(Displayable):
    """A display element of a rectangle filled with a solid color"""

    def __init__(self, width: int, height: int, fillColor: Color):
        super().__init__()

        self.fillColor = fillColor
        self._size = (width, height)

        self._surface = makeSurface(width,
                                    height,
                                    len(self.fillColor) == 4)
        self._surface.fill(self.fillColor)

    @property
    def size(self) -> Size:
        return self._size

    def render(self) -> Surface:
        return self._surface.copy()


class Image(Displayable):
    """An image display element"""

    def __init__(self,
                 source: Surface,
                 area: (Rect | None) = None):
        super().__init__()

        self._source = source.copy()
        if area is not None:
            self._source = self._source.subsurface(area)

    def scale(self, size: Size) -> Image:
        """Returns a scaled version of the original image

        Args:
            size: the (width, height) to scale to

        Returns:
            Image: the resulting scaled image
        """
        scaled = pygame.transform.scale(self._source, size)
        return Image(scaled)

    def crop(self, area: Rect) -> Image:
        """Returns a cropped version of the original image

        Args:
            area: the area of the image to crop to

        Returns:
            Image: the resulting cropped image
        """
        return Image(self._source, area)

    @property
    def size(self) -> Size:
        return self._source.get_size()

    def render(self) -> Surface:
        return self._source.copy()


class Panel(Container):
    """A display element that can contain child displayables"""

    def __init__(self,
                 width: int,
                 height: int,
                 fillColor: Color = (0, 0, 0, 0),
                 background: (Image | None) = None):
        super().__init__()

        self._size = (width, height)
        self.fillColor = fillColor

        if background is not None:
            # Scale the image to fit the panel
            self._background = background.scale((width, height))
        else:
            self._background = None

        self._surface = makeSurface(width, height, len(fillColor) == 4)

    def add(self,
            disp: Displayable,
            pos: Coord,
            z: int = 0,
            pivot: tuple[float, float] = (0.0, 0.0)):
        """Adds a child displayable to the panel

        Args:
            disp: the displayable to add
            pos: the position at which to display the child
            z: the child's z layer. Defaults to 0.
            pivot: the pivot point to use when positioning. Defaults to (0.0, 0.0).
        """
        disp.localPosition = pos
        disp.pivot = pivot
        disp.zOrder = z
        self._addChild(disp)

    @property
    def size(self) -> Size:
        return self._size

    def render(self) -> Surface:
        self._surface.fill(self.fillColor)

        if self._background is not None:
            background = self._background.render()
            self._surface.blit(background, (0, 0))

        children = super().render()
        self._surface.blit(children, (0, 0))

        return self._surface.copy()


class Grid(Container):
    """A container that lays out its children in a grid"""

    def __init__(self,
                 numRows: int,
                 numCols: int,
                 items: Sequence[Displayable],
                 spacing: int = 0):
        super().__init__()

        if numRows * numCols != len(items):
            raise ValueError("Grid dimensions do not match number of items!")

        self.numRows = numRows
        self.numCols = numCols
        self.spacing = spacing

        self._columnWidth = self._getColumnWidth(items)
        self._rowHeight = self._getRowHeight(items)

        self._addItems(items)

    def _addItems(self, items: Sequence[Displayable]):
        for i, item in enumerate(items):
            colIdx = i % self.numCols
            rowIdx = i // self.numCols

            item.localPosition = self._getItemPosition(colIdx, rowIdx)
            item.pivot = (0.5, 0.5)
            self._addChild(item)

    def _getColumnWidth(self, items: Sequence[Displayable]) -> int:
        maxWidth = 0
        for item in items:
            width = item.size[0]
            maxWidth = max(maxWidth, width)
        return maxWidth

    def _getRowHeight(self, items: Sequence[Displayable]) -> int:
        maxHeight = 0
        for item in items:
            height = item.size[1]
            maxHeight = max(maxHeight, height)
        return maxHeight

    def _getItemPosition(self, colIdx: int, rowIdx: int) -> Coord:
        xOffset = self._columnWidth * colIdx + (colIdx + 1) * self.spacing
        yOffset = self._rowHeight * rowIdx + (rowIdx + 1) * self.spacing

        x = xOffset + self._columnWidth // 2
        y = yOffset + self._rowHeight // 2

        return (x, y)

    @property
    def size(self) -> Size:
        width = self._columnWidth * self.numCols + \
            (self.numCols + 1) * self.spacing
        height = self._rowHeight * self.numRows + \
            (self.numRows + 1) * self.spacing
        return (width, height)


class Button(Displayable):
    """A solid-colored button that performs an action on click"""

    def __init__(self,
                 width: int,
                 height: int,
                 idleColor: Color,
                 hoverColor: Color,
                 onClick: (Callable | None) = None):
        super().__init__()

        self._size = (width, height)
        self.idleColor = idleColor
        self.hoverColor = hoverColor
        self.onClick = onClick

        hasAlpha = len(idleColor) == 4 or len(hoverColor) == 4
        self._surface = makeSurface(width, height, hasAlpha)

        self._hovered = False

    @property
    def size(self) -> Size:
        return self._size

    def render(self) -> Surface:
        color = self.hoverColor if self._hovered else self.idleColor
        self._surface.fill(color)

        return self._surface

    def handle(self, event: Event) -> bool:
        bounds = getBounds(self)

        if event.type == pygame.MOUSEMOTION:
            self._hovered = bounds.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            if self.onClick is not None and bounds.collidepoint(event.pos):
                self.onClick()

        return super().handle(event)


# class ImageButton(Button):
#     def __init__(self,
#                  image: Image,
#                  onClick: Callable,
#                  hoverColor: Color):
#         width, height = image.getBounds().size
#         super().__init__(width, height, (0, 0, 0, 0), hoverColor, onClick)

#     def render(self) -> Surface:
#         return super().render()
