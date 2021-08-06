# encoding: utf-8
from __future__ import division, print_function, unicode_literals

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from math import radians, tan

class showNextFontComponents(ReporterPlugin):
	
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Next Font Components',
			'de': 'Komponenten der nächsten Schrift',
			'fr': 'les Composants de la police suivante',
			'es': 'componentes de la siguiente fuente',
			'pt': 'componentes da próxima fonte',
			})
		
		self.missingComponents=None

	@objc.python_method
	def background( self, Layer ):
		try:
			if len(Glyphs.fonts) > 1:
				NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.5, 0.3, 0.5 ).set()
				self.checkComponents( Layer )
		except Exception as e:
			print(e)
			print()
			import traceback
			print(traceback.format_exc())
	
	@objc.python_method
	def checkComponents ( self, Layer ):
		thisGlyph = Layer.parent
		thisFont = thisGlyph.parent
		thisMaster = Layer.master
		masters = thisFont.masters
		
		nextFont = Glyphs.fonts[1]
		nextFontMasters = nextFont.masters
		nextGlyph = nextFont.glyphs[thisGlyph.name]
		if not nextGlyph and "." in thisGlyph.name:
			dotOffset = thisGlyph.name.find(".")
			coreGlyphName = thisGlyph.name[:dotOffset]
			nextGlyph = nextFont.glyphs[coreGlyphName]
		
		if not nextGlyph:
			self.missingComponents = None
		else:
			activeMasterIndex = masters.index(thisMaster)
		
			if len(masters) != len(nextFontMasters):
				nextLayer = nextGlyph.layers[0]
			else:
				nextLayer = nextGlyph.layers[activeMasterIndex]
		
			orange = NSColor.orangeColor().colorWithAlphaComponent_(0.67)
			grey = NSColor.grayColor().colorWithAlphaComponent_(0.9)
		
			#Hago sets de las listas
			nextFontComponentsSet = set([a.name for a in nextLayer.components])
			thisFontComponentsSet = set([a.name for a in Layer.components])

			#Hace sets con las difrencias
			missingInNextFont = thisFontComponentsSet.difference(nextFontComponentsSet)
			missingInThisFont = nextFontComponentsSet.difference(thisFontComponentsSet)

			componentsNamesMissingInThisFont = "\n".join(["+ %s "%name for name in missingInThisFont])
			self.drawTextAtPoint( componentsNamesMissingInThisFont, NSPoint(0,0), fontSize=10.0, fontColor=orange, align="bottomright" )
			
			componentsNamesMissingInNextFont = "\n".join(["− %s"%name for name in missingInNextFont])
			self.drawTextAtPoint( componentsNamesMissingInNextFont, NSPoint(0,0), fontSize=10.0, fontColor=grey, align="bottomleft" )
			
			print (componentsNamesMissingInNextFont)
			self.missingComponents = missingInThisFont
			
	
	@objc.python_method
	def conditionalContextMenus(self):
		# Execute only if layers are actually selected
		if not self.missingComponents or len(Glyphs.font.selectedLayers)!=1:
			return []
		else:
			# Add context menu item
			contextMenus = [{
				'name': Glyphs.localize({
					'en': 'Add missing components from next font',
					'de': 'Fehlende Komponenten aus der nächsten Schrift hinzufügen',
					'fr': 'Ajouter les Composants manquantes de la police suivante',
					'es': 'Agregar componentes faltantes de la próxima fuente',
					'pt': 'Adicionar componentes ausentes da próxima fuente',
					}), 
				'action': self.addMissingComponents_
				}]

			# Return list of context menu items
			return contextMenus
	
	def addMissingComponents_(self, sender=None):
		pass
		if self.missingComponents:
			currentLayer = Glyphs.font.selectedLayers[0]
			if currentLayer:
				currentLayer.clearSelection()
				for i, componentName in enumerate(self.missingComponents):
					newComponent = GSComponent(componentName)					
					try:
						# Glyphs 3
						currentLayer.shapes.append(newComponent)
					except:
						# Glyphs 2
						currentLayer.components.append(newComponent)
					currentLayer.selection.append(newComponent)
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
