import asyncio
from collections.abc import Coroutine
import math

import numpy as np

from ..abstract_renderer import AbstractRenderer

class BaseEntity:

    def __init__(self, pos=None, speed: float = 0., angle: float = 0., size: float = 0.):
        assert size >= 0
        if pos:
            assert len(pos) == 2
            self.pos = np.array(pos, dtype=float)
        else:
            self.pos = np.zeros(2, dtype=float)
        self.speed = speed
        self.angle = angle
        self.size = size
        self._removed: bool = False
        self._coro = None

    def is_removed(self) -> bool:
        return self._removed

    def remove(self) -> None:
        assert not self.is_removed()
        if self._coro:
            self._coro.close()
        self._removed = True

    def tick(self) -> None:
        assert not self.is_removed()
        self.pos[0] += self.speed * math.cos(self.angle)
        self.pos[1] += self.speed * math.sin(self.angle)

    def start(self) -> None:
        pass

    def step(self):
        pass

    def render(self, renderer: AbstractRenderer) -> None:
        renderer.render_circle(self.pos, self.size)
