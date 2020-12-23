#Nish Bike Shop - finance module. KEA BE-IT, WaaSE course, group Nishiki, 2019
from __main__ import debug,mode,generateDefaultData,Invoice,func_invoicePrinter
import os

def new_Invoice():
    if generateDefaultData==True and os.path.isfile('./data/invoices.yml')==False:
        print('Generating default invoice database...')
        Invoice.setDefaultInvoices()
    Invoice.addInvoice()
    while True:
        printInvoiceQuestion = input('\nWould you like to print a pdf invoice? [Y/N]: ').upper()
        if printInvoiceQuestion == 'Y' or printInvoiceQuestion == 'N':
            break
        else:
            print('Invalid choice. Please try again.')
            continue
    if printInvoiceQuestion == 'Y':
        func_invoicePrinter()

print('\nFinance module (re)loaded') if debug==True else ''
