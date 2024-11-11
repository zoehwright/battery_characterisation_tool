####import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib.colors as colors 
import os

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

    def _get_file_list(self) -> list:
        """
        Retrieves a list of valid files in the specified folder path.

        This method scans the folder path for files with .txt or .csv extensions
        and returns their full paths in a list.

        Returns:
            list: List of file paths with valid extensions.
        """
        arr = os.listdir(self.folder_path)
        arr = [f"{self.folder_path}\{item}" for item in arr if item.endswith((".txt"))]
        return arr 
    
    def dqdv_multiple_cycles(self):
        """
        Generates a plot with specific cycle datasets listed in the folder_path.
        """
        files = self._get_file_list()

        palette = sns.color_palette("husl", len(files))  # Choose a palette and set number of colors

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
            ax.scatter(x, y, label=file, color=palette[idx], marker='o', s=5) #, markerfacecolor ="none", lw=0.7) 
            #plt.plot(x, y, label=file, color=palette[idx], markerfacecolor ="none", lw=0.7) 
        # plt.title(label=self.plot_title, fontsize=self.fontsize) 
        ax.set_title(label=self.plot_title, fontsize=self.fontsize)
        ax.set_xlabel("Ewe/V", fontsize=self.fontsize)
        ax.set_ylabel("d(Q-Qo)/dE/mA.h/V", fontsize=self.fontsize)
        ax.tick_params(axis='both', which='major', labelsize=18)
        # plt.xlabel("Ewe/V", fontsize=self.fontsize)   
        # plt.ylabel("d(Q-Qo)/dE/mA.h/V", fontsize=self.fontsize) 
        # plt.xlim(self.xlim[0], self.xlim[1])
        #ax.set_xlim(self.xlim[0], self.xlim[1])
        # plt.ylim(self.ylim[0], self.ylim[1])
        #ax.set_ylim(self.ylim[0], self.ylim[1])
        # plt.xticks(fontsize=self.fontsize)
        # plt.yticks(fontsize=self.fontsize)
        # plt.legend(bbox_to_anchor=(1, 1), fontsize = self.fontsize, labels = self.legend_labels)
        ax.legend(bbox_to_anchor=(1, 1), fontsize = self.fontsize, labels = self.legend_labels)
        #plt.rcParams.update({'font.size': 10})  
        #plt.show()

    def dqdv_single_cycle(self):

        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Load the data using pandas
        df = pd.read_csv(self.file_path, sep="\t", header=2)
        
        x = df["Ewe/V"]
        y = df["d(Q-Qo)/dE/mA.h/V"]

        # Plot the data
        #ax.plot(x, y, linewidth=0.5, color="dodgerblue")
        ax.scatter(x, y, linewidth=0.5, color="blue", marker='o', s=1)
        ax.set_xlim(self.xlim[0], self.xlim[1])
        ax.set_ylim(self.ylim[0], self.ylim[1])
        ax.set_xlabel('Ewe/V', fontsize=self.fontsize)
        ax.set_ylabel('d(Q-Qo)/dE/mA.h/V', fontsize=self.fontsize)
        ax.set_title('dQ/dV Cycle 1', fontsize=self.fontsize)
        ax.tick_params(axis='both', which='major', labelsize=self.fontsize)

        ax.legend(bbox_to_anchor=(1, 1), fontsize=self.fontsize, labels=self.legend_labels)
        # Show the plot
        plt.show()