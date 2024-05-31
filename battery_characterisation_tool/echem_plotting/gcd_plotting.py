import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.colors as colors 
import os

from typing import Optional
from battery_characterisation_tool.echem_plotting.process_dataframe import ProcessDataframe

class GCDPlotting:
     """
    A class for plotting GCD (Galvanostatic Charge-Discharge) data.

    Parameters:
    -----------
    file_path : str, optional
        The file path to the dataset. Default is an empty string.
    dataset_name : str, optional
        The name of the dataset. Default is an empty string.
    plot_title : str, optional
        The title of the plot. Default is an empty string.
    legend_labels : list, optional
        A list of labels for the legend. Default is an empty list.
    active_mass : float, optional
        The active mass value. Default is 0.
    active_mass_list : list, optional
        A list of active mass values. Default is an empty list.
    folder_path : list, optional
        A list of folder paths. Default is an empty list.
    figsize : tuple, optional
        A tuple specifying the figure size in inches. Default is (8, 6).
    xlim : tuple, optional
        A tuple specifying the x-axis limits. Default is (0, 150).
    ylim : tuple, optional
        A tuple specifying the y-axis limits. Default is (1, 4.5).
    fontsize : int, optional
        The fontsize for labels and title. Default is 16.
    """
     def __init__(
        self, 
        file_path: Optional[str] = "",
        dataset_name: Optional[str] = "",
        plot_title: Optional[str] = "",
        legend_labels: Optional[list] = [],
        active_mass: Optional[float] = 0,
        active_mass_list: Optional[list] = [],
        folder_path: Optional[list] = [],
        figsize: Optional[tuple] = (8, 6),
        xlim: Optional[tuple] = (-5, 175),
        ylim: Optional[tuple] = (1, 4.5),
        fontsize: Optional[int] = 16,
    ):
    
        self.file_path = file_path
        self.dataset_name = dataset_name
        self.plot_title = plot_title
        self.legend_labels = legend_labels
        self.active_mass = active_mass
        self.active_mass_list = active_mass_list
        self.folder_path = folder_path
        self.figsize = figsize
        self.xlim = xlim
        self.ylim = ylim
        self.fontsize = fontsize
        if folder_path != []:    
            self.file_list = self._get_file_list()
        self.process_df = ProcessDataframe()


     def gcd_single_dataset(self):
    
        fig, ax = plt.subplots(figsize=self.figsize)
        df = self.process_df.process_voltage_capacity_df(file_path=self.file_path, 
                                                       active_mass=self.active_mass)

        charge_data = df[df["charge_discharge"] == 1]
        discharge_data = df[df["charge_discharge"] == -1]

        charge_color = "blue" #sns.color_palette("Blue") #, n_colors=1)[-1]    
        discharge_color = "red" #sns.color_palette("Reds", n_colors=1)[-1]

        x_charge, x_discharge = charge_data["Specific Capacity mAh/g"], discharge_data["Specific Capacity mAh/g"]
        y_charge, y_discharge = charge_data["Ewe/V"], discharge_data["Ewe/V"]

        ax.scatter(x_charge, y_charge, marker='o', s=0.01, color = charge_color)
        ax.scatter(x_discharge, y_discharge, marker='o', s=0.1, color = discharge_color)
        ax.set_xlabel("Specific Capacity (mAh/g)", fontsize = self.fontsize)
        ax.set_ylabel("Ewe/V", fontsize = self.fontsize)
        #ax2.tick_params(axis='y', labelsize=10)
        ax.set_xlim(self.xlim[0], self.xlim[1])
        ax.set_ylim(self.ylim[0], self.ylim[1])
        plt.legend(bbox_to_anchor=(1, 1), fontsize = self.fontsize, labels = self.legend_labels) #, loc = 'lower left'
        #plt.legend(bbox_to_anchor=(1, 1)) 

     def gcd_color_grad(self):

        fig, ax = plt.subplots(figsize=self.figsize)
        df = self.process_df.process_voltage_capacity_df(file_path=self.file_path, 
                                                       active_mass=self.active_mass)

        charge_data = df[df["charge_discharge"] == 1]
        discharge_data = df[df["charge_discharge"] == -1]

        # x_charge, x_discharge = charge_data["Specific Capacity mAh/g"], discharge_data["Specific Capacity mAh/g"]
        # y_charge, y_discharge = charge_data["Ewe/V"], discharge_data["Ewe/V"]

        cycle_numbers = df["cycle number"].unique()
        n = len(cycle_numbers)
        blues = sns.color_palette("Blues", n_colors=n, as_cmap=False)
        #blues = [colors.rgb2hex(i) for i in blues]
        reds = sns.color_palette("Reds", n_colors=n, as_cmap=False)
        #reds = [colors.rgb2hex(i) for i in reds]
        print(cycle_numbers)

        for i in cycle_numbers:
            #if i != 41:
                x_charge_filtered = charge_data[charge_data["cycle number"] == i]["Specific Capacity mAh/g"]
                x_discharge_filtered = discharge_data[discharge_data["cycle number"] == i]["Specific Capacity mAh/g"]
                y_charge_filtered = charge_data[charge_data["cycle number"] == i]["Ewe/V"]
                y_discharge_filtered = discharge_data[discharge_data["cycle number"] == i]["Ewe/V"]
                import pdb
                #pdb.set_trace()
                ax.scatter(x_charge_filtered, y_charge_filtered, marker='o', s=0.1, color=blues[int(i)])  
                ax.scatter(x_discharge_filtered, y_discharge_filtered, marker='o', s=0.1, color=reds[int(i)])

        ax.set_xlabel("Specific Capacity (mAh/g)", fontsize = self.fontsize)
        ax.set_ylabel("Ewe/V", fontsize = self.fontsize)
        ax.set_xlim(self.xlim[0], self.xlim[1])
        ax.set_ylim(self.ylim[0], self.ylim[1])
        ax.legend(bbox_to_anchor=(1, 1), fontsize = self.fontsize, labels = self.legend_labels) #, loc = 'lower left'

