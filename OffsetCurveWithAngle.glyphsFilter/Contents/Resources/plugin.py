# encoding: utf-8

###########################################################################################################
#
#
#	Filter with dialog Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20with%20Dialog
#
#	For help on the use of Interface Builder:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates
#
#
###########################################################################################################

import objc, math
from GlyphsApp import *
from GlyphsApp.plugins import *

class OffsetCurveWithAngle(FilterWithDialog):
	
	# Definitions of IBOutlets
	
	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()
	
	# Text field in dialog
	xOffsetField = objc.IBOutlet()
	yOffsetField = objc.IBOutlet()
	angleField = objc.IBOutlet()
	
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'Offset Curve with Angle',
			'de': u'Verfetten mit Winkel'
		})
		
		# Word on Run Button (default: Apply)
		self.actionButtonLabel = Glyphs.localize({
			'en': u'Offset', 
			'de': u'Verfetten'
		})
		
		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog', __file__)
	
	# On dialog show
	def start(self):
		
		# Set default value
		Glyphs.registerDefault('com.mekkablue.OffsetCurveWithAngle.xOffset', 15.0)
		Glyphs.registerDefault('com.mekkablue.OffsetCurveWithAngle.yOffset', 10.0)
		Glyphs.registerDefault('com.mekkablue.OffsetCurveWithAngle.angle', 27.0)
		
		# Set value of text field
		self.xOffsetField.setStringValue_(Glyphs.defaults['com.mekkablue.OffsetCurveWithAngle.xOffset'])
		self.yOffsetField.setStringValue_(Glyphs.defaults['com.mekkablue.OffsetCurveWithAngle.yOffset'])
		self.angleField.setStringValue_(Glyphs.defaults['com.mekkablue.OffsetCurveWithAngle.angle'])
		
		# Set focus to text field
		self.xOffsetField.becomeFirstResponder()
		
	# Action triggered by UI
	@objc.IBAction
	def setXOffset_( self, sender ):
		Glyphs.defaults['com.mekkablue.OffsetCurveWithAngle.xOffset'] = sender.floatValue()
		self.update()
	
	# Action triggered by UI
	@objc.IBAction
	def setYOffset_( self, sender ):
		Glyphs.defaults['com.mekkablue.OffsetCurveWithAngle.yOffset'] = sender.floatValue()
		self.update()
	
	# Action triggered by UI
	@objc.IBAction
	def setAngle_( self, sender ):
		Glyphs.defaults['com.mekkablue.OffsetCurveWithAngle.angle'] = sender.floatValue()
		self.update()
	
	# Actual filter
	def filter(self, layer, inEditView, customParameters):
		xOffset = 15.0
		yOffset = 10.0
		angle = 27.0
		
		if not inEditView:
			if customParameters.has_key('xOffset'):
				xOffset = customParameters['xOffset']
			if customParameters.has_key('yOffset'):
				yOffset = customParameters['yOffset']
			if customParameters.has_key('angle'):
				angle = customParameters['angle']
		else:
			xOffset = float(Glyphs.defaults['com.mekkablue.OffsetCurveWithAngle.xOffset'])
			yOffset = float(Glyphs.defaults['com.mekkablue.OffsetCurveWithAngle.yOffset'])
			angle = float(Glyphs.defaults['com.mekkablue.OffsetCurveWithAngle.angle'])
		
		layer.applyTransform(self.transform( rotate=-angle ).transformStruct())
		self.offsetLayer( layer, xOffset, yOffset )
		layer.applyTransform(self.transform( rotate=angle ).transformStruct())
			
	
	def transform(self, shiftX=0.0, shiftY=0.0, rotate=0.0, skew=0.0, scale=1.0):
		"""
		Returns an NSAffineTransform object for transforming layers.
		Apply an NSAffineTransform t object like this:
			Layer.transform_checkForSelection_doComponents_(t,False,True)
		Access its transformation matrix like this:
			tMatrix = t.transformStruct() # returns the 6-float tuple
		Apply the matrix tuple like this:
			Layer.applyTransform(tMatrix)
			Component.applyTransform(tMatrix)
			Path.applyTransform(tMatrix)
		Chain multiple NSAffineTransform objects t1, t2 like this:
			t1.appendTransform_(t2)
		"""
		myTransform = NSAffineTransform.transform()
		if rotate:
			myTransform.rotateByDegrees_(rotate)
		if scale != 1.0:
			myTransform.scaleBy_(scale)
		if not (shiftX == 0.0 and shiftY == 0.0):
			myTransform.translateXBy_yBy_(shiftX,shiftY)
		if skew:
			skewStruct = NSAffineTransformStruct()
			skewStruct.m11 = 1.0
			skewStruct.m22 = 1.0
			skewStruct.m21 = math.tan(math.radians(skew))
			skewTransform = NSAffineTransform.transform()
			skewTransform.setTransformStruct_(skewStruct)
			myTransform.appendTransform_(skewTransform)
		return myTransform
	
	def offsetLayer( self, thisLayer, offsetX, offsetY, makeStroke=False, position=0.5, autoStroke=False ):
		offsetFilter = NSClassFromString("GlyphsFilterOffsetCurve")
		offsetFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_(
			thisLayer,
			offsetX, offsetY, # horizontal and vertical offset
			makeStroke,     # if True, creates a stroke
			autoStroke,     # if True, distorts resulting shape to vertical metrics
			position,       # stroke distribution to the left and right, 0.5 = middle
			None, None )
		
		
	def generateCustomParameter( self ):
		return "%s; xOffset:%s; yOffset:%s; angle:%s;" % (
			self.__class__.__name__,
			Glyphs.defaults['com.mekkablue.OffsetCurveWithAngle.xOffset'],
			Glyphs.defaults['com.mekkablue.OffsetCurveWithAngle.yOffset'],
			Glyphs.defaults['com.mekkablue.OffsetCurveWithAngle.angle'],
			)
	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
