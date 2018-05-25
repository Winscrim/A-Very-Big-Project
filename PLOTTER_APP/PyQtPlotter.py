import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QFormLayout,\
    QMainWindow,QStyleFactory,QGridLayout,QComboBox,QLineEdit,QLabel,QFileDialog
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

class PlotWindow(QDialog):
    """
    Main app
    """
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)
        #print the styles available for PyQt
        print(QStyleFactory.keys())


        #define application parameters
        self.setGeometry(10, 10, 1000, 500)

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

        #Set default matplotlib style
        Style = 'ggplot'

        self.name = None

        fig_var = ['style', 'Plots', 'title', 'xlabel', 'ylabel',
               'Xmin',
               'Xmax',
               'Ymin', 'Ymax']
        self.data = dict.fromkeys(fig_var)
        self.data['style'] = Style

        self.data['Plots'] = {}

    def gen_right_panel(self):
        """
        Generate all widgets wanted for the right panel of the app main window
        :return:
        """

        #set the right side of the app containing all the buttons
        self.right_panel = QGridLayout()
        self.widgets()
        self.right_panel.addWidget(self.TitleLabel,0,0)
        self.right_panel.addWidget(self.Title,0,1)
        self.right_panel.addWidget(self.XLab,1,0)
        self.right_panel.addWidget(self.Xlabel,1,1)
        self.right_panel.addWidget(self.YLab,2,0)
        self.right_panel.addWidget(self.Ylabel,2,1)
        self.right_panel.addWidget(self.StyleLabel,3,0)
        self.right_panel.addWidget(self.Drop_style_menu,3,1)
        # self.right_panel.addWidget(self.button1,4,1)
        self.right_panel.addWidget(self.Apply,4,1)
        self.right_panel.addWidget(self.Open,4,0)
        self.right_panel.addWidget(self.OpenFile,5,1)
        # self.right_panel.addWidget(self.button3,2,0)



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
        self.TitleLabel.setStyleSheet('color : white')
        self.Title = QLineEdit()
        self.Title.setMinimumWidth(200)

        self.StyleLabel = QLabel('Style')
        self.StyleLabel.setStyleSheet('color : white')

        self.XLab = QLabel('X Label')
        self.XLab.setStyleSheet('color : white')
        self.Xlabel = QLineEdit()
        self.YLab = QLabel('Y Label')
        self.YLab.setStyleSheet('color : white')
        self.Ylabel = QLineEdit()

        #Matplotlib Figure and Toolbar
        self.figure = plt.figure(figsize=(100,10))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = CustomToolbar(self.canvas, self)




        #COMBO BOX
        self.Drop_style_menu = QComboBox()
        for i in plt.style.available:
            self.Drop_style_menu.addItem(i)
        # self.Drop_style_menu.activated[str].connect(self.bckgrd)


    def gen_left_panel(self):
        """
        set the left side of the app containing the plotting area
        """

        self.left_panel = QGridLayout()
        self.left_panel.addWidget(self.canvas, 0, 0)
        # self.toolbar = NavigationToolbar(self.canvas, self)
        # print(NavigationToolbar.toolitems)
        # self.left_panel.addWidget(self.toolbar, 1, 0)

        self.left_panel.addWidget(self.toolbar, 1, 0)

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
        # self.ax.set_xlim(self.data['Xmin'], self.data['Xmax'])
        # self.ax.set_ylim(self.data['Ymin'], self.data['Ymax'])

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


    def update_data_dict(self):
        print('updata dict')

        self.data['style'] = str(self.Drop_style_menu.currentText())

        self.data['title'] = self.Title.text()
        self.data['xlabel'] = self.Xlabel.text()
        self.data['ylabel'] = self.Ylabel.text()

        # self.data['Xmin'] = Xlim[0]
        # self.data['Xmax'] = Xlim[1]
        # self.data['Ymin'] = Ylim[0]
        # self.data['Ymax'] = Ylim[1]

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
        p.setColor(self.backgroundRole(),Qt.darkGray)
        self.setPalette(p)
        self.setStyleSheet("font: 20pt Palatino")

        # set the layout
        self.layout = QFormLayout()
        self.widgets()
        self.layout.setHorizontalSpacing(200)
        self.layout.setVerticalSpacing(20)
        self.setLayout(self.layout)

    def widgets(self):
        # BUTTONS
        form_name_list=['Xmin','Xmax','Ymin','Ymax']

        for i in form_name_list:
            setattr(self,i+'Label',QLabel(i))
            setattr(self,i,QLineEdit())
            getattr(self,i+'Label').setMinimumWidth(500)
            self.layout.addRow(QLabel(i),QLineEdit())
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


