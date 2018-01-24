"""
Trying to figure out BasePen stuff...

Update docstring please!
"""
from math import atan2, degrees, sqrt
import random as r
from vanilla import *
from defconAppKit.windows.baseWindow import BaseWindowController

import drawBot as db # Importing this way so drawBot commands don't get lost in the mix
from drawBot.ui.drawView import DrawView

from mojo.events import addObserver, removeObserver

from fontTools.pens.basePen import BasePen
from robofab.interface.all.dialogs import Message
from lib.UI.spaceCenter.glyphSequenceEditText import GlyphSequenceEditText

import string as s

# Global variable for max width for easy adjustment
MAXWIDTH = 100

class StrokePen(BasePen):
    """
    A pen draws the strokes of glyph.

    This pen is a subclass of the FontTools BasePen and extends it
    by accepting the desired stroke width as a parameter.
    """
    def __init__(self, glyphset, width):
        super(StrokePen, self).__init__(glyphset)
        self.width = width
        self.pointsList = []
        
    def _moveTo(self, pt):
        db.newPath()
        self.pointsList.append(pt)
        
    def _lineTo(self, pt):
        x0, y0 = self._getCurrentPoint()
        x, y = pt
        
        db.fill(None)
        db.stroke(r.random(), r.random(), r.random(), 1)
        db.strokeWidth(self.width)
        
        # db.newPath()
        db.moveTo((x0, y0))
        db.lineTo(pt)
        db.drawPath()
        
        # Or use line() instead of newPath, moveTo, lineTo, drawPath combo
        # line((x0, y0), (x, y))
        
        # Use rectangle below... still not sure why one over the other
        # angle = self.getAngle((x0, y0), (x, y))
        # distance = self.getDistance((x0, y0), (x, y))
    
        # fill(0, 0, 1, 1)    
        
        # with savedState():
        #     rotate(angle, (x0, y0))
        #     rect(x0, y0 - self.width / 2, distance, self.width)
            
        self.pointsList.append(pt)        
        
    def _curveToOne(self, pt1, pt2, pt3):
        x0, y0 = self._getCurrentPoint()
        
        db.fill(None)
        db.stroke(r.random(), r.random(), r.random(), 1)
        db.strokeWidth(self.width)

        # db.newPath()
        db.moveTo((x0, y0))
        db.curveTo(pt1, pt2, pt3)
        db.drawPath()
        
        self.pointsList.append(pt3)
        
    def _closePath(self):
        db.moveTo(self.pointsList[0])
        db.lineTo(self.pointsList[-1])
        db.drawPath()
        self.drawCircles()
            
    def _endPath(self):
        self.pointsList.append(self._getCurrentPoint())
        self.drawCircles()
      
    def drawCircles(self):
        """
        Draw circle at all points in pointsList
        """
        # db.blendMode("multiply")
        db.fill(1, 0, 0, 1)
        db.stroke(None)
        
        for point in self.pointsList:
            x, y = point
            db.newPath()
            db.oval(x - self.width / 2, y - self.width / 2, self.width, self.width)
  
    def getAngle(self, pt0, pt1):
        """
        Returns angle between 2 points, in degrees
        """
        x0, y0 = pt0
        x1, y1 = pt1
        
        xDiff = x1 - x0
        yDiff = y1 - y0
        
        return degrees(atan2(yDiff, xDiff))
        
    def getDistance(self, pt0, pt1):
        """
        Returns distance between two points
        """
        x0, y0 = pt0
        x1, y1 = pt1
        
        return sqrt((x1 - x0)**2 + (y1 - y0)**2)


class PreviewStroke(BaseWindowController):
    """
    GUI preview of ProgressPen result
    """

    def __init__(self):
        self.f = RFont("/Users/jesentanadi/Dropbox/1-Type/z-Scripts/_JT/0-Fonts for Testing/rectPen_TESTFONT.ufo")
        self.letters = ""
        self.widthValue = 55
        self.scale = 0.25

        self.w = FloatingWindow((1200, 400),
                                "Preview Width")

        self.w.inputText = GlyphSequenceEditText((10, 10, 500, 24),
                                                 self.f.naked(),
                                                 callback=self.inputTextCallback)

        self.w.widthSlider = Slider((520, 10, 325, 24),
                                    minValue=10,
                                    maxValue=MAXWIDTH,
                                    value=self.widthValue,
                                    callback=self.widthSliderCallback)

        self.w.scaleSlider = Slider((865, 10, 325, 24),
                                    minValue=0,
                                    maxValue=0.5,
                                    value=self.scale,
                                    callback=self.scaleSliderCallback)

        self.w.canvas = DrawView((10, 50, -10, -10))

        addObserver(self, "updateFont", "fontBecameCurrent")
        self.setUpBaseWindowBehavior()

        self.updateCanvas()

        self.w.open()

    def updateFont(self, info):
        self.f = info.get("font", None)
        self.breakGlyphCopies()

        self.updateCanvas()

    def inputTextCallback(self, sender):
        #This doesn't work that well yet...
        # for letter in sender.get():
        #     if letter not in self.fCopy:
        #         self.w.inputText.set("".join(self.letters))

        self.letters = sender.get()

        self.updateCanvas()

    def widthSliderCallback(self, sender):
        self.widthValue = int(sender.get())

        self.updateCanvas()

    def scaleSliderCallback(self, sender):
        self.scale = sender.get()

        self.updateCanvas()

    def updateCanvas(self):
        db.newDrawing()
        db.newPage(1200, 330)
        self.draw()

        pdf = db.pdfImage()
        self.w.canvas.setPDFDocument(pdf)

    def windowCloseCallback(self, sender):
        removeObserver(self, "fontBecameCurrent")
        super(PreviewStroke, self).windowCloseCallback(sender)


    def draw(self):
        """
        This function is what Canvas calls to draw
        """

        db.translate(10, 90)
        db.scale(self.scale)

        for letter in self.letters:
            glyph = self.f[letter]
            
            db.newPath()
            pen = StrokePen(glyph.getParent(), self.widthValue)
            glyph.draw(pen)
            db.drawPath()
            
            db.translate(glyph.width, 0)


try:
    PreviewStroke()

except:
    Message("Something's not right... Is the font there?")
# if CurrentFont() is not None:
#     PreviewStroke()

# else:
#     Message("You need to open a font!")
