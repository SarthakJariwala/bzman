import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json
from util import read_file, write_file
from datetime import date
# import qtmodern.windows

class MasterViewerWidget(QWidget):

    def __init__(self, idx_no, name, std, school, rem_fees, database_filename, ctx):
        super(MasterViewerWidget, self).__init__()
        self.ctx = ctx

        self.name = name
        self.idx_no = str(idx_no)
        self.database_filename = database_filename
        self.std = str(std)
        self.school = school
        self.rem_fees = rem_fees # will convert to string later 

        self.idx_lbl = QLabel(self.idx_no)
        
        self.name_lbl = QLabel("Name: "+self.name)
        # lbl_font = self.name_lbl.font()
        # lbl_font.setPointSize(14)
        # self.name_lbl.setFont(lbl_font)

        self.std_lbl = QLabel("Standard: "+self.std)
        #lbl_font = self.std_lbl.font()
        #lbl_font.setPointSize(10)
        #self.std_lbl.setFont(lbl_font)

        self.school_lbl = QLabel("School: "+self.school)
        #lbl_font = self.school_lbl.font()
        #lbl_font.setPointSize(10)
        #self.school_lbl.setFont(lbl_font)
        self.rem_fees_lbl = QLabel("Fees Remaining (Rs.): \n"+str(self.rem_fees))
        if self.rem_fees == 0:
            self.rem_fees_lbl.setStyleSheet("QLabel {color: #4ecca3;} ")
        else:
            self.rem_fees_lbl.setStyleSheet("QLabel {color: #ff6363;} ") # #35e3e3
        self.btn_view = QPushButton("View")
        self.btn_view.setStyleSheet("QPushButton {background-color: #46b5d1; color: black;}")#font-size:25px;}") #bbe1fa
        self.btn_edit = QPushButton("Edit")
        self.btn_edit.setStyleSheet("QPushButton {background-color: #4ecca3; color:black;}")#font-size:25px;}")
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.setStyleSheet("QPushButton {background-color: #ff4866; color: black;}")#font-size:25px;}")
        self.btn_delete.setVisible(False)

        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.idx_lbl)
        self.vbox1.addWidget(self.name_lbl)
        self.vbox1.addWidget(self.std_lbl)
        self.vbox1.addWidget(self.school_lbl)
        self.vbox1.addWidget(self.rem_fees_lbl)
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.btn_view)
        self.hbox2.addWidget(self.btn_edit)
        self.hbox2.addWidget(self.btn_delete)
        
        self.hbox3 = QHBoxLayout()
        self.hbox3.addLayout(self.vbox1)
        self.hbox3.addLayout(self.hbox2)

        self.idx_lbl.setVisible(False)

        self.btn_view.clicked.connect(self.open_view_window)
        self.btn_edit.clicked.connect(self.open_edit_window)
        self.btn_delete.clicked.connect(self.delete_entry)
        
        self.setLayout(self.hbox3)

        #self.update_button_state()
        
    def open_view_window(self):
        self.view_window = EditViewPanel(self.idx_no, False, self.database_filename, self.ctx)
        # self.view_window = qtmodern.windows.ModernWindow(self.view_window)
        self.view_window.show()
    
    def open_edit_window(self):
        self.edit_window = EditViewPanel(self.idx_no, True, self.database_filename, self.ctx)
        # self.edit_window = qtmodern.windows.ModernWindow(self.edit_window)
        self.edit_window.show()
    
    def delete_entry(self):
        answer = QMessageBox.question(
            self, None, "Are you sure you want to delete the entry? This can not be undone!", 
            QMessageBox.Ok | QMessageBox.Cancel)
        
        if answer & QMessageBox.Ok:
            data_pkl = read_file(self.database_filename)
            data_pkl.pop(int(self.idx_no))
            write_file(data_pkl, self.database_filename)
            ask_user_to_reload(self, "Entry Deleted! You may now reload.")

    def show(self):
        """
        Show this widget, and all child widgets.
        """
        for w in [self, self.name_lbl, self.std_lbl, self.school_lbl, self.rem_fees_lbl, self.btn_view, self.btn_edit]:
            w.setVisible(True)
        try:
            self.btn_delete.setVisible(True)
        except:
            pass

    def hide(self):
        """
        Hide this widget, and all child widgets.
        """
        for w in [self, self.name_lbl, self.std_lbl, self.school_lbl,self.rem_fees_lbl, self.btn_view, self.btn_edit]:
            w.setVisible(False)
        try:
            self.btn_delete.setVisible(False)
        except:
            pass

class EntryWidget(QWidget):

    def __init__(self, name):
        super(EntryWidget, self).__init__()

        self.name = name

        self.lbl = QLabel(self.name)
        self.lbl.setStyleSheet("QLabel {font-weight: bold;}")
        self.ledit = QLineEdit()
        self.ledit.setStyleSheet("QLineEdit {font-weight: bold;}")

        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.lbl)
        self.vbox1.addWidget(self.ledit)
        self.setLayout(self.vbox1)

class EntryTextEditWidget(QWidget):

    def __init__(self, name):
        super(EntryTextEditWidget, self).__init__()

        self.name = name

        self.lbl = QLabel(self.name)
        self.lbl.setStyleSheet("QLabel {font-weight: bold;}")
        self.tedit = QTextEdit()
        self.tedit.setStyleSheet("QTextEdit {font-weight: bold;}")

        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.lbl)
        self.vbox1.addWidget(self.tedit)
        self.setLayout(self.vbox1)

class EntrySpinBoxWidget(QWidget):

    def __init__(self, name):
        super(EntrySpinBoxWidget, self).__init__()

        self.name = name

        self.lbl = QLabel(self.name)
        self.lbl.setStyleSheet("QLabel {font-weight: bold;}")
        self.spin_box = QDoubleSpinBox()
        self.spin_box.setStyleSheet("QDoubleSpinBox {font-weight: bold}")
        self.spin_box.setMaximum(1000000000.00)
        self.spin_box.setMinimum(0.00)

        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.lbl)
        self.vbox1.addWidget(self.spin_box)
        self.setLayout(self.vbox1)

class EntryPanel(QMainWindow):

    def __init__(self, database_filename, ctx, *args, **kwargs):
        self.database_filename = database_filename
        self.ctx = ctx
        super().__init__(*args, **kwargs)

        self.panels = QWidget()
        self.panelsLayout = QGridLayout() 

        self.panel_entry_names = [
            "NAME", "STANDARD","SCHOOL",
            "ANNUAL FEES (Rs.)", "FEES PAID (Rs.)",
            "FEES REMAINING (Rs.)", "PHONE NO.",
            "BANK", "CHEQUE NO.", "NEW PAYMENT",
            "DETAILS" 
        ]

        self.panel_entry = []

        # for panel_name in self.panel_entry_names:
        #     self.item = EntryWidget(panel_name)
        #     self.panelsLayout.addWidget(self.item)
        #     self.panel_entry.append(self.item) ### Change to gridlayout
        tabs = QTabWidget()
        tabs.setStyleSheet('QTabBar::tab {height: 100px; width: 300px; font-weight:bold;}')
        self.tab1 = QWidget()
        self.tab1Layout = QGridLayout() 
        self.tab2 = QWidget()
        self.tab2Layout = QGridLayout()
        self.tab3 = QWidget()
        self.tab3Layout = QGridLayout()
        tabs.addTab(self.tab1, "INFORMATION")
        tabs.addTab(self.tab2, "PAYMENT")
        tabs.addTab(self.tab3, "LOG")
        
        # Tab1
        item = EntryWidget(self.panel_entry_names[0])#Name
        self.tab1Layout.addWidget(item,0,0,1,2)
        self.panel_entry.append(item)
        item = EntryWidget(self.panel_entry_names[1])#Standard
        self.tab1Layout.addWidget(item,1,0)
        self.panel_entry.append(item)
        item = EntryWidget(self.panel_entry_names[2])#School
        self.tab1Layout.addWidget(item,1,1)
        self.panel_entry.append(item)
        
        # Tab2
        item = EntrySpinBoxWidget(self.panel_entry_names[3])#"Annual Fees (Rs.)"
        self.tab2Layout.addWidget(item,0,0)
        self.panel_entry.append(item)
        item = EntrySpinBoxWidget(self.panel_entry_names[4])#"Fees Paid (Rs.)"
        item.lbl.setStyleSheet("QLabel {font-weight: bold; color: #4ecca3;}")
        self.tab2Layout.addWidget(item,0,1)
        self.panel_entry.append(item)
        item = EntrySpinBoxWidget(self.panel_entry_names[5])#"Fees Remaining (Rs.)"
        item.lbl.setStyleSheet("QLabel {font-weight: bold; color: #ff4866;}")
        self.tab2Layout.addWidget(item,1,0)
        self.panel_entry.append(item)

        # From tab1 but kept order the same as previous version to avoid changing list indexing in "panel_entry_names" in the class
        item = EntryWidget(self.panel_entry_names[6]) # Phone No
        self.tab1Layout.addWidget(item,2,0,1,1)
        self.panel_entry.append(item)

        # Tab2 continued
        payment_label = QLabel("PAYMENT METHOD")
        payment_label.setStyleSheet("QLabel {font-weight: bold;}")
        self.tab2Layout.addWidget(payment_label,2,0)
        self.payment_radio_setup = QWidget() # Cash/cheque widget
        payment_method_layout = QHBoxLayout()
        self.radio_button1 = QRadioButton("Cash")
        self.radio_button1.setStyleSheet("QRadioButton {font-weight: bold;}")
        self.radio_button1.setChecked(True)
        self.radio_button1.toggled.connect(self.check_payment_method)
        payment_method_layout.addWidget(self.radio_button1)
        self.radio_button2 = QRadioButton("Cheque")
        self.radio_button2.setStyleSheet("QRadioButton {font-weight: bold;}")
        self.radio_button2.toggled.connect(self.check_payment_method)
        payment_method_layout.addWidget(self.radio_button2)
        self.payment_radio_setup.setLayout(payment_method_layout)
        self.tab2Layout.addWidget(self.payment_radio_setup,3,0)

        item = EntryWidget(self.panel_entry_names[7])# bank name
        self.tab2Layout.addWidget(item,4,0)
        self.panel_entry.append(item)
        item = EntryWidget(self.panel_entry_names[8])# cheque no
        self.tab2Layout.addWidget(item,4,1)
        self.panel_entry.append(item)

        # From tab2 but kept order the same as in "panel_entry_names" in the class to avoid correcting all number indexing of panel_entry items
        item = EntrySpinBoxWidget(self.panel_entry_names[9])#"NEW Payment"
        item.lbl.setStyleSheet("QLabel {font-weight: bold; color: #927fbf;}")
        # palette = QPalette() # Doesn't work
        # palette.setColor(QPalette.Text, QColor("#927fbf"))
        # item.spin_box.setPalette(palette)
        self.tab2Layout.addWidget(item,1,1)
        self.panel_entry.append(item)

        # From tab1 but kept order the same as previous version to avoid changing list indexing in "panel_entry_names" in the class
        item = EntryTextEditWidget(self.panel_entry_names[10]) # Details
        self.tab1Layout.addWidget(item,3,0,2,2)
        self.panel_entry.append(item)

        # Tab3
        self.log_textEdit = QTextEdit()
        self.log_textEdit.setReadOnly(True)
        self.log_textEdit.setStyleSheet("QTextEdit {font-weight: bold;}")
        self.tab3Layout.addWidget(self.log_textEdit)

        #Set Layout for tabs
        self.tab1.setLayout(self.tab1Layout)
        self.tab2.setLayout(self.tab2Layout)
        self.tab3.setLayout(self.tab3Layout)

        self.panel_entry[3].spin_box.valueChanged.connect(self.paid_fees_signal)
        self.panel_entry[4].spin_box.valueChanged.connect(self.paid_fees_signal)
        self.panel_entry[5].spin_box.valueChanged.connect(self.rem_fees_signal)
        self.panel_entry[9].spin_box.setKeyboardTracking(False)
        self.panel_entry[9].spin_box.valueChanged.connect(self.new_payment_signal)
        
        # Adding Save Button
        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet("QPushButton {background-color: #4ecca3; color: black;}")# #4ecca3
        self.save_btn.clicked.connect(self.update_database)
        
        # Adding Unfo Button
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
        
        # Add status bar
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

        self.container = QWidget()
        self.containerLayout = QVBoxLayout()
        self.containerLayout.addWidget(self.edit_checkbox)
        self.containerLayout.addWidget(tabs)
        self.containerLayout.addWidget(btn_widgets)
        self.container.setLayout(self.containerLayout)

        self.setCentralWidget(self.container)

        self.setGeometry(1500, 100, 1000,800)
        self.setWindowTitle('Entry Panel')

        self.check_payment_method()# check correct option selection and enabling of lineedits
        # self.show()
    
    def check_payment_method(self):
        if self.radio_button2.isChecked():#Cheque radio button
            self.panel_entry[7].ledit.setEnabled(True)
            self.panel_entry[8].ledit.setEnabled(True)
        else:
            self.panel_entry[7].ledit.setEnabled(False)
            self.panel_entry[8].ledit.setEnabled(False)


    def paid_fees_signal(self):#sets remaining value
        total = self.panel_entry[3].spin_box.value()
        paid = self.panel_entry[4].spin_box.value()
        if total-paid >= 0:
            self.panel_entry[5].spin_box.setValue(float(total-paid))
        else:
            self.statusBar.showMessage("Error: Make sure the numbers are positive!", 2000)

    def rem_fees_signal(self):#sets paid value
        total = self.panel_entry[3].spin_box.value()
        rem = self.panel_entry[5].spin_box.value()
        if total-rem >= 0:
            self.panel_entry[4].spin_box.setValue(float(total-rem))
        else:
            self.statusBar.showMessage("Error: Make sure the numbers are positive!", 2000)
    
    def new_payment_signal(self):
        new_payment = self.panel_entry[9].spin_box.value()
        paid = self.panel_entry[4].spin_box.value()
        total = self.panel_entry[3].spin_box.value()
        new_paid = paid + new_payment
        if total - new_paid >= 0:
            self.panel_entry[4].spin_box.setValue(new_paid)
        else:
            self.statusBar.showMessage("Error: Make sure the numbers are positive!", 2000)
    
    def collect_widget_data(self):# TODO collect Log entries while editing and reading file
       name = self.panel_entry[0].ledit.text()
       std =  self.panel_entry[1].ledit.text()
       school =  self.panel_entry[2].ledit.text()
       fees_ann = float(self.panel_entry[3].spin_box.value())
       fees_paid = float(self.panel_entry[4].spin_box.value())
       fees_rem = float(self.panel_entry[5].spin_box.value())
       phone_no = self.panel_entry[6].ledit.text()
       details = self.panel_entry[10].tedit.toPlainText()
       # Read in database file to write in
       data_pkl = read_file(self.database_filename)
       data_dict={
           "Name": name, "Std": std, "School": school,
           "Annual Fees (Rs.)": fees_ann, "Fees Paid (Rs.)": fees_paid, 
           "Fees Remaining (Rs.)": fees_rem, "Phone No.": phone_no,
           "Details": details,
           "Logs":{}
           }
       data_pkl.append(data_dict)
       #print(data_pkl.to_dict()) #Debug line
       return data_pkl

    def update_database(self): #TODO: Catch user entering empty strings
        data_pkl = self.collect_widget_data() # rerturns a pandas df
        write_file(data_pkl, self.database_filename)
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
        self.previous_data = self.get_data()
        self.populate_view(data=self.previous_data)
        if self.edit_true is True:
            self.edit_checkbox.setChecked(True)
        else:
            self.edit_checkbox.setChecked(False)
        self.undo_btn.clicked.connect(self.undo_changes)
        
        self.setWindowTitle('View/Edit Panel')
        self.show()
    
    def edit_or_view(self):
        if self.edit_checkbox.isChecked():
            self.save_btn.setVisible(True)
            self.undo_btn.setVisible(True)
            self.payment_radio_setup.setEnabled(True)
            self.check_payment_method()
            for i in range(len(self.panel_entry)):
                try:
                    try:
                        self.panel_entry[i].ledit.setReadOnly(False)
                    except:
                        self.panel_entry[i].tedit.setReadOnly(False)
                except:
                    self.panel_entry[i].spin_box.setReadOnly(False)
        else:
            self.save_btn.setVisible(False)
            self.undo_btn.setVisible(False)
            self.payment_radio_setup.setEnabled(False)
            self.check_payment_method()
            for i in range(len(self.panel_entry)):
                try:
                    try:
                        self.panel_entry[i].ledit.setReadOnly(True)
                    except:
                        self.panel_entry[i].tedit.setReadOnly(True)
                except:
                    self.panel_entry[i].spin_box.setReadOnly(True)
    
    def get_data(self):
        data_pkl = read_file(self.database_filename)
        name = data_pkl[int(self.idx_no)]["Name"]#.iloc[int(self.idx_no)]
        std = data_pkl[int(self.idx_no)]["Std"]
        school = data_pkl[int(self.idx_no)]["School"]
        fees_ann = data_pkl[int(self.idx_no)]["Annual Fees (Rs.)"]
        fees_paid = data_pkl[int(self.idx_no)]["Fees Paid (Rs.)"]
        fees_rem = data_pkl[int(self.idx_no)]["Fees Remaining (Rs.)"]
        phone_no = data_pkl[int(self.idx_no)]["Phone No."]
        details = data_pkl[int(self.idx_no)]["Details"]
        self.prev_log = data_pkl[int(self.idx_no)]["Logs"]
        return name, std, school, fees_ann, fees_paid, fees_rem, phone_no, details
    
    def populate_view(self, data):
        name, std, school, fees_ann, fees_paid, fees_rem, phone_no, details = data
        self.panel_entry[0].ledit.setText(str(name))
        self.panel_entry[1].ledit.setText(str(std))
        self.panel_entry[2].ledit.setText(str(school))
        self.panel_entry[3].spin_box.setValue(float(fees_ann))
        self.panel_entry[4].spin_box.setValue(float(fees_paid))
        self.panel_entry[5].spin_box.setValue(float(fees_rem))
        self.panel_entry[6].ledit.setText(str(phone_no))
        self.panel_entry[10].tedit.setText(str(details))
        self.set_log_text()
        self.edit_or_view()

    def set_log_text(self):#, x=None):
        # if x is not None:
        # #     self.search_text = x.lower()
        # old_scroll_pos = self.log_textEdit.verticalScrollBar().value()
        # print(old_scroll_pos)
        self.log_str = ""  
        #self.f.visititems(self._visitfunc)
        self.traverse_dict(self.prev_log, self.prev_log, 0)

        
        self.log_text_html = \
        """<html><h4">{}</h4></hr>
        <div>
            {} 
            </div>
            </html>""".format("Payment Log", self.log_str)
        
        self.log_textEdit.setText(self.log_text_html) #; font-size: 40px;
        self.log_textEdit.verticalScrollBar().setValue(self.log_textEdit.verticalScrollBar().maximum())

    def traverse_dict(self, dictionary, previous_dict, level):
        """
        Visit all values in the dictionary and its subdictionaries.
        dictionary -- dictionary to traverse
        previous_dict -- dictionary one level up
        level -- track how far to indent 
        """
        for key in dictionary:
            if key not in previous_dict:
                level -=1
            indent = "&nbsp;"*4*(level)

            if type(dictionary[key]) == dict:
                print_string = key
                # if self.search_text and self.search_text in print_string:
                #     self.tree_str += indent + """<span style="color: red;">{}</span>""".format(print_string)
                # else:
                self.log_str += indent + """> <b>{}/</b><br/>""".format(print_string)
                level += 1
                previous_dict = dictionary[key]
                self.traverse_dict(dictionary[key], previous_dict, level)
            else:
                value = dictionary[key]

                print_string = key + " : " + str(value)
                # if self.search_text and self.search_text in print_string:
                    # self.tree_str += indent + """<span style="color: red;">{}</span>""".format(print_string)
                # else:
                if key == "Closing Balance":
                    self.log_str += indent + ">"+ """<b style="color: #4ecca3;"> {}</b><br/>""".format(print_string)
                elif key == "Opening Balance":
                    self.log_str += indent + ">"+ """<b style="color: #ff4866;"> {}</b><br/>""".format(print_string)
                elif key == "Payment Amount":
                    self.log_str += indent + ">"+ """<b style="color: #927fbf;"> {}</b><br/>""".format(print_string)
                else:
                    self.log_str += indent + ">"+ """<b> {}</b><br/>""".format(print_string)

    def collect_widget_data(self):
       name = self.panel_entry[0].ledit.text()
       std =  self.panel_entry[1].ledit.text()
       school =  self.panel_entry[2].ledit.text()
       fees_ann = float(self.panel_entry[3].spin_box.value())
       fees_paid = float(self.panel_entry[4].spin_box.value())
       fees_rem = float(self.panel_entry[5].spin_box.value())
       phone_no = self.panel_entry[6].ledit.text()
       payment = float(self.panel_entry[9].spin_box.value())
       details = self.panel_entry[10].tedit.toPlainText()

       data_pkl = read_file(self.database_filename)
       prev_balance = data_pkl[int(self.idx_no)]["Fees Remaining (Rs.)"]
       data_pkl[int(self.idx_no)]["Name"] = name
       data_pkl[int(self.idx_no)]["Std"] = std
       data_pkl[int(self.idx_no)]["School"] = school
       data_pkl[int(self.idx_no)]["Annual Fees (Rs.)"] = fees_ann
       data_pkl[int(self.idx_no)]["Fees Paid (Rs.)"] = fees_paid
       data_pkl[int(self.idx_no)]["Fees Remaining (Rs.)"] =  fees_rem
       data_pkl[int(self.idx_no)]["Phone No."] =  phone_no
       data_pkl[int(self.idx_no)]["Details"] =  details
       
       if prev_balance != fees_rem: # only log payments if there has been a change in the balance
           new_log = {}
           new_log["Record Date"] = date.today().strftime("%B %d, %Y")
           new_log["Opening Balance"] = prev_balance
           new_log["Closing Balance"] = fees_rem
           new_log["Payment Amount"] = payment
           if self.radio_button1.isChecked():
               new_log["Payment Method"] = self.radio_button1.text()
           if self.radio_button2.isChecked():
               new_log["Payment Method"] = self.radio_button2.text()
               new_log["Details"] = {}
               new_log["Details"]['Bank Name'] = self.panel_entry[7].ledit.text()
               new_log["Details"]['Cheque Number'] = self.panel_entry[8].ledit.text()

           data_pkl[int(self.idx_no)]["Logs"]["Log"+str(len(data_pkl[int(self.idx_no)]["Logs"])+1)] = new_log
       return data_pkl

    def update_database(self):
        data_pkl = self.collect_widget_data()
        self.panel_entry[9].spin_box.setValue(0.00)#set payment spinbox to 0 after saving
        write_file(data_pkl,self.database_filename)
        self.statusBar.showMessage("Edited & Saved!", 2000)
        self.populate_view(self.get_data())
        ask_user_to_reload(self, "Entry updated. You may now reload.")
        self.close()

    def undo_changes(self):
        self.populate_view(self.previous_data)# set it to previous data # TODO : should take care of details text edit too
        self.panel_entry[9].spin_box.setValue(0.00)#set payment spinbox to 0 after saving

def ask_user_to_reload(parent, text):
    QMessageBox.information(
        parent, None, text,
        QMessageBox.Ok
    )