import sys
# from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QFormLayout,\
#     QMainWindow,QStyleFactory,QGridLayout,QComboBox,QLineEdit,QLabel,QFileDialog
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as \
    NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from src.plotting import Graph


class CustomToolbar(NavigationToolbar):
    """
    This block alloaws to add/remove items from the matplotlib toolbar
    """
    toolitems = [t for t in NavigationToolbar.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save','Back','Forward',
                          'Subplots')]

class PlotWindow(QWidget):
    """
    Main app
    """
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)
        #print the styles available for PyQt
        print(QStyleFactory.keys())


        #define application parameters
        self.setGeometry(10, 10, 1100, 500)

        self.setWindowTitle("Happy Plotter and the pyplot stone")
        # #change PyQt palette color
        # p = self.palette()
        # p.setColor(self.backgroundRole(), Qt.darkRed)
        # self.setPalette(p)
        # self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))

        p = self.palette()
        p.setColor(self.backgroundRole(),Qt.darkGray)
        self.setPalette(p)
        self.setStyleSheet("font: 20pt Palatino")

        # Set default matplotlib style
        Style = 'ggplot'

        self.name = None

        fig_var = ['style', 'Plots', 'title', 'xlabel', 'ylabel',
                   'Xmin',
                   'Xmax',
                   'Ymin', 'Ymax']
        self.data = dict.fromkeys(fig_var)
        self.data['style'] = Style

        self.data['Plots'] = {}

        # set the layout
        self.layout = QGridLayout()
        self.gen_right_panel()
        self.gen_left_panel()
        self.layout.addItem(self.right_panel, 0, 1)
        self.layout.addItem(self.left_panel, 0, 0)
        self.setLayout(self.layout)
        self.i = 2
        #self.toolbar =None
        # self.canvas =None



    def gen_right_panel(self):
        # Initialize tab screen
        self.right_panel=QVBoxLayout()

        self.tabs = QTabWidget()
        self.main_tab = QWidget()
        self.tab2 = QWidget()
        # self.tabs.resize(200, 300)

        # Add tabs
        self.tabs.addTab(self.main_tab, "Main")
        self.tabs.addTab(self.tab2, "Axes")

        # Create first tab
        self.tab2.layout = QFormLayout()
        self.axes_widgets()
        self.tab2.layout.setHorizontalSpacing(100)
        self.tab2.layout.setVerticalSpacing(10)
        self.tab2.setLayout(self.tab2.layout)

        self.widgets()

        self.gen_main_tab()

        self.buttons = QWidget()
        self.buttons.layout = QHBoxLayout()
        self.buttons.layout.addWidget(self.OpenFile)
        self.buttons.layout.addWidget(self.Apply)
        self.buttons.setLayout(self.buttons.layout)



        # Overall layout
        self.right_panel.addWidget(self.tabs)
        self.right_panel.addWidget(self.buttons)

        """
        Generate all widgets wanted for the right panel of the app main window
        :return:
        """

        #set the right side of the app containing all the buttons


    def gen_main_tab(self):
        self.main_tab.layout = QFormLayout()
        # self.widgets()
        self.main_tab.layout.addRow(self.TitleLabel, self.Title)
        self.main_tab.layout.addRow(QLabel(''))
        self.main_tab.layout.addRow(self.XLabel, self.Xlab)
        self.main_tab.layout.addRow(QLabel(''))
        self.main_tab.layout.addRow(self.YLabel, self.Ylab)
        self.main_tab.layout.addRow(QLabel(''))
        self.main_tab.layout.addRow(self.StyleLabel, self.Drop_style_menu)
        # self.main_tab.layout.addWidget(self.Apply,4,1)
        # self.main_tab.layout.addWidget(self.Open,4,0)
        # self.main_tab.layout.addWidget(self.OpenFile,5,1)
        # self.main_tab.addWidget(self.button3,2,0)
        self.main_tab.setLayout(self.main_tab.layout)

    def axes_widgets(self):
        # BUTTONS
        # form_name_list=['Xmin','Xmax','Ymin','Ymax']
        #
        # for i in form_name_list:
        #     setattr(self,i+'Label',QLabel(i))
        #     setattr(self,i,QLineEdit())
        #     # getattr(self,i+'Label').setMinimumWidth(500)
        #     self.tab2.layout.addRow(i,QLineEdit())
        #     # self.tab2.layout.addRow(QLabel(''))
        #     # print(getattr(self,i))
        self.LimitsTitle= QLabel('Limits')
        self.LimitsTitle.setStyleSheet('font : 30pt')
        self.tab2.layout.addRow(self.LimitsTitle)
        # Xlimits
        self.LimX = QWidget()
        self.LimX.layout = QHBoxLayout()
        self.Xmin = QLineEdit(self.data['Xmin'])
        self.XminLabel = QLabel('Xmin')
        self.XmaxLabel = QLabel('Xmax')
        self.Xmax = QLineEdit(self.data['Xmax'])
        self.LimX.layout.addWidget(self.XminLabel)
        self.LimX.layout.addWidget(self.Xmin)
        self.LimX.layout.addWidget(self.XmaxLabel)
        self.LimX.layout.addWidget(self.Xmax)
        self.LimX.setLayout(self.LimX.layout)
        self.tab2.layout.addRow(self.LimX)

        # Ylimits
        self.LimY = QWidget()
        self.LimY.layout = QHBoxLayout()
        self.Ymin = QLineEdit()
        self.YminLabel = QLabel('Ymin')
        self.YmaxLabel = QLabel('Ymax')
        self.Ymax = QLineEdit()
        self.LimY.layout.addWidget(self.YminLabel)
        self.LimY.layout.addWidget(self.Ymin)
        self.LimY.layout.addWidget(self.YmaxLabel)
        self.LimY.layout.addWidget(self.Ymax)
        self.LimY.setLayout(self.LimY.layout)
        self.tab2.layout.addRow(self.LimY)

        self.ScaleTitle = QLabel('Scales')
        self.ScaleTitle.setStyleSheet('font : 30pt')
        self.tab2.layout.addRow(self.ScaleTitle)

        #log check buttons
        self.checks = QWidget()
        self.checks.layout = QHBoxLayout()
        self.Xlog = QCheckBox()
        self.XlogLabel = QLabel('X log scale')
        self.YlogLabel = QLabel('Y log scale')
        self.Ylog = QCheckBox()
        self.checks.layout.addWidget(self.XlogLabel)
        self.checks.layout.addWidget(self.Xlog)
        self.checks.layout.addWidget(self.YlogLabel)
        self.checks.layout.addWidget(self.Ylog)
        self.checks.setLayout(self.checks.layout)
        self.tab2.layout.addRow(self.checks)

        self.legendTitle = QLabel('Legend')
        self.legendTitle.setStyleSheet('font : 30pt')
        self.tab2.layout.addRow(self.legendTitle)


        lengendloclist= ['None','best','upper right','upper left','lower left',
                         'lower right','right','left','center left','center right',
                         'lower center','upper center','center']

        self.legend_loc_menu = QComboBox()
        for i in lengendloclist:
            self.legend_loc_menu.addItem(i)
            self.legend_loc_menu.insertSeparator(4)
        self.tab2.layout.addRow(self.legend_loc_menu)





    def widgets(self):
        """
        This blockcontains all widgets of the app
        """
        #BUTTONS
        self.button1 = QPushButton('Plot')
        self.button1.clicked.connect(lambda : self.plot(name = self.name))

        self.Apply = QPushButton('Apply')
        self.Apply.clicked.connect(self.refresh)

        self.Open = QPushButton('More Params')
        self.Open.clicked.connect(self.Open_param)
        self.paramwin = ParamWindow(self)

        self.OpenFile = QPushButton('Open File')
        self.OpenFile.clicked.connect(self.getfile)
        # self.button3 = QPushButton('ggplot')
        # self.button3.clicked.connect(lambda: self.bckgrd('ggplot'))

        #LABEL and LINE EDIT
        self.TitleLabel = QLabel('Title')
        self.TitleLabel.setStyleSheet('color : black')
        self.Title = QLineEdit()
        self.Title.setMinimumWidth(200)

        self.StyleLabel = QLabel('Style')
        self.StyleLabel.setStyleSheet('color : black')

        self.XLabel = QLabel('X Label')
        self.XLabel.setStyleSheet('color : black')
        self.Xlab = QLineEdit()
        self.YLabel = QLabel('Y Label')
        self.YLabel.setStyleSheet('color : black')
        self.Ylab = QLineEdit()

        #Matplotlib Figure and Toolbar
        self.figure = plt.figure(figsize=(200,200))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = CustomToolbar(self.canvas, self)
        self.toolbar




        #COMBO BOX
        self.Drop_style_menu = QComboBox()
        for i in plt.style.available:
            self.Drop_style_menu.addItem(i)
        self.Drop_style_menu.insertSeparator(len(plt.style.available))
        self.Drop_style_menu.addItem('black_and_white.mplstyle')
        # self.Drop_style_menu.activated[str].connect(self.bckgrd)


    def gen_left_panel(self):
        """
        set the left side of the app containing the plotting area
        """

        self.left_panel = QVBoxLayout()
        self.left_panel.addWidget(self.canvas)
        # self.toolbar = NavigationToolbar(self.canvas, self)
        # print(NavigationToolbar.toolitems)
        # self.left_panel.addWidget(self.toolbar, 1, 0)



        self.left_panel.addWidget(self.toolbar)

    def new_plot(self,name=None):
        ''' plot some random stuff '''

        if not name is None:
          print('new_plot')

          A = np.loadtxt(name,delimiter=',')
          X = A[:,0]
          Y = A[:,1]

          legend = None


          plot_var = ['Xdata', 'Ydata', 'legend', 'mark', 'marknb']
          plot_nb = len(self.data['Plots'])

          if legend:
             plot_name = legend
          else:
             plot_name = 'plot%s' % (plot_nb)

          self.data['Plots']['%s' % (plot_name)] = dict.fromkeys(plot_var)

          local_plot = self.data['Plots']['%s' % (plot_name)]
          local_plot['Xdata'] = X
          local_plot['Ydata'] = Y
          local_plot['legend'] = legend
         #local_plot['marknb'] = nbmark

          self.update_data_dict()
          self.change_plot_params()
          self.canvas.draw()
        else:
            pass



        #  # instead of ax.hold(False)
        #  self.figure.clear()
        #
        #  # create an axis
        #  self.ax = self.figure.add_subplot(111)
        #
        #  if self.style_name is 'dark_background':
        #      self.ax.tick_params(labelcolor='black')
        #
        #  # plot data
        #  #ax.plot(data, '*-')
        #  self.lines, = self.ax.plot(X,Y,'x-',label='$x^{2}$')
        #  # self.bla, = self.ax.plot(X,2*X,'o-',label='doubled')
        #
        #  # refresh canvas
        #  self.canvas.draw()
        #  #self.i +=1
        # else:
        #  pass


    def refresh(self):
        """Refresh plot parameters"""
        print('refresh')
        if self.figure.get_axes():
            print('refresh')
            self.update_data_dict()
            self.change_plot_params()
            self.canvas.draw()
        else:
            pass

    def change_plot_params(self):
        print('change_plot_params')

        # if self.figure.get_axes():
        #     self.ax.set_title(u'%s'%(self.Title.text()),color='black')
        #     self.ax.set_xlabel(u'%s'%(self.Xlabel.text()),color='black')
        #     self.ax.set_ylabel(u'%s'%(self.Ylabel.text()),color='black')
        #     # self.lines.set_marker('o')
        #     if self.ax.get_legend():
        #         self.ax.legend_.remove()
        # else:
        #     pass


        self.figure.clear()
        plt.style.use(self.data['style'])

        self.ax = self.figure.add_subplot(111)

        self.ax.set_title(self.data['title'])
        self.ax.set_xlabel(self.data['xlabel'])
        self.ax.set_ylabel(self.data['ylabel'])



        for key in self.data['Plots']:

            print(self.data['Plots'][key])

            local_plot = self.data['Plots'][key]

            if local_plot['marknb']:
                a= len(local_plot['Xdata'])
                b = local_plot['marknb']
                markev = int(a/b)
            else:
                markev = None

            if local_plot['legend']:
                self.ax.plot(local_plot['Xdata'], local_plot['Ydata'],
                             label=local_plot['legend'],
                             markevery=markev)
                self.ax.legend(loc='best')

            else:
                self.ax.plot(local_plot['Xdata'], local_plot['Ydata'],
                             markevery=markev)


        if self.data['Xmin'] and self.data['Xmax']:
            self.ax.set_xlim(self.data['Xmin'], self.data['Xmax'])
        else:
            xlimits = self.ax.get_xlim()
            print(xlimits[0])
            self.data['Xmin'],self.data['Xmax'] = xlimits[0],xlimits[1]
            # self.ax.set_ylim(self.data['Ymin'], self.data['Ymax'])


    def update_data_dict(self):
        print('updata dict')

        self.data['style'] = str(self.Drop_style_menu.currentText())

        self.data['title'] = self.Title.text()
        self.data['xlabel'] = self.Xlab.text()
        self.data['ylabel'] = self.Ylab.text()

        # self.data['Xmin'] = self.Xmin.text()
        print(self.data['Xmin'])
        # self.data['Xmax'] = self.Xmax.text()
        self.data['Ymin'] = self.Ymin.text()
        self.data['Ymax'] = self.Ymax.text()

    def getfile(self):
        print('getfile')
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        filename = dlg.getOpenFileName()
        self.name = filename[0]
        if self.name:
            self.new_plot(name = self.name)
        # dlg.setFilter("Text files (*.txt)")


    def Open_param(self):
        self.paramwin.show()

class FileWindow(QMainWindow):

    def __init__(self, parent=None):
        super(FileWindow, self).__init__(parent)

        #define application parameters
        self.setGeometry(300, 150, 500, 200)

        self.setWindowTitle("File Window")
        self.setWindowModality(Qt.ApplicationModal)

        p = self.palette()
        p.setColor(self.backgroundRole(),Qt.darkGray)
        self.setPalette(p)
        self.setStyleSheet("font: 20pt Palatino")

        # set the layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)


class ParamWindow(QDialog):

    def __init__(self, parent=None):
        super(ParamWindow, self).__init__(parent)

        #define application parameters
        self.setGeometry(300, 150, 500, 200)

        self.setWindowTitle("Params")
        self.setWindowModality(Qt.ApplicationModal)

        p = self.palette()
        p.setColor(self.backgroundRole(),Qt.white)
        self.setPalette(p)
        self.setStyleSheet("font: 20pt Palatino")

        # set the layout
        # self.layout = QFormLayout()
        # self.widgets()
        # self.layout.setHorizontalSpacing(200)
        # self.layout.setVerticalSpacing(20)
        # self.setLayout(self.layout)

        self.layout = QVBoxLayout(self)





        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Curves")
        self.tabs.addTab(self.tab2, "Axes")

        # Create first tab
        self.tab1.layout = QFormLayout()
        self.axes_widgets()
        self.tab1.layout.setHorizontalSpacing(100)
        self.tab1.layout.setVerticalSpacing(10)
        self.tab1.setLayout(self.tab1.layout)

        #Bottom buttons
        self.buttons = QWidget()
        self.buttons.layout= QHBoxLayout()
        self.apply = QPushButton("Apply")
        self.apply.clicked.connect(PlotWindow.refresh)
        self.space=QLabel('')
        self.space.setMinimumWidth(100)
        self.okay = QPushButton("OK")
        self.cancel = QPushButton("Cancel")

        self.buttons.layout.addWidget(self.apply)
        self.buttons.layout.addWidget(self.space)
        self.buttons.layout.addWidget(self.okay)
        self.buttons.layout.addWidget(self.cancel)
        self.buttons.setLayout(self.buttons.layout)

        # Overall layout
        self.layout.addWidget(self.tabs)
        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def axes_widgets(self):
        # BUTTONS
        form_name_list=['Xmin','Xmax','Ymin','Ymax']

        for i in form_name_list:
            setattr(self,i+'Label',QLabel(i))
            setattr(self,i,QLineEdit())
            # getattr(self,i+'Label').setMinimumWidth(500)
            self.tab1.layout.addRow(i,QLineEdit())
            self.tab1.layout.addRow(QLabel(''))
            print(getattr(self,i))

            # self.XlimLabel = QLabel('Xlimits')
            # self.XlimLabel.setStyleSheet('color : white')
            # self.Xmax = QLineEdit()
            # self.Xmin = QLineEdit()




    #Axes limits and scales

    #


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))

    main = PlotWindow()
    # main=FileWindow()
    main.show()

    sys.exit(app.exec_())


