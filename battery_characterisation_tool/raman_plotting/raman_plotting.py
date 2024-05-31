import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl
import seaborn as sns
import matplotlib.colors as colors 
import os

#from echem_plotting.process_dataframe import ProcessDataframe
from matplotlib.lines import Line2D 
from typing import Optional, Tuple

class RamanPlot:
    """
    A class to generate and customize Raman spectroscopy plots.

    Attributes:
    ----------
    dataset_name : str, optional
        Name of the dataset to be used in the plot (default is an empty string).
    plot_title : str, optional
        Title of the plot (default is an empty string).
    legend_labels : list, optional
        Labels to be used for the legend in the plot (default is an empty list).
    folder_path : list, optional
        Path(s) to the folder(s) containing the dataset(s) (default is an empty list).
    fontsize : int, optional
        Font size for the plot labels (default is 16).
    title_fontsize : int, optional
        Font size for the plot title (default is 18).
    figsize : tuple, optional
        Size of the plot figure (default is (10, 8)).

    Methods:
    -------
    __init__(self, dataset_name: Optional[str] = "", plot_title: Optional[str] = "",
             legend_labels: Optional[list] = [], folder_path: Optional[list] = [],
             fontsize: Optional[int] = 16, title_fontsize: Optional[int] = 18,
             figsize: Optional[tuple] = (10, 8)):
        Initializes the RamanPlot class with the provided parameters.

    raman_plot(self):
        Generates a Raman plot for the dataset specified by dataset_name.
    
    raman_stacked_plot(self):
        Generates a stacked Raman plot for all datasets in the folder_path.
    
    _get_file_list(self) -> list:
        Helper method to retrieve a list of files from the folder_path.
    """

    def __init__(
        self, 
        dataset_name: Optional[str] = "",
        plot_title: Optional[str] = "",
        legend_labels: Optional[list] = [],
        folder_path: Optional[list] = [],
        fontsize: Optional[int] = 16,
        title_fontsize: Optional[int] = 18,
        figsize: Optional[tuple] = (10,8),
    ):
    
        self.dataset_name = dataset_name
        self.plot_title = plot_title
        self.legend_labels = legend_labels
        self.folder_path = folder_path
        self.figsize = figsize
        self.fontsize = fontsize
        self.title_fontsize = title_fontsize
        if folder_path != []:    
            self.file_list = self._get_file_list()
        #self.process_df = ProcessDataframe()

    def _get_file_list(self) -> list:
        """
        Retrieves a list of valid files in the specified folder path.

        This method scans the folder path for files with .txt or .csv extensions
        and returns their full paths in a list.

        Returns:
            list: List of file paths with valid extensions.
        """
        arr = os.listdir(self.folder_path)
        arr = [f"{self.folder_path}\{item}" for item in arr if item.endswith((".xy"))]
        return arr 
    
    def raman_plot(self):
        """
        Generates a Raman plot for the dataset specified by dataset_name.
        """
        path = f"{self.folder_path}\{self.dataset_name}"
        data = np.loadtxt(path)

        x, y = data[:,0], data[:,1]

        plt.figure(figsize=self.figsize) 
        plt.plot(x,y)       
        plt.title(label=self.plot_title, fontsize=self.title_fontsize) 
        plt.xlabel("Raman shift (cm$^{-1}$)", fontsize=self.fontsize)   
        plt.ylabel("Intensity (a.u.)", fontsize=self.fontsize) 
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        plt.rcParams.update({'font.size': 10}) 


    def raman_stacked_plot(self):
        """
        Generates a stacked Raman plot for all datasets in the folder_path.
        """
        files = self._get_file_list()
        offset = 0

        palette = sns.color_palette("husl", len(files))  # Choose a palette and set number of colors

        plt.figure(figsize=(10, 6))

        for idx, file in enumerate(files):
            path = os.path.join(self.folder_path, file)
            try:
                data = np.loadtxt(path, encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    data = np.loadtxt(path, encoding='latin1')
                except UnicodeDecodeError as e:
                    print(f"Error reading {path}: {e}")
                    continue

            x = data[:,0]
            y = data[:,1]

            plt.plot(x, y + offset, label=file, color=palette[idx]) 
            offset += np.max(y)*1.2
        plt.yticks([])
        plt.title(label=self.plot_title, fontsize=self.title_fontsize) 
        plt.xlabel("Raman shift (cm$^{-1}$)", fontsize=self.fontsize)   
        plt.ylabel("Intensity (a.u.)", fontsize=self.fontsize) 
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        plt.legend(bbox_to_anchor=(1, 1), fontsize = self.fontsize, labels = self.legend_labels)
        plt.rcParams.update({'font.size': 10})  
        plt.show()
