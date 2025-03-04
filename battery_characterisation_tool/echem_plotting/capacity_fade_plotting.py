import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.colors as colors 
import os
import pandas as pd

from battery_characterisation_tool.echem_plotting.process_dataframe import ProcessDataframe
from typing import Optional


class CapacityFadePlotting:
    """
    A class to handle the plotting of capacity fade data for battery analysis.

    Attributes:
        file_path (Optional[str]): Path to the input file containing capacity data. Defaults to an empty string.
        dataset_name (Optional[str]): Name of the dataset for labeling purposes. Defaults to an empty string.
        plot_title (Optional[str]): Title of the plot. Defaults to an empty string.
        legend_labels (Optional[list]): Labels for the legend entries. Defaults to an empty list.
        active_mass (Optional[float]): The active mass value for the dataset. Defaults to 0.
        active_mass_list (Optional[list]): List of active mass values. Defaults to an empty list.
        folder_path (Optional[list]): List of folder paths to read data from. Defaults to an empty list.
        figsize (Optional[tuple]): Size of the figure for the plot. Defaults to (8, 6).
        xlim (Optional[tuple]): Limits for the x-axis of the plot. Defaults to (-2, 50.60).
        ylim (Optional[tuple]): Limits for the y-axis of the plot. Defaults to (0, 150).

    Methods:
        __init__(file_path, dataset_name, plot_title, legend_labels, active_mass, active_mass_list, folder_path, figsize, xlim, ylim):
            Initializes the CapacityFadePlotting class with the provided parameters.
        capacity_fade_ce() -> np.array:
            Generates a plot for capacity fade and Coulombic efficiency.
        _get_file_list() -> list:
            Retrieves a list of valid files in the specified folder path.
        capacity_fade() -> np.array:
            Generates a plot for capacity fade from multiple datasets.
        vc_cycle_comparison() -> np.array:
            Generates a plot comparing voltage curves across multiple cycles.
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
        xlim: Optional[tuple] = (-2, 50.60),
        ylim: Optional[tuple] = (0, 150),
        fontsize: Optional[int] = 16,
        file_names: Optional[list] = None,
        #file_names = Optional[list] = [],  # New argument
        labels: Optional[list] = None
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
        self.file_names = file_names  # New argument
        self.labels = labels 

    def capacity_fade_ce(self) -> np.array:
        """
        Generates a plot for capacity fade with Coulombic efficiency.

        This method reads capacity data from the specified file path and active mass,
        processes the data to extract the cycle number, specific discharge capacity,
        and Coulombic efficiency, and then generates a scatter plot for visual analysis.

        Returns:
            np.array: Processed data array.
        """
        fig, ax1 = plt.subplots(figsize=self.figsize)
        df = self.process_df.process_capacity_fade_df(file_path=self.file_path, 
                                                       active_mass=self.active_mass)
        x = df['cycle number']
        y1 = df['Specific Discharge Capacity mAh/g']
        y2 = df['Efficiency/%']

        ax2 = ax1.twinx()

        ax1.scatter(x, y1, marker='o', color='deepskyblue', label=self.dataset_name)
        ax2.scatter(x, y2, marker='o', color='hotpink', label="Coulombic efficiency")

        ax1.set_xlabel("Cycle Number", fontsize = self.fontsize)
        ax1.set_ylabel("Specific Discharge Capacity (mAh/g)", fontsize = self.fontsize)
        ax2.set_ylabel("Coulombic Efficiency %", color='hotpink', fontsize=self.fontsize)
        
        plt.title(self.plot_title, fontsize=self.fontsize)
        ax1.legend(bbox_to_anchor=(1.4, 1), fontsize = self.fontsize) #, loc = 'lower left'

        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        ax2.tick_params(axis='y', labelsize=10)
        ax1.set_xlim(self.xlim[0], self.xlim[1])
        ax1.set_ylim(self.ylim[0], self.ylim[1])
        ax2.set_ylim(0, 105)

    def capacity_fade_ce_neware(self) -> np.array:
        """
        Generates a plot for capacity fade with Coulombic efficiency.

        This method reads capacity data from the specified file path and active mass,
        processes the data to extract the cycle number, specific discharge capacity,
        and Coulombic efficiency, and then generates a scatter plot for visual analysis.

        Returns:
            np.array: Processed data array.
        """
        fig, ax1 = plt.subplots(figsize=self.figsize)
        df = pd.read_csv(self.file_path, header=0)
        x = df['Cycle Index']
        y1 = df['DChg. Spec. Cap.(mAh/g)']
        y2 = df['Chg.-DChg. Eff']

        ax2 = ax1.twinx()

        ax1.scatter(x, y1, marker='o', color='deepskyblue', label=self.dataset_name)
        ax2.scatter(x, y2, marker='o', color='hotpink', label="Coulombic efficiency")

        ax1.set_xlabel("Cycle Number", fontsize = self.fontsize)
        ax1.set_ylabel("Specific Discharge Capacity (mAh/g)", fontsize = self.fontsize)
        ax2.set_ylabel("Coulombic Efficiency %", color='hotpink', fontsize=self.fontsize)
        
        plt.title(self.plot_title, fontsize=self.fontsize)
        ax1.legend(bbox_to_anchor=(1.4, 1), fontsize = self.fontsize) #, loc = 'lower left'

        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        ax2.tick_params(axis='y', labelsize=16)
        ax1.tick_params(axis='y', labelsize=16)
        ax1.tick_params(axis='x', labelsize=16)
        ax1.set_xlim(self.xlim[0], self.xlim[1])
        ax1.set_ylim(self.ylim[0], self.ylim[1])
        ax2.set_ylim(0, 105)

    def _get_file_list(self) -> list:
        """
        Retrieves a list of valid files in the specified folder path.

        This method scans the folder path for files with .txt or .csv extensions
        and returns their full paths in a list.

        Returns:
            list: List of file paths with valid extensions.
        """
        arr = os.listdir(self.folder_path)
        arr = [f"{self.folder_path}\{item}" for item in arr if item.endswith((".txt", ".csv"))]
        return arr
    
    
    def capacity_fade(self) -> np.array:
        """
        Generates a plot for capacity fade from multiple datasets.

        This method processes a list of file paths and active mass values,
        extracts capacity fade data, and generates a scatter plot with different
        colors for each dataset.

        Returns:
            np.array: Processed data array.
        """
        length = len(self.file_list)
        fig, ax = plt.subplots(figsize=self.figsize)
        df = self.process_df.process_capacity_fade_df_list(file_paths=self.file_list, 
                                                    active_mass_list=self.active_mass_list)
        for i in range(length):
            x = df[f'cycle number_{i}']
            y = df[f'Specific Discharge Capacity mAh/g_{i}']

            colours = sns.color_palette('Dark2', n_colors=length)
            ax.scatter(x, y, marker='o', color=colours[i], label=self.legend_labels[i], s=10)  #label=self.dataset_name)
            ax.set_xlabel("Cycle Number", fontsize = self.fontsize)
            ax.set_ylabel("Specific Discharge Capacity mAh/g", fontsize=self.fontsize)
            plt.title(self.plot_title, fontsize = self.fontsize)
            
            ax.legend(loc = 'upper right', fontsize = (self.fontsize-4), ncol=3) #, loc = 'upper left' bbox_to_anchor=(1, 0.55)
            plt.xticks(fontsize=self.fontsize)
            plt.yticks(fontsize=self.fontsize)
            ax.tick_params(labelsize=10)

            plt.xlim(self.xlim[0], self.xlim[1])
            plt.ylim(self.ylim[0], self.ylim[1])

    def capacity_fade_percentage_biologic(self) -> np.array:
        """
        Generates a plot for % capacity fade from multiple datasets.

        This method processes a list of file paths and active mass values,
        extracts capacity fade data, and generates a scatter plot with different
        colors for each dataset.

        Returns:
            np.array: Processed data array.
        """
        length = len(self.file_list)
        fig, ax = plt.subplots(figsize=self.figsize)
        df = self.process_df.process_capacity_fade_df_list(file_paths=self.file_list, 
                                                    active_mass_list=self.active_mass_list)
        for i in range(length):
            cycle_num = df[f'cycle number_{i}']
            sdc = df[f'Specific Discharge Capacity mAh/g_{i}']
            #cycle_num= df['Cycle Index']
            #sdc = df['DChg. Spec. Cap.(mAh/g)']

            if not cycle_num.empty and not sdc.empty:
                #processed_df = df.groupby(cycle_num[0])[sdc[0]].max().reset_index() 
                processed_df = df.groupby(f'cycle number_{i}')[f'Specific Discharge Capacity mAh/g_{i}'].max().reset_index()
                
                # Get the max discharge specific capacity for Cycle 1
                #original_cycle_1_cap = processed_df[sdc[0]].iloc[0]

            
                # Get the max discharge specific capacity for Cycle 1
                original_cycle_1_cap = processed_df[f'Specific Discharge Capacity mAh/g_{i}'].max() #.iloc[0] - uses first cycle max value. .max() uses overall max value.
                
                # Calculate remaining capacity percentage
                #processed_df['Remaining Capacity (%)'] = (
                #    (processed_df[sdc[0]] / original_cycle_1_cap) * 100
                #)
                processed_df['Remaining Capacity (%)'] = (
                    (processed_df[f'Specific Discharge Capacity mAh/g_{i}'] / original_cycle_1_cap) * 100
                )   

            colours = sns.color_palette('Dark2', n_colors=length)
            #ax.scatter(processed_df[cycle_num[0]], processed_df['Remaining Capacity (%)'], marker='o', color=colours[i], label=self.legend_labels[i], s=10)  #label=self.dataset_name)
            ax.scatter(processed_df[f'cycle number_{i}'], processed_df['Remaining Capacity (%)'], 
                       marker='o', color=colours[i], label=self.legend_labels[i], s=10)  
            ax.set_xlabel("Cycle Number", fontsize = self.fontsize)
            ax.set_ylabel("Discharge Capacity Fade (%)", fontsize=self.fontsize)
            plt.title(self.plot_title, fontsize = self.fontsize)
            
            ax.legend(loc = 'lower left', fontsize = (self.fontsize-4), ncol=3) #, loc = 'upper left' bbox_to_anchor=(1, 0.55)
            plt.xticks(fontsize=self.fontsize)
            plt.yticks(fontsize=self.fontsize)
            ax.tick_params(labelsize=10)

            plt.xlim(self.xlim[0], self.xlim[1])
            plt.ylim(self.ylim[0], self.ylim[1])

    def energy_fade(self) -> np.array:
        """
        Generates a plot for capacity fade from multiple datasets.

        This method processes a list of file paths and active mass values,
        extracts capacity fade data, and generates a scatter plot with different
        colors for each dataset.

        Returns:
            np.array: Processed data array.
        """
        length = len(self.file_list)
        fig, ax = plt.subplots(figsize=self.figsize)

        # Get the list of DataFrames (passing the file paths and active masses)
        all_data = self.process_df.process_energy_fade_df_list(file_paths=self.file_list, 
                                                            active_mass_list=self.active_mass_list)
        #print("Columns in processed DataFrame:", all_data.columns.tolist())

        # Loop over each DataFrame and plot the data
        """
        colours = sns.color_palette('Dark2', n_colors=length)
        for i, df in enumerate(all_data):
            x = df['cycle number']
            y = df['Energy discharge/mW.h/g']

            ax.scatter(x, y, marker='o', color=colours[i], label=self.legend_labels[i], s=10)
            ax.set_xlabel("Cycle Number", fontsize=self.fontsize)
            ax.set_ylabel("Specific Energy (Discharge) mW.h/g", fontsize=self.fontsize)
            ax.set_title(self.plot_title, fontsize=self.fontsize)
            
            ax.legend(loc='upper right', fontsize=(self.fontsize - 4), ncol=3)
            plt.xticks(fontsize=self.fontsize)
            plt.yticks(fontsize=self.fontsize)
            ax.tick_params(labelsize=10)

            plt.xlim(self.xlim[0], self.xlim[1])
            plt.ylim(self.ylim[0], self.ylim[1])

        # You can return the processed data if needed (for now, returning None)
        return np.array([df[['cycle number', 'Energy discharge/mW.h/g']].values for df in all_data])
        """

        for i in range(length):
            x = all_data[f'cycle number_{i}']
            y = all_data[f'Spec. Energy(mWh/g)_{i}']

            y = y.abs()

            colours = sns.color_palette('Dark2', n_colors=length)
            ax.scatter(x, y, marker='o', color=colours[i], label=self.legend_labels[i], s=10)
            ax.set_xlabel("Cycle Number", fontsize=self.fontsize)
            ax.set_ylabel("Specific Energy (Discharge) mWh/g", fontsize=self.fontsize)
            ax.set_title(self.plot_title, fontsize=self.fontsize)

            ax.legend(loc='upper right', fontsize=(self.fontsize - 4), ncol=3)
            plt.xticks(fontsize=self.fontsize)
            plt.yticks(fontsize=self.fontsize)
            ax.tick_params(labelsize=10)

            plt.xlim(self.xlim[0], self.xlim[1])
            plt.ylim(self.ylim[0], self.ylim[1])

    #def capacity_fade_neware(self) -> np.array:
    def capacity_fade_neware(self, folder_path, file_names, labels): #(self, folder_path: str, file_names: list, labels: list):
        """
        Generates a plot for capacity fade from multiple datasets stored as CSV files.

        This method reads CSV files from the specified folder, processes them to extract
        capacity fade data, and generates a scatter plot with different colors for each dataset.

        Args:
            folder_path (str): Path to the folder containing the CSV files.
            file_names (list): A list of CSV file names (strings) to be loaded.
            labels (list): A list of labels for each dataset to be used in the plot legend.

        Returns:
            None: Displays the plot.
        """
        # Create an empty list to hold the dataframes
        datasets = []

        # Load each CSV file into a DataFrame and append to datasets list
        for file_name in file_names:
            file_path = os.path.join(folder_path, file_name)  # Construct full file path
            df = pd.read_csv(file_path)  # Read CSV into DataFrame
            datasets.append(df)  # Add DataFrame to the list

        # Now plot the datasets
        length = len(datasets)
        fig, ax = plt.subplots(figsize=(7, 6))

        # Iterate over each dataset and plot it
        for i, df in enumerate(datasets):
            x = df['Cycle Index']
            y = df['DChg. Spec. Cap.(mAh/g)']

            # Use seaborn color palette to differentiate each dataset
            colours = sns.color_palette('Dark2', n_colors=length)
            ax.scatter(x, y, marker='o', color=colours[i], label=labels[i], s=15)

        # Set axis labels, title, and legend
        ax.set_xlabel("Cycle Number", fontsize=self.fontsize)
        ax.set_ylabel("Specific Discharge Capacity mAh/g", fontsize=self.fontsize)
        plt.title(self.plot_title, fontsize=self.fontsize)

        # Legend and other aesthetic settings
        ax.legend(loc='lower right', fontsize=(self.fontsize-4), ncol=2)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        ax.tick_params(labelsize=10)

        # Set axis limits if needed
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])

    def dqdv_capacity_fade_both(self):
        """
        Generates a plot with specific cycle datasets listed in the folder_path.
        """
        files = self._get_file_list()
        print("Files to be plotted:", files)

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
            plt.scatter(x, y, s = 15, color=palette[idx], marker='o') #label="dQ/dV vs Voltage", 
        plt.xlabel("Cycle Number", fontsize = self.fontsize)
        plt.ylabel("Specific Discharge Capacity (mAh/g)", fontsize = self.fontsize)
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])
        plt.title(label=self.plot_title, fontsize=self.fontsize)
        plt.legend(loc = "lower right", fontsize = self.fontsize - 4 , labels = self.legend_labels, ncol =2) # bbox_to_anchor = (1,1)
        #ax.legend(loc = 'lower right', fontsize = (self.fontsize-4), ncol=2)
        #plt.grid(True)
        plt.tick_params(axis='both', which='major', labelsize=self.fontsize)
        #plt.show()



    def vc_cycle_comparison(self) -> np.array:
        """
        Generates a plot comparing voltage curves across a specific cycle.

        This method processes voltage-capacity data from the specified file path and active mass list,
        removes large voltage values, and generates a scatter plot comparing the voltage curves
        for each dataset.

        Returns:
            np.array: Processed data array.
        """
        length = len(self.active_mass_list)
        fig, ax = plt.subplots(figsize=(self.figsize))
        df = self.process_df.process_vc_cycle_comparison_df(file_path=self.file_path, 
                                                    active_mass_list=self.active_mass_list)
        df = self.process_df.remove_large_voltage_values(df)
        #df = self.process_df.remove_ocv_voltage_values(df)
        for i in range(length):
            x = df.iloc[:, 2*i].rolling(100).mean()
            y = df.iloc[:, 2*i+1] #.rolling(50).mean()

            colours = sns.color_palette('Dark2', n_colors=length)
            # TODO: Add in support for colour continuity of larger series
            #colours = sns.color_palette('Dark2', n_colors=length+3)
            #ax.scatter(x, y, color=colours[i+3], label=self.legend_labels[i], s=10, marker='_')
            #ax.scatter(x, y, color=colours[i], label=self.legend_labels[i], s=10, marker='_')
            ax.plot(x, y, color=colours[i], label=self.legend_labels[i], linewidth =1.5)
            ax.set_xlabel("Specific Capacity (mAh/g)", fontsize = self.fontsize)
            ax.set_ylabel("Voltage (V)", fontsize=self.fontsize)
            ax.tick_params(labelsize=10)
            plt.xlim(self.xlim[0], self.xlim[1])
            plt.ylim(self.ylim[0], self.ylim[1])
            plt.title(self.plot_title, fontsize = self.fontsize)
            ax.legend(bbox_to_anchor=(1, 0.9), fontsize = (self.fontsize-4), markerscale=2.5) #, loc = 'upper left'
            #ax.legend(loc = 'upper right', fontsize = (self.fontsize-4), markerscale=5) 

    def dqdv_cycle_comparison(self) -> np.array:
        """
        Generates a plot comparing voltage curves across a specific cycle.

        This method processes voltage-capacity data from the specified file path and active mass list,
        removes large voltage values, and generates a scatter plot comparing the voltage curves
        for each dataset.

        Returns:
            np.array: Processed data array.
        """

        df = pd.read_csv(self.file_path)

        length = len(self.legend_labels)
        fig, ax = plt.subplots(figsize=(7,6))
        #df = self.process_df.process_vc_cycle_comparison_df(file_path=self.file_path, 
                                                    #active_mass_list=self.active_mass_list)
        #df = self.process_df.remove_large_voltage_values(df)
        for i in range(length):
            x = df.iloc[:, 2*i]
            y = df.iloc[:, 2*i+1]

            colours = sns.color_palette('Dark2', n_colors=length)
            # TODO: Add in support for colour continuity of larger series
            #colours = sns.color_palette('Dark2', n_colors=length+3)
            #ax.scatter(x, y, color=colours[i+3], label=self.legend_labels[i], s=10, marker='_')
            ax.plot(x, y, color=colours[i], label=self.legend_labels[i])
            ax.set_xlabel("Voltage (V)", fontsize = self.fontsize)
            ax.set_ylabel("dQ/dV (mAh/V)", fontsize=self.fontsize)
            ax.tick_params(labelsize=10)
            plt.xlim(self.xlim[0], self.xlim[1])
            plt.ylim(self.ylim[0], self.ylim[1])
            plt.title(self.plot_title, fontsize = self.fontsize)
            ax.legend(bbox_to_anchor=(1, 1), fontsize = (self.fontsize-4), markerscale=5) #, loc = 'upper left'
            ax.legend(loc = 'lower right', fontsize = (self.fontsize-4), markerscale=5) 

    def dqdv_vc_comparison_both(self): #this function works with editing to the raw data files to allow biologic and neware to work together. Need to to update read me with how this works!
        """
        Generates a plot with specific cycle datasets listed in the folder_path.
        """
        files = self._get_file_list()
        print("Files to be plotted:", files)

        palette = sns.color_palette("Dark2", len(files))  # Choose a palette and set number of colors

        plt.figure(figsize=self.figsize)
        #fig, ax = plt.subplots(figsize=self.figsize)

        for idx, file in enumerate(files):
            path = os.path.join(self.folder_path, file)
            # Check if the file has a header (skip_header_value = 1 means it has a header)
            skip_header_value = self.process_df.check_file_header_present(path)
            #df = self.process_df.remove_large_voltage_values(df)
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
            
            x = df.iloc[1:,1].astype(float) #.astype(float) is used to ensure that the data in the selected columns (x and y) are explicitly converted to numeric values (floating-point numbers).
            y = df.iloc[1:,0].astype(float)
            plt.scatter(x, y, s = 1, color=palette[idx], ) #label="dQ/dV vs Voltage", 
        plt.ylabel("Voltage (V)", fontsize = self.fontsize)
        plt.xlabel("Specific Discharge Capacity (mAh/g)", fontsize = self.fontsize)
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])
        plt.title(label=self.plot_title, fontsize=self.fontsize)
        plt.legend(loc = "center right", fontsize = self.fontsize - 4 , labels = self.legend_labels, markerscale=5) # bbox_to_anchor = (1,1)
        #ax.legend(loc = 'lower right', fontsize = (self.fontsize-4), ncol=2)
        #plt.grid(True)
        plt.tick_params(axis='both', which='major', labelsize=self.fontsize)
        #plt.show()

    def vc_cycle_comparison_neware(self) -> np.array:
        """
        Generates a plot comparing voltage curves across a specific cycle.

        This method processes voltage-capacity data from the specified file path and active mass list,
        removes large voltage values, and generates a scatter plot comparing the voltage curves
        for each dataset.

        Returns:
            np.array: Processed data array.
        """

        fig, ax = plt.subplots(figsize= self.figsize)
        self.df = pd.read_csv(self.file_path, header=1)
        self.df = self.process_df.remove_large_voltage_values_2_4V(self.df)
        length = len(self.df.columns) // 2
        
        for i in range(length):
            x = self.df.iloc[:, 2*i]
            y = self.df.iloc[:, 2*i+1]

            colours = sns.color_palette('Dark2', n_colors=length)
            # TODO: Add in support for colour continuity of larger series
            #ax.scatter(x, y, color=colours[i], label=self.legend_labels[i], s=10, marker='_')
            ax.plot(x, y, color=colours[i], label=self.legend_labels[i], linewidth = 2)
            ax.set_xlabel("Specific Capacity (mAh/g)", fontsize = self.fontsize)
            ax.set_ylabel("Voltage (V)", fontsize=self.fontsize)
            ax.tick_params(labelsize=10)
            plt.xlim(self.xlim[0], self.xlim[1])
            plt.ylim(self.ylim[0], self.ylim[1])
            plt.title(self.plot_title, fontsize = self.fontsize)
            ax.legend(bbox_to_anchor=(0.75, 0.7), fontsize = (self.fontsize-4), markerscale=5) #, loc = 'upper left'
            #ax.legend(loc = 'center right', fontsize = (self.fontsize-4), markerscale=5) 

    def capacity_fade_neware_percentage(self, folder_path, file_names, labels): #(self, folder_path: str, file_names: list, labels: list):
        """
        Generates a plot for capacity fade from multiple datasets stored as CSV files.

        This method reads CSV files from the specified folder, processes them to extract
        capacity fade data, and generates a scatter plot with different colors for each dataset.

        Args:
            folder_path (str): Path to the folder containing the CSV files.
            file_names (list): A list of CSV file names (strings) to be loaded.
            labels (list): A list of labels for each dataset to be used in the plot legend.

        Returns:
            None: Displays the plot.
        """
        # Create an empty list to hold the dataframes
        datasets = []

        # Load each CSV file into a DataFrame and append to datasets list
        for file_name in file_names:
            file_path = os.path.join(folder_path, file_name)  # Construct full file path
            df = pd.read_csv(file_path)  # Read CSV into DataFrame
            datasets.append(df)  # Add DataFrame to the list

        # Now plot the datasets
        length = len(datasets)
        fig, ax = plt.subplots(figsize=(7, 6))

        # Iterate over each dataset and plot it
        for i, df in enumerate(datasets):
            x = df['Cycle Index']
            y = df['DChg. Spec. Cap.(mAh/g)']

            # Use seaborn color palette to differentiate each dataset
            colours = sns.color_palette('Dark2', n_colors=length)
            ax.scatter(x, y, marker='o', color=colours[i], label=labels[i], s=15)

        # Set axis labels, title, and legend
        ax.set_xlabel("Cycle Number", fontsize=self.fontsize)
        ax.set_ylabel("Specific Discharge Capacity mAh/g", fontsize=self.fontsize)
        plt.title(self.plot_title, fontsize=self.fontsize)

        # Legend and other aesthetic settings
        ax.legend(loc='lower right', fontsize=(self.fontsize-4), ncol=2)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        ax.tick_params(labelsize=10)

        # Set axis limits if needed
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])
    
    
    def dchg_spec_cap_remaining_neware_folder(self):
        # Initialize the plot
        plt.figure(figsize=self.figsize)  # Example: (10, 6)

        colors = sns.color_palette("Dark2", len(self.file_list))
        
        for idx, file_path in enumerate(self.file_list):
            print(f"Processing file: {file_path}")
            try:
                # Read the CSV file
                df = pd.read_csv(file_path)
                
                # Extract relevant columns
                dchg_spec_cap_columns = [col for col in df.columns if col.startswith("DChg. Spec. Cap.")]
                cycle_columns = [col for col in df.columns if col.startswith("Cycle Index")]
                
                if dchg_spec_cap_columns and cycle_columns:
                    # Process data
                    processed_df = df.groupby(cycle_columns[0])[dchg_spec_cap_columns[0]].max().reset_index()
                    
                    # Adjust for formation cycles if needed
                    processed_df[cycle_columns[0]] = processed_df[cycle_columns[0]] - 5
                    
                    # Get the max discharge specific capacity for Cycle 1
                    original_cycle_1_cap = processed_df[dchg_spec_cap_columns[0]].max() #.iloc[0] #max indicates normalized to 100% in plot
                    
                    # Calculate remaining capacity percentage
                    processed_df['Remaining Capacity (%)'] = (
                        (processed_df[dchg_spec_cap_columns[0]] / original_cycle_1_cap) * 100
                    )
                    
                    # Plot the remaining capacity percentage
                    plt.scatter(
                        processed_df[cycle_columns[0]], 
                        processed_df['Remaining Capacity (%)'], 
                        s=10, 
                        label=os.path.basename(file_path),
                        color=colors[idx]
                    )
                else:
                    print(f"Skipped file {file_path}: Required columns not found.")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
        
        # Customize the plot
        plt.ylabel('Discharge Capacity Fade (%)', fontsize=self.fontsize)
        plt.xlabel('Cycle Index', fontsize=self.fontsize)
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])
        plt.tick_params(axis='both', which='major', labelsize=self.fontsize)
        plt.title(label=self.plot_title, fontsize=self.fontsize)
        #plt.legend(bbox_to_anchor=(1, 1), fontsize=self.fontsize-4, labels=self.legend_labels, ncol=2)
        plt.legend(loc='lower left', fontsize=(self.fontsize-4), labels=self.legend_labels, ncol=2)
        #plt.grid(True)
        plt.show()

