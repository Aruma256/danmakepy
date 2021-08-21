import asyncio
import math
import unittest
from unittest.mock import Mock

import numpy as np

from danmakepy.core.entities.baseentity import BaseEntity


class TestBaseEntity(unittest.TestCase):

    def test___init__(self):
        base_entity = BaseEntity(
            pos=(0.5, 0.25),
            speed=1.5,
            angle=0.75,
            size=2.5
        )
        self.assertEqual(base_entity.pos[0], 0.5)
        self.assertEqual(base_entity.pos[1], 0.25)
        self.assertEqual(base_entity.speed, 1.5)
        self.assertEqual(base_entity.angle, 0.75)
        self.assertEqual(base_entity.size, 2.5)
        with self.assertRaises(AssertionError):
            BaseEntity((0.5, 0.25), 1.5, 0.75, size=-2.5)

    def test_is_removed(self):
        base_entity = BaseEntity()
        self.assertIs(base_entity.is_removed(), base_entity._removed)

    def test_remove(self):
        base_entity = BaseEntity()
        base_entity._coro = Mock()
        self.assertFalse(base_entity.is_removed())
        base_entity.remove()
        self.assertTrue(base_entity.is_removed())
        base_entity._coro.close.assert_called_once()

    def test_tick(self):
        base_entity = BaseEntity((1, 2), 2, math.radians(30))
        base_entity.tick()
        self.assertAlmostEqual(base_entity.pos[0], 1 + 3**0.5)
        self.assertAlmostEqual(base_entity.pos[1], 2 + 1)
        base_entity.remove()
        with self.assertRaises(AssertionError):
            base_entity.tick()

    @unittest.skip("not implemented")
    def test_start(self):
        pass

    @unittest.skip("not implemented")
    def test_step(self):
        pass

    def test_render(self):
        base_entity = BaseEntity((1.1, 2.2), size=3.3)
        mock = Mock()
        base_entity.render(mock)
        pos, size = mock.render_circle.call_args.args
        self.assertTrue(np.array_equal(pos, np.array((1.1, 2.2), dtype=float)))
        self.assertEqual(size, 3.3)
