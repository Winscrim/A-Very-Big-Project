"""
replot.py contains functions that allow to save(replot.save()) and load(
replot.load()) plot objects (saved in a binary file)
and also allow to add (replot.add()) a plot values to an existing one
"""

import pickle
import matplotlib.pyplot as plt

def extension(file_name):
    """
    Adds the correct extension to a file name
    :param file_name: file name
    :return: name withth extension
    """
    if not file_name.endswith('.rplt'):
        file_name += '.rplt'

    return file_name

def save(obj, file_name='Default.rplt'):
    """
    Function which allows to save the plot object for reusability and/or display/show it.
    :param obj: name of pyplot object containing the plot information
    :param file_name: Name of the saved binary file wanted, if not specified no saving is done
    :param plot: Boolean to know if the display of the graph is wanted(show()), default is yes.
    :return: create a binary file used for the replotting and/or display the graph
    """
    if not hasattr(obj, 'data'):
        quit("ERROR : Input object is not consistent with a plotter object "
             "!\n Stopping script...")


    if file_name != 'Default.rplt':
        save = extension(file_name)
        print('Saving as ', save)
        pickle.dump(obj, open(save, "wb"))
    else:
        quit('ERROR = saving file name not specified !')

def load(file_name):
    """
    Loads the object saved via pickle

    :param file_name: name of the binary file containing the pyplot object ( ex: 'plot.rplt')
    :return: object saved in the file
    """
    name = extension(file_name)
    obj = pickle.load(open(name, "rb"))

    return obj

def add(file_name, x_data, y_data, *args, **kwargs):
    """
    Add a new set of values (x,y) with plot params to an old plot saved in binary(name)
    :param file_name: name of the binary file containing the pyplot object ( ex: 'plot.rplt')
    :param x: data for the abcsissa
    :param y: data for the ordinate
    :param args: arguments for pyplot.plot function for the new set of values
    :param kwargs: keywords arguments for the pyplot.plot for the new set of values
    :return:
    """
    file_name = extension(file_name)
    obj = pickle.load(open(file_name, "rb"))
    plt.plot(x_data, y_data, *args, **kwargs)
    plt.legend()
    return obj
