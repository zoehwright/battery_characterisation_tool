####import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

import matplotlib.colors as colors 
import os
import glob 

from typing import Optional
from battery_characterisation_tool.echem_plotting.process_dataframe import ProcessDataframe

class dQdVPlotter:
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
            xlim: Optional[tuple] = (-0.5, 5),
            ylim: Optional[tuple] = (-15, 15),
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
    """
    def _get_file_list(self) -> str:
        
        Retrieves a list of valid files in the specified folder path.

        This method scans the folder path for files with .txt or .csv extensions
        and returns their full paths in a list.

        Returns:
            list: List of file paths with valid extensions.
        
        import pdb
        # pdb.set_trace()
        arr = os.listdir(self.folder_path)
        # pdb.set_trace()
        arr = [f"{self.folder_path}\{item}" 
               for item in arr 
               if item.endswith(".txt") or 
               item.endswith(".csv")]
        return arr 
    """
    def _get_file_list(self) -> list:
        arr = os.listdir(self.folder_path)
        arr = [f"{self.folder_path}\{item}" for item in arr if item.endswith((".txt", ".csv"))]
        return arr
    
    def dqdv_multiple_cycles(self):
        """
        Generates a plot with specific cycle datasets listed in the folder_path.
        """
        files = self._get_file_list()

        palette = sns.color_palette("Dark2", len(files))  # Choose a palette and set number of colors #husl

        #plt.figure(figsize=self.figsize)
        fig, ax = plt.subplots(figsize=self.figsize)

        for idx, file in enumerate(files):
            path = os.path.join(self.folder_path, file)
            skip_header_value = self.process_df.check_file_header_present(path)
            try:
                data = np.loadtxt(path, encoding='utf-8', skiprows=skip_header_value)
            except UnicodeDecodeError:
                try:
                    data = np.loadtxt(path, encoding='latin1', skiprows=skip_header_value)
                except UnicodeDecodeError as e:
                    print(f"Error reading {path}: {e}")
                    continue

            x = data[:,2]
            y = data[:,4]
            #print(df)
            #ax.scatter(x, y, label=file, color=palette[idx], marker='o', s=5) #, markerfacecolor ="none", lw=0.7) 
            ax.plot(x, y, label=file, color=palette[idx], linewidth = 1)  #, markerfacecolor ="none", lw=0.7
        # plt.title(label=self.plot_title, fontsize=self.fontsize) 
        ax.set_title(label=self.plot_title, fontsize=self.fontsize)
        ax.set_xlabel("Ewe/V", fontsize=self.fontsize)
        ax.set_ylabel("d(Q-Qo)/dE/mA.h/V", fontsize=self.fontsize)
        ax.tick_params(axis='both', which='major', labelsize=18)
        ax.set_xlim(self.xlim[0], self.xlim[1])
        ax.set_ylim(self.ylim[0], self.ylim[1])
        # plt.xlabel("Ewe/V", fontsize=self.fontsize)   
        # plt.ylabel("d(Q-Qo)/dE/mA.h/V", fontsize=self.fontsize) 
        # plt.xlim(self.xlim[0], self.xlim[1])
        #ax.set_xlim(self.xlim[0], self.xlim[1])
        # plt.ylim(self.ylim[0], self.ylim[1])
        #ax.set_ylim(self.ylim[0], self.ylim[1])
        # plt.xticks(fontsize=self.fontsize)
        # plt.yticks(fontsize=self.fontsize)
        # plt.legend(bbox_to_anchor=(1, 1), fontsize = self.fontsize, labels = self.legend_labels)
        ax.legend(loc = "upper left", fontsize = self.fontsize, labels = self.legend_labels) #bbox_to_anchor=(1, 1)
        #plt.rcParams.update({'font.size': 10})  
        #plt.show()

    def dqdv_single_cycle(self):

        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Load the data using pandas
        df = pd.read_csv(self.file_path, sep="\t", header=0)

        df = df.drop(df[df["d(Q-Qo)/dE/mA.h/V"] == 0].index)
        
        x = df["Ewe/V"]
        y = df["d(Q-Qo)/dE/mA.h/V"]

        # Plot the data
        ax.plot(x, y, linewidth=3, color="darkcyan")
       # ax.scatter(x, y, linewidth=0.8, color="darkcyan", marker='o', s=2)
        ax.set_xlim(self.xlim[0], self.xlim[1])
        ax.set_ylim(self.ylim[0], self.ylim[1])
        ax.set_xlabel('Ewe/V', fontsize=self.fontsize)
        ax.set_ylabel('d(Q-Qo)/dE/mA.h/V', fontsize=self.fontsize)
        ax.set_title(label=self.plot_title, fontsize=self.fontsize)
        ax.tick_params(axis='both', which='major', labelsize=self.fontsize)

        ax.legend(bbox_to_anchor=(0.8, 1), fontsize=self.fontsize, labels=self.legend_labels)
        # Show the plot
        plt.show()

    def read_neware_data(self):
        
        self.df = pd.read_csv(self.file_path, header=1)
        print(self.df)

    def count_neware_voltage_columns(self):
        self.df.columns.str.startswith('dQ/dV').sum()
        print(self.df.columns.str.startswith('dQ/dV').sum())

        self.df.columns.str.startswith('Voltage').sum()
        print(self.df.columns.str.startswith('Voltage').sum())

    def dqdv_single_cycle_neware(self):   

        self.df = pd.read_csv(self.file_path, header=0)
        
        # Plot the data
        plt.plot(self.df["Voltage(V)"], self.df["dQ/dV(mAh/V)"], label="dQ/dV vs Voltage", linewidth = 1)
        plt.xlabel("Ewe/V", fontsize = self.fontsize)
        plt.ylabel("dQ/dV(mAh/V)", fontsize = self.fontsize)
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])
        plt.title(label=self.plot_title, fontsize=self.fontsize)
        plt.legend(loc = "upper left", fontsize = self.fontsize - 4 , labels = self.legend_labels)
        #plt.grid(True)
        plt.tick_params(axis='both', which='major', labelsize=self.fontsize)
        plt.show()
    
    def dqdv_multiple_cycles_neware(self):
        """
        Generates a plot with specific cycle datasets listed in the folder_path.
        """
        files = self._get_file_list()
        #print("Files to be plotted:", files)

        palette = sns.color_palette("Dark2", len(files))  # Choose a palette and set number of colors

        plt.figure(figsize=self.figsize)
        #fig, ax = plt.subplots(figsize=self.figsize)

        for idx, file in enumerate(files):
            path = os.path.join(self.folder_path, file)
            # Check if the file has a header (skip_header_value = 1 means it has a header)
            skip_header_value = self.process_df.check_file_header_present(path)

            try:
            # Read the file using pandas, with handling for header
                if skip_header_value == 0:
                    df = pd.read_csv(path, header=None, encoding='utf-8')  # No header
                else:
                    df = pd.read_csv(path, encoding='utf-8')  # Header present
            except UnicodeDecodeError:
                try:
                    # Try reading with a different encoding if UnicodeDecodeError occurs
                    if skip_header_value == 0:
                        df = pd.read_csv(path, header=0, encoding='latin1')
                    else:
                        df = pd.read_csv(path, encoding='latin1')
                except UnicodeDecodeError as e:
                    print(f"Error reading {path} with both UTF-8 and Latin1 encoding: {e}")
                    continue
            
            x = df.iloc[1:,0].astype(float) #.astype(float) is used to ensure that the data in the selected columns (x and y) are explicitly converted to numeric values (floating-point numbers).
            y = df.iloc[1:,1].astype(float)
            plt.plot(x, y, linewidth = 1, color=palette[idx]) #label="dQ/dV vs Voltage", 
        plt.xlabel("Ewe/V", fontsize = self.fontsize)
        plt.ylabel("dQ/dV(mAh/V)", fontsize = self.fontsize)
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])
        plt.title(label=self.plot_title, fontsize=self.fontsize)
        plt.legend(loc = "upper left", fontsize = self.fontsize - 4 , labels = self.legend_labels) # bbox_to_anchor = (1,1)
        #plt.grid(True)
        plt.tick_params(axis='both', which='major', labelsize=self.fontsize)
        #plt.show()
    
    def dqdv_all_cycles_neware(self):

        self.df = pd.read_csv(self.file_path, header=0)
        
        # Plot the data
        plt.plot(self.df["Voltage(V)"], self.df["dQ/dV(mAh/V)"], label="dQ/dV vs Voltage", linewidth = 1)
        plt.xlabel("Ewe/V", fontsize = self.fontsize)
        plt.ylabel("dQ/dV(mAh/V)", fontsize = self.fontsize)
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])
        plt.title(label=self.plot_title, fontsize=self.fontsize)
        plt.legend(bbox_to_anchor = (1,1), fontsize = self.fontsize - 4 , labels = self.legend_labels)
        #plt.grid(True)
        plt.tick_params(axis='both', which='major', labelsize=self.fontsize)
        plt.show()
    
    def dqdv_all_cycles_neware_colour(self):
    
        # Read the dataset
        self.df = pd.read_csv(self.file_path, header=0)
        
        # Ensure Cycle Index is sorted for consistent coloring
        self.df = self.df.sort_values(by="Cycle Index")
        
        # Get unique cycle indices
        unique_cycles = self.df["Cycle Index"].unique()
        
        # Create a fading sequential color palette
        palette = sns.color_palette("viridis", len(unique_cycles))  # "viridis" is great for fading colors
        
        # Set up the plot
        plt.figure(figsize=self.figsize)
        
        # Plot each cycle with a distinct color
        for idx, cycle in enumerate(unique_cycles):
            # Filter data for the current cycle
            cycle_data = self.df[self.df["Cycle Index"] == cycle]
            
            # Extract voltage and dQ/dV
            x = cycle_data["Voltage(V)"]
            y = cycle_data["dQ/dV(mAh/V)"]
            
            # Plot the line for the current cycle with a fading color
            plt.scatter(x, y, color=palette[idx], label=f"Cycle {cycle}", s= 5) #linewidth=1)
        
        # Configure plot aesthetics
        plt.xlabel("Ewe/V", fontsize=self.fontsize)
        plt.ylabel("dQ/dV (mAh/V)", fontsize=self.fontsize)
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])
        plt.title(label=self.plot_title, fontsize=self.fontsize)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=self.fontsize - 4, ncol =4)
        plt.grid(True)
        plt.tick_params(axis='both', which='major', labelsize=self.fontsize)
        
        # Show the plot
        #plt.tight_layout()
        plt.show()

    def dqdv_multiple_cycles_biologic_test(self):
        """
        Generates a plot with specific cycle datasets listed in the folder_path.
        """
        files = self._get_file_list()
        #print("Files to be plotted:", files)

        palette = sns.color_palette("Dark2", len(files))  # Choose a palette and set number of colors

        plt.figure(figsize=self.figsize)
        #fig, ax = plt.subplots(figsize=self.figsize)

        for idx, file in enumerate(files):
            path = os.path.join(self.folder_path, file)
            # Check if the file has a header (skip_header_value = 1 means it has a header)
            skip_header_value = self.process_df.check_file_header_present(path)

            try:
            # Read the file using pandas, with handling for header
                if skip_header_value == 0:
                    df = pd.read_csv(path, header=None, encoding='utf-8')  # No header
                else:
                    df = pd.read_csv(path, encoding='utf-8')  # Header present
            except UnicodeDecodeError:
                try:
                    # Try reading with a different encoding if UnicodeDecodeError occurs
                    if skip_header_value == 0:
                        df = pd.read_csv(path, header=0, encoding='latin1')
                    else:
                        df = pd.read_csv(path, encoding='latin1')
                except UnicodeDecodeError as e:
                    print(f"Error reading {path} with both UTF-8 and Latin1 encoding: {e}")
                    continue
            
            x = df.iloc[1:,0].astype(float) #.astype(float) is used to ensure that the data in the selected columns (x and y) are explicitly converted to numeric values (floating-point numbers).
            y = df.iloc[1:,1].astype(float)
            plt.plot(x, y, linewidth=1, color=palette[idx]) #label="dQ/dV vs Voltage", 
        plt.xlabel("Ewe/V", fontsize = self.fontsize)
        plt.ylabel("dQ/dV(mAh/V)", fontsize = self.fontsize)
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])
        plt.title(label=self.plot_title, fontsize=self.fontsize)
        plt.legend(loc = "upper left", fontsize = self.fontsize - 4 , labels = self.legend_labels) # bbox_to_anchor = (1,1)
        #plt.grid(True)
        plt.tick_params(axis='both', which='major', labelsize=self.fontsize)
        #plt.show()

    def dqdv_single_cycle_biologic_test(self):   

        self.df = pd.read_csv(self.file_path, header=0)
        
        # Plot the data
        plt.plot(self.df["Ewe/V"], self.df["d(Q-Qo)/dE/mA.h/V"], label="dQ/dV vs Voltage", linewidth = 1)
        plt.xlabel("Ewe/V", fontsize = self.fontsize)
        plt.ylabel("dQ/dV(mAh/V)", fontsize = self.fontsize)
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])
        plt.title(label=self.plot_title, fontsize=self.fontsize)
        plt.legend(loc = "upper left", fontsize = self.fontsize - 4 , labels = self.legend_labels)
        #plt.grid(True)
        plt.tick_params(axis='both', which='major', labelsize=self.fontsize)
        plt.show()