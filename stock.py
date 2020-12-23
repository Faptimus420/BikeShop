#Nish Bike Shop - stock module. KEA BE-IT, WaaSE course, group Nishiki, 2019
from __main__ import debug,mode,generateDefaultData,stockMode
import os

if stockMode == 'bike':
	from __main__ import Bike
	if generateDefaultData==True and os.path.isfile('./data/bikes.yml')==False:
		print('Generating default bike database...')
		Bike.setDefaultBikes()
	def displayBikeStock():
		Bike.showAllBikes()

print('\nStock module (re)loaded') if debug == True else ''
