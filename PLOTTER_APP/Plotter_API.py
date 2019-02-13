'''
THIS IS AN API TO ENHANCE THE PLOTTING PART OF A PHD

THis essentially is a sup layer of matplotlib
'''


from src.plotting import graph
import src.replot as rplt
from src.file_reader import create_dico
import numpy as np
import os

class plotter():
    def __init__(self,parent=None):
        X = 20
        rl = '\n'
        print('#'*X+rl)
        print('THIS IS THE PLOTTER_API')
        print('VERSION :  ALPHA 0.1'+rl)
        print('#'*X+rl)

        self.column_names = []
        self.PLOT = graph()

    def test(self):
        print('hello')



    def read(self,raw_filename):
        print('READING THE FILE')
        if raw_filename.endswith('.txt') or raw_filename.endswith('.dat'):
            filename = raw_filename  #need to add a file trimming function
            fmt = 'txt'
            print('reading .dat or .txt file')
        if raw_filename.endswith('.csv'):
            filename = raw_filename
            fmt = 'csv'
            print('reading csv file')

        FILE = create_dico(filename,filetype=fmt)
        for key in FILE:
            self.column_names.append(key)
        print('File column names:',self.column_names)

        return FILE

    def create_graph(self,FILE,Xname,Yname):
        self.PLOT.setData(FILE[Xname],FILE[Yname])
        self.PLOT.setlabels(Xaxis=Xname,Yaxis=Yname)
        self.PLOT.disp()

    def add_graph(self,FILE,Xname,Yname):
        self.PLOT.setData(FILE[Xname],FILE[Yname])
        self.PLOT.disp()


    def save(self):
        rplt.save(self.PLOT,'test')

    def load(self,load_file):
        self.PLOT = rplt.load(load_file)

    def restore(self):
        self.PLOT.disp()

    def info(self):
        print(self.PLOT.data.keys())



