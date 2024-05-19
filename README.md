# How to use Echem Plotter

## Get Started

In order to use this package firstly clone the repository with:

`git clone https://github.com/zoehwright/echem_code.git`

Next, in the terminal/powershell, navigate to the echem code file path and run:

`pip install -e .`

This command will install the echem_plotting module to enable the module to be run from the provided template jupyter notebooks.

## Classes

### **ProcessDataFrame**

This is a small class which only has a few functions (described below). It is called into several of the other classes and is not something you need to worry about but it is useful to know what is being used to make everything work!

#### **process_voltage_capacity**

- This function processes your raw .txt/.csv files from biologic and neware (note for neware I have assumed that you have extracted the data from the BTS software and copied it into an excel workbook which has then been saved as a .csv file).
- For biologic data it will insert and calculate specific capacities (this is already done in neware).

#### **process_capacity_fade_df**

- This function processes both .txt biologic files (cnQECe.txt files) and .csv neware files (using the cycle index data set).
- It is for plotting a single cell’s data not for comparison. It will plot specific discharge capacity vs cycle number with coulombic efficiency on a second y axis.

#### **process_capacity_fade_df_list**

- Similar to the above but this can be used for multiple cells to compare capacity fade (does not plot coulombic efficiency – this would look messy with multiple cells on the same plot).

###	**RateCapabilityPlotting**

#### **_get_file_list**

- This function allows the code to read through all the files within a folder path. We need this in order to use multiple .txt .csv files and collate the data into one rate capability plot.

#### **rate_capability**

- This function will plot the rate capability plot. For this you will need to export biologic data in the cnQECe.txt format and for neware data you need to extract the cycle index data and save it as a .csv file.
- For Neware .csv files - insert a column on cycle index to add 0 - that way all rates align (before they were shifted across 1 cycle due to cycles starting at 1 vs biologic starting at cycle 0).
- A seaborn colour scheme is employed for these plots which follows the colours in the image below. If you want the same colours to be associated with the same data sets throughout your plots it is worth numerically ordering your files within the folder path (see images below).
![ ](/Images/dark2.png) ![alt text](/Images/file_path_structure.png)

- To plot a rate capability plot follow the below code structure (using your own folder path):

![alt text](/Images/rate_capability_code.png)

- The output should look something like this:
![alt text](/Images/rate_cap_plot.png)

###	**CapacityFadePlotting**

#### **capacity_fade_ce**

- This function can be used to plot a single cell and will show discharge capacity vs cycle number with coulombic efficiency on a second y axis.
- Use the code below to get the plot.

![ ](/Images/cap_fade_ce_code.png)![ ](/Images/cap_fade_with_ce.png)

#### **capacity_fade**

- This function will plot a series of cell datasets with discharge capacity vs cycle number.
- Use the below code to get your plot.
- Again, if you wish to have the same colours for the same datasets (linking to other types of plots such as rate capability) ensure to number your files in order within the folder path which is being used.

![alt text](/Images/cap_fade_comp_code.png)
![alt text](/Images/cap_fade_comparison.png)

#### **vc_cycle_comparison**

- This is a very useful funtion which will plot a single charge/discharge cycle.
- The data required to plot this file requires individual cycles to be extracted from the VC (voltage-capacity) plot on neware or biologic (remember on biologic cycle 1 is actually cycle 0. So if you want to compare a whole series of cells you need to take cycle 49 from biologic and cycle 50 from neware). Once you have extracted e.g. the 50th cycle, copy the data into a spreadsheet. Do this for every data set you wish to plot in the same figure. Save the file as a .csv (note the the order of each cell data. This must match the order of the active masses in the active_mass_list.)

![alt text](/Images/cycle_comp_spreadsheet.png)

- In the figure above you can see in row 1 column C starts with 'Capacity' not 'Spec. Cap' like in columns A & E. Do not worry about biologic not exporting the specific capacity whilst neware does - this is dealt with in the code and you just need to manually put in each active mass using active_mass_list. When putting these values into the list ensure they are in the same order as your exported cycle data (otherwise your specific capacity will be incorrect).
- Use the below code ensuring to add the legend_labels in the same order as the active_mass_list values.

![alt text](/Images/cycle_comp_code.png)

![alt text](/Images/cycle_comparison.png)

- You can use this same code for any cycle comparison data set. The way that each charge/discharge curve is not connected with a line at the top of the figure is because a scatter plot is being used. A line plot can be used as an alternative  but you may need to go through the datasets manually to modify them.
