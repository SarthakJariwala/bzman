from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property
import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from customwidgets import MasterViewerWidget 
from panels import EntryPanel, EditViewPanel
import qdarkstyle
from util import read_file, write_file, ask_user, inform_user, get_company_summary
from charts import DrawPieChart, PieWindow
import breeze_resources
import functools
import operator
import cProfile

class AppContext(ApplicationContext):
    def run(self):
        window = WelcomeWindow(ctx=self)
        version = self.build_settings['version'] 
        window.setWindowTitle("BZMAN v" + version)
        # window.resize(250, 150) 
        window.show()
        return self.app.exec_()

    @cached_property
    def get_logo(self):
        return self.get_resource('logo.png')
    
    @cached_property
    def get_plus_sign(self):
        return self.get_resource("plus-button.png")

    @cached_property
    def get_settings_file(self):
        return self.get_resource("BZMAN_settings.json")
    
    @cached_property
    def get_demo_data(self):
        return self.get_resource('Demo Company_BZMAN_DATABASE.json')

    @cached_property
    def get_breeze_dark(self):
        return self.get_resource("dark.qss")
    
    @cached_property
    def get_breeze_light(self):
        return self.get_resource("light.qss")

    def dark_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
        return palette

# Welcome Window here -
# options to load the file and then will pass the file data to MainWindow
class WelcomeWindow(QMainWindow):
    
    def __init__(self, ctx, *args, **kwargs):
        super().__init__()
        self.ctx = ctx
        self.check_trial_validity()

        self.setWindowTitle("Welcome to BZMAN!")

        text = "<center>" \
            "<br><br><h1></h1>" \
            "&#8291;" \
            "<img src=%r>" \
            "</center>" \
            "<p>BZMAN<br/>"\
            "Version 0.2.Beta</p>"\
            % self.ctx.get_logo#<br/>" \
            # "Copyright &copy; JSS Inc.</p>"
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)

        hbox = QHBoxLayout()
        btn_new = QPushButton("   New   ")
        btn_new.setMaximumSize(300,100)
        # btn_new.setStyleSheet("QPushButton {border-radius: 20px;}")
        btn_new.clicked.connect(self.new_file)
        hbox.addWidget(btn_new)
        btn_open = QPushButton("   Open   ")
        btn_open.setMaximumSize(300,100)
        # btn_open.setStyleSheet("QPushButton {border-radius: 20px;}")
        btn_open.clicked.connect(self.load_file)
        hbox.addWidget(btn_open)
        hbox_widget = QWidget()
        hbox_widget.setLayout(hbox)
        
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.addWidget(label)
        container_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding))
        container_layout.addWidget(hbox_widget)
        container.setLayout(container_layout)
        self.setCentralWidget(container)

        # toolbar = QToolBar("My Toolbar")
        # toolbar.setIconSize(QSize(30,30))
        # self.addToolBar(toolbar)

        new_action = QAction("New", self)
        new_action.setStatusTip("Create a new file")
        new_action.triggered.connect(self.new_file)
        new_action.setShortcut(QKeySequence.New)
        # toolbar.addAction(new_action)
        
        # toolbar.addSeparator()

        load_action = QAction("Open", self)
        load_action.setStatusTip("Open an existing file")
        load_action.triggered.connect(self.load_file)
        load_action.setShortcut(QKeySequence.Open)
        # toolbar.addAction(load_action)

        load_demo = QAction("Open Demo", self)
        load_demo.setStatusTip("Open demo file")
        load_demo.triggered.connect(self.load_demo)

        set_new_file_path = QAction("Set New Path", self)
        set_new_file_path.setStatusTip("Sets a new path for an existing file")
        set_new_file_path.triggered.connect(self.set_new_file_location)

        dark_theme = QAction("Dark", self)
        dark_theme.triggered.connect(self.change_theme)
        breeze_dark = QAction("Breeze Dark", self)
        breeze_dark.triggered.connect(self.change_dark_breeze_theme)
        breeze_light = QAction("Light", self)
        breeze_light.triggered.connect(self.change_light_theme)
        blue = QAction("Blue", self)
        blue.triggered.connect(self.change_blue_theme)

        font = QAction("Fonts", self)
        font.triggered.connect(self.font_choice)

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()
        menu_font_size = menu.font()
        menu_font_size.setPointSize(10)
        menu.setFont(menu_font_size)
        menu.setNativeMenuBar(False) # for mac
        file_menu = menu.addMenu("&File")
        file_menu.setFont(menu_font_size)
        file_menu.addAction(new_action)
        file_menu.addAction(load_action)
        file_menu.addAction(load_demo)
        file_menu.addAction(set_new_file_path)

        options = menu.addMenu("&Customize")
        options.setFont(menu_font_size)
        theme = options.addMenu("Theme")
        theme.setFont(menu_font_size)
        theme.addAction(dark_theme)
        theme.addAction(breeze_dark)
        theme.addAction(breeze_light)
        theme.addAction(blue)
        options.addAction(font)

        # self.setGeometry(800,100,2000*self.devicePixelRatio(),1000*self.devicePixelRatio())
        self.setWindowState(Qt.WindowMaximized)
        self.centerOnScreen()

        self.BZMAN_settings = read_file(self.ctx.get_settings_file)
        if self.BZMAN_settings['path'] != "":
            self.load_file()
        else:
            self.show()
            inform_user(
                self, "Welcom to BZMAN! \n\n"+ 
                "Click on the 'New' button to begin.")

    def centerOnScreen (self):
        '''centerOnScreen() Centers the window on the screen.'''
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
    
    def check_trial_validity(self):
        self.BZMAN_settings = read_file(self.ctx.get_settings_file)
        trial_start = self.BZMAN_settings["trial_start"]
        
        if trial_start == "":
            trial_start = datetime.strftime(datetime.today(),"%Y-%m-%d")
            self.BZMAN_settings["trial_start"] = trial_start
            write_file(self.BZMAN_settings, self.ctx.get_settings_file)
        
        else:
            if (datetime.today() - datetime.strptime(trial_start, "%Y-%m-%d")).days > 14:
                inform_user(self, "Your trial period has expired.\n\nThank you for using trial version of BZMAN. You can purchase the full software online.")
                sys.exit()
            else:
                pass
    
    def load_file(self):
    
        self.BZMAN_settings = read_file(self.ctx.get_settings_file)

        if self.BZMAN_settings['path'] == "":
            inform_user(self, "There is no database location specified.\n\n"+ "If you haven't created a database, create a new database using 'New'\n\n"+
            "If you have recently moved the file to a new location, use the 'Set New Path' option in File menu to set the new file location"
            )
        
        else:
            # x = [os.path.abspath(f) for f in os.listdir(self.BZMAN_settings['path']) if os.path.isfile(f)]
            x = os.listdir(self.BZMAN_settings['path'])
            temp_list =[]
            filename = None
            for i in range(len(x)):
                if x[i].find("_BZMAN_DATABASE.json") != -1:
                    temp_list.append(x[i])
            
            if len(temp_list) >1:
                inform_user(self, "There are more than one database files. Please select the one you want to open")
                filename = QFileDialog.getOpenFileName(self, "Open", self.BZMAN_settings['path'], filter="Database Files (*.json)")[0]

            elif len(temp_list) == 0:
                ans = ask_user(self, "No Company Database found! \n\n" + "If you haven't created a company database yet, you can do it using 'New' option. Click 'Ok' to create a new database.\n\n"+
                "If you have already created a Database but moved it to a differenct location, please open it manually by clicking 'Cancel'.")
                if ans == QMessageBox.Ok:
                    self.new_file()
                elif ans == QMessageBox.Cancel:
                    filename = QFileDialog.getOpenFileName(self, "Open", self.BZMAN_settings['path'], filter="Database Files (*.json)")[0]
                    if filename:
                        ans = ask_user(self, "Do you want to save this file location for future use? This will overwrite your existing path where the file wasn't found.")

                        if ans == QMessageBox.Ok:
                            new_path, new_filename = os.path.split(filename)
                            new_company_name = " ".join(os.path.split(os.path.splitext(filename)[0])[1].split('_')[:-2])
                            self.BZMAN_settings['path'] = new_path
                            self.BZMAN_settings['database_name'] = new_filename
                            self.BZMAN_settings['company'] = new_company_name
                            write_file(self.BZMAN_settings, self.ctx.get_settings_file)

                else: #4194304
                    pass

            else:
                filename = os.path.join(self.BZMAN_settings['path'] + '/' + temp_list[0])

            if filename:
                self._open_main_window(filename)
    
    def _open_main_window(self, filename):
        self.main_window = MainWindow(filename, self.ctx)
        self.main_window.show()
        self.setWindowState(Qt.WindowMinimized)
    
    def new_file(self, called_from_tutorial = False):

        self.BZMAN_settings = read_file(self.ctx.get_settings_file)

        if self.BZMAN_settings["path"] == "":

            inform_user(
                self, "Welcom to BZMAN! \n\n"+ 
                "Please select a folder to save your company database.")

            self.folder_path = QFileDialog.getExistingDirectory(self, 'Select a folder to save your database')
            
            if self.folder_path:
                
                self.BZMAN_settings["path"] = self.folder_path
                self._new_file_logic()
            
            else:
                inform_user(self, "No folder location selected.")
        
        else:
            ans = ask_user(
                self, 
                "Company database already exists.\n\n"+
                "Do you still want to create a new database?\n\n"
            )

            if ans == QMessageBox.Ok:
                self.BZMAN_settings["path"] = ""
                write_file(self.BZMAN_settings, self.ctx.get_settings_file)

                inform_user(
                    self,
                    "Your old database will now need to be manually opened using 'Open'\n\n"+
                    "You may now create a new database"
                )
                self.new_file()
    
    def _new_file_logic(self):
        dlg =  QInputDialog(self)                 
        dlg.setInputMode(QInputDialog.TextInput) 
        dlg.setWindowTitle('New Database : Enter Your Company Name')
        dlg.setLabelText('Company Name')                        
        dlg.resize(800,100)                             
        ok = dlg.exec_()                                
        filename = dlg.textValue()

        if ok and filename:
            
            self.BZMAN_settings['company'] = filename
            self.BZMAN_settings['database_name'] = filename + "_BZMAN_DATABASE.json"
            
            filename = os.path.join(self.folder_path + "/" + filename)
            self.database_filename = filename+"_BZMAN_DATABASE.json"
            
            new_database = list()
            write_file(new_database, self.database_filename)
            write_file(self.BZMAN_settings, self.ctx.get_settings_file)
            
            ans = inform_user(self, "Great! Company database created!\n\n"+
            "Click 'Ok' to open it.")
            
            if ans == QMessageBox.Ok:
                
                self.load_file()
                ans = ask_user(self, "There are no entries in your company database.\n\n"+
                "You can now add a new customer by clicking on 'Create New Customer' option in the top left or by clicking 'Ok'.\n")
                
                if ans == QMessageBox.Ok:
                    self.entry_panel = EntryPanel(self.database_filename, self.ctx)
                    self.entry_panel.show() #move this after opening file
        
        elif ok and not filename:
            inform_user(self, "Company name was left blank. \nEnter a valid name.")
            self._new_file_logic()
        
        else:
            self.BZMAN_settings["path"] = ""
            write_file(self.BZMAN_settings, self.ctx.get_settings_file)
    
    def load_demo(self):
        self.main_window = MainWindow(self.ctx.get_demo_data, self.ctx)
        self.main_window.show()
        self.main_window.setWindowTitle("BZMAN : Demo Company Database")
        self.setWindowState(Qt.WindowMinimized)
    
    def set_new_file_location(self):
        ans = ask_user(self, "This will let 'B Z M A N' set a new path to your exisiting company database. "+
        "This means you will be able to open files that you have moved to a new location after saving them.\n\n"+ 
        "If you want to continue, click 'Ok'. If you want to exit, click 'Cancel'.")
        
        if ans == QMessageBox.Ok:
            filename = QFileDialog.getOpenFileName(self, "Open", self.BZMAN_settings['path'], filter="Database Files (*.json)")[0]
            if filename:
                new_path, new_filename = os.path.split(filename)
                new_company_name = ",".join(os.path.split(os.path.splitext(filename)[0])[1].split('_')[:-2])
                self.BZMAN_settings['path'] = new_path
                self.BZMAN_settings['database_name'] = new_filename
                self.BZMAN_settings['company'] = new_company_name
                write_file(self.BZMAN_settings, self.ctx.get_settings_file)
                inform_user(self, "New path to the company database has been set. You can now open the database using 'Open'")

            else:
                inform_user(self, "Select a valid database file")
    def change_theme(self):
        self.ctx.app.setPalette(self.ctx.dark_palette())
        self.ctx.app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
    
    def change_light_theme(self):
        file = QFile(self.ctx.get_breeze_light)
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        self.ctx.app.setStyleSheet(stream.readAll())
    
    def change_dark_breeze_theme(self):
        file = QFile(self.ctx.get_breeze_dark)
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        self.ctx.app.setStyleSheet(stream.readAll())
    
    def change_blue_theme(self):
        self.ctx.app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    
    def font_choice(self):
        font, valid = QFontDialog.getFont()
        if valid:
            self.ctx.app.setFont(font)


class MainWindow(QMainWindow): #TODO add file menu with different options here too

    def __init__(self, database_filename, ctx, *args, **kwargs):
        super().__init__()

        self.database_filename = database_filename
        self.ctx = ctx
        self.widgets = []
        self.widget_names = []

        self.pie_view = QWidget()
        self.pie_view_layout = QGridLayout()
        self.controls = QWidget()  # Controls container widget.
        self.controlsLayout = QGridLayout()   # Controls container layout.

        self.load_widgets()
        self.controls.setLayout(self.controlsLayout)
        self.pie_view.setLayout(self.pie_view_layout)

        self.load_scroll_area()

        # Search bar.
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search")
        self.searchbar.textChanged.connect(self.update_display)

        # Adding Completer.
        self.completer = QCompleter(self.widget_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchbar.setCompleter(self.completer)

        # Adding Reload button
        self.reload_btn = QPushButton("Reload")
        self.reload_btn.setShortcut(QKeySequence.Refresh)
        self.reload_btn.setFixedSize(250,65)
        self.reload_btn.setStyleSheet("QPushButton {background-color:#acdbdf; color:black; border-radius: 20px;}")
        self.reload_btn.clicked.connect(self.reload_func)

        # Adding "Add" Button ----> added as a quick action
        # self.add_new_btn = QPushButton("Create New Customer")
        # self.add_new_btn.setFixedSize(450,65)
        # self.add_new_btn.setStyleSheet("QPushButton {background-color: #927fbf;color:black; border-radius: 10px;}")#7045af
        # self.add_new_btn.clicked.connect(self.add_new_entry)

        # Add Checkbox to toggle delete 
        self.delete_checkbox = QCheckBox("Enable Delete")
        self.delete_checkbox.setStyleSheet("QCheckbox {color: red}")# #ff6363; #Not able to set this color!
        self.delete_checkbox.setChecked(False)
        self.delete_checkbox.stateChanged.connect(self.check_delete_state)

        # Adding Quick add ToolButton
        add_new_customer = QAction("New Customer", self)
        new_invoice_action = QAction("New Invoice", self)
        record_payment_action = QAction("New Payment", self)
        view_active_invoices = QAction("View Active Invoices", self)
        quick_summ_action = QAction("Quick Company Summary", self)
        self.quick_add = QToolButton()
        self.quick_add.setIcon(QIcon(QPixmap(self.ctx.get_plus_sign)))
        self.quick_add.addAction(add_new_customer)
        self.quick_add.addAction(new_invoice_action)
        self.quick_add.addAction(record_payment_action)
        self.quick_add.addAction(view_active_invoices)
        self.quick_add.addAction(quick_summ_action)
        self.quick_add.setPopupMode(QToolButton.InstantPopup)
        self.quick_add.setIconSize(QSize(75, 75))
        self.quick_add.setStyleSheet('QToolButton{border: 0px solid;} QToolButton::menu-indicator { image: none;}')
        add_new_customer.triggered.connect(self.add_new_entry)
        new_invoice_action.triggered.connect(self.new_invoice)
        record_payment_action.triggered.connect(self.new_payment)
        view_active_invoices.triggered.connect(self.view_active_invoices)
        quick_summ_action.triggered.connect(self.quick_summary)

        btn_container = QWidget()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.quick_add)
        hbox1.addItem(QSpacerItem(35, 35, QSizePolicy.Fixed))
        hbox1.addWidget(self.searchbar)
        # hbox1.addWidget(self.add_new_btn)
        hbox1.addItem(QSpacerItem(35, 35, QSizePolicy.Fixed))
        hbox1.addWidget(self.reload_btn)
        hbox1.addItem(QSpacerItem(35, 35, QSizePolicy.Fixed))
        hbox1.addWidget(self.delete_checkbox)
        hbox1.setAlignment(Qt.AlignLeft)
        btn_container.setLayout(hbox1)

        pie_w_control = QWidget()
        pie_w_control_layout = QHBoxLayout()
        pie_w_control_layout.addWidget(self.pie_view)
        pie_w_control_layout.addWidget(self.scroll)
        pie_w_control.setLayout(pie_w_control_layout)
        # Add the items to VBoxLayout (applied to container widget) 
        # which encompasses the whole window.
        container = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(btn_container)
        # containerLayout.addWidget(self.searchbar)
        # containerLayout.addWidget(self.overall_view_widget)
        # containerLayout.addWidget(self.scroll)
        containerLayout.addWidget(pie_w_control)

        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        # self.setGeometry(800, 100, 1500*self.devicePixelRatio(), 1500*self.devicePixelRatio())
        self.setWindowState(Qt.WindowMaximized)
        company_name = read_file(self.ctx.get_settings_file)['company']
        self.setWindowTitle('BZMAN : ' + str(company_name) + " Database")
        self.centerOnScreen()

    def centerOnScreen (self):
        '''centerOnScreen() Centers the window on the screen.'''
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2)) 
    
    def load(self):
        data_pkl = read_file(self.database_filename)
        company_names = []
        contact_names = []
        outstanding = []
        paid = []
        for i in range(len(data_pkl)):
            company_names.append(data_pkl[i]["Company Name"])
            contact_names.append(data_pkl[i]["Contact Name"])
            outstanding.append(data_pkl[i]["Outstanding"])
            paid.append(data_pkl[i]["Total Paid"])
        
        total_outstanding = sum(outstanding)
        total_paid = sum(paid)
        self._company_list_for_quick_actions = company_names
        return company_names, contact_names, outstanding, total_outstanding, total_paid
    
    def load_widgets(self):
        company_names,contact_names,outstanding, total_outstanding, total_paid = self.load()
        self.widget_names = functools.reduce(operator.iconcat, [company_names, contact_names, str(outstanding)], [])
        self.widgets = []
        idx_numbers = list(range(0,len(company_names)))

        piechart = DrawPieChart(total_paid,total_outstanding)
        self.pie_view_layout.addWidget(piechart.draw_pie_chart(), 0,0, 5, 1)

        for idx_no, company_name, contact_name, rem_bal in list(zip(idx_numbers, company_names, contact_names, outstanding)):
            # TODO Load Widgets on a different thread
            item = MasterViewerWidget(idx_no, company_name, contact_name, rem_bal, database_filename=self.database_filename, ctx=self.ctx)#in the future, can reduce redundancy by only passing ctx and creating a function in Appctxt that reads database filename
            self.controlsLayout.addWidget(item, idx_no, 1, 1,2)
            self.widgets.append(item)
        
        spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.controlsLayout.addItem(spacer)
    
    def load_scroll_area(self):
        # Scroll Area Properties.
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.controls)

    def update_display(self, text):
        try:
            for widget in self.widgets:
                if text.lower() in widget.company_name.lower():
                    widget.show()
                elif text.lower() in widget.contact_name.lower():
                    widget.show()
                else:
                    widget.hide()
                self.check_delete_state()
        except:
            pass
    
    def add_new_entry(self):
        self.add_panel = EntryPanel(self.database_filename, self.ctx)
        self.add_panel.show()
        
    def reload_func(self):
        self.clearLayout(self.controlsLayout)
        self.load_widgets()
        self.check_delete_state()
    
    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def check_delete_state(self):
        if self.delete_checkbox.isChecked():
            for i in range(len(self.widgets)):
                self.widgets[i].btn_delete.setVisible(True)
        else:
            for i in range(len(self.widgets)):
                self.widgets[i].btn_delete.setVisible(False)
    
    def enter_company_name(self):
        dlg =  QInputDialog(self)                 
        dlg.setInputMode(QInputDialog.TextInput) 
        dlg.setWindowTitle('Enter Company Name')
        dlg.setLabelText('Company Name')    
        line_edit = dlg.findChild(QLineEdit) # search Qlineedit child to set QCompleter 
        completer = QCompleter(self._company_list_for_quick_actions, line_edit)
        completer.setCaseSensitivity(Qt.CaseInsensitive)       
        line_edit.setCompleter(completer)           
        dlg.resize(800,100)                             
        ok = dlg.exec_()                                
        company_name = dlg.textValue()

        if ok and company_name:
            if company_name in self._company_list_for_quick_actions:
                return self._company_list_for_quick_actions.index(company_name)

            elif not company_name in self._company_list_for_quick_actions:
                inform_user(self, "This company name does not exist in database.\n\nIf this is a new customer, please use the 'Create New Customer' option.")

        elif ok and not company_name:
            inform_user(self, "Please enter a valid company name")

    def new_invoice (self):
        idx = self.enter_company_name()
        if isinstance(idx, int):
            new_invoice_dialog = EditViewPanel(idx, True, self.database_filename, self.ctx)
            new_invoice_dialog.open_invoice_dialog()
    
    def new_payment(self):
        idx = self.enter_company_name()
        if isinstance(idx, int):
            payment = EditViewPanel(idx, True, self.database_filename, self.ctx)
            payment.open_payment_dialog()
    
    def view_active_invoices(self):
        idx = self.enter_company_name()
        if isinstance(idx, int):
            view_active_invoices = EditViewPanel(idx, True, self.database_filename, self.ctx)
            view_active_invoices.show_active_invoices_frm_payment()
        
    def quick_summary(self):
        idx = self.enter_company_name()
        if isinstance(idx, int):
            paid, outstanding = get_company_summary(self.database_filename, idx)
            self.pie_chart = PieWindow(paid, outstanding)
            self.pie_chart.setWindowTitle("Quick Account Summary")
            self.pie_chart.show()

    #def run():
    #    app = QApplication(sys.argv)
    #    w = MainWindow()
    #    w.show()
    #   sys.exit(app.exec_())

def run():
        from time import time
        start_time = time()
        appctxt = AppContext()       # 1. Instantiate ApplicationContext
        # app = QApplication(sys.argv)
        # change font style globally
        try:
            font = QFont("Calibri") # "Verdana" "Avenir" "Helvetica" "Proxima Nova" "Playfair Display" "Roboto" "Open Sans" "Montserrat" "SansSerif"
        # font.setStyleHint(QFont.Calibri)
        except:
            try:
                font = QFont("Open Sans")
            except:
                font = QFont("Arial")
        finally:
            font.setPointSize(14)
        appctxt.app.setFont(font)
        appctxt.app.setStyle("Fusion")
        # appctxt.app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        appctxt.app.setPalette(appctxt.dark_palette())
        appctxt.app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
        # w = WelcomeWindow()
        # w.show()
        print("starting app took :" + str(time()-start_time))
        exit_code = appctxt.run()      # 2. Invoke appctxt.app.exec_()
        sys.exit(exit_code)

run()
# For debugging uncomment below
# cProfile.run("run()", sort="cumtime")