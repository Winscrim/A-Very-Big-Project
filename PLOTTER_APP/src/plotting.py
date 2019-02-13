import matplotlib.pyplot as plt
"""
Class to make the plotting part easy ( pyplot super layer )

"""


class graph():
    def __init__(self, Style='ggplot'):
        """
        Initialization of graph class with specification of the style
        used, default is 'ggplot'
        :param Style: string or list of string of style the user wants to use
        """

        fig_var = ['style', 'Plots', 'title', 'xlabel', 'ylabel',
                   'Xmin',
                   'Xmax',
                   'Ymin', 'Ymax']
        self.data = dict.fromkeys(fig_var)
        self.data['style'] = Style

        self.data['Plots'] = {}

    def setData(self, Xdata, Ydata, legend=None, nbmark=10):
        """
        Plot the wanted Dataset
        :param Xdata: Xaxis data
        :param Ydata: Yaxis data
        :return:
        """
        plot_var = ['Xdata', 'Ydata', 'legend', 'mark', 'marknb']
        plot_nb = len(self.data['Plots'])

        if legend:
            plot_name = legend
        else:
            plot_name = 'plot%s' % (plot_nb)

        self.data['Plots']['%s' % (plot_name)] = dict.fromkeys(plot_var)

        local_plot = self.data['Plots']['%s' % (plot_name)]
        local_plot['Xdata'] = Xdata
        local_plot['Ydata'] = Ydata
        local_plot['legend'] = legend
        local_plot['marknb'] = nbmark

    def setlabels(self, title=None, Xaxis=None, Yaxis=None):
        """
        Define the labels wanted on the figure(title, x and y)
        :param title: str
        :param Xaxis: str
        :param Yaxis: str
        """
        self.data['title'] = title
        self.data['xlabel'] = Xaxis
        self.data['ylabel'] = Yaxis

    def setlimits(self, Xlim=[], Ylim=[]):
        """
        define the X and Y axis limits
        :param Xlim:
        :param Ylim:
        """
        self.data['Xmin'] = Xlim[0]
        self.data['Xmax'] = Xlim[1]
        self.data['Ymin'] = Ylim[0]
        self.data['Ymax'] = Ylim[1]

    def disp(self):
        """
        Display the graph
        """
        self._refresh()
        plt.show()

    def _refresh(self):

        plt.style.use(self.data['style'])
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        self.ax.set_title(self.data['title'])
        self.ax.set_xlabel(self.data['xlabel'])
        self.ax.set_ylabel(self.data['ylabel'])
        # self.ax.set_xlim(self.data['Xmin'], self.data['Xmax'])
        # self.ax.set_ylim(self.data['Ymin'], self.data['Ymax'])

        for key in self.data['Plots']:

            # print(key)

            local_plot = self.data['Plots'][key]

            markev = int(len(local_plot['Xdata']) / local_plot['marknb'])

            if local_plot['legend']:
                self.ax.plot(local_plot['Xdata'], local_plot['Ydata'],
                             label=local_plot['legend'],
                             markevery=markev)

                self.ax.legend(loc='best')

            else:
                self.ax.plot(local_plot['Xdata'], local_plot['Ydata'],
                             markevery=markev)
