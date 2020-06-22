from PyQt5.QtWidgets import * #QMainWindow, QApplication, QWidget, QGridLayout, QGraphicsWidget
from PyQt5.QtChart import *# QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtCore import *#Qt
from PyQt5.QtGui import *#QPainter, QPen
import sys

class PieWindow(QMainWindow):

    def __init__(self, paid, outstanding):
        self.paid = paid
        self.outstanding = outstanding
        super().__init__()

        # self.setWindowTitle('BZMAN Quick Summary')

        piechart = DrawPieChart(self.paid, self.outstanding)

        pie_widget = QWidget()
        grid_layout = QGridLayout()
        grid_layout.addWidget(piechart.draw_pie_chart(), 0,0, 5,1)
        pie_widget.setLayout(grid_layout)

        self.setCentralWidget(pie_widget)
        self.setGeometry(800, 100, 1000*self.devicePixelRatio(),1000*self.devicePixelRatio())
        # self.show()

class DrawPieChart(QGraphicsWidget):
    def __init__(self, paid, outstanding):
        self.paid = paid # float or int
        self.outstanding = outstanding # float or int
        super().__init__()

    def draw_pie_chart(self):

        series = QPieSeries()
        series.append("  Paid: " + str(self.paid)+" ", self.paid)
        series.append("  Outstanding: " + str(self.outstanding)+" ", self.outstanding)

        font = QFont()
        font.setPointSize(14)
        font.bold()
        # font.setStyleHint(QFont.Courier)

        slice = QPieSlice()
        slice = series.slices()
        slice[0].setExploded(True)
        slice[0].setLabelVisible(True)
        # slice.setPen(QPen(QColor("#ff4866"), 2))
        slice[0].setBrush(QColor("#4ecca3"))
        slice[0].setLabelBrush(QColor("#4ecca3")) # "#4ecca3"
        slice[0].setLabelFont(font)
        # slice[0].setLabelPosition(slice[0].LabelInsideHorizontal)

        # slice[1].setExploded(True)
        slice[1].setLabelVisible(True)
        slice[1].setBrush(QColor("#FBB040"))
        slice[1].setLabelBrush(QColor("#FBB040")) # "#ff4866" "#d95555"
        slice[1].setLabelFont(font)
        # slice[1].setLabelPosition(slice[1].LabelInsideHorizontal)

        chart = QChart()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Overview - Total Business : "+ str(self.paid + self.outstanding))
        font.setPointSize(18)
        chart.setTitleFont(font)
        chart.legend().setVisible(True)
        chart.legend().setLabelBrush(QBrush(QColor("#ffffff"))) # 927fbf
        chart.legend().setAlignment(Qt.AlignBottom)
        font.setPointSize(16)
        chart.legend().setFont(font)
        chart.setMargins(QMargins(0,0,0,0))
        chart.setBackgroundVisible(False)
        chart.setTitleBrush(QBrush(QColor("#ffffff")))

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        return chartview

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PieWindow(3000,7000)
    sys.exit(app.exec_())
