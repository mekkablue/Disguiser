# encoding: utf-8
from __future__ import division, print_function, unicode_literals


import objc
from Foundation import NSPoint
from GlyphsApp import GSPath, GSNode, GSLINE
from GlyphsApp.plugins import FilterWithoutDialog


class Disguiser(FilterWithoutDialog):

	@objc.python_method
	def rectToPath(self, rectangle):
		"""Turns an NSRect into a GSPath."""
		rectPath = GSPath()
		p1 = rectangle.origin
		p2 = NSPoint(rectangle.origin.x + rectangle.size.width, rectangle.origin.y)
		p3 = NSPoint(rectangle.origin.x + rectangle.size.width, rectangle.origin.y + rectangle.size.height)
		p4 = NSPoint(rectangle.origin.x, rectangle.origin.y + rectangle.size.height)
		for pos in (p1, p2, p3, p4):
			node = GSNode(pos, GSLINE)
			rectPath.nodes.append(node)
		rectPath.closed = True
		return rectPath

	@objc.python_method
	def settings(self):
		self.menuName = "Disguiser"
		self.keyboardShortcut = None  # With Cmd+Shift

	@objc.python_method
	def filter(self, Layer, inEditView, customParameters):
		rectangle = None
		selection = Layer.selection
			
		if inEditView and selection:
			pointsInSelection = selection.values()
			xMin = min(pointsInSelection, key=lambda point: point.x)
			xMax = max(pointsInSelection, key=lambda point: point.x)
			yMin = min(pointsInSelection, key=lambda point: point.y)
			yMax = max(pointsInSelection, key=lambda point: point.y)
			rectangle = NSRect()
			rectangle.origin = NSPoint(xMin.x, yMin.y)
			rectangle.size = NSSize(xMax.x-xMin.x, yMax.y-yMin.y)
			myPath = self.rectToPath(rectangle)
			Layer.addPath_(myPath)
		
		if not rectangle:
			if Layer.paths:
				rectangle = Layer.bounds
				myPath = self.rectToPath(rectangle)
				try:
					# GLYPHS 3
					Layer.setShapes_([myPath])
				except:
					# GLYPHS 2
					Layer.setPaths_([myPath])

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
