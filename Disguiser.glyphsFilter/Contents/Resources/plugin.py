# encoding: utf-8

###########################################################################################################
#
#
#	Filter without dialog Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20without%20Dialog
#
#
###########################################################################################################


from GlyphsApp.plugins import *

class Disguiser(FilterWithoutDialog):
	
	def rectToPath( self, Rectangle ):
		"""Turns an NSRect into a GSPath."""
		rectPath = GSPath()
		p1 = Rectangle.origin
		p2 = NSPoint( Rectangle.origin.x + Rectangle.size.width, Rectangle.origin.y )
		p3 = NSPoint( Rectangle.origin.x + Rectangle.size.width, Rectangle.origin.y + Rectangle.size.height )
		p4 = NSPoint( Rectangle.origin.x, Rectangle.origin.y + Rectangle.size.height )
		for pos in (p1,p2,p3,p4):
			P = GSNode()
			P.type = 1
			P.position = pos
			rectPath.nodes.append( P )
		rectPath.closed = True
		return rectPath
	
	def settings(self):
		self.menuName = "Disguiser"
		self.keyboardShortcut = None # With Cmd+Shift

	def filter(self, layer, inEditView, customParameters):
		rectangle = None
		selection = Layer.selection
			
		if selectionCounts and selection:
			pointsInSelection = selection.values()
			xMin = min( pointsInSelection, key=lambda point: point.x )
			xMax = max( pointsInSelection, key=lambda point: point.x )
			yMin = min( pointsInSelection, key=lambda point: point.y )
			yMax = max( pointsInSelection, key=lambda point: point.y )
			rectangle = NSRect()
			rectangle.origin = NSPoint( xMin.x, yMin.y )
			rectangle.size = NSSize( xMax.x-xMin.x, yMax.y-yMin.y )
			myPath = self.rectToPath( rectangle )
			Layer.addPath_( myPath )
		
		if not rectangle:
			if Layer.paths:
				rectangle = Layer.bounds
				myPath = self.rectToPath( rectangle )
				Layer.setPaths_( [myPath] )
	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	