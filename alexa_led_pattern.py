#!/usr/bin/env python

# Copyright (C) 2017 Seeed Technology Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import numpy
import time


class AlexaLedPattern(object):
    def __init__(self, show=None, number=12):
        self.pixels_number = number
        self.pixels = [0] * 4 * number

        if not show or not callable(show):
            def dummy(data):
                pass
            show = dummy

        self.show = show
        self.stop = False

    def bootup(self):

        step = 1
        position = 12
        for x in range(45):
            pixels  = [12, 0, 12 - position, 0] * self.pixels_number
            self.show(pixels)
            time.sleep(0.02)
            if position <= 0:
                step = 1
                time.sleep(0.01)
            elif position >=12:
                step = -1
                time.sleep(0.01)

            position += step
        self.show([0] * 4 * 12)


    def wakeup(self, direction=0):
        position = int((direction + 15) / (360 / self.pixels_number)) % self.pixels_number

        pixels = [0, 0, 0, 24] * self.pixels_number
        pixels[position * 4 + 2] = 48

        self.show(pixels)

    def loading(self, direction=0):
        while not self.stop: #Runs until changed
                time.sleep(0.01)
                direction=direction+1
                position = int((direction + 15) / (360 / self.pixels_number)) % self.pixels_number
                pixels = [0, 0, 2, 2, 0,0,0,2] * self.pixels_number
                pixels[position * 4 + 2] = 12
                self.show(pixels)

    def listen(self):
        pixels = [0, 0, 0, 24] * self.pixels_number

        self.show(pixels)

    def think(self):
        pixels  = [0, 0, 12, 12, 0, 0, 0, 24] * self.pixels_number

        while not self.stop: #Runs until changed
            self.show(pixels)
            time.sleep(0.2)
            pixels = pixels[-4:] + pixels[:-4]

    def error(self):
        step = 1
        position = 12
        for x in range(95): #Runs for 90 cycles
            pixels  = [14, 14 - position, 0, 0] * self.pixels_number
            self.show(pixels)
            time.sleep(0.01)
            if position <= 0:
                step = 1
                time.sleep(0.05)
            elif position >= 12:
                step = -1
                time.sleep(0.05)

            position += step
        self.show([0] * 4 * 12)

    def speak(self):
        step = 1
        position = 12
        for x in range(85):
            pixels  = [0, 0, position, 24 - position] * self.pixels_number
            self.show(pixels)
            time.sleep(0.01)
            if position <= 0:
                step = 1
                time.sleep(0.4)
            elif position >= 12:
                step = -1
                time.sleep(0.4)

            position += step
        self.show([0] * 4 * 12)

    def off(self):
        self.show([0] * 4 * 12)
