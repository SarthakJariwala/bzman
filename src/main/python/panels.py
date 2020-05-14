from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json
from util import read_file, write_file, write_invoice_to_file, write_new_payment, inform_user

# def inform_user(parent, text):
#     QMessageBox.information(
#         parent, None, text,
#         QMessageBox.Ok
#     )

class EntryWidget(QWidget):

    def __init__(self, name):
        super(EntryWidget, self).__init__()

        self.name = name

        self.lbl = QLabel(self.name)
        # self.lbl.setStyleSheet("QLabel {font-weight: bold;}")
        self.ledit = QLineEdit()
        # self.ledit.setStyleSheet("QLineEdit {font-weight: bold;}")

        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.lbl)
        self.vbox1.addWidget(self.ledit)
        self.setLayout(self.vbox1)

class EntryComboBox(QWidget):

    def __init__(self, name):
        super(EntryComboBox, self).__init__()

        self.name = name

        self.lbl = QLabel(self.name)
        # self.lbl.setStyleSheet("QLabel {font-weight: bold;}")
        self.comboBox = QComboBox()
        # self.ledit.setStyleSheet("QLineEdit {font-weight: bold;}")

        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.lbl)
        self.vbox1.addWidget(self.comboBox)
        self.setLayout(self.vbox1)

class EntryTextEditWidget(QWidget):

    def __init__(self, name):
        super(EntryTextEditWidget, self).__init__()

        self.name = name

        self.lbl = QLabel(self.name)
        # self.lbl.setStyleSheet("QLabel {font-weight: bold;}")
        self.tedit = QTextEdit()
        # self.tedit.setStyleSheet("QTextEdit {font-weight: bold;}")

        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.lbl)
        self.vbox1.addWidget(self.tedit)
        self.setLayout(self.vbox1)

class EntrySpinBoxWidget(QWidget):

    def __init__(self, name):
        super(EntrySpinBoxWidget, self).__init__()

        self.name = name

        self.lbl = QLabel(self.name)
        # self.lbl.setStyleSheet("QLabel {font-weight: bold;}")
        self.spin_box = QDoubleSpinBox()
        self.spin_box.setStyleSheet("QDoubleSpinBox {font-weight: bold;}")
        self.spin_box.setMaximum(1000000000000000.00)
        self.spin_box.setMinimum(0.00)

        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.lbl)
        self.vbox1.addWidget(self.spin_box)
        self.setLayout(self.vbox1)

class EntryCalendarWidget(QWidget):
    def __init__(self, name):
        super(EntryCalendarWidget, self).__init__()
        
        self.name = name
        self.lbl = QLabel(self.name)
        # self.lbl.setStyleSheet("QLabel {font-weight: bold;}")
        self.calendar = QCalendarWidget()
        # self.spin_box.setStyleSheet("QCalendarWidget {font-weight: bold;}")
        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.lbl)
        self.vbox1.addWidget(self.calendar)
        self.setLayout(self.vbox1)


class PaymentWidget(QWidget):
    def __init__(self):
        super(PaymentWidget, self).__init__()
        # self.payment_widget = QWidget()
        self.payment_layout = QGridLayout()
        self.payment_label = QLabel("Payment Method")
        # payment_label.setStyleSheet("QLabel {font-weight: bold;}")
        self.payment_layout.addWidget(self.payment_label,0,0,1,2)
        self.payment_radio_setup = QWidget() # Cash/cheque widget
        payment_method_layout = QHBoxLayout()
        self.radio_button1 = QRadioButton("Cash")
        # self.radio_button1.setStyleSheet("QRadioButton {font-weight: bold;}")
        self.radio_button1.setChecked(True)
        self.radio_button1.toggled.connect(self.check_payment_method)
        payment_method_layout.addWidget(self.radio_button1)
        self.radio_button2 = QRadioButton("Cheque")
        # self.radio_button2.setStyleSheet("QRadioButton {font-weight: bold;}")
        self.radio_button2.toggled.connect(self.check_payment_method)
        payment_method_layout.addWidget(self.radio_button2)
        self.payment_radio_setup.setLayout(payment_method_layout)
        self.payment_layout.addWidget(self.payment_radio_setup,1,0,1,2)

        self.bank_name = EntryWidget("Bank Name")# bank name
        self.payment_layout.addWidget(self.bank_name,2,0)
        self.cheque_no = EntryWidget("Cheque Number")# cheque no
        self.payment_layout.addWidget(self.cheque_no,2,1)

        self.remarks = EntryTextEditWidget("Remarks") #remarks
        self.payment_layout.addWidget(self.remarks, 3,0,4,2)

        self.setLayout(self.payment_layout)
        self.check_payment_method()
    
    def check_payment_method(self):
        if self.radio_button2.isChecked():#Cheque radio button
            self.bank_name.ledit.setEnabled(True)
            self.cheque_no.ledit.setEnabled(True)
        else:
            self.bank_name.ledit.setEnabled(False)
            self.cheque_no.ledit.setEnabled(False)

class InvoiceDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        QBtn = QDialogButtonBox.Save | QDialogButtonBox.Cancel
        
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.inp_widgets = QWidget()
        self.inp_widgetsLayout = QVBoxLayout()
        self.item_1 = EntryWidget("Invoice Number:")
        self.inp_widgetsLayout.addWidget(self.item_1)

        # Adding active invoices button
        self.item_button = QPushButton("               Show Active Invoices               ")
        # self.item_button.setMaximumSize(800,100)
        self.item_button.setStyleSheet("QPushButton {color: '#DCDCDC'};")
        self.inp_widgetsLayout.addWidget(self.item_button, alignment = Qt.AlignCenter)
        self.item_button.setVisible(False)
        
        self.item_2 = EntryWidget("Purchase Order Reference:")
        self.inp_widgetsLayout.addWidget(self.item_2)
        self.item_3 = EntrySpinBoxWidget("Amount:")
        self.inp_widgetsLayout.addWidget(self.item_3)
        self.item_4 = EntryCalendarWidget("Date:")
        self.inp_widgetsLayout.addWidget(self.item_4)
        self.inp_widgets.setLayout(self.inp_widgetsLayout)

        self.payment_entry_widget = PaymentWidget()
        for w in [
            self.payment_entry_widget.payment_label,
            self.payment_entry_widget.radio_button1,
            self.payment_entry_widget.radio_button2,
            self.payment_entry_widget.bank_name,
            self.payment_entry_widget.cheque_no,
            self.payment_entry_widget.remarks]:
            w.setVisible(False)

        self.layout = QGridLayout()
        self.layout.addWidget(self.inp_widgets, 0,0,4,1)
        self.layout.addWidget(self.payment_entry_widget, 0,1,1,1)
        self.layout.addWidget(self.buttonBox, 5,0)
        self.setLayout(self.layout)

class PaymentDialog(InvoiceDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout.removeWidget(self.buttonBox)
        self.layout.addWidget(self.buttonBox, 5,1)
        self.item_button.setVisible(True)
        for w in [
            self.payment_entry_widget.payment_label,
            self.payment_entry_widget.radio_button1,
            self.payment_entry_widget.radio_button2,
            self.payment_entry_widget.bank_name,
            self.payment_entry_widget.cheque_no,
            self.payment_entry_widget.remarks]:
            w.setVisible(True)

class EntryPanel(QMainWindow):

    def __init__(self, database_filename, ctx, *args, **kwargs):
        self.database_filename = database_filename
        self.ctx = ctx
        super().__init__(*args, **kwargs)

        self.panels = QWidget()
        self.panelsLayout = QGridLayout() 
        self.panel_entry = []

        tabs = QTabWidget()
        tabs.setStyleSheet('QTabBar::tab {height: 100px; width: 300px; font-weight:bold;}')
        self.tab1 = QWidget()
        self.tab1Layout = QGridLayout() 
        self.tab2 = QWidget()
        self.tab2Layout = QGridLayout()
        self.tab3 = QWidget()
        self.tab3Layout = QGridLayout()
        tabs.addTab(self.tab1, "Information")
        tabs.addTab(self.tab2, "Invoices")
        tabs.addTab(self.tab3, "LOG")
        
        # Tab1 # TODO: add QCompleter to the text entries
        item = EntryWidget("Company")#Company Name
        self.tab1Layout.addWidget(item,0,0)
        self.panel_entry.append(item)
        item = EntryWidget("Contact")#Contact Name
        self.tab1Layout.addWidget(item,0,1)
        self.panel_entry.append(item)
        item = EntryTextEditWidget("Address") # Address
        item.tedit.setPlaceholderText("Enter company address here")
        self.tab1Layout.addWidget(item,1,0,2,2)
        self.panel_entry.append(item)
        item = EntryWidget("E-Mail")#Email
        item.ledit.setPlaceholderText("name@company.com")
        self.tab1Layout.addWidget(item,3,0)
        self.panel_entry.append(item)
        item = EntryWidget("Phone Number") # Phone No
        # item.ledit.setPlaceholderText("+X-XXXXX-XXXXX")
        self.tab1Layout.addWidget(item,3,1)
        self.panel_entry.append(item)
        item = EntryWidget("Fax Number") # Fax No
        # item.ledit.setPlaceholderText("+Y-XXXXX-XXXXX")
        self.tab1Layout.addWidget(item,4,0)
        self.panel_entry.append(item)
        """Opening Balance here""" # TODO move this to after user saves info
        item = EntrySpinBoxWidget("Opening Balance")#"NEW Payment"
        self.tab1Layout.addWidget(item,4,1)
        self.panel_entry.append(item)
        item = EntryTextEditWidget("Details") # Details
        item.tedit.setPlaceholderText("Add additional details here")
        self.tab1Layout.addWidget(item,5,0,2,2)
        self.panel_entry.append(item)
        # Tab2
        self.invoice_list_view = QListView()
        self.invoice_model = QStandardItemModel(self.invoice_list_view)
        self.invoice_list_view.setModel(self.invoice_model)
        # self.invoice_list_view.setReadOnly(True)
        # self.log_textEdit.setStyleSheet("QTextEdit {font-weight: bold;}")
        self.tab2Layout.addWidget(self.invoice_list_view)

        # Tab3
        self.log_textEdit = QTextEdit()
        self.log_textEdit.setReadOnly(True)
        # self.log_textEdit.setStyleSheet("QTextEdit {font-weight: bold;}")
        self.tab3Layout.addWidget(self.log_textEdit)

        #Set Layout for tabs
        self.tab1.setLayout(self.tab1Layout)
        self.tab2.setLayout(self.tab2Layout)
        self.tab3.setLayout(self.tab3Layout)
        
        # Adding Save Button
        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet("QPushButton {background-color: #4ecca3; color: black;}")# #4ecca3
        self.save_btn.clicked.connect(self.update_database)
        
        # Adding Undo Button
        self.undo_btn = QPushButton("Undo Changes")
        self.undo_btn.setStatusTip("Can only undo/revert changes if they are not saved!")
        self.undo_btn.setStyleSheet("QPushButton {background-color: #acdbdf; color: black;}")
        self.undo_btn.setVisible(False)

        btn_widgets = QWidget()
        btn_widgets_layout = QHBoxLayout()
        btn_widgets_layout.addWidget(self.save_btn)
        btn_widgets_layout.addWidget(self.undo_btn)
        btn_widgets.setLayout(btn_widgets_layout)

        # Adding edit checkbox for child classes
        self.edit_checkbox = QCheckBox("Edit Entry")
        self.edit_checkbox.setStyleSheet("QCheckBox {font-weight:bold;}")
        self.edit_checkbox.setVisible(False)
        # Add new invoice
        self.new_invoice_btn = QPushButton("New Invoice")
        self.new_invoice_btn.setStyleSheet("QPushButton {background-color: #927fbf; color: black;}")
        self.new_invoice_btn.setVisible(False)
        self.new_invoice_btn.clicked.connect(self.open_invoice_dialog)
        # Add new payment
        self.new_payment_btn = QPushButton("New Payment")
        self.new_payment_btn.setStyleSheet("QPushButton {background-color: #4ecca3; color: black;}")
        self.new_payment_btn.setVisible(False)
        self.new_payment_btn.clicked.connect(self.open_payment_dialog)

        edit_widget = QWidget()
        edit_layout = QHBoxLayout()
        edit_layout.addWidget(self.edit_checkbox)
        edit_layout.addWidget(self.new_invoice_btn)
        edit_layout.addWidget(self.new_payment_btn)
        edit_widget.setLayout(edit_layout)

        # Add status bar
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

        self.container = QWidget()
        self.containerLayout = QVBoxLayout()
        self.containerLayout.addWidget(edit_widget)
        self.containerLayout.addWidget(tabs)
        self.containerLayout.addWidget(btn_widgets)
        self.container.setLayout(self.containerLayout)

        self.setCentralWidget(self.container)

        self.setGeometry(800, 100, 1000*self.devicePixelRatio(),800*self.devicePixelRatio())
        self.setWindowTitle('Create New Customer')

        # self.check_payment_method()# check correct option selection and enabling of lineedits
        # self.show()
        # self.centerOnScreen()

    def centerOnScreen (self):
        '''centerOnScreen() Centers the window on the screen.'''
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2)) 

    def open_invoice_dialog(self):
        new_invoice_dialog = InvoiceDialog(self)
        new_invoice_dialog.setWindowTitle('New invoice for '+ str(self.panel_entry[0].ledit.text()))
        ok = new_invoice_dialog.exec_()
        
        if ok and new_invoice_dialog.item_1.ledit.text() and new_invoice_dialog.item_3.spin_box.value() != 0:
            # TODO add to database
            write_invoice_to_file(self, self.database_filename, self.idx_no,
            str(new_invoice_dialog.item_1.ledit.text()),
            str(new_invoice_dialog.item_2.ledit.text()),
            float(new_invoice_dialog.item_3.spin_box.value()),
            str(new_invoice_dialog.item_4.calendar.selectedDate().toString())
            )
        elif ok and not new_invoice_dialog.item_1.ledit.text() and new_invoice_dialog.item_3.spin_box.value() == 0:
            inform_user(self, "Invoice field was left empty or Amount was 0.\n\n"+
                "No new invoice was created.")
    
    def open_payment_dialog(self):
        new_payment_dialog = PaymentDialog(self)
        new_payment_dialog.setWindowTitle("New Payment for "+ str(self.panel_entry[0].ledit.text()))
        ok = new_payment_dialog.exec_()
        # TODO write if else statements
        if ok and new_payment_dialog.item_1.ledit.text() and new_payment_dialog.item_3.spin_box.value() != 0:
            if new_payment_dialog.payment_entry_widget.radio_button1.isChecked():
                payment_method = new_payment_dialog.payment_entry_widget.radio_button1.text()
                bank_name = None
                cheque_no = None
            elif new_payment_dialog.payment_entry_widget.radio_button2.isChecked():
                payment_method = new_payment_dialog.payment_entry_widget.radio_button2.text()
                bank_name = new_payment_dialog.payment_entry_widget.bank_name.ledit.text()
                cheque_no = new_payment_dialog.payment_entry_widget.cheque_no.ledit.text()
            
            remarks = new_payment_dialog.payment_entry_widget.remarks.tedit.toPlainText()
            
            write_new_payment(self, self.database_filename,
            self.idx_no,
            str(new_payment_dialog.item_1.ledit.text()),
            str(new_payment_dialog.item_2.ledit.text()),
            float(new_payment_dialog.item_3.spin_box.value()),
            str(new_payment_dialog.item_4.calendar.selectedDate().toString()),
            payment_method, bank_name, cheque_no, remarks            
            )
        elif ok and new_payment_dialog.item_3.spin_box.value() == 0:
            inform_user(self, "Payment amount was '0'. Ener a valid payment amount")
            self.open_payment_dialog()

        elif ok and not new_payment_dialog.item_1.ledit.text():
            inform_user(self, "No invoice number entered. Ener a valid invoice number")
            self.open_payment_dialog()
    
    def _collect_widget_data(self):# TODO collect Log entries while editing and reading file
       company_name = self.panel_entry[0].ledit.text()
       contact_name =  self.panel_entry[1].ledit.text()
       address = self.panel_entry[2].tedit.toPlainText()
       email =  self.panel_entry[3].ledit.text()
       phone_no = self.panel_entry[4].ledit.text()
       fax_no = self.panel_entry[5].ledit.text()
       total_business = 0#float(self.panel_entry[3].spin_box.value())
       total_paid = 0#float(self.panel_entry[4].spin_box.value())
       outstanding = 0#float(self.panel_entry[5].spin_box.value())
       details = self.panel_entry[7].tedit.toPlainText()
    #    # Read in database file to write in
       data_pkl = read_file(self.database_filename)
       self.idx_no = len(data_pkl) # for setting invoice through entry panel, otherwise there is no reference of index no in entry panel
       data_dict={
           "Company Name": company_name, "Contact Name": contact_name,
           "Address": address, 
           "Email": email, "Phone No.": phone_no, "Fax No.": fax_no,
           "Total Business": total_business, "Total Paid": total_paid, 
           "Outstanding": outstanding,"Details": details,
           "Invoices":{},
           "Logs":{},
           "Price Quote Log":{}
           }
       data_pkl.append(data_dict)
       return data_pkl

    def update_database(self): #TODO: Catch user entering empty strings
        data_pkl = self._collect_widget_data()
        write_file(data_pkl, self.database_filename)
        answer = QMessageBox.question(
            self, None, "Do you want to create an opening balance for this company?", 
            QMessageBox.Ok | QMessageBox.Cancel)
        
        if answer and QMessageBox.Ok:
            self.open_invoice_dialog()
        # data_pkl.to_csv(self.database_filename, index = False)#, sheet_name="Sheet1")
        self.statusBar.showMessage("Entry Added!", 2000)
        for i in range(len(self.panel_entry)):
            try:
                try:
                    self.panel_entry[i].ledit.setText("")
                except:
                    self.panel_entry[i].tedit.setText("")
            except:
                self.panel_entry[i].spin_box.setValue(0.00)
                # self.statusBar.clearMessage()# only to remove any message that comes while resetting spinboxes (due to their connections)
    
class EditViewPanel(EntryPanel):

    def __init__(self, idx_no, edit_true = True, *args, **kwargs):#Order of arguments "name,std,school" etc must be the same everywhere!
        self.idx_no = idx_no
        self.edit_true = edit_true
        self.prev_log = {}
        super().__init__(*args, **kwargs)

        self.edit_checkbox.setVisible(True)
        self.edit_checkbox.stateChanged.connect(self.edit_or_view)
        self.previous_data = self._get_data()
        self.populate_view(data=self.previous_data)
        if self.edit_true is True:
            self.edit_checkbox.setChecked(True)
        else:
            self.edit_checkbox.setChecked(False)
        # self.undo_btn.clicked.connect(self.undo_changes)
        
        self.setWindowTitle('View/Edit Panel')
        # self.show()
    
    def edit_or_view(self):
        if self.edit_checkbox.isChecked():
            self.new_invoice_btn.setVisible(True)
            self.new_payment_btn.setVisible(True)
            self.save_btn.setVisible(True)
            self.undo_btn.setVisible(True)
            # self.payment_radio_setup.setEnabled(True)
            # self.check_payment_method()
            for i in range(len(self.panel_entry)):
                try:
                    try:
                        self.panel_entry[i].ledit.setReadOnly(False)
                    except:
                        self.panel_entry[i].tedit.setReadOnly(False)
                except:
                    self.panel_entry[i].spin_box.setReadOnly(False)
        else:
            self.new_invoice_btn.setVisible(False)
            self.new_payment_btn.setVisible(False)
            self.save_btn.setVisible(False)
            self.undo_btn.setVisible(False)
            # self.payment_radio_setup.setEnabled(False)
            # self.check_payment_method()
            for i in range(len(self.panel_entry)):
                try:
                    try:
                        self.panel_entry[i].ledit.setReadOnly(True)
                    except:
                        self.panel_entry[i].tedit.setReadOnly(True)
                except:
                    self.panel_entry[i].spin_box.setReadOnly(True)
    
    def _get_data(self):
        data_pkl = read_file(self.database_filename)
        company_name = data_pkl[int(self.idx_no)]["Company Name"]#.iloc[int(self.idx_no)]
        contact_name = data_pkl[int(self.idx_no)]["Contact Name"]
        address = data_pkl[int(self.idx_no)]["Address"]
        email = data_pkl[int(self.idx_no)]["Email"]
        phone_no = data_pkl[int(self.idx_no)]["Phone No."]
        fax_no = data_pkl[int(self.idx_no)]["Fax No."]
        total_business = data_pkl[int(self.idx_no)]["Total Business"]
        total_paid = data_pkl[int(self.idx_no)]["Total Paid"]
        outstanding = data_pkl[int(self.idx_no)]["Outstanding"]
        details = data_pkl[int(self.idx_no)]["Details"]
        self.prev_log = data_pkl[int(self.idx_no)]["Logs"]
        
        # self.existing_invoice_no = []
        if len(data_pkl[int(self.idx_no)]["Invoices"]) > 0:
            for i in range(len(data_pkl[int(self.idx_no)]["Invoices"])):
                item = QStandardItem(data_pkl[int(self.idx_no)]["Invoices"]["Invoice "+str(i+1)]["Invoice No"])
                self.invoice_model.appendRow(item)

        return company_name, contact_name, address, email, phone_no, fax_no, total_business, total_paid, outstanding, details
    
    def populate_view(self, data):
        company_name, contact_name, address, email, phone_no, fax_no, total_business, total_paid, outstanding, details = data
    
        self.panel_entry[0].ledit.setText(str(company_name))
        self.panel_entry[1].ledit.setText(str(contact_name))
        self.panel_entry[2].tedit.setText(str(address))
        self.panel_entry[3].ledit.setText(str(email))
        self.panel_entry[4].ledit.setText(str(phone_no))
        self.panel_entry[5].ledit.setText(str(fax_no))
        self.panel_entry[7].tedit.setText(str(details))

        # self.panel_entry[3].spin_box.setValue(float(fees_ann))
        # self.panel_entry[4].spin_box.setValue(float(fees_paid))
        # self.panel_entry[5].spin_box.setValue(float(fees_rem))
        # self.set_log_text()
        self.edit_or_view()

    # def set_log_text(self):#, x=None): # TODO save a separate log file to keep track of everything
    #     # if x is not None:
    #     # #     self.search_text = x.lower()
    #     # old_scroll_pos = self.log_textEdit.verticalScrollBar().value()
    #     # print(old_scroll_pos)
    #     self.log_str = ""  
    #     #self.f.visititems(self._visitfunc)
    #     self.traverse_dict(self.prev_log, self.prev_log, 0)

        
    #     self.log_text_html = \
    #     """<html><h4">{}</h4></hr>
    #     <div>
    #         {} 
    #         </div>
    #         </html>""".format("Payment Log", self.log_str)
        
    #     self.log_textEdit.setText(self.log_text_html) #; font-size: 40px;
    #     self.log_textEdit.verticalScrollBar().setValue(self.log_textEdit.verticalScrollBar().maximum())

    # def traverse_dict(self, dictionary, previous_dict, level):
    #     """
    #     Visit all values in the dictionary and its subdictionaries.
    #     dictionary -- dictionary to traverse
    #     previous_dict -- dictionary one level up
    #     level -- track how far to indent 
    #     """
    #     for key in dictionary:
    #         if key not in previous_dict:
    #             level -=1
    #         indent = "&nbsp;"*4*(level)

    #         if type(dictionary[key]) == dict:
    #             print_string = key
    #             # if self.search_text and self.search_text in print_string:
    #             #     self.tree_str += indent + """<span style="color: red;">{}</span>""".format(print_string)
    #             # else:
    #             self.log_str += indent + """> <b>{}/</b><br/>""".format(print_string)
    #             level += 1
    #             previous_dict = dictionary[key]
    #             self.traverse_dict(dictionary[key], previous_dict, level)
    #         else:
    #             value = dictionary[key]

    #             print_string = key + " : " + str(value)
    #             # if self.search_text and self.search_text in print_string:
    #                 # self.tree_str += indent + """<span style="color: red;">{}</span>""".format(print_string)
    #             # else:
    #             if key == "Closing Balance":
    #                 self.log_str += indent + ">"+ """<b style="color: #4ecca3;"> {}</b><br/>""".format(print_string)
    #             elif key == "Opening Balance":
    #                 self.log_str += indent + ">"+ """<b style="color: #ff4866;"> {}</b><br/>""".format(print_string)
    #             elif key == "Payment Amount":
    #                 self.log_str += indent + ">"+ """<b style="color: #927fbf;"> {}</b><br/>""".format(print_string)
    #             else:
    #                 self.log_str += indent + ">"+ """<b> {}</b><br/>""".format(print_string)

    def collect_widget_data(self):
       company_name = self.panel_entry[0].ledit.text()
       contact_name =  self.panel_entry[1].ledit.text()
       address = self.panel_entry[2].tedit.toPlainText()
       email =  self.panel_entry[3].ledit.text()
       phone_no = self.panel_entry[4].ledit.text()
       fax_no = self.panel_entry[5].ledit.text()
       total_business = 0#float(self.panel_entry[3].spin_box.value())
       total_paid = 0#float(self.panel_entry[4].spin_box.value())
       outstanding = 0#float(self.panel_entry[5].spin_box.value())
       details = self.panel_entry[7].tedit.toPlainText()

       data_pkl = read_file(self.database_filename)
    #    prev_balance = data_pkl[int(self.idx_no)]["Remaining"]

       data_pkl[int(self.idx_no)]["Company Name"] = company_name
       data_pkl[int(self.idx_no)]["Contact Name"] = contact_name
       data_pkl[int(self.idx_no)]["Address"] = address
       data_pkl[int(self.idx_no)]["Email"] = email
       data_pkl[int(self.idx_no)]["Phone No."] =  phone_no
       data_pkl[int(self.idx_no)]["Fax No."] =  fax_no
    #    data_pkl[int(self.idx_no)]["Total Balance"] = fees_ann
    #    data_pkl[int(self.idx_no)]["Paid"] = fees_paid
    #    data_pkl[int(self.idx_no)]["Remaining"] =  fees_rem
       data_pkl[int(self.idx_no)]["Details"] =  details
       
    #    if prev_balance != fees_rem: # only log payments if there has been a change in the balance
    #        new_log = {}
    #        new_log["Record Date"] = date.today().strftime("%B %d, %Y")
    #        new_log["Opening Balance"] = prev_balance
    #        new_log["Closing Balance"] = fees_rem
    #        new_log["Payment Amount"] = payment
    #        if self.radio_button1.isChecked():
    #            new_log["Payment Method"] = self.radio_button1.text()
    #        if self.radio_button2.isChecked():
    #            new_log["Payment Method"] = self.radio_button2.text()
    #            new_log["Details"] = {}
    #            new_log["Details"]['Bank Name'] = self.panel_entry[7].ledit.text()
    #            new_log["Details"]['Cheque Number'] = self.panel_entry[8].ledit.text()

    #        data_pkl[int(self.idx_no)]["Logs"]["Log"+str(len(data_pkl[int(self.idx_no)]["Logs"])+1)] = new_log
       return data_pkl

    def update_database(self):
        data_pkl = self.collect_widget_data()
        # self.panel_entry[9].spin_box.setValue(0.00)#set payment spinbox to 0 after saving
        write_file(data_pkl,self.database_filename)
        self.statusBar.showMessage("Edited & Saved!", 2000)
        self.reload()
        
    def reload(self):
        self.populate_view(self._get_data())
        inform_user(self, "Entry updated. You may now reload.")
        self.close()

    def undo_changes(self):
        self.populate_view(self.previous_data)# set it to previous data # TODO : should take care of details text edit too
        # self.panel_entry[9].spin_box.setValue(0.00)#set payment spinbox to 0 after saving