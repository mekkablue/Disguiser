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
	def filter(self, layer, inEditView, customParameters):
		print("__filter.controller", self.controller())
		# if inEditView: is not set correctly, will be fixed soon.
		if self.controller().className() == "GSEditViewController":
			print("__inEditView")
			selection = layer.selection
			if selection:
				rectangle = layer.boundsOfSelection()
			else:
				rectangle = layer.bounds
			path = self.rectToPath(rectangle)
			try:
				# GLYPHS 3
				layer.shapes.append(path)
			except:
				# GLYPHS 2
				layer.paths.append(path)
		else:
			print("__inFontView")
			for currLayer in layer.parent.layers:
				if currLayer.paths:
					rectangle = currLayer.bounds
					path = self.rectToPath(rectangle)
					try:
						# GLYPHS 3
						currLayer.shapes = [path]
					except:
						# GLYPHS 2
						currLayer.paths = [path]
					currLayer.hints = None

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
