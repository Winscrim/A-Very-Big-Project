'''
This module allows to read various scientific files and convert them into
python dictonnaries
'''

import numpy as np


def create_dico(file_name,filetype='csv',skiprows=0):


    if filetype is 'csv':
        A=np.loadtxt(file_name,dtype=str,delimiter=',',skiprows=skiprows)
        DICO ={}
        for n in range(0,A.shape[1]):
            # print(n)
            DICO[A[0,n]] = A[1:,n].astype(float)

        return DICO

    elif filetype is 'igor':
        print('igor file reading is not yet implemented')

    elif filetype is 'hash':
        NAME=[]
        with open(file_name, 'rt') as B:
            for line in B:
                if '#' in line:
                    NAME.append(line[2:].rstrip())
        A = np.loadtxt(file_name, dtype=str, skiprows=skiprows)
        DICO = {}
        for n in range(0, A.shape[1]):
            # print(n)
            DICO[NAME[n]] = A[0:, n].astype(float)

        return DICO
    else:
        A = np.loadtxt(file_name, dtype=str, skiprows=skiprows)
        DICO = {}
        for n in range(0, A.shape[1]):
            # print(n)
            DICO[A[0, n]] = A[1:, n].astype(float)

        return DICO