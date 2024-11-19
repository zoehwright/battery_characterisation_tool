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
        self.data = None
        self.df = None

     def read_neware_data(self):
        
        self.df = pd.read_csv(self.file_path, header=1)

        #self.df = self.df.drop(index=0)

        #self.df.head()
        #print(self.df)
        
     def count_neware_voltage_columns(self):
        self.df.columns.str.startswith('Spec. Cap.(mAh/g)').sum()
        print(self.df.columns.str.startswith('Spec. Cap.(mAh/g)').sum())

        self.df.columns.str.startswith('Voltage').sum()
        print(self.df.columns.str.startswith('Voltage').sum())

     def specific_cycle_plot_neware(self, cycle_number=1):   

        self.df = self.process_df.remove_large_voltage_values(self.df)

        # Validate the input (check if it's a number)
        cycle_number = f'.{cycle_number}'  # Format the cycle number as a string like '.2', '.3', etc.

        # Filter columns that end with the given cycle number
        columns_ending_with_cycle = self.df.columns[self.df.columns.str.endswith(cycle_number)]

        # Check if the specific columns exist for the selected cycle
        if f'Spec. Cap.(mAh/g){cycle_number}' in columns_ending_with_cycle and f'Voltage(V){cycle_number}' in columns_ending_with_cycle:
            # Extract the columns for the given cycle
            spec_cap_column = self.df[f'Spec. Cap.(mAh/g){cycle_number}']
            voltage_column = self.df[f'Voltage(V){cycle_number}']
            
            # Plot the data
            plt.plot(spec_cap_column, voltage_column, color = "lightseagreen")
            plt.xlabel("Specific Capacity (mAh/g)", fontsize = self.fontsize)
            plt.ylabel("Ewe/V", fontsize = self.fontsize)
            plt.xlim(self.xlim[0], self.xlim[1])
            plt.ylim(self.ylim[0], self.ylim[1])
            plt.title(f'GCD Plot for cycle {cycle_number[1:]}')  # Remove the dot for display
            #plt.legend(bbox_to_anchor=(1, 0.9), fontsize = self.fontsize, labels = self.legend_labels)
            #plt.grid(True)
            plt.tick_params(axis='both', which='major', labelsize=self.fontsize)
            plt.show()
        else:
            print(f"The specified columns for cycle {cycle_number[1:]} are not available in the dataframe.")

     def gcd_neware(self):
        
        #fig, ax = plt.subplots(figsize=self.figsize)
        #self.df = pd.read_csv(self.file_path, header=1)
        self.df = pd.read_csv(self.file_path, header=1)
        self.df = self.process_df.remove_large_voltage_values(self.df)

    
        #charge_data = df[df["charge_discharge"] == 1]
        #discharge_data = df[df["charge_discharge"] == -1]
        
        voltage_count = self.df.columns.str.startswith('Voltage').sum()
        cycle_numbers = list(range(1, voltage_count + 1))
        n = len(cycle_numbers)
        blues = sns.dark_palette("darkcyan", n_colors=n, as_cmap=False)
        #blues = [colors.rgb2hex(i) for i in blues]
        print(cycle_numbers)

        spec_cap_columns = [col for col in self.df.columns if col.startswith("Spec. Cap.")]
        voltage_columns = [col for col in self.df.columns if col.startswith("Voltage")]

        # Check if the lengths of the two column groups match
        if len(spec_cap_columns) != len(voltage_columns):
            print("Warning: The number of 'Spec. Cap.' and 'Voltage' columns do not match.")
            print("Ensure they are properly aligned for correct plotting.")
    
        # Plot each pair
        plt.figure(figsize=(10, 6))
        for idx, (spec_cap_col, voltage_col) in enumerate(zip(spec_cap_columns, voltage_columns)):
        # Use blues[idx] to assign a unique color for each pair
            plt.plot(self.df[spec_cap_col], self.df[voltage_col], color=blues[idx])

        # Customize the plot
        plt.xlabel('Specific Capacity (mAh/g)', fontsize = self.fontsize)
        plt.ylabel('Voltage (V)', fontsize = self.fontsize)
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])
        plt.tick_params(axis='both', which='major', labelsize=self.fontsize)
        plt.title(label=self.plot_title, fontsize=self.fontsize)
        #plt.legend(bbox_to_anchor=(1, 1), fontsize = self.fontsize, labels = self.legend_labels) #, loc = 'lower left'
        #plt.grid(True)
        
           
     def gcd_single_dataset(self):
    
        fig, ax = plt.subplots(figsize=self.figsize)
        df = self.process_df.process_voltage_capacity_df(file_path=self.file_path, 
                                                       active_mass=self.active_mass)

        charge_data = df[df["charge_discharge"] == 1]
        discharge_data = df[df["charge_discharge"] == -1]

        charge_color = "darkslategray" #sns.color_palette("Blue") #, n_colors=1)[-1]    
        discharge_color = "lightseagreen" #sns.color_palette("Reds", n_colors=1)[-1]

        x_charge, x_discharge = charge_data["Specific Capacity mAh/g"], discharge_data["Specific Capacity mAh/g"]
        y_charge, y_discharge = charge_data["Ewe/V"], discharge_data["Ewe/V"]

        ax.scatter(x_charge, y_charge, marker='o', s=1, color = charge_color)
        ax.scatter(x_discharge, y_discharge, marker='o', s=1, color = discharge_color)
        ax.set_xlabel("Specific Capacity (mAh/g)", fontsize = self.fontsize)
        ax.set_ylabel("Ewe/V", fontsize = self.fontsize)
        #ax2.tick_params(axis='y', labelsize=10)
        ax.set_xlim(self.xlim[0], self.xlim[1])
        ax.set_ylim(self.ylim[0], self.ylim[1])
        ax.tick_params(axis='both', which='major', labelsize=self.fontsize)
        plt.legend(bbox_to_anchor=(1, 1), fontsize = self.fontsize, labels = self.legend_labels) #, loc = 'lower left'

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
        blues = sns.dark_palette("darkcyan", n_colors=n, as_cmap=False)
        #blues = [colors.rgb2hex(i) for i in blues]
        reds = sns.dark_palette("darkcyan", n_colors=n, as_cmap=False)
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
                ax.scatter(x_charge_filtered, y_charge_filtered, marker='o', s=0.05, color=blues[int(i)])  
                ax.scatter(x_discharge_filtered, y_discharge_filtered, marker='o', s=0.05, color=reds[int(i)])

        ax.set_xlabel("Specific Capacity (mAh/g)", fontsize = self.fontsize)
        ax.set_ylabel("Ewe/V", fontsize = self.fontsize)
        ax.set_xlim(self.xlim[0], self.xlim[1])
        ax.set_ylim(self.ylim[0], self.ylim[1])
        ax.tick_params(axis='both', which='major', labelsize=self.fontsize)
        ax.set_title(label=self.plot_title, fontsize=self.fontsize)
        #ax.legend(bbox_to_anchor=(1, 0.8), fontsize = self.fontsize, labels = self.legend_labels) #, loc = 'lower left'

