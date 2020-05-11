import json
from PyQt5.QtWidgets import *
from time import time

def inform_user(parent, text):
    ans = QMessageBox.information(
        parent, None, text,
        QMessageBox.Ok
    )
    return ans

def ask_user(parent, text):
    ans = QMessageBox.question(
        parent, None, text, 
        QMessageBox.Ok | QMessageBox.Cancel)
    return ans

def write_file(obj, filename):
    """takes a list obj and saves a json file"""
    start_time = time()
    with open(filename, 'w') as outputfile:
        json.dump(obj, outputfile, indent=4)
        print("writing file took: "+ str(time() - start_time))

def read_file(filename):
    """Reads in a json file"""
    start_time = time()
    with open(filename, 'r') as inputfile:
        json_file = json.load(inputfile)
        print("Reading file took: "+ str(time() - start_time))
    return json_file

def get_company_summary(filename, index):
    data_pkl = read_file(filename)
    paid = data_pkl[int(index)]['Total Paid']
    outstanding = data_pkl[int(index)]["Outstanding"]
    return paid, outstanding

def write_invoice_to_file(parent, filename, index, invoice_no, po_no, amount, date):
    data_pkl = read_file(filename)
    existing_invoice_no = []
    
    if len(data_pkl[int(index)]["Invoices"]) > 0:
        for i in range(len(data_pkl[int(index)]["Invoices"])):
            existing_invoice_no.append(data_pkl[int(index)]["Invoices"]["Invoice "+str(i+1)]["Invoice No"])
    
    if invoice_no in existing_invoice_no:
        inform_user(parent, "Invoice number already exists.\n\n"+
        "Enter a 'new number' or if you want to add payment for this invoice, use 'New Payment'")
    else:
        new_invoice ={}
        new_invoice["Invoice No"] = invoice_no
        new_invoice["P/O ref"] = po_no
        new_invoice["Invoice Amount"] = amount
        new_invoice["Outstanding"] = amount # when creating a new invoice, outstanding amount is the same as invoice amount
        new_invoice["Issue Date"] = date
        new_invoice["Payments"] = {}
        data_pkl[int(index)]["Invoices"]["Invoice "+str(len(data_pkl[int(index)]["Invoices"])+1)] = new_invoice
        
        prev_outstanding = data_pkl[int(index)]["Outstanding"]
        data_pkl[int(index)]["Outstanding"] = prev_outstanding + amount

        prev_total = data_pkl[int(index)]["Total Business"]
        data_pkl[int(index)]["Total Business"] = prev_total + amount
        #finally write update
        write_file(data_pkl,filename)

def write_new_payment(
    parent, filename, index, invoice_no, po_no,amount, date, 
    payment_method, bank_name, cheque_no, remarks):
    
    data_pkl = read_file(filename)
    existing_invoice_no = []

    if len(data_pkl[int(index)]["Invoices"]) == 0:
        inform_user(
                parent,
                "There are no invoices for this company.\n\n"+
                "Create a new invoice first using the 'New Invoice' option."
            )
        
    elif len(data_pkl[int(index)]["Invoices"]) > 0:
        for i in range(len(data_pkl[int(index)]["Invoices"])):
            existing_invoice_no.append(data_pkl[int(index)]["Invoices"]["Invoice "+str(i+1)]["Invoice No"])
    
        if invoice_no not in existing_invoice_no:
            inform_user(
                parent,
                "Invoice number doesn't exist. Enter a valid invoice number.\n\n"+
                "If this is a new invoice, use the 'New Invoice' option."
            )
        else:
            invoice_index = existing_invoice_no.index(invoice_no)
            invoice_amount = data_pkl[int(index)]["Invoices"]["Invoice "+str(invoice_index+1)]["Invoice Amount"]
            payments = data_pkl[int(index)]["Invoices"]["Invoice "+str(invoice_index+1)]["Payments"]
            invoice_outstanding = data_pkl[int(index)]["Invoices"]["Invoice "+str(invoice_index+1)]["Outstanding"]
            # if len(payments)>0:
            #     prev_payments = []
            #     for i in range(len(payments)):
            #         prev_payments.append(payments["Payment "+str(i+1)]["Payment Amount"])
            #     prev_payments = sum(prev_payments)
            # else:
            #     prev_payments = 0

            if invoice_outstanding - amount >=0:# <= invoice_amount:
                new_payment = {}
                new_payment["Payment Date"] = date
                new_payment["Payment Amount"] = amount
                new_payment["Payment Method"] = payment_method
                if payment_method == "Cheque":
                    new_payment["Bank Name"] = bank_name
                    new_payment["Cheque No"] = cheque_no
                
                new_payment["Remarks"] = remarks

                payments["Payment "+str(len(payments)+1)] = new_payment
                
                # invoice outstanding total update
                data_pkl[int(index)]["Invoices"]["Invoice "+str(invoice_index+1)]["Outstanding"] = invoice_outstanding - amount
                
                # overall outstanding balance update for all invoices with this company
                prev_outstanding = data_pkl[int(index)]["Outstanding"]
                data_pkl[int(index)]["Outstanding"] = prev_outstanding - amount

                prev_paid = data_pkl[int(index)]["Total Paid"]
                data_pkl[int(index)]["Total Paid"] = prev_paid + amount
                
                write_file(data_pkl,filename)
            
            elif invoice_outstanding == 0:
                inform_user(parent, "There are no outstanding payments for this invoice.")
            
            else:
                inform_user(parent, "Amount you entered ("+str(amount)+") is greater than remaining amount ("+
                str(invoice_outstanding)+ ") for this invoice.")