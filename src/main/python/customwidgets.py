import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json
from util import read_file, write_file, write_invoice_to_file, inform_user, get_company_summary
from panels import EntryPanel, EditViewPanel, InvoiceDialog, PaymentDialog
from charts import PieWindow

class MasterViewerWidget(QWidget):

    def __init__(self, idx_no, company_name, contact_name, rem_fees, database_filename, ctx):
        super(MasterViewerWidget, self).__init__()
        self.ctx = ctx

        self.company_name = company_name
        self.idx_no = str(idx_no)
        self.database_filename = database_filename
        self.contact_name = contact_name
        self.rem_fees = rem_fees # will convert to string later 

        self.idx_lbl = QLabel(self.idx_no)
        
        self.name_lbl = QLabel("Company: "+self.company_name)
        # lbl_font = self.name_lbl.font()
        # lbl_font.setPointSize(14)
        # self.name_lbl.setFont(lbl_font)

        self.contact_lbl = QLabel("Contact: "+self.contact_name)
        #lbl_font = self.std_lbl.font()
        #lbl_font.setPointSize(10)
        #self.std_lbl.setFont(lbl_font)

        self.rem_fees_lbl = QLabel("Pending Payment: \n"+str(self.rem_fees))
        if self.rem_fees == 0:
            self.rem_fees_lbl.setStyleSheet("QLabel {color: #4ecca3;} ")
        else:
            self.rem_fees_lbl.setStyleSheet("QLabel {color: #ff6363;} ") # #35e3e3
        
        # Adding Quick add ToolButton
        # new_invoice_action = QAction("New Invoice", self)
        # record_payment_action = QAction("New Payment", self)
        # view_active_invoices = QAction("View Active Invoices", self)
        # quick_summ_action = QAction("Quick Summary", self)
        # self.quick_add = QToolButton()
        # self.quick_add.setIcon(QIcon(QPixmap(self.ctx.get_plus_sign)))
        # # self.quick_add.setMenu(menu)
        # self.quick_add.addAction(new_invoice_action)
        # self.quick_add.addAction(record_payment_action)
        # self.quick_add.addAction(view_active_invoices)
        # self.quick_add.addAction(quick_summ_action)
        # self.quick_add.setPopupMode(QToolButton.InstantPopup)
        # self.quick_add.setIconSize(QSize(75, 75))
        # self.quick_add.setStyleSheet('QToolButton{border: 0px solid;} QToolButton::menu-indicator { image: none;}')

        self.btn_view = QPushButton("View")
        self.btn_view.setMinimumHeight(65)
        self.btn_view.setStyleSheet("QPushButton {background-color: #46b5d1; color: black; border-radius: 10px;}")#font-size:25px;}") #bbe1fa
        self.btn_edit = QPushButton("Edit")
        self.btn_edit.setMinimumHeight(65)
        self.btn_edit.setStyleSheet("QPushButton {background-color: #4ecca3; color:black; border-radius: 10px;}")#font-size:25px;}")
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.setMinimumHeight(65)
        self.btn_delete.setStyleSheet("QPushButton {background-color: #ff4866; color: white; border-radius: 10px;}")#font-size:25px;}")
        self.btn_delete.setVisible(False)

        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.idx_lbl)
        self.vbox1.addWidget(self.name_lbl)
        self.vbox1.addWidget(self.contact_lbl)
        self.vbox1.addWidget(self.rem_fees_lbl)
        self.hbox2 = QHBoxLayout()
        # self.hbox2.addWidget(self.quick_add)
        self.hbox2.setSpacing(30) # add stretch to create space
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
        # new_invoice_action.triggered.connect(self.new_invoice)
        # record_payment_action.triggered.connect(self.new_payment)
        # view_active_invoices.triggered.connect(self.view_active_invoices)
        # quick_summ_action.triggered.connect(self.quick_summary)
        
        self.setLayout(self.hbox3)

        #self.update_button_state()

    # def new_invoice (self):
    #     new_invoice_dialog = EditViewPanel(self.idx_no, True, self.database_filename, self.ctx)
    #     new_invoice_dialog.open_invoice_dialog()
    
    # def new_payment(self):
    #     payment = EditViewPanel(self.idx_no, True, self.database_filename, self.ctx)
    #     payment.open_payment_dialog()
    
    # def view_active_invoices(self):
    #     view_active_invoices = EditViewPanel(self.idx_no, True, self.database_filename, self.ctx)
    #     view_active_invoices.show_active_invoices_frm_payment(called_from_payment=False)
        
    # def quick_summary(self):
    #     paid, outstanding = get_company_summary(self.database_filename, self.idx_no)
    #     self.pie_chart = PieWindow(paid, outstanding)
    #     self.pie_chart.setWindowTitle("Quick Summary for "+str(self.company_name))
    #     self.pie_chart.show()
        

    def open_view_window(self):
        self.view_window = EditViewPanel(self.idx_no, False, self.database_filename, self.ctx)
        self.view_window.show()
    
    def open_edit_window(self):
        self.edit_window = EditViewPanel(self.idx_no, True, self.database_filename, self.ctx)
        self.edit_window.show()
    
    def delete_entry(self):
        answer = QMessageBox.question(
            self, None, "Are you sure you want to delete the entry? This can not be undone!", 
            QMessageBox.Ok | QMessageBox.Cancel)
        
        if answer & QMessageBox.Ok:
            data_pkl = read_file(self.database_filename)
            data_pkl.pop(int(self.idx_no))
            write_file(data_pkl, self.database_filename)
            inform_user(self, "Entry Deleted! You may now reload.")

    def show(self):
        """
        Show this widget, and all child widgets.
        """
        for w in [self, self.name_lbl, self.contact_lbl, self.rem_fees_lbl, self.btn_view, self.btn_edit]:
            w.setVisible(True)
        try:
            self.btn_delete.setVisible(True)
        except:
            pass

    def hide(self):
        """
        Hide this widget, and all child widgets.
        """
        for w in [self, self.name_lbl, self.contact_lbl, self.rem_fees_lbl, self.btn_view, self.btn_edit]:
            w.setVisible(False)
        try:
            self.btn_delete.setVisible(False)
        except:
            pass