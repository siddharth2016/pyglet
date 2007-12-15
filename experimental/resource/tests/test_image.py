#!/usr/bin/python
# $Id:$

import os
import sys
import unittest

from pyglet.gl import *
from pyglet import image
from pyglet import window

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import resource

# Test image is laid out
#  M R
#  B G
# In this test the image is sampled at four points from top-right clockwise:
#  R G B M (red, green, blue, magenta)

class TestCase(unittest.TestCase):
    def check(self, img, colors):
        glClear(GL_COLOR_BUFFER_BIT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        img.blit(0, 0)
        buffer = image.get_buffer_manager().get_color_buffer().image_data
        buffer.format = 'RGBA'
        buffer.pitch = len(buffer.format) * buffer.width
        bytes = buffer.data
        def sample(x, y):
            i = y * buffer.pitch + x * len(buffer.format)
            r, g, b, _ = bytes[i:i+len(buffer.format)]
            r, g, b = map(ord, (r, g, b))
            return {
                (255, 0, 0): 'r',
                (0, 255, 0): 'g',
                (0, 0, 255): 'b',
                (255, 0, 255): 'm'}.get((r, g, b), 'x')

        samples = ''.join([
            sample(3, 3), sample(3, 0), sample(0, 0), sample(0, 3)])
        self.assertTrue(samples == colors, samples)

    def test0(self):
        self.check(resource.image('rgbm.png'), 'rgbm')

    def test1(self):
        self.check(resource.image('rgbm.png', pad=1), 'rgbm')

    def test1a(self):
        self.check(resource.image('rgbm.png', pad=2), 'rgbm')

    def test1b(self):
        self.check(resource.image('rgbm.png', pad=4), 'rgbm')

    def test2(self):
        self.check(resource.image('rgbm.png', flip_x=True), 'mbgr')

    def test3(self):
        self.check(resource.image('rgbm.png', flip_y=True), 'grmb')

    def test4(self):
        self.check(resource.image('rgbm.png', flip_x=True, flip_y=True), 'bmrg')

    def test5(self):
        self.check(resource.image('rgbm.png', rotate=90), 'mrgb')
    
    def test5a(self):
        self.check(resource.image('rgbm.png', rotate=-270), 'mrgb')

    def test6(self):
        self.check(resource.image('rgbm.png', rotate=180), 'bmrg')

    def test6a(self):
        self.check(resource.image('rgbm.png', rotate=-180), 'bmrg')

    def test7(self):
        self.check(resource.image('rgbm.png', rotate=270), 'gbmr')

    def test7a(self):
        self.check(resource.image('rgbm.png', rotate=-90), 'gbmr')

if __name__ == '__main__':
    w = window.Window(width=10, height=10, visible=True)
    w.dispatch_events()
    unittest.main()
