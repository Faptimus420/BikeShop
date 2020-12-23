#Nish Bike Shop - logic core. KEA BE-IT, WaaSE course, group Nishiki, 2019
#Next iteration: Stock comparison, search and filter databases, proper classes, more action confirmations, pretty print/pagination
#Current to do: Comments, missing menu options, file does not exist exceptions

#----------Settings----------
debug=False  #Set variable to 'True' to enable debug mode. Default: False
mode='user' #Start in selected user mode. Options: 'user', 'admin'. Default: 'user'
menuLogo=True #Set to 'True' to print the logo in the main menu. Default: True
generateDefaultData=True    #Set to 'True' to generate YAML databases with default data entries, if the files don't exist. Default: True
#----------------------------

#----------Start initialization----------
print('Initializing...')
print("WARNING: You're running the Nish Bike Shop with the generateDefaultData setting set to False. This setting should only be used for debugging purposes. Procees with caution, as the program has not been properly tested with this behavior.") if generateDefaultData==False else ''

#Loading libraries
import sys,datetime,os,hashlib,getpass,pickle
from importlib import reload
from time import sleep

from platform import system
user_os=system()
print('Built-in libraries loaded') if debug==True else ''

from subprocess import check_output #Adapted from StackExchange (Answer by Artur Barseghyan, https://stackoverflow.com/questions/1051254/check-if-python-package-is-installed)
required_pkgs = ['fpdf','PyYAML']
reqs = check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_pckgs = [r.decode().split('==')[0] for r in reqs.split()]
for package in required_pkgs:
    if package not in installed_pckgs:
        print(f'The package "{package}" is required to run the Nish Bike Shop.')
        if user_os == 'Windows':
            print(f'Open the Anaconda Prompt (or the Command Prompt, if you are not using the Anaconda Distribution), and run the following command: "pip install {package}" without the quotes to install the {package} package.')
        else:
            print(f'Open the Anaconda Prompt (or the Terminal, if you are not using the Anaconda Distribution), and run the following command: "pip install {package}" without the quotes to install the {package} package.')
            sys.exit('The program will now terminate.')
from fpdf import FPDF
import yaml
print('External libraries loaded\n') if debug == True else ''


#Testing modules
if os.path.isfile('./finance.py')==True:
    if debug==True:
        print('Finance module OK')
else:
    sys.exit('finance.py module missing. Your installation of the Nish Bike Shop is corrupt. The program will now terminate.')

if os.path.isfile('./sales.py')==True:
    if debug==True:
        print('Sales module OK')
else:
    sys.exit('sales.py module missing. Your installation of the Nish Bike Shop is corrupt. The program will now terminate.')

if os.path.isfile('./stock.py')==True:
    if debug==True:
        print('Stock module OK')
else:
    sys.exit('stock.py module missing. Your installation of the Nish Bike Shop is corrupt. The program will now terminate.')
print('All modules OK\n') if debug == True else ''


#Testing databases
if not os.path.exists('./data'):
    os.mkdir('./data')
if os.path.isfile('./data/bikes.yml')==True:
    if debug==True:
        print('Bike database OK')
else:
    print('bikes.yml not found. Your bike database is corrupt. A new database will be generated if you proceed.')

if os.path.isfile('./data/parts.yml')==True:
    if debug==True:
        print('Part database OK')
else:
    print('parts.yml not found. Your bike part database is corrupt. A new database will be genrated if you proceed.')

if os.path.isfile('./data/invoices.yml')==True:
    if debug==True:
        print('Invoice database OK')
else:
    print('invoices.yml not found. Your invoice database is corrupt. A new database will be generated if you proceed.')

if os.path.isfile('./data/repairs.yml')==True:
    if debug==True:
        print('Repair database OK')
else:
    print('repairs.yml not found. Your repair database is corrupt. A new database will be generated if you proceed.')
print('All databases OK\n') if debug==True else ''


#Global functions
def func_clearOutput():
    os.system('cls' if user_os=='Windows' else 'clear')

def func_MainMenu():
    global initialize
    sleep(3) if debug == False else ''
    if debug==False and initialize != 1:
        func_clearOutput()
    initialize = 0
    if menuLogo==True:
        print('\n'+27*'*')
        print(' _   _ _____  _____ _    _')
        print('| \ | |_   _|/ ____| |  | |')
        print('|  \| | | | | (___ | |__| |')
        print('| . ` | | |  \___ \|  __  |')
        print('| |\  |_| |_ ____) | |  | |')
        print('|_| \_|_____|_____/|_|  |_|')
        print(9*'*'+'BIKE SHOP'+9*'*')
    print('Current time: '+datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    print('Debug mode active\tMode: '+mode if debug==True else 'Mode: '+mode)
    print('\n\nWelcome to the Nish Bike Shop!')
    print('Write 1 to buy a bike.')
    print('Write 2 to buy a bike part.')
    print('Write 3 to order a repair.')
    print('Write 4 to review your order(s) and reprint invoices.')
    print('Write 5 to change to '+('Administration' if mode=='user' else 'Standard')+' user mode.')
    if mode != 'user':
        print('Write 6 to manage the bike database.')
        print('Write 7 to manage the part database.')
        print('Write 8 to manage orders.')
        print('Write 9 to change the administration password.')
    print('Write 10 to read the about.')
    print('Leave empty to quit.')

def func_setPassword(): #Adapted from Nitratine, https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
    while True:
        newPass = getpass.getpass('\nEnter the new password: ')
        if newPass == 'reset':
            print("'reset' is a reserved string. Please choose a different password.")
            continue
        newPass = str.encode(newPass)
        newSalt = os.urandom(32)
        newKey = (hashlib.pbkdf2_hmac('sha256',newPass,newSalt,100000)).hex()
        toSave = (newSalt.hex()+newKey)
        passFile = open('password.pickle','wb+')
        pickle.dump(toSave,passFile)
        passFile.close()
        print('New password set.\n')
        break

def func_invoicePrinter():
    global newInvoiceGlob,newSaleGlob,invoiceType
    print(f"The invoice will be saved as: {newInvoiceGlob.timestamp}.pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, txt="INVOICE", ln=1, align="C")
    pdf.cell(44, 10, txt="Nishiki Bike Shop", ln=0, border="LTR")
    pdf.cell(0, 10, txt="INVOICE NUMBER: " + str(newInvoiceGlob.id).zfill(6), ln=1, align="R")
    pdf.cell(44, 10, txt="Lygten 16", ln=0, border="LR")
    pdf.cell(0, 10, txt="PRINT DATE: " + datetime.datetime.now().strftime("%d/%m/%Y"), ln=1, align="R")
    pdf.cell(44, 10, txt="Copenhagen, 2400", ln=0, border="LRB")
    pdf.cell(0, 10, txt='ORDER TIMESTAMP: '+newInvoiceGlob.timestamp, ln=0, align='R')
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.cell(100, 10, txt="BILL TO:", ln=1, border=1)
    pdf.cell(0, 10, txt="" + newInvoiceGlob.customer_name, ln=1)
    pdf.cell(0, 10, txt="" + newInvoiceGlob.address, ln=1)
    pdf.cell(0, 10, txt="" + newInvoiceGlob.zip +' '+newInvoiceGlob.city, ln=1)
    pdf.cell(0, 10, txt="" + newInvoiceGlob.phone, ln=1)
    pdf.cell(0, 10, txt="" + newInvoiceGlob.email, ln=1)
    pdf.ln()
    pdf.ln()
    pdf.ln()
    if invoiceType != 'reprint':
        vat = float(newSaleGlob['price'] - (newSaleGlob['price']/1.25))
        baseprice = float(newSaleGlob['price'] - vat)
        pdf.cell(150, 10, txt="DESCRIPTION", ln=1, border=1,align='C')
        pdf.cell(150, 10, txt=""+'('+(newInvoiceGlob.invoiceType).title()+') '+newInvoiceGlob.content, ln=0, border=1,align='LTR')
        pdf.cell(0, 10, txt="" + str(baseprice)+' DKK', ln=1, align="R", border="TR")
        pdf.cell(150, 10, txt="VAT 25%", ln=0, border="LRB")
        pdf.cell(0, 10, txt="" + str(vat)+' DKK', ln=1, align="R", border="TR")
        pdf.cell(150, 10, txt="TOTAL", ln=0, border=1)
        pdf.cell(0, 10, txt="" + str(newSaleGlob['price'])+' DKK', ln=1, align="R", border=1)
    else:
        vat = float(newInvoiceGlob.price-(newInvoiceGlob.price/1.25))
        baseprice = float(newInvoiceGlob.price-vat)
        pdf.cell(150, 10, txt="DESCRIPTION", ln=1, border=1,align='C')
        pdf.cell(150, 10, txt=""+'('+(newInvoiceGlob.invoiceType).title()+') '+newInvoiceGlob.content, ln=0, border=1,align='LTR')
        pdf.cell(0, 10, txt="" + str(baseprice)+' DKK', ln=1, align="R", border="TR")
        pdf.cell(150, 10, txt="VAT 25%", ln=0, border="LRB")
        pdf.cell(0, 10, txt="" + str(vat)+' DKK', ln=1, align="R", border="TR")
        pdf.cell(150, 10, txt="TOTAL", ln=0, border=1)
        pdf.cell(0, 10, txt="" + str(newInvoiceGlob.price)+' DKK', ln=1, align="R", border=1)
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.cell(0, 10, txt="Thank you for shopping at Nish!",ln=1)
    pdf.cell(0,10,txt='You may contact our customer support at nishbikes@email.com')
    pdf.output(newInvoiceGlob.timestamp + ".pdf")
    print('Invoice saved.')
print('Global functions OK') if debug == True else ''

#Loading class definitions
repairsList,invoicesList,bikesList,partsList = [],[],[],[]
newSaleGlob,newInvoiceGlob,reprintInvoice = None,None,None
class Bike:
    def __init__(self, id, brand, model, color, size, price, qty):
        self.id = id
        self.brand = brand
        self.model = model
        self.color = color
        self.size = size
        self.price = price
        self.qty = qty

    def setDefaultBikes():
        global bikesList
        b1 = Bike(1, "Centurion", "Challenger", "red", 28, 3000.0, 6)
        b2 = Bike(2, "Nishiki", "Touring Master", "green", 30, 9000.0, 2)
        b3 = Bike(3, "Raleigh", "DL24", "red", 26, 1500.0, 9)
        b4 = Bike(4, "Giant", "Propel", "blue", 28, 6000.0, 5)
        b5 = Bike(5, "Scott", "Aspect", "orange", 28, 12000.0, 1)
        bikesList.append({'id':b1.id,'brand':b1.brand,'model':b1.model,'color':b1.color,'size':b1.size,'price':b1.price,'qty':b1.qty})
        bikesList.append({'id':b2.id,'brand':b2.brand,'model':b2.model,'color':b2.color,'size':b2.size,'price':b2.price,'qty':b2.qty})
        bikesList.append({'id':b3.id,'brand':b3.brand,'model':b3.model,'color':b3.color,'size':b3.size,'price':b3.price,'qty':b3.qty})
        bikesList.append({'id':b4.id,'brand':b4.brand,'model':b4.model,'color':b4.color,'size':b4.size,'price':b4.price,'qty':b4.qty})
        bikesList.append({'id':b5.id,'brand':b5.brand,'model':b5.model,'color':b5.color,'size':b5.size,'price':b5.price,'qty':b5.qty})
        with open("./data/bikes.yml", "w+") as bikeData:
            yaml.dump(bikesList, bikeData)

    def showAllBikes():
        global bikesList
        with open("./data/bikes.yml", "r") as bikeData:
            bikesList = yaml.safe_load(bikeData)
        print('Bike ID\tBrand\tModel\t\tColor\tSize\tPrice\tQuantity')
        if not bikesList:
            print("There are no bikes in stock.")
        else:
            for item in bikesList:
                print(f"{str(item['id']).zfill(6)}\t{item['brand']}\t\t\t{item['model']}\t{item['color']}\t\t{str(item['size'])}\t\t{str(item['price'])} DKK\t\t{str(item['qty'])}")

    def addNewBike():
        global bikesList
        print ("\nNow adding a new bike to stock.")
        with open("./data/bikes.yml", "r") as bikeData:
            bikesList = yaml.safe_load(bikeData)
            try:
                new_id = int((bikesList[-1])['id'])+1
            except IndexError:
                new_id = 1
            new_brand = str(input("Enter the brand of the bike: "))
            new_model = str(input("Enter the model of the bike: "))
            new_color = str(input("Enter the color of the bike: "))
            while True:
                try:
                    new_size = int(input("Enter the size of the bike: "))
                except ValueError:
                    print("That's not a valid size. Please try again.")
                    continue
                else:
                    break
            while True:
                try:
                    new_price = float(input("Enter the price of the bike (including VAT): "))
                except ValueError:
                    print("That's not a valid price. Please try again.")
                    continue
                else:
                    break
            while True:
                try:
                    new_qty = int(input("Enter the quantity in stock: "))
                except ValueError:
                    print("That's not a valid quantity. Please try again.")
                    continue
                else:
                    break
            newBike = Bike(new_id,new_brand,new_model,new_color,new_size,new_price,new_qty)
            bikesList.append({'id':new_id,'brand':new_brand,'model':new_model,'color':new_color,'size':new_size,'price':new_price,'qty':new_qty})
        with open("./data/bikes.yml", "w+") as bikeData:
            yaml.dump(bikesList,bikeData)
        print(f"\nThe bike with ID {str(new_id).zfill(6)} ({new_brand} {new_model}, {new_color}, size {new_size}) for {str(new_price)} DKK has been added to the database successfully.")

    def deleteBike():
        global bikesList
        while True:
            try:
                selectBike = int(input("Enter the ID of the bike you'd like to remove from the database: "))
            except ValueError:
                print("That's not a valid ID. Please try again.")
                continue
            else:
                break
        with open("./data/bikes.yml", "r") as bikeData:
            bikesList = yaml.safe_load(bikeData)
        while True:
            if not any(d['id'] == selectBike for d in bikesList):
                print('Invalid bike ID. Please try again.')
                continue
            break
        bikesList = list(filter(lambda i: i['id'] != selectBike, bikesList))
        with open("./data/bikes.yml", "w+") as bikeData:
            yaml.dump(bikesList,bikeData)
        print('Bike deleted.')

    def editBike():
        global bikesList
        new_brand,new_model,new_color,new_size,new_price,new_qty = None,None,None,None,None,None
        with open("./data/bikes.yml", "r") as bikeData:
            bikesList = yaml.safe_load(bikeData)
        while True:
            try:
                selectBike = int(input("Enter the ID of the bike you'd like to edit: "))
            except ValueError:
                print("That's not a valid ID. Please try again.")
                continue
            if not any(d['id'] == selectBike for d in bikesList):
                print('Invalid bike ID. Please try again.')
                continue
            break
        print('While editing, keep input blank to preserve the current value.')
        new_brand = str(input("Enter the new brand of the bike: "))
        new_model = str(input("Enter the new model of the bike: "))
        new_color = str(input("Enter the new color of the bike: "))
        while True:
            try:
                new_size = int(input("Enter the new size of the bike: "))
            except ValueError:
                if new_size == None:
                    break
                else:
                    print("That's not a valid size. Please try again.")
                    continue
            else:
                break
        while True:
            try:
                new_price = float(input("Enter the new price of the bike (including VAT): "))
            except ValueError:
                if new_price == None:
                    break
                else:
                    print("That's not a valid price. Please try again.")
                    continue
            else:
                break
        while True:
            try:
                new_qty = int(input("Enter the new quantity in stock: "))
            except ValueError:
                if new_qty== None:
                    break
                else:
                    print("That's not a valid quantity. Please try again.")
                    continue
            else:
                break
        for d in bikesList:
            if new_brand != None or new_brand != '' and d['id'] == selectBike:
                d.update(brand= new_brand)
            if new_model != None or new_brand != '' and d['id'] == selectBike:
                d.update(model= new_model)
            if new_color != None or new_brand != '' and d['id'] == selectBike:
                d.update(color= new_color)
            if new_size != None or new_brand != '' and d['id'] == selectBike:
                d.update(size= new_size)
            if new_price != None or new_brand != '' and d['id'] == selectBike:
                d.update(price= new_price)
            if new_qty != None or new_brand != '' and d['id'] == selectBike:
                d.update(qty= new_qty)
        with open("./data/bikes.yml", "w+") as bikeData:
            yaml.dump(bikesList,bikeData)
        print('Changes saved.')

    def subtractBikeStock(bikeStockChangeID):
        global bikesList,bikeStockChange
        with open("./data/bikes.yml", "r+") as bikeData:
            bikesList = yaml.safe_load(bikeData)
            for d in bikesList:
                if d['id'] == bikeStockChangeID:
                    d.update('qty',-bikeStockChange)

class Part:
    def __init__(self, id, name, brand, model, price, qty):
        self.id = id
        self.name = name
        self.brand = brand
        self.model = model
        self.price = price
        self.qty = qty

    def setDefaultParts():
        global partsList
        p1 = Part(1, 'Wheels',"Centurion", "Challenger", 3000.0, 6)
        p2 = Part(2, 'Handlebars', "Raleigh", "DL24H",9000.0, 2)
        p3 = Part(3, "Suspension","Giant", "Propel", 1500.0, 9)
        p4 = Part(4, 'Frame',"Scott", "Aspect", 6000.0, 5)
        p5 = Part(5, 'Chain',"Nishiki", "Touring Master", 12000.0, 1)
        partsList.append({'id':p1.id,'name':p1.name,'brand':p1.brand,'model':p1.model,'price':p1.price,'qty':p1.qty})
        partsList.append({'id':p2.id,'name':p2.name,'brand':p2.brand,'model':p2.model,'price':p2.price,'qty':p2.qty})
        partsList.append({'id':p3.id,'name':p3.name,'brand':p3.brand,'model':p3.model,'price':p3.price,'qty':p3.qty})
        partsList.append({'id':p4.id,'name':p4.name,'brand':p4.brand,'model':p4.model,'price':p4.price,'qty':p4.qty})
        partsList.append({'id':p5.id,'name':p5.name,'brand':p5.brand,'model':p5.model,'price':p5.price,'qty':p5.qty})
        with open("./data/parts.yml", "w+") as partData:
            yaml.dump(partsList, partData)

class Repair:
    def __init__(self, id, brand, model, part_damaged, price):
        self.id = id
        self.brand = brand
        self.model = model
        self.part_damaged = part_damaged
        self.price = price

    def setDefaultRepairs():
        global repairsList
        r1 = Repair(1, "Centurion", "Challenger", "Brakes", 250.0)
        r2 = Repair(2, "Nishiki", "Touring Master", "Chain", 450.0)
        r3 = Repair(3, "Raleigh", "DL24H", "Handlebars", 500.0)
        r4 = Repair(4, "Giant", "Propel", "Suspension", 750.0)
        r5 = Repair(5, "Scott", "Aspect", "Frame", 4500.0)
        repairsList.append({'id':r1.id,'brand':r1.brand,'model':r1.model,'part_damaged':r1.part_damaged,'price':r1.price})
        repairsList.append({'id':r2.id,'brand':r2.brand,'model':r2.model,'part_damaged':r2.part_damaged,'price':r2.price})
        repairsList.append({'id':r3.id,'brand':r3.brand,'model':r3.model,'part_damaged':r3.part_damaged,'price':r3.price})
        repairsList.append({'id':r4.id,'brand':r4.brand,'model':r4.model,'part_damaged':r4.part_damaged,'price':r4.price})
        repairsList.append({'id':r5.id,'brand':r5.brand,'model':r5.model,'part_damaged':r5.part_damaged,'price':r5.price})
        with open("./data/repairs.yml", "w+") as repairData:
            yaml.dump(repairsList, repairData)

    def addRepairJob():
        global repairsList
        print ("\nNow creating a new repair order.")
        with open("./data/repairs.yml", "r") as repairData:
            repairsList = yaml.safe_load(repairData)
            new_id = int((repairsList[-1])['id'])+1
            new_brand = str(input("Enter the brand of the bike that needs repairs: "))
            new_model = str(input("Enter the model of the bike that needs repairs: "))
            new_part = str(input("Which part needs repairs?: "))
            while True:
                try:
                    new_price = float(input("Enter the price of the repair (including VAT): "))
                except ValueError:
                    print("That's not a valid price. Please try again.")
                    continue
                else:
                    break
            newRepair = Repair(new_id,new_brand,new_model,new_part,new_price)
            repairsList.append({'id':new_id,'brand':new_brand,'model':new_model,'part_damaged':new_part,'price':new_price})
        with open("./data/repairs.yml", "w+") as repairData:
            yaml.dump(repairsList,repairData)
        global newSaleGlob
        newSaleGlob = {'id':new_id,'brand':new_brand,'model':new_model,'part_damaged':new_part,'price':new_price}
        print(f"\nA repair order with repair ID {str(new_id).zfill(6)} for part '{new_part}' on your '{new_brand} {new_model}' for {str(new_price)} DKK has been placed successfully.")
        print("To finish your order, we'll now need some of your personal details...")

class Invoice:
    def __init__(self, id, invoiceType, timestamp, customer_name, address, zip, city, phone, email, price, content, status):
        self.id = id
        self.invoiceType = invoiceType
        self.timestamp = timestamp
        self.customer_name = customer_name
        self.address = address
        self.zip = zip
        self.city = city
        self.phone = phone
        self.email = email
        self.price = price
        self.content = content
        self.status = status

    def setDefaultInvoices():
        global invoicesList
        i1 = Invoice(1,'repair',datetime.datetime.now().strftime('%d%m%Y%H%M%S'),"Jakub Schovanec", "Manjasdjnasjd 19", '1300',"Copenhagen", "12345678", "j.schovanec@mail.sk",500.0,"Centurion 3000\tHandlebars",'Incomplete')
        invoicesList.append({'id':i1.id,'invoiceType':i1.invoiceType,'timestamp':i1.timestamp,'customer_name':i1.customer_name,'address':i1.address,'zip':i1.zip,'city':i1.city,'phone':i1.phone,'email':i1.email,'price':i1.price,'content':i1.content,'status':i1.status})
        with open("./data/invoices.yml", "w+") as invoiceData:
            yaml.dump(invoicesList, invoiceData)

    def showAllInvoices():
        global invoicesList
        with open("./data/invoices.yml", "r") as invoiceData:
            invoicesList = yaml.safe_load(invoiceData)
        print('Invoice ID\tOrder type\tTimestamp\tName\t\tContent\t\t\tPrice\tStatus')
        if not invoicesList:
            print("There are no invoices in the database.")
        else:
            for item in invoicesList:
                print(f"{str(item['id']).zfill(6)}\t\t{(item['invoiceType']).title()}\t\t{item['timestamp']}   {item['customer_name']}\t{item['content']}\t{str(item['price'])} DKK\t{item['status']}")

    def addInvoice():
        global newSaleGlob,invoicesList,invoiceType,newInvoiceGlob,selectQTY
        with open("./data/invoices.yml", "r") as invoiceData:
            invoicesList = yaml.safe_load(invoiceData)
            new_id = int((invoicesList[-1])['id'])+1
            new_type = str(invoiceType)
            new_timestamp = datetime.datetime.now().strftime('%d%m%Y%H%M%S')
            new_customer_name = str(input("Enter your full name: "))
            new_address = str(input("Enter your address (street and number): "))
            new_zip = str(input("Enter your ZIP: "))
            new_city = str(input("Enter your city: "))
            new_phone = str(input("Enter your phone number: "))
            new_email = str(input("Enter your email: "))
            if invoiceType == 'repair':
                new_price = float(newSaleGlob['price'])
                new_content = str(newSaleGlob['brand']+' '+newSaleGlob['model']+'\t'+newSaleGlob['part_damaged'])
            elif invoiceType == 'bike':
                selectQTY = sales.selectQTY
                newSaleGlob = sales.newSaleGlob
                new_price = float(newSaleGlob['price'])
                new_content = str(str(selectQTY)+'x '+newSaleGlob['brand']+' '+newSaleGlob['model']+' ('+newSaleGlob['color']+') (size: '+str(newSaleGlob['size'])+')')
            new_status = 'Incomplete'
            newInvoice = Invoice(new_id,new_type,new_timestamp,new_customer_name,new_address,new_zip,new_city,new_phone,new_email,new_price,new_content,new_status)
            invoicesList.append({'id':new_id,'invoiceType':new_type,'timestamp':new_timestamp,'customer_name':new_customer_name,'address':new_address,'zip':new_zip,'city':new_city,'phone':new_phone,'email':new_email,'price':new_price,'content':new_content,'status':new_status})
            with open("./data/invoices.yml", "w+") as invoiceData:
                yaml.dump(invoicesList,invoiceData)
        newInvoiceGlob = newInvoice

    def readdInvoice():
        global reprintInvoice,newInvoiceGlob
        new_id = reprintInvoice['id']
        new_type = reprintInvoice['invoiceType']
        new_timestamp = reprintInvoice['timestamp']
        new_customer_name = reprintInvoice['customer_name']
        new_address = reprintInvoice['address']
        new_zip = reprintInvoice['zip']
        new_city = reprintInvoice['city']
        new_phone = reprintInvoice['phone']
        new_email = reprintInvoice['email']
        new_price = reprintInvoice['price']
        new_content = reprintInvoice['content']
        new_status = reprintInvoice['status']
        newInvoice = Invoice(new_id,new_type,new_timestamp,new_customer_name,new_address,new_zip,new_city,new_phone,new_email,new_price,new_content,new_status)
        newInvoiceGlob = newInvoice
print('Class definitions OK\n') if debug == True else ''

print('Intialization complete. Ready!')
initialize = 1
#----------End initialization----------

callMenu = True
while True:
    print('\nLoading menu...\n')
    if callMenu == True:
        func_MainMenu()
    menuChoice = str(input('What would you like to do?: ' if callMenu == True else 'What would you like to do now?: '))
    callMenu = True
    if menuChoice == '' or menuChoice == None:
        print('Attempting to quit...') if debug==True else ''
        break
    elif menuChoice == '1':
        stockMode = 'bike'
        salesMode = 'bike'
        invoiceType = 'bike'
        selectQTY = 0
        if 'stock' not in sys.modules:
            import stock
        else:
            reload(stock)
        stock.displayBikeStock()
        if 'sales' not in sys.modules:
            import sales
        else:
            reload(sales)
        selectBike = input("\nEnter the ID of the bike you'd like to purchase, or leave empty to return to the menu: ")
        if selectBike == '' or selectBike == None:
            continue
        sales.new_Sales()
        print('Sales module end') if debug == True else ''
        if 'finance' not in sys.modules:
            import finance
        else:
            reload(finance)
        finance.new_Invoice()
        print('Finance module end') if debug == True else ''
        print('\nThank you for your order!')
        continue
    elif menuChoice == '2':
        stockMode = 'part'
        func_loadAllModules() if debug==False else ''


        continue
    elif menuChoice == '3':
        salesMode = 'repair'
        if 'sales' not in sys.modules:
            import sales
        else:
            reload(sales)
        sales.new_Sales()
        print('Sales module end') if debug == True else ''
        if 'finance' not in sys.modules:
            import finance
        else:
            reload(finance)
        invoiceType = 'repair'
        finance.new_Invoice()
        print('Finance module end') if debug == True else ''
        print('\nThank you for your order!')
        continue
    elif menuChoice == '4':
        if os.path.isfile('./data/invoices.yml')==True:
            email = input('\nEnter the email address you have used when placing your order(s), or leave blank to return to the menu: ')
            if email == '' or email == None:
                continue
            with open("./data/invoices.yml", "r") as invoiceData:
                invoicesList = yaml.safe_load(invoiceData)
            foundInvoices = list(filter(lambda item: item['email'] == email, invoicesList))
            if foundInvoices == []:
                print('No invoices with this email have been found.\n')
                callMenu = False
                continue
            print('Invoice ID\tOrder type\tTimestamp\tName\t\tContent\t\t\tPrice\tStatus')
            for item in foundInvoices:
                print(f"{str(item['id']).zfill(6)}\t\t{(item['invoiceType']).title()}\t\t{item['timestamp']}   {item['customer_name']}\t{item['content']}\t{str(item['price'])} DKK\t{item['status']}")
            while True:
                reprintInvoice = input("\nEnter the Invoice ID of the invoice you'd like to reprint, or leave blank to return to the main menu: ")
                if reprintInvoice == '' or reprintInvoice == None:
                    break
                elif reprintInvoice.isdigit() == True:
                    reprintInvoice = int(reprintInvoice)
                if not any(d['id'] == reprintInvoice for d in foundInvoices):
                    print('Invalid Invoice ID. Please try again.')
                    continue
                else:
                    reprintInvoice = next(item for item in foundInvoices if item["id"] == reprintInvoice)
                    Invoice.readdInvoice()
                    invoiceType = 'reprint'
                    func_invoicePrinter()
                    break
        else:
            print('The invoice database is empty.\n')
            callMenu = False
            continue
        continue
    elif menuChoice == '5':
        if mode == 'user':
            passCorrect = False
            if os.path.isfile('./password.pickle')==False:
                print("There's currently no password set for accessing database administration. You must set a new password before proceeding.")
                func_setPassword()
                callMenu = False
                continue
            while passCorrect != True:
                print("\nYou must enter a password to access the administration menu. You may also type 'reset' to reset the password.")
                password = getpass.getpass("Password: ")
                if password == 'reset':
                    os.remove('./password.pickle')
                    print('Password reset.')
                    callMenu = False
                    break
                else:
                    savedKey = open('password.pickle','rb')
                    savedKey = pickle.load(savedKey)
                    password = str.encode(password)
                    salt = bytes.fromhex(savedKey[:64])
                    savedKey = bytes.fromhex(savedKey[-64:])
                    key = hashlib.pbkdf2_hmac('sha256',password,salt,100000)
                    if key == savedKey:
                        print('Access granted. Switching to administration mode...')
                        mode = 'admin'
                        passCorrect = True
                    else:
                        print('Access denied. Please try again.')
                        continue
        else:
            mode = 'user'
        continue
    elif menuChoice == '6' and mode == 'admin':
        if os.path.isfile('./data/bikes.yml')==False:
            print('The bike database does not exist.')
            continue
        while True:
            Bike.showAllBikes()
            print('\nWhat would you like to do?')
            print('You can:')
            print('Type 1 to add a new bike to the database.')
            print("Type 2 to edit a bike's details.")
            print('Type 3 to remove a bike from the database.')
            print('Leave blank to return to the main menu.')
            bikeAdminMenu = str(input('Choice: '))
            if bikeAdminMenu == '' or bikeAdminMenu == None:
                break
            elif bikeAdminMenu == '1':
                Bike.addNewBike()
                continue
            elif bikeAdminMenu == '2':
                Bike.editBike()
                continue
            elif bikeAdminMenu == '3':
                Bike.deleteBike()
                continue
            else:
                print('Invalid choice. Please try again.')
                continue
    elif menuChoice == '7' and mode == 'admin':
        print('This menu is currently under construction. We apologize for the inconvenience. In the mean time, you can edit the appropariate yml databases manually.')
        continue
    elif menuChoice == '8' and mode == 'admin':
        print('\n')
        Invoice.showAllInvoices()
        with open("./data/invoices.yml", "r") as invoiceData:
            invoicesList = yaml.safe_load(invoiceData)
        print('\nFor legal reasons, you may only change the status of an invoice.')
        while True:
            selectInvoice = input('Enter the ID of the invoice you wish to change the status of: ')
            try:
                selectInvoice = int(selectInvoice)
            except ValueError:
                selectInvoice = input('Invalid invoice ID. Please try again: ')
                continue
            if not any(d['id'] == selectInvoice for d in invoicesList):
                selectInvoice = input('Invalid invoice ID. Please try again: ')
                continue
            break
        newStatus = input(f'Enter the new status of invoice {str(selectInvoice).zfill(6)}: ')
        for d in invoicesList:
            if d['id'] == selectInvoice:
                d.update(status=newStatus)
        with open("./data/invoices.yml", "w+") as invoiceData:
            yaml.dump(invoicesList, invoiceData)
        print('Invoice status updated successfully.')
        continue
    elif menuChoice == '9' and mode == 'admin':
        func_setPassword()
        callMenu = False
        continue
    elif menuChoice == '10':
        print('\nNish Bike Shop, v1.0.0')
        print('Built in Python 3.7')
        print('Authors: Patrik Žori, Tom Russell, Jakub Schovanec, Oliver Sørensen, Daniel Kajári, Mark Sergeyev, Kieran Olivier Holm')
        print('Made for the 5th semester Working as a Software Engineer exam of the Business Economics & IT bachelor at KEA, Copenhagen, Denmark.')
        print('v1.0.0: 2019; latest revision: 2019\n')
        callMenu = False
        sleep(7) if debug == False else ''
        continue
    else:
        print("\nYou entered an invalid choice, or you don't have the necessary access permissions to use this option. Please try again.")
        callMenu = False
        continue
    print('Main menu loop end') if debug == True else ''

print('\nThank you for shopping at Nish. Have a nice day!')
