

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as colors
import pandas as pd
import seaborn as sns
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
        xlim: Optional[tuple] = (0, 60),
        ylim: Optional[tuple] = (0, 1000000),
        xlabel: Optional[str] = "2$\theta$ / °",
        ylabel: Optional[str] = "Intensity",
    ):
        self.dataset_name = dataset_name
        self.file_path = file_path
        self.plot_title = plot_title
        self.label = label
        self.legend_labels = legend_labels
        self.folder_path = folder_path
        self.figsize = figsize
        self.xlim = xlim
        self.ylim = ylim
        self.xlabel = xlabel
        self.ylabel = ylabel

    def _get_file_list(self) -> list:
        arr = os.listdir(self.folder_path)
        arr = [f"{self.folder_path}\{item}" for item in arr if item.endswith((".txt", ".csv"))]
        return arr    

    def raw_xye_plot(self)
        #dataset_name = np.loadtxt(r'C:\Users\chem-exet5737\OneDrive - Nexus365\I11 Data\March 2023\P2014ZW_119.dat')
        df = self(file_path=self.file_path,)
        x = df[: , 0]
        y_obs = df[: , 1]
        #y_calc = data[:, 2]

        plt.rcParams['font.family']='serif'

        plt.figure(figsize=self.figsize)
        plt.plot(x, y_obs, label=self.label, linewidth = 0.5, color = self.color)
        #plt.plot(x, y_calc, label='Calculated{self.label}', linewidth = 0.5, color = self.color)
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])

        plt.title(plot_title=self.plot_title)
        plt.xlabel(xlabel=self.xlabel)
        plt.ylabel(ylabel=self.ylabel)



    def raw_multiple_xye_plot(self)
        directoryPath = os.path.join(r'C:\Users\chem-exet5737\OneDrive - Nexus365\Group Data\Paul_I11_Oct23\800-900\*')
        data = pd.DataFrame()
        #i = 0
        for file_name in glob.glob(directoryPath):
            temp = (file_name.split('P2-Na0.67Fe0.33Mn0.33Mn0.33O2-')[1]).split(".dat")[0]
            print(temp)
            name = f"{temp}°C"
            data[f"{name}"], data[f"{name}_y"] = np.loadtxt(file_name, usecols=(0,1), unpack=True)
            #i+=1
            print(file_name)

        plt.rcParams['font.family']='serif'
        fig, ax = plt.subplots(2, 1, figsize=(16, 10))
        plt.suptitle('Varied Temperature Synthesis', fontsize=18)

        x = data["800°C"]
        #y_obs = data[:, 1]
        #y_calc = data[:, 2]

        colours = sns.color_palette("Greys", 5)
        #colours = pl.cm.Pastel1(4)
        #colours = ['orange','green','darkviolet', 'hotpink', 'steelblue']

        #(np.linspace(0,1,4))

        for i in range(2):
            #ax[i].scatter(x, y_obs, s=0.2, color='black', label='Observed')
            for j in range(5):
                col = data.iloc[:,(1+(j*2))]
                ax[i].plot(x, col, linewidth=1.5, color=colours[j], label=col.name.split("_")[0])
            ax[i].set_xlabel(r'2$\theta$ / °', fontsize= 16)
            ax[i].yaxis.set_ticklabels([])
            ax[i].yaxis.set_ticks([])
        ax[0].set_xlim(7, 45)
        ax[1].set_xlim(16,27)
        ax[1].set_ylim(-100, 500000)
        ax[0].set_ylabel('Intensity', fontsize=16)
        ax[1].set_ylabel('Intensity', fontsize=16)    
        ax[0].legend(loc='upper right', fontsize=16) #remove bbox section to put legen box inside data figure.bbox_to_anchor=(1, 1),
        ax[1].legend(loc='upper right', fontsize=16)
        plt.tight_layout()          

    def rietveld_refinement_plot(self)
        #dataset_name = np.loadtxt(r'C:\Users\chem-exet5737\OneDrive - Nexus365\I11 Data\March 2023\P2014ZW_119.dat')
        df = self(file_path=self.file_path,)
        x = df[: , 0]
        y_obs = df[: , 1]
        y_calc = df[:, 2]

        plt.rcParams['font.family']='serif'

        plt.figure(figsize=self.figsize)
        plt.plot(x, y_obs, label=self.label, linewidth = 0.5, color = self.color)
        plt.plot(x, y_calc, label='Calculated{self.label}', linewidth = 0.5, color = self.color)
        plt.xlim(xlim=self.xlim)
        plt.ylim(ylim=self.ylim)
        plt.title(plot_title=self.plot_title)
        plt.xlabel(xlabel=self.xlabel)
        plt.ylabel(ylabel=self.ylabel)

    def rietveld_refinement_zoom_plot(self)
        #df = np.loadtxt(r'C:\Users\chem-exet5737\OneDrive - Nexus365\I11 Data\Jan 2024\P2P3.asc')
        df = self(file_path=self.file_path,)
        #x_P2P3, y_calc_P2P3, y_obs_P2P3 = P2P3_data[:, 0], P2P3_data[:, 1], P2P3_data[:, 2]
        x = df[: , 0]
        y_obs = df[: , 1]
        y_calc = df[:, 2]

        #offset_P2P3 = 300

        plt.figure(figsize=(4, 6))

        # Plot 1: P2P3
        plt.plot(x, np.sqrt(y_obs) + offset_P2P3, label = self.label, linewidth = 0.5, color='black')
        plt.plot(x, np.sqrt(y_calc) + offset_P2P3, label='Calculated P2P3', linestyle='--', color='plum')

        #plt.scatter(data_ticks_x_NiO, [100 for x in data_ticks_x_NiO], marker='|', label='NiO', color='blue')
        #plt.scatter(data_ticks_x_P2, [200 for x in data_ticks_x_P2], marker='|', label='P2', color = 'red')
        ##plt.scatter(data_ticks_x_P3, [300 for x in data_ticks_x_P3], marker='|', label='P3', color ='green')

        plt.xlim(21.5, 22.7)  # Replace x_min and x_max with your desired limits
        plt.ylim(400, 1450)

        plt.xlabel(r'2$\theta$ / °', fontsize=16)
        plt.ylabel('Intensity sqrt(y)', fontsize=16)
        #plt.title('Ca doped P2P3 Series', fontsize=16)
        #plt.xticks(fontsize=16)
        #plt.yticks(fontsize=16)

        plt.show()


    def rr_plot_with_ticks(self)
        data = np.loadtxt('C:\\Users\\chem-exet5737\\OneDrive - Nexus365\\RAL\\Rietveld Refinement\\ToS data\\P2_JSZW.asc')

        x = data[:, 0]
        y_obs = data[:, 1]
        y_calc = data[:, 2]

        plt.rcParams['font.family']='serif'

        data_ticks_x_NiO = np.loadtxt('C:\\Users\\chem-exet5737\\OneDrive - Nexus365\\RAL\\Rietveld Refinement\\ToS data\\P2_JSZW_ticks_NiO.tic')[:, 0]
        data_ticks_x_P2_narrow = np.loadtxt('C:\\Users\\chem-exet5737\\OneDrive - Nexus365\\RAL\\Rietveld Refinement\\ToS data\\P2_JSZW_ticks_P2_narrow.tic')[:, 0]
        data_ticks_x_P2_broad_odd = np.loadtxt('C:\\Users\\chem-exet5737\\OneDrive - Nexus365\\RAL\\Rietveld Refinement\\ToS data\\P2_JSZW_ticks_P2_broad_odd.tic')[:, 0]
        data_ticks_x_P2_broad_even = np.loadtxt('C:\\Users\\chem-exet5737\\OneDrive - Nexus365\\RAL\\Rietveld Refinement\\ToS data\\P2_JSZW_ticks_P2_broad_even.tic')[:, 0]


        fig, ax = plt.subplots(2, 1, figsize=(10, 10))

        for i in range(2):
            ax[i].scatter(x, y_obs, s=0.2, color='black', label='Observed')
            ax[i].plot(x, y_calc, linewidth=0.5, color='red', label='Calculated')
            ax[i].set_xlabel(r'2$\theta$ / °', fontsize = 16)
            ax[i].yaxis.set_ticklabels([])
            ax[i].yaxis.set_ticks([])
        ax[0].set_xlim(5, 65)
        #ax[1].set_xlim(16.5, 26.5)
        ax[0].set_ylim(-600000,2500000) #(-600000,4400000)
        #ax[1].set_ylim(-200000,800000)
        #ax[0, 1].set_xlim(20, 35)
        #ax[1, 1].set_xlim(35, 50)
        #ax[0].set_facecolor('cyan', extent=(10, 20, 100, 300))

        ax[0].scatter(data_ticks_x_NiO, [-100000 for x in data_ticks_x_NiO], marker='|', label='NiO')
        #ax[0].scatter(data_ticks_x_P2_Or, [-3300 for x in data_ticks_x_P2_Or], marker='|', label='P2 Or')
        ax[0].scatter(data_ticks_x_P2_narrow, [-200000 for x in data_ticks_x_P2_narrow], marker='|', label='P2') # Narrow')
        ax[0].scatter(data_ticks_x_P2_broad_odd, [-400000 for x in data_ticks_x_P2_broad_odd], marker='|', label='P2') # Broad Odd')
        ax[0].scatter(data_ticks_x_P2_broad_even, [-500000 for x in data_ticks_x_P2_broad_even], marker='|', label='P2') # Broad Even')

        #ax[1].scatter(data_ticks_x_NiO, [-1000 for x in data_ticks_x_NiO], marker='|', label='NiO')
        #ax[1].scatter(data_ticks_x_P2_Or, [-3300 for x in data_ticks_x_P2_Or], marker='|', label='P2_Or')
        #ax[1].scatter(data_ticks_x_P2_narrow, [-50000 for x in data_ticks_x_P2_narrow], marker='|', label='P2') # Narrow')
        #ax[1].scatter(data_ticks_x_P2_broad_odd, [-100000 for x in data_ticks_x_P2_broad_odd], marker='|', label='P2') # Broad Odd')
        #ax[1].scatter(data_ticks_x_P2_broad_even, [-150000 for x in data_ticks_x_P2_broad_even], marker='|', label='P2') # Broad Even')

        #rect = patches.Rectangle((16, -250000), 12, 10000000, linewidth=2, edgecolor='mediumorchid', facecolor='palevioletred', alpha=0.1)
        #ax[0,0].add_patch(rect)
        #rect = patches.Rectangle((16, -250000), 12, 10000000, linewidth=2, edgecolor='blue', facecolor='cyan', alpha=0.1)
        #ax[0,1].add_patch(rect)
        #rect = patches.Rectangle((16, -250000), 12, 8000000, linewidth=2, edgecolor='mediumorchid', facecolor='palevioletred', alpha=0.1)
        #ax[1,0].add_patch(rect)
        #rect = patches.Rectangle((16, -250000), 12, 8000000, linewidth=2, edgecolor='blue', facecolor='cyan', alpha=0.1)



        #rect = patches.Rectangle((16, -600000), 12, 5800000, linewidth=2, edgecolor='mediumorchid', facecolor='palevioletred', alpha=0.1)
        #ax[0].add_patch(rect)
        #rect = patches.Rectangle((16, -200000), 12, 3000000, linewidth=2, edgecolor='mediumorchid', facecolor='palevioletred', alpha=0.1)
        #ax[1].add_patch(rect)
        plt.subplots_adjust(hspace=0.3)
        ax[0].set_ylabel('Intensity', fontsize=16)
        #ax[1].set_ylabel('Intensity', fontsize=16)
        #ax[0].yaxis.set_label_coords(-0.02, -0.15)

        ax[0].legend(bbox_to_anchor=(1, 1.05), loc='upper left', fontsize =14)
        #ax[1].legend(bbox_to_anchor=(1, 1.05), loc='upper left', fontsize =14)
        plt.tight_layout()


    def rietveld_refinement_stacked_plot(self) 
        # Load data
        P2_data = np.loadtxt('C:\\Users\\chem-exet5737\\OneDrive - Nexus365\\RAL\\Rietveld Refinement\\ToS data\\P2_JSZW.asc')
        P2Ca121_data = np.loadtxt('C:\\Users\\chem-exet5737\\OneDrive - Nexus365\\RAL\\Rietveld Refinement\\ToS data\P2_Ca121.asc')
        P2Ca127_data = np.loadtxt('C:\\Users\\chem-exet5737\\OneDrive - Nexus365\\RAL\\Rietveld Refinement\\ToS data\\P2_Ca127.asc')

        x_P2, y_obs_P2, y_calc_P2 = P2_data[:, 0], P2_data[:, 1], P2_data[:, 2]
        x_P2Ca121, y_obs_P2Ca121, y_calc_P2Ca121 = P2Ca121_data[:, 0], P2Ca121_data[:, 1], P2Ca121_data[:, 2]
        x_P2Ca127, y_obs_P2Ca127, y_calc_P2Ca127 = P2Ca127_data[:, 0], P2Ca127_data[:, 1], P2Ca127_data[:, 2]

        # Set offset values
        offset_P2 = 500 #80000
        offset_P2Ca121 = 2000 #500000  # Adjust this value as needed
        offset_P2Ca127 = 4000 #1200000 # Adjust this value as needed

        # Plotting
        plt.figure(figsize=(7, 6))

        # Plot 1: P2
        plt.plot(x_P2, np.sqrt(y_obs_P2) + offset_P2, label='Observed P2', linewidth = 0.5, color='black')
        plt.plot(x_P2, np.sqrt(y_calc_P2) + offset_P2, label='Calculated P2', linestyle='--', color='plum')

        # Plot 2: P2_Ca121
        plt.plot(x_P2Ca121, np.sqrt(y_obs_P2Ca121) + offset_P2Ca121, label='Observed P2-Ca1/21', linewidth = 1, color='black')
        plt.plot(x_P2Ca121, np.sqrt(y_calc_P2Ca121) + offset_P2Ca121, label='Calculated P2-Ca1/21', linestyle='--', color='mediumturquoise')

        # Plot 3: P2Ca127
        plt.plot(x_P2Ca127, np.sqrt(y_obs_P2Ca127) + offset_P2Ca127, label='Observed P2-Ca1/27', linewidth = 1, color='black')
        plt.plot(x_P2Ca127, np.sqrt(y_calc_P2Ca127) + offset_P2Ca127, label='Calculated P2-Ca1/27', linestyle='--', color='darkseagreen') 

        # Set x-axis limit
        plt.xlim(5, 60)  # Replace x_min and x_max with your desired limits
        plt.ylim(0, 6500) #100000,0 (4e4, 6e6) 

        # Set y-axis to logarithmic scale
        #plt.yscale('log')
        #plt.yscale('sqrt')

        # Adjust labels and legend
        plt.xlabel(r'2$\theta$ / °', fontsize=16)
        plt.ylabel('Intensity sqrt(y)', fontsize=16)
        plt.title('Ca doped P2 Series', fontsize=16)
        plt.legend(bbox_to_anchor=(0.207, 1), loc='upper left', ncol=2)


        # Show the plot
        plt.show()
    
    
    def rr_stacked_plot_with_ticks(self)
        # Load data
        P2P3_data = np.loadtxt(r'C:\Users\chem-exet5737\OneDrive - Nexus365\I11 Data\Jan 2024\P2P3.asc')
        P2P3Ca272_data = np.loadtxt(r'C:\Users\chem-exet5737\OneDrive - Nexus365\I11 Data\Jan 2024\P2P3Ca272.asc')
        P2P3Ca372_data = np.loadtxt(r'C:\Users\chem-exet5737\OneDrive - Nexus365\I11 Data\Jan 2024\P2P3Ca372.asc')

        # Load ticks Data
        data_ticks_x_NiO = np.loadtxt(r'C:\Users\chem-exet5737\OneDrive - Nexus365\I11 Data\Jan 2024\NiO_Ca272_ticks.asc')[:, 0]
        data_ticks_x_P2 = np.loadtxt(r'C:\Users\chem-exet5737\OneDrive - Nexus365\I11 Data\Jan 2024\P2_Ca272_ticks.asc')[:, 0]
        data_ticks_x_P3 = np.loadtxt(r'C:\Users\chem-exet5737\OneDrive - Nexus365\I11 Data\Jan 2024\P3_Ca272_ticks.asc')[:, 0]

        x_P2P3, y_calc_P2P3, y_obs_P2P3 = P2P3_data[:, 0], P2P3_data[:, 1], P2P3_data[:, 2]
        x_P2P3Ca272, y_calc_P2P3Ca272, y_obs_P2P3Ca272 = P2P3Ca272_data[:, 0], P2P3Ca272_data[:, 1], P2P3Ca272_data[:, 2]
        x_P2P3Ca372, y_calc_P2P3Ca372, y_obs_P2P3Ca372 = P2P3Ca372_data[:, 0], P2P3Ca372_data[:, 1], P2P3Ca372_data[:, 2]

        # Set offset values
        offset_P2P3 = 300 #80000
        offset_P2P3Ca272 = 1400 #500000  # Adjust this value as needed
        offset_P2P3Ca372 = 2600 #1200000 # Adjust this value as needed

        # Plotting
        plt.figure(figsize=(9, 6))

        # Plot 1: P2P3
        plt.plot(x_P2P3, np.sqrt(y_obs_P2P3) + offset_P2P3, label='Observed P2P3', linewidth = 0.5, color='black')
        plt.plot(x_P2P3, np.sqrt(y_calc_P2P3) + offset_P2P3, label='Calculated P2P3', linestyle='--', color='plum')
        #legend1 = plt.legend(bbox_to_anchor=(0.75, 1), loc='upper left')

        # Plot 2: P2P3Ca272
        plt.plot(x_P2P3Ca272, np.sqrt(y_obs_P2P3Ca272) + offset_P2P3Ca272, label='Observed P2P3Ca2/72', linewidth = 1, color='black')
        plt.plot(x_P2P3Ca272, np.sqrt(y_calc_P2P3Ca272) + offset_P2P3Ca272, label='Calculated P2P3Ca2/72', linestyle='--', color='mediumturquoise')
        #legend2 = plt.legend(bbox_to_anchor=(0.5, 1), loc='upper left')

        # Plot 3: P2P3Ca372
        plt.plot(x_P2P3Ca372, np.sqrt(y_obs_P2P3Ca372) + offset_P2P3Ca372, label='Observed P2P3Ca3/72', linewidth = 1, color='black')
        plt.plot(x_P2P3Ca372, np.sqrt(y_calc_P2P3Ca372) + offset_P2P3Ca372, label='Calculated P2P3Ca3/72', linestyle='--', color='darkseagreen') 
        #legend3 = plt.legend(bbox_to_anchor=(0.25, 1), loc='upper left')

        # Plot ticks 
        plt.scatter(data_ticks_x_NiO, [100 for x in data_ticks_x_NiO], marker='|', label='NiO', color='blue')
        plt.scatter(data_ticks_x_P2, [200 for x in data_ticks_x_P2], marker='|', label='P2', color = 'red')
        plt.scatter(data_ticks_x_P3, [300 for x in data_ticks_x_P3], marker='|', label='P3', color ='green')


        # Set x-axis limit
        plt.xlim(5, 59.6)  # Replace x_min and x_max with your desired limits
        plt.ylim(0, 4000) #100000,0 (4e4, 6e6) 

        # Set y-axis to logarithmic scale
        #plt.yscale('log')
        #plt.yscale('sqrt')

        # Adjust labels and legend
        plt.xlabel(r'2$\theta$ / °', fontsize=16)
        plt.ylabel('Intensity sqrt(y)', fontsize=16)
        plt.title('Ca doped P2P3 Series', fontsize=16)
        plt.xticks(fontsize=20)
        #plt.yticks(fontsize=20)
        #plt.legend(bbox_to_anchor=(0.4, 1), loc='upper left', ncol=3)

        legend_P2P3 = plt.legend(['Observed P2P3', 'Calculated P2P3'], loc='upper left', bbox_to_anchor=(0.77, 0.35), labelcolor=['black', 'plum'], handlelength=0)
        plt.gca().add_artist(legend_P2P3)
        legend_P2P3Ca272 = plt.legend(['Observed P2P3Ca2/72', 'Calculated P2P3Ca2/72'], loc='upper left', bbox_to_anchor=(0.7, 0.65), labelcolor=['black', 'mediumturquoise'], handlelength=0)
        plt.gca().add_artist(legend_P2P3Ca272)
        legend_P2P3Ca372 = plt.legend(['Observed P2P3Ca3/72', 'Calculated P2P3Ca3/72'], loc='upper left', bbox_to_anchor=(0.7, 1), labelcolor=['black', 'darkseagreen'], handlelength=0)
        plt.gca().add_artist(legend_P2P3Ca372)
        legend_ticks = plt.legend(['P3', 'P2', 'NiO'], loc='upper left', bbox_to_anchor=(1, 0.155), labelcolor=['green','red', 'blue'], handlelength=0)
        plt.gca().add_artist(legend_P2P3)

    def two_rr_zoom_in_patches(self)

    def EP_rr_difference_plot(self)
        
        data = np.genfromtxt("C:/Users/fbw29189/Documents/AMBHER/CSIC/Batch2/Batch2_StandardRefined_X_Yobs.txt", usecols=(0,1), dtype=float)
        #print(file_data)
        X = data[:,0]
        print(X)

        Yobs = data[:,1]
        print(Yobs)

        Ycalc = data[:,2]

        diff = Ycalc - Yobs
        
        fig = plt.figure(figsize=(10,4))
        gs = gridspec.GridSpec(2,1, height_ratios=[1,0.25])
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        #gs.update(hspace=0) 

        ax1.plot(X, Yobs, 'b.', label='Measured', ms=0.5)
        ax1.plot(X, Ycalc, 'r-', label='Calculated')#,\
         #label="y= %0.2f$e^{%0.2fx}$ + %0.2f" % (popt_exponential[0], popt_exponential[1], popt_exponential[2]))

        # residual
        ax2.plot(X, Diff, "0.4", label='Difference')
            
        #ax1.set_xlim(-5,105)
        #ax1.set_ylim(-0.5,8)

        #ax2.set_xlim(-5,105)
        #ax2.set_ylim(-0.5,0.75)

        ax2.set_xlabel("2theta",family="serif",  fontsize=12)
        ax1.set_ylabel("Intensity",family="serif",  fontsize=12)
        ax2.set_ylabel("Difference",family="serif",  fontsize=12)

        ax1.legend(loc="best")

    def phases_pie_chart(self)
        val1 = 3.99
        val2 = 41.99
        val3 = 54.03
        val4 = 10
        val5 = 4
        n_colors=5

        labels =

        y = np.array([val1, val2, val3, val4, val5])
        mycolors = sns.color_palette('Dark2', n_colors)
        plt.pie(y, colors=mycolors)
        plt.legend(labels=['NiO','P2', 'P3', '4', '5'], fontsize=16, bbox_to_anchor=(1,1))
        plt.show()


"""
