from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from customwidgets import MasterViewerWidget 
from panels import EntryPanel
from tutorial import Tutorial
import qdarkstyle
from util import read_file, write_file
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
    def get_demo_data(self):
        return self.get_resource('Company_database.json')

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

        self.setWindowTitle("Welcome to BZMAN!")

        # label = QLabel("Welcome to Tuition Manager!\nCreate or Load a File")
        # label.setAlignment(Qt.AlignCenter)
        # label.setPixmap(QPixmap("logo.png"))
        text = "<center>" \
            "<h1></h1>" \
            "&#8291;" \
            "<img src=%r>" \
            "</center>" \
            "<p>BZMAN<br/>"\
            "Version 0.1.Beta</p>"\
            % self.ctx.get_logo#<br/>" \
            # "Copyright &copy; JSS Inc.</p>"
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

        toolbar = QToolBar("My Toolbar")
        toolbar.setIconSize(QSize(30,30))
        self.addToolBar(toolbar)

        new_action = QAction("New", self)
        new_action.setStatusTip("Create a new file")
        new_action.triggered.connect(self.new_file)
        new_action.setShortcut(QKeySequence.New)
        toolbar.addAction(new_action)
        
        toolbar.addSeparator()

        load_action = QAction("Open", self)
        load_action.setStatusTip("Open an existing file")
        load_action.triggered.connect(self.load_file)
        load_action.setShortcut(QKeySequence.Open)
        toolbar.addAction(load_action)

        load_demo = QAction("Open Demo", self)
        load_demo.setStatusTip("Open demo file")
        load_demo.triggered.connect(self.load_demo)

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

        # Tutorial actions
        tu_add_new_entry_acc = QAction("Create or Add New", self)
        tu_add_new_entry_acc.triggered.connect(self.tu_add_new_entry)
        tu_edit_entry_acc = QAction("Edit Entry", self)

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()
        menu.setNativeMenuBar(False) # for mac
        file_menu = menu.addMenu("&File")
        file_menu.addAction(new_action)
        file_menu.addAction(load_action)
        file_menu.addAction(load_demo)

        tutorial = menu.addMenu("Tutorial")
        tutorial.addAction(tu_add_new_entry_acc)
        tutorial.addAction(tu_edit_entry_acc)

        options = menu.addMenu("&Customize")
        theme = options.addMenu("Theme")
        theme.addAction(dark_theme)
        theme.addAction(breeze_dark)
        theme.addAction(breeze_light)
        theme.addAction(blue)
        options.addAction(font)

        self.setGeometry(800,100,1000*self.devicePixelRatio(),1000*self.devicePixelRatio())
        self.centerOnScreen()

    def centerOnScreen (self):
        '''centerOnScreen() Centers the window on the screen.'''
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2)) 
    
    def load_file(self):
        filename = QFileDialog.getOpenFileName(self, "Open", filter="Database Files (*.json)")[0]
        if filename:
            self.main_window = MainWindow(filename, self.ctx)
            # self.main_window = qtmodern.windows.ModernWindow(self.main_window)
            self.main_window.show()
            self.setWindowState(Qt.WindowMinimized)
    
    def new_file(self): # TODO change this to inputdialog
        filename = QFileDialog.getSaveFileName(self, "New - Enter Filename You Want to Use")[0]#, filter="Scan files (*.pkl *.h5 *.txt)")
        if filename:
            self.database_filename = filename+".json"
            new_database = list()
            write_file(new_database, self.database_filename)
            # new_database.to_csv(self.database_filename, index=False)
            self.entry_panel = EntryPanel(self.database_filename, self.ctx)
            self.entry_panel.show()
    
    def load_demo(self):
        self.main_window = MainWindow(self.ctx.get_demo_data, self.ctx)
        self.main_window.show()
        self.setWindowState(Qt.WindowMinimized)
    
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
    
    def tu_add_new_entry(self):
        self.tu = Tutorial()
        ans = self.tu.start_tutorial(parent = self)

        if ans == QMessageBox.Ok:
            print("yes begin tutorial")
            self.new_file()
            self.tu.new_entry(parent=self)


class MainWindow(QMainWindow):

    def __init__(self, database_filename, ctx, *args, **kwargs):
        super().__init__()

        self.database_filename = database_filename
        self.ctx = ctx
        self.widgets = []
        self.widget_names = []

        self.controls = QWidget()  # Controls container widget.
        self.controlsLayout = QGridLayout()   # Controls container layout.

        self.load_widgets()
        self.controls.setLayout(self.controlsLayout)

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
        self.reload_btn.setStyleSheet("QPushButton {background-color:#acdbdf; color:black;}")
        self.reload_btn.clicked.connect(self.reload_func)

        # Adding "Add" Button
        self.add_new_btn = QPushButton("Create New")
        self.add_new_btn.setStyleSheet("QPushButton {background-color: #927fbf;color:black}")#7045af
        self.add_new_btn.clicked.connect(self.add_new_entry)

        # Add Checkbox to toggle delete 
        self.delete_checkbox = QCheckBox("Enable Delete")
        self.delete_checkbox.setStyleSheet("QCheckbox {color: red}")# #ff6363; #Not able to set this color!
        self.delete_checkbox.setChecked(False)
        self.delete_checkbox.stateChanged.connect(self.check_delete_state)

        btn_container = QWidget()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.add_new_btn)
        hbox1.addWidget(self.reload_btn)
        hbox1.addWidget(self.delete_checkbox)
        btn_container.setLayout(hbox1)

        # Add the items to VBoxLayout (applied to container widget) 
        # which encompasses the whole window.
        container = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(btn_container)
        containerLayout.addWidget(self.searchbar)
        containerLayout.addWidget(self.scroll)

        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        self.setGeometry(800, 100, 1500*self.devicePixelRatio(), 1500*self.devicePixelRatio())
        self.setWindowTitle('BZMAN')
        self.centerOnScreen()

    def centerOnScreen (self):
        '''centerOnScreen() Centers the window on the screen.'''
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2)) 
    
    def load(self):
        #data_pkl = pd.ExcelFile(self.database_filename)
        #data_pkl = data_pkl.parse("Sheet1")
        data_pkl = read_file(self.database_filename)
        company_names = []
        contact_names = []
        outstanding = []
        for i in range(len(data_pkl)):
            company_names.append(data_pkl[i]["Company Name"])
            contact_names.append(data_pkl[i]["Contact Name"])
            outstanding.append(data_pkl[i]["Outstanding"])
        return company_names, contact_names, outstanding
    
    def load_widgets(self):
        company_names,contact_names,outstanding = self.load()
        self.widget_names = functools.reduce(operator.iconcat, [company_names, contact_names, str(outstanding)], [])
        self.widgets = []
        idx_numbers = list(range(0,len(company_names)))

        for idx_no, company_name, contact_name, rem_bal in list(zip(idx_numbers, company_names, contact_names, outstanding)):
            # TODO Load Widgets on a different thread
            item = MasterViewerWidget(idx_no, company_name, contact_name, rem_bal, database_filename=self.database_filename, ctx=self.ctx)#in the future, can reduce redundancy by only passing ctx and creating a function in Appctxt that reads database filename
            self.controlsLayout.addWidget(item)
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
            font = QFont("Verdana") # "Avenir" "Helvetica" "Proxima Nova" "Playfair Display" "Roboto" "Open Sans" "Montserrat" "SansSerif"
        # font.setStyleHint(QFont.Calibri)
        except:
            font = QFont("Open Sans")
        else:
            font = QFont("Arial")
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