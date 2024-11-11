import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as colors 
import os

from battery_characterisation_tool.echem_plotting.process_dataframe import ProcessDataframe
from typing import Optional


class RateCapabilityPlotting:
    def __init__(
        self, 
        file_path: Optional[str] = "",
        dataset_name: Optional[str] = "",
        plot_title: Optional[str] = "",
        legend_labels: Optional[list] = [],
        active_mass: Optional[float] = 0,
        active_mass_list: Optional[list] = [],
        #markers_colour: ,
        #markers_shape: ,
        folder_path: Optional[list] = [],
        figsize: Optional[tuple] = (10,8),
        xlim: Optional[tuple] = (-2, 50.60),
        ylim: Optional[tuple] = (0, 150),
        fontsize: Optional[int] = 16,
    ):
    
        self.file_path = file_path
        self.dataset_name = dataset_name
        self.plot_title = plot_title
        self.legend_labels = legend_labels
        self.active_mass = active_mass
        self.active_mass_list = active_mass_list
        #self.markers_colour = 
        #self.markers_shape =
        self.folder_path = folder_path
        self.figsize = figsize
        self.xlim = xlim
        self.ylim = ylim
        self.fontsize = fontsize
        if folder_path != []:    
            self.file_list = self._get_file_list()
        self.process_df = ProcessDataframe()


    def _get_file_list(self) -> list:
        arr = os.listdir(self.folder_path)
        arr = [f"{self.folder_path}\{item}" for item in arr if item.endswith((".txt", ".csv"))]
        return arr

    def rate_capability(self):
        df = self.process_df.process_capacity_fade_df_list(file_paths=self.file_list, 
                                                active_mass_list=self.active_mass_list)
        
        length = len(self.file_list)
        plt.rcParams['font.family'] = 'calibri'
        fig, ax = plt.subplots(figsize=self.figsize)
        plt.title(self.plot_title, fontsize = self.fontsize)
        for i in range(length):
            x = df[f'cycle number_{i}']
            y = df[f'Specific Discharge Capacity mAh/g_{i}']

            colours = sns.color_palette('Dark2', n_colors=length)
            markers = ['o', 'o', 'o', 'o', 'o', 'o'] 
            # TODO:  - work out whether markers should be user defined/inputted
            ax.scatter(x, y, marker=markers[i], color=colours[i], label=self.legend_labels[i], s=30)  #label=self.dataset_name)
        ax.set_xlabel("Cycle Number", fontsize = self.fontsize+2)
        ax.set_ylabel("Specific Discharge Capacity mAh/g", fontsize=self.fontsize+4)
        plt.title(self.plot_title, fontsize = self.fontsize)
        ax.text(0, 140, "C/10", fontsize=self.fontsize-4)
        ax.text(6, 140, "C/5", fontsize=self.fontsize-4)
        ax.text(11, 140, "C/2", fontsize=self.fontsize-4)
        ax.text(17, 140, "C", fontsize=self.fontsize-4)
        ax.text(22, 140, "2C", fontsize=self.fontsize-4)
        ax.text(27, 140, "5C", fontsize=self.fontsize-4)
        ax.text(31, 140, "C/5", fontsize=self.fontsize-4)
        ax.legend(bbox_to_anchor=(1, 0.4), fontsize = (self.fontsize)) #, loc = 'upper left'
        ax.tick_params(labelsize=20)
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])

        #for Neware - inserted a column on cycle index to add 0 - that way all rates align (before they were shifted across 1 cycle due to cycles starting at 1 vs biologic starting at cycle 0)
