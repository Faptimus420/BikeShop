#Nish Bike Shop - sales module. KEA BE-IT, WaaSE course, group Nishiki, 2019
from __main__ import debug,mode,generateDefaultData,salesMode,newSaleGlob
import os,yaml

def new_Sales():
    global newSaleGlob
    if salesMode == 'repair':
        from __main__ import Repair
        if generateDefaultData==True and os.path.isfile('./data/repairs.yml')==False:
            print('Generating default repair database...')
            Repair.setDefaultRepairs()
        Repair.addRepairJob()
    elif salesMode == 'bike':
        from __main__ import Bike,selectBike,selectQTY
        global selectQTY
        with open("./data/bikes.yml", "r") as bikeData:
            bikesList = yaml.safe_load(bikeData)
            while True:
                try:
                    selectBike = int(selectBike)
                except ValueError:
                    selectBike = input('Invalid bike ID. Please try again: ')
                    continue
                if not any(d['id'] == selectBike for d in bikesList):
                    selectBike = input('Invalid bike ID. Please try again: ')
                    continue
                break
            newSaleGlob = list(filter(lambda item: item['id'] == selectBike, bikesList))
        while True:
            try:
                selectQTY = int(input('How many would you like to buy?: '))
            except ValueError:
                selectQTY = input('Invalid choice. Please try again: ')
                continue
            break
        bikeStockChange = selectQTY
        bikeStockChangeID = [y['id'] for y in newSaleGlob]
        newSaleGlob = newSaleGlob[0]
        Bike.subtractBikeStock(bikeStockChangeID)

print('\nSales module (re)loaded') if debug==True else ''
