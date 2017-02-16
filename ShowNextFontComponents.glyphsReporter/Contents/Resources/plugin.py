# encoding: utf-8

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################


from GlyphsApp.plugins import *
import math

class NextFontComponents(ReporterPlugin):



	def checkComponents(self, layer):
	
		thisFont = layer.parent.parent 
		thisGlyph = layer.parent
		nextFont = Glyphs.fonts[1]

		activeMasterIndex = thisFont.masters.index(thisFont.selectedFontMaster)

		initPos = thisFont.selectedFontMaster.descender
		step = + 20		
		xHeight = thisFont.selectedFontMaster.xHeight
		angle = thisFont.selectedFontMaster.italicAngle
		offset = math.tan(math.radians(angle)) * xHeight/2

		fontColor1 = NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.91, 0.32, 0.06, 0.45 )
		fontColor2 = NSColor.colorWithCalibratedRed_green_blue_alpha_( 0, 0, 0, 0.45 )
		fontColor3 = NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.5, 0.3, 0.8 )
		
		thisComp = []
		nextComp = []


		if len(thisFont.masters) != len(nextFont.masters):
			nextLayer = nextFont.glyphs[thisGlyph.name].layers[0]
		else:
			nextLayer = nextFont.glyphs[thisGlyph.name].layers[activeMasterIndex]

		for nextLayerComp in nextLayer.components:
			thisComp.append(nextLayerComp.componentName)
			self.drawTextAtPoint( u"· %s" % nextLayerComp.componentName, NSPoint(10 - offset, initPos), 14.0, fontColor1 )
			initPos = initPos + step

		for thisLayerComp in layer.components:
			nextComp.append(thisLayerComp.componentName)
			self.drawTextAtPoint( u"· %s" % thisLayerComp.componentName, NSPoint(10 - offset, initPos), 14.0, fontColor2 )
			initPos = initPos + step

		#Hago sets de las listas
		font1Set = set(thisComp)
		font2Set = set(nextComp)
		
		#Hace sets con las difrencias
		diff1 = font1Set.difference(font2Set)
		diff2 = font2Set.difference(font1Set)

		if not diff1 and not diff2:
			self.drawTextAtPoint( u"OK", NSPoint(10 - offset, initPos), 14.0, fontColor3 )

	def settings(self):
		self.menuName = Glyphs.localize({'en': u'Next Font Components', 'de': u'Next Font Components'})
		
	def foreground(self, layer):
		self.checkComponents ( layer )


	#def preview(self, layer):

