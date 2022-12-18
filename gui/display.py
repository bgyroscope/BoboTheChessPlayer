import pygame

from typedefs import (
    ColorRGB,
    Coord
)
from .displayable import Displayable

ERROR = -1
READY = 0
ACTIVE = 1
QUIT = 2


class Display:
    """Represents a display window that can be updated at a fixed framerate"""

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
        """Causes the display to be shown"""

        pygame.display.flip()
        self.state = ACTIVE

    def add(self, disp: Displayable, pos: Coord, z: int = 0):
        """Adds a displayable to the display

        Args:
            disp: the displayable to add
            pos: the screen position at which to render the displayable
            z: the displayable's z order. Defaults to 0.
        """
        disp.localPosition = pos
        disp.zOrder = z
        self._displayables.append(disp)
        # Maintain z-order sort
        self._displayables.sort(key=lambda x: x.zOrder)

    def tick(self):
        """Updates the display by one frame"""

        self._processEvents()

        self._surface.fill(self.fillColor)
        for disp in self._displayables:
            surface = disp.render()
            self._surface.blit(surface, disp.localPosition)

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
