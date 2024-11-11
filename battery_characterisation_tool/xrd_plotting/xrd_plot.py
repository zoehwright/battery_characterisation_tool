import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as colors
import pandas as pd
import seaborn as sns
import glob as glob
import os
import sympy
import matplotlib
import scipy as scipy
from matplotlib import gridspec
from typing import Optional, Tuple

class XRDPlotter:
    def __init__(
        self,
        dataset_name: Optional [str] = "",
        #data now = dataset_name
        file_path: Optional[str] = "",
        plot_title: Optional[str] = "",
        label: Optional[str] = "",
        legend_labels: Optional[list] = [],
        folder_path: Optional[list] = [],
        figsize: Optional[tuple] = (10, 8),
        fontsize: Optional[int] = 16,
        xlim: Optional[tuple] = (0, 90),
        ylim: Optional[tuple] = (100, 1500),
        xlabel: Optional[str] = r"2$\theta$ / °",
        ylabel: Optional[str] = "Intensity",
        offsets: Optional[int] = [0, 100000, 200000, 300000], 
        transformation_type: Optional[str] = "",
        zoom_x_limit: Optional[int] = 16,
        zoom_width: Optional[int] = 10,

    ):
        self.dataset_name = dataset_name
        self.file_path = file_path
        self.plot_title = plot_title
        self.label = label
        self.legend_labels = legend_labels
        self.folder_path = folder_path
        self.figsize = figsize
        self.fontsize = fontsize
        self.xlim = xlim
        self.ylim = ylim
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.offsets = offsets
        self.transformation_type = transformation_type
        self.zoom_x_limit= zoom_x_limit
        self.zoom_width = zoom_width

    def _get_file_list(self) -> list:
        arr = os.listdir(self.folder_path)
        arr = [f"{self.folder_path}\{item}" for item in arr if item.endswith((".xye", ".dat", ".asc"))]
        return arr    
    
    def transformation_y(self, y):
        if self.transformation_type == "sqrt":
            return np.sqrt(y)
        elif self.transformation_type == "log":
            return np.log(y)
        else:
            return y

    #def convert_to_d(self):
     #   df = np.loadtxt(self.file_path, delimiter=' ', encoding= 'unicode_escape')
      #  x_2theta = df[:, 0]
       # self.x_d = self.wavel/(2*np.sin(np.radians(self.x_2theta)/2))

    #def convert_to_Q(self):
     #   df = np.loadtxt(self.file_path, delimiter=' ', encoding= 'unicode_escape')
      #  x_2theta = df[:, 0]
       # self.x_Q=(4*np.pi*np.sin(np.radians(self.x_2theta)/2)/self.wavel) 

    def convert_to_Q(self):
        # Extract the first column as x_2theta
        df = np.loadtxt(self.file_path, delimiter=' ', encoding= 'unicode_escape')

        x_2theta = df[:, 0]

        # Specify the wavelength
        wavel = 0.8239868  # This value should come from the Si input file.

        # Calculate x_Q
        x_Q = (4 * np.pi * np.sin(np.radians(x_2theta) / 2)) / wavel

        # Create a new NumPy array where x_2theta is replaced with x_Q
        # Copy the original data to avoid modifying it directly
        new_data = df.copy()

        # Replace the first column (x_2theta) with the calculated x_Q values
        new_data[:, 0] = x_Q
        #print(new_data)
 

    def raw_xye_plot(self):
       #df = self(file_path=self.file_path,)
        df = np.loadtxt(self.file_path, delimiter=' ', encoding= 'unicode_escape')
        x = df[:, 0]
        y = self.transformation_y(df[:, 1])
        #y_calc = data[:, 2]

        plt.rcParams['font.family']='serif'

        plt.figure(figsize=self.figsize)
        plt.plot(x, y, label=self.label, linewidth = 0.5) #, color = self.color
        #plt.plot(x, y_calc, label='Calculated{self.label}', linewidth = 0.5, color = self.color)
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])

        plt.title(self.plot_title, fontsize=self.fontsize)
        plt.xlabel(self.xlabel, fontsize=self.fontsize)
        plt.ylabel(self.ylabel, fontsize=self.fontsize)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        plt.legend(self.legend_labels, bbox_to_anchor=(1.4, 1), fontsize = self.fontsize)
        plt.show()

    def raw_xye_plot_in_d(self):
       #df = self(file_path=self.file_path,)
        df = np.loadtxt(self.file_path, delimiter=' ', encoding= 'unicode_escape')
        #x = df[:, 0]
        x_d = df[:, 0]
        y = self.transformation_y(df[:, 1])
        #y_calc = data[:, 2]

        plt.rcParams['font.family']='serif'

        plt.figure(figsize=self.figsize)
        plt.plot(x_d, y, label=self.label, linewidth = 0.5) #, color = self.color
        #plt.plot(x, y_calc, label='Calculated{self.label}', linewidth = 0.5, color = self.color)
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])

        plt.title(self.plot_title, fontsize=self.fontsize)
        plt.xlabel(self.xlabel, fontsize=self.fontsize)
        plt.ylabel(self.ylabel, fontsize=self.fontsize)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        plt.legend(self.legend_labels, bbox_to_anchor=(1.4, 1), fontsize = self.fontsize)
        plt.show()

    def raw_xye_plot_inQ(self):
       #df = self(file_path=self.file_path,)
        df = np.loadtxt(self.file_path, delimiter=' ', encoding= 'unicode_escape')
        #x = df[:, 0]
        x_Q = new_df[:, 0]
        y = self.transformation_y(df[:, 1])
        #y_calc = data[:, 2]

        plt.rcParams['font.family']='serif'

        plt.figure(figsize=self.figsize)
        plt.plot(x_Q, y, label=self.label, linewidth = 0.5) #, color = self.color
        #plt.plot(x, y_calc, label='Calculated{self.label}', linewidth = 0.5, color = self.color)
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])

        plt.title(self.plot_title, fontsize=self.fontsize)
        plt.xlabel(self.xlabel, fontsize=self.fontsize)
        plt.ylabel(self.ylabel, fontsize=self.fontsize)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        plt.legend(self.legend_labels, bbox_to_anchor=(1.4, 1), fontsize = self.fontsize)
        plt.show()

    def raw_xye_plot_zoom(self):
        df = np.loadtxt(self.file_path, delimiter=' ', encoding= 'unicode_escape')
        x = df[:, 0]
        y_obs = df[:, 1]

        plt.rcParams['font.family']='serif'
        fig, ax = plt.subplots(2, 1, figsize=(16, 10))

        for i in range(2):
            ax[i].plot(x, y_obs, linewidth=0.5, color='black') #, label='Observed pattern')
            ax[i].set_xlabel(r'2$\theta$ / °', fontsize=self.fontsize)
            ax[i].yaxis.set_ticklabels([])
            ax[i].yaxis.set_ticks([])
        ax[0].set_xlim(self.xlim[0], self.xlim[1])
        ax[1].set_xlim(self.zoom_x_limit, self.zoom_width+self.zoom_x_limit)
        ax[1].set_ylim(self.ylim[0], self.ylim[1]) #-100,700000)
        #TODO fix the rectangle patches
        rect = patches.Rectangle((16, -2000000), 11, self.ylim[0], linewidth=2, edgecolor='blue', facecolor='cyan', alpha=0.1)
        ax[0].add_patch(rect)
        rect = patches.Rectangle((12, -200), 200, self.ylim[1], linewidth=2, edgecolor='blue', facecolor='cyan', alpha=0.1)
        ax[1].add_patch(rect)
        plt.subplots_adjust(hspace=0.3)      #This adjusts the space between the two plots
        ax[0].set_ylabel('Intensity', fontsize=self.fontsize)
        ax[1].set_ylabel('Intensity', fontsize=self.fontsize)

        ax[0].tick_params(axis='x', labelsize=self.fontsize)
        ax[0].tick_params(axis='y', labelsize=self.fontsize)
        ax[1].tick_params(axis='x', labelsize=self.fontsize)
        ax[1].tick_params(axis='y', labelsize=self.fontsize)

        ax[0].legend(self.legend_labels, bbox_to_anchor=(1, 1.05), loc='upper left', fontsize=self.fontsize)
        plt.tight_layout()

    def read_data(self, file_path):
        """Reads data from a given file path."""
        try:
            return np.loadtxt(file_path, delimiter=' ', encoding='unicode_escape')
        except Exception as e:
            print(f"Error reading data file {file_path}: {e}")
            return pd.DataFrame()
    
    def read_data_csv(self, file_path):
        try:
            return pd.read_csv(file_path, delimiter=r'\s+', header=None, encoding='unicode_escape')
        except Exception as e:
            print(f"Error reading CSV file {file_path}: {e}")
            return np.array([])
    
    def plot_stacked_datasets(self):
        """Plots multiple datasets with offsets on the same figure."""
        plt.rcParams['font.family'] = 'serif'
        plt.figure(figsize=self.figsize)

        for i, filename in enumerate(self._get_file_list()):
            if filename.endswith('.xye') or filename.endswith('.asc') or filename.endswith('.dat'):
                file_path = os.path.join(self.folder_path, filename)
                data = self.read_data(file_path)
                x = data[:, 0]
                y = self.transformation_y(data[:, 1]) + self.offsets[i]  # Apply offset to y-values

                plt.plot(x, y, label=self.legend_labels[i], linewidth=0.5)
        
        # Set plot limits and labels
        plt.xlim(self.xlim)
        plt.ylim(self.ylim)
        plt.title(self.plot_title, fontsize=self.fontsize)
        plt.xlabel(self.xlabel, fontsize=self.fontsize)
        plt.ylabel(self.ylabel, fontsize=self.fontsize)
        plt.legend()
        plt.show()        

    def rietveld_refinement_plot(self):
        df = pd.read_csv(self.file_path, delimiter=r'\s+', header=None, encoding='unicode_escape')  #, delimiter=' ', encoding='unicode_escape')
    
        # Debugging steps
        # print("DataFrame shape:", df.shape)
        # print("First few rows of the DataFrame:")
        # print(df.head())
        
        # Check if the DataFrame has at least three columns
        # if df.shape[1] < 3:
        #     raise ValueError("DataFrame does not have enough columns. Expected at least 3 columns.")
        
        # Ensure the columns are accessible
        
        x = df.iloc[:, 0]
        y_obs = self.transformation_y(df.iloc[:, 1])
        y_calc = self.transformation_y(df.iloc[:, 2])
        # except IndexError as e:
        #      print(f"Index error: {e}")
        #      return

        plt.rcParams['font.family'] = 'serif'

        plt.figure(figsize=self.figsize)
        plt.plot(x, y_obs, label=self.label, linewidth=0.5, color='black')
        plt.plot(x, y_calc, label=f'Calculated {self.label}', linewidth=1, linestyle='--', color='red')
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])

        plt.title(self.plot_title, fontsize=self.fontsize)
        plt.xlabel(self.xlabel, fontsize=self.fontsize)
        plt.ylabel(self.ylabel, fontsize=self.fontsize)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        plt.legend(self.legend_labels, bbox_to_anchor=(1, 1), fontsize=self.fontsize)
        plt.show()

    def rietveld_refinement_with_ticks(self):
        #TODO generate files with ticks in a folder with a single .asc refinement then test - need to add in the ticks and offset section too. 
        #df = pd.read_csv(self.file_path, delimiter=r'\s+', header=None, encoding='unicode_escape')
        
        # df = pd.read_csv(self.file_path, delimiter=r'\s+', header=None, encoding='unicode_escape')  #, delimiter=' ', encoding='unicode_escape')
        
        # x = df.iloc[:, 0]
        # y_obs = self.transformation_y(df.iloc[:, 1])
        # y_calc = self.transformation_y(df.iloc[:, 2])
        # # except IndexError as e:
        # #      print(f"Index error: {e}")
        # #      return

        # plt.rcParams['font.family'] = 'serif'

        # plt.figure(figsize=self.figsize)
        # plt.plot(x, y_obs, label=self.label, linewidth=0.5, color='black')
        # plt.plot(x, y_calc, label=f'Calculated {self.label}', linewidth=1, linestyle='--', color='red')
        # plt.xlim(self.xlim[0], self.xlim[1])
        # plt.ylim(self.ylim[0], self.ylim[1])

        # plt.title(self.plot_title, fontsize=self.fontsize)
        # plt.xlabel(self.xlabel, fontsize=self.fontsize)
        # plt.ylabel(self.ylabel, fontsize=self.fontsize)
        # plt.xticks(fontsize=self.fontsize)
        # plt.yticks(fontsize=self.fontsize)
        # plt.legend(self.legend_labels, bbox_to_anchor=(1, 1), fontsize=self.fontsize)
        # plt.show()

        plt.rcParams['font.family'] = 'serif'
        plt.figure(figsize=self.figsize)

        # print("Reading files and plotting data...")
        # file_list = self._get_file_list()
        # print(f"Files found: {file_list}")

        pattern = "ticks"

        for i, filename in enumerate(self._get_file_list()):
            if "ticks" in filename and (filename.endswith('.asc')):
                file_path = os.path.join(self.folder_path, filename)
                data = self.read_data_csv(file_path)
                if isinstance(data, np.ndarray):
                    x = data[:, 0]   # Apply offset to y-values
                    y = data[:, 1] + self.offsets[i]
                    plt.plot(x, y, linewidth=0.5, marker='|') #label=self.legend_labels[i]
        #    elseif "ticks" not in filename and filename.endswith('.asc'):

        for i, filename in enumerate(self._get_file_list()):
             if "ticks" not in filename and filename.endswith('.asc'):
                 file_path = os.path.join(self.folder_path, filename)
                 data = self.read_data(file_path)
                 if isinstance(data, pd.DataFrame):
                     x = data.iloc[:, 0]
                     y_obs = self.transformation_y(data.iloc[:, 1]) + self.offsets[i]
                     y_calc = self.transformation_y(data.iloc[:, 2]) + self.offsets[i]

                     plt.plot(x, y_obs, label=self.label, linewidth=0.5, color='black')
                     plt.plot(x, y_calc, label=f'Calculated {self.label}', linewidth=1, linestyle='--', color='red')

        #plt.figure(figsize=self.figsize)
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])

        plt.title(self.plot_title, fontsize=self.fontsize)
        plt.xlabel(self.xlabel, fontsize=self.fontsize)
        plt.ylabel(self.ylabel, fontsize=self.fontsize)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        plt.legend(self.legend_labels, bbox_to_anchor=(1, 1), fontsize=self.fontsize)
        plt.show()    

    def rietveld_stacked(self):
        """Plots multiple datasets with offsets on the same figure."""
        plt.rcParams['font.family'] = 'serif'
        plt.figure(figsize=self.figsize)

        for i, filename in enumerate(self._get_file_list()):
            if filename.endswith('.xye') or filename.endswith('.asc') or filename.endswith('.dat'):
                file_path = os.path.join(self.folder_path, filename)
                data = self.read_data_csv(file_path)
                x = data.iloc[:, 0]
                y_obs = self.transformation_y(data.iloc[:, 1]) + self.offsets[i]  # Apply offset to y-values
                y_calc = self.transformation_y(data.iloc[:, 2]) + self.offsets[i] 
                plt.plot(x, y_obs, label="Observed " + self.legend_labels[i], linewidth=0.5)
                plt.plot(x, y_calc, label="Calculated " + self.legend_labels[i], linewidth=1, linestyle="--")
        #TODO duplicate this function but for with ticks - use above for loop but add in function to search for files with ticks in their file name and create a separate offset function for ticks stacking at bottom of plot
        # Set plot limits and labels
        plt.xlim(self.xlim)
        plt.ylim(self.ylim)
        plt.title(self.plot_title, fontsize=self.fontsize)
        plt.xlabel(self.xlabel, fontsize=self.fontsize)
        plt.ylabel(self.ylabel, fontsize=self.fontsize)
        plt.legend()
        plt.show()  

    def rietveld_difference_plot(self):
        df = pd.read_csv(self.file_path, delimiter=r'\s+', header=None, encoding='unicode_escape')  #, delimiter=' ', encoding='unicode_escape')

        x = df.iloc[:, 0]
        y_obs = self.transformation_y(df.iloc[:, 1])
        y_calc = self.transformation_y(df.iloc[:, 2])
        diff = df.iloc[:, 3]
        
        fig = plt.figure(figsize=(10,4))
        gs = gridspec.GridSpec(2,1, height_ratios=[1,0.25])
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        #gs.update(hspace=0) 

        ax1.plot(x, y_obs, 'b.', label='Measured', ms=0.5)
        ax1.plot(x, y_calc, 'r-', label='Calculated', linestyle="--")

        # residual
        ax2.plot(x, diff, "0.4", label='Difference')

        ax1.set_xlim(self.xlim[0], self.xlim[1])
        ax2.set_xlim(self.xlim[0], self.xlim[1])
        #ax2.set_ylim(self.ylim[0], self.ylim[1])

        ax2.set_xlabel(self.xlabel,family="serif",  fontsize=self.fontsize)
        ax1.set_ylabel(self.ylabel,family="serif",  fontsize=self.fontsize)
        ax2.set_ylabel("Difference",family="serif",  fontsize=self.fontsize)

        ax1.legend(loc="best")