import numpy as np
from psychopy.tools.monitorunittools import deg2pix
from psychopy.visual import dot


class CustomDotStim(dot.DotStim):
    def __init__(self,
                 win,
                 units="",
                 nDots=1,
                 coherence=0.5,
                 fieldPos=(0.0, 0.0),
                 fieldSize=(1.0, 1.0),
                 fieldShape="sqr",
                 dotSize=2.0,
                 dotLife=3,
                 dir=0.0,
                 speed=0.5,
                 rgb=None,
                 color=(1.0, 1.0, 1.0),
                 colorSpace="rgb",
                 opacity=1.0,
                 contrast=1.0,
                 depth=0,
                 element=None,
                 signalDots="same",
                 noiseDots="direction",
                 name=None,
                 autoLog=None,
                 xys=None):

        if xys is None:
            self._xys = [[0.0, 0.0]] * nDots
        else:
            self._xys = xys

        if units == "deg" or (units == "" and win.units == "deg"):
            dotSize = deg2pix(dotSize, win.monitor)

        super().__init__(win, units, nDots, coherence, fieldPos, fieldSize,
                         fieldShape, dotSize, dotLife, dir, speed, rgb,
                         color, colorSpace, opacity, contrast, depth,
                         element, signalDots, noiseDots, name, autoLog)

    def _newDotsXY(self, _):
        return np.array(self._xys)

    def _update_dotsXY(self):
        if self.noiseDots == "direction":
            cosDots = np.reshape(np.cos(self._dotsDir), (self.nDots,))
            sinDots = np.reshape(np.sin(self._dotsDir), (self.nDots,))

            self._verticesBase[:, 0] += self.speed * cosDots
            self._verticesBase[:, 1] += self.speed * sinDots

        self._updateVertices()

    def set_xys(self, xys):
        self._verticesBase = np.array(xys)
