# How to use the Battery Characterisation Tool

## Get Started

In order to use this package firstly clone the repository with:

`git clone https://github.com/zoehwright/battery_characterisation_tool`

Next, in the terminal/powershell, navigate to the echem code file path and run:

`pip install -e .`

This command will install the battery_characterisation_tool module to enable the module to be run from the provided template jupyter notebooks.

## Template Notebooks

### **How they work**

- This package has a folder within echem_plotting called 'templates'. There are .ipynb jupyter notebooks for each type of figure plotting you require. The current types of figures which can be plotted using the echem_plotting package are listed below:
- Voltage Capacity Plots
- Capacity Fade Plots (with and without Coulombic Efficiency)
- Rate Capability Plots
- dQdV Differential Capacity Plots

## Classes

### **ProcessDataFrame**

This is a small class which only has a few functions (described below). It is called into several of the other classes and is not something you need to worry about but it is useful to know what is being used to make everything work!

#### **check_file_header_present**

- This is a useful function just for biologic datasets (this does not apply to Neware datasets). When using EC-Lab software to extract the cycled datasets often EC-Lab software when it produces a .txt file will produce the file with 2 lines of text before the header row stating something like the below:

![alt text](/readme_images/EC-lab%20text.png)

- If this text is not deleted the python will throw an error as it only expects text to be in the header row which is only one row instead of three. The check_file_header_present function will check to see if these lines of text are present in the file and if so avoid them allowing python to read and plot your dataset efficiently. This will also save you the time of manually going through and altering your own datasets to remove the text.

#### **process_voltage_capacity_df**

- This function processes your raw .txt/.csv files from biologic and neware (note for neware I have assumed that you have extracted the data from the BTS software and copied it into an excel workbook which has then been saved as a .csv file).
- For biologic data it will insert and calculate specific capacities (this is already done in neware).

#### **process_capacity_fade_df**

- This function processes both .txt biologic files (cnQECe.txt files) and .csv neware files (using the cycle index data set).
- It is for plotting a single cell’s data not for comparison. It will plot specific discharge capacity vs cycle number with coulombic efficiency on a second y axis.

#### **process_capacity_fade_df_list**

- Similar to the above but this can be used for multiple cells to compare capacity fade (does not plot coulombic efficiency – this would look messy with multiple cells on the same plot).

### Note: How to process your datasets in Biologic ready to use in echem_plotting:

#### For rate capability & capacity fade plots using Biologic datasets you will need 'cnQECe.txt' file formats

- To export data as a 'cnQECe.txt' format complete the following instructions: 
  - In EC-lab software click Analysis -> Batteries -> Capacity & Energy per Cycle or Sequence -> Load file -> leave everything ticked and 'Process'. 
  - Then click Experiment -> Export as Text -> then selecting the file you just created export the following variables: time, cycle number, Q charge, Q discharge, Energy charge, Energy discharge, Efficiency.

#### For Cycle Comparison Plotting & GCD Plotting:

- The method for this is highlighted in the vc_cycle_comparison function description below. You will need to copy data directly across from your .txt files. To make your basic .txt data files for the vc_cycle_comparison & GCD/voltage_capacity_plotting fucntions, follow the below instructions:
  - In EC-Lab click: Experiment -> Export as Text -> add file (the .mpr raw data file of a particular cycling cell) and select the following variables: time, cycle number, Ewe, I, Capacity. Click Export and the .txt file will have been created.

#### For dQdV differential capacity Plotting:

- In EC-lab click: Experiment -> Load Data File -> Select the .mpr raw data file of a cycled cell. 
  - To extract a single cycle: click Tools -> Extract Cycles/Loops -> Load -> Load the .mpr raw file if it is not already stated in the Input File path. Parameters -> Extract Cycles -> enter the specific cycle number 'X' you want to be extracted.  Make sure that prompt on replace in NOT ticked. Click Extract.
  ![alt text](/readme_images/extract-cycles-bio-dqdv.png)
  - To extract all cycles: click Tools -> Extract Cycles/Loops -> Load -> Load the .mpr file if it is not already stated in the Input File path. Parameters -> Extract Cycles -> all -> Make sure that prompt on replace in NOT ticked. Click Extract.
  - Next go back to the loaded up raw data in EC-Lab and go to the Process data function:
  ![alt text](/readme_images/process-data-location.png)
  - In this tab you now need to add the .mpp file you just created when extracting the specific cycle. Untick 'Allow Reprocessing' and untick 'All'. Then select the 5 following options: 'time/s', 'Ewe/V' and 'I/mA' from the left hand box (time & I will be mandatory - you cannot unselect them). Then select 'cycle number' & d(Q-Qo)/dE/mA.h/V' from the right hand side box. Then press process.
  ![alt text](/readme_images/process-data-edits.png)
  - For both of the above to convert that .mpr file or .mpp file to a .txt file click on Experiment -> Export data as text -. click the plus icon and load the .mpr individual cycle file (should be named as  NAMEOFMATERIAL_cycleX.mpr 'X' being defined in the previous step). In variables to export box choose the following in this order: time/s; cycle number; Ewe/V; I/mA; d(Q-Qo)/dE/mA.h/V -> Click Export and the .txt file of that cycle will be produced.

- In Neware BTS, load up one dataset by clicking: File -> Open -> Select a .ndax file. In the circulation range ensure you have all cycles plotted to check the figure it shows on the window viewer.
- Then on the top bar click the funnel icon labelled as 'Data Filter'. Click the button 'C1 rate' which will alter the filter conditions to a standard preset. Choose the folder where your wish to save the filtered dataset and give a file name for this dataset. The file will be saved as a .ndax. It is important to alter the file name as otherwise it may save the filtered dataset over your existing raw dataset. Ensure both tick boxes at the bottom are selected. Then press 'OK'.
![alt text](/readme_images/Data_filter.png)
- Now Neware will open up this new .ndax file. Load all cycles in the viewer window to check that your data looks similar.
-To export a specific cycle, load that cycle in the circulation range in the dQ/dV window (click double arrows in top right hand corner of plotting window). Then click the 'Export report' button (on the top bar to the left of the excel icon with a big green X on it).
- In the export report menu, first ensure customize report is selected and csv file type. Add in the file name you wish to save it as and the file path. The custom report setting tab will also now be open. Go to the 'Recording layer' tab. In circulation range put the specific cycle from and to you wish to export. Then in the tick box on the right hand side, ensure only voltage and dQ/dV boxes are selected. At the bottom of this window is a subsection called 'CSV settings' ensure that the 'Recording layer' box is selected. Then press 'Export' in the 'Export report' tab.
![alt text](/readme_images/Export-tab-neware-dqdv.png)
- Alternatively, to export multiple cycles you can follow the above but just change the circulation range to encorporate more cycles.

To understand the influence that the Neware filtering setting has see the below figures. The top figure is just the raw data. The bottom figure is with the filtering.
![alt text](/readme_images/dqdv-without-filter.png)
![alt text](/readme_images/dqdv-with-filtering.png)

###	**RateCapabilityPlotting**

#### **_get_file_list**

- This function allows the code to read through all the files within a folder path. We need this in order to use multiple .txt .csv files and collate the data into one rate capability plot.

#### **rate_capability**

- This function will plot the rate capability plot. For this you will need to export biologic data in the cnQECe.txt format and for neware data you need to extract the cycle index data and save it as a .csv file.
  - To export data as a 'cnQECe.txt' format complete the following instructions: In EC-lab software click Analysis -> Batteries -> Capacity & Energy per Cycle or Sequence -> Load file -> leave everything ticked and 'Process'. Then click Experiment -> Export as Text -> then selecting the file you just created export the following variables: time, cycle number, Q charge, Q discharge, Energy charge, Energy discharge, Efficiency.
- For Neware .csv files - insert a column on cycle index to add 0 - that way all rates align (before they were shifted across 1 cycle due to cycles starting at 1 vs biologic starting at cycle 0).
  - For Neware datasets in the BTS software you can copy the datasets across to an excel file.
- A seaborn colour scheme is employed for these plots which follows the colours in the image below. If you want the same colours to be associated with the same data sets throughout your plots it is worth numerically ordering your files within the folder path (see readme_images below).
![ ](/readme_images/dark2.png) ![alt text](/readme_images/file_path_structure.png)

- To plot a rate capability plot follow the below code structure (using your own folder path):

![alt text](/readme_images/rate_capability_code.png)

- The output should look something like this:
![alt text](/readme_images/rate_cap_plot.png)

###	**CapacityFadePlotting**

#### **capacity_fade_ce**

- This function can be used to plot a single cell and will show discharge capacity vs cycle number with coulombic efficiency on a second y axis.
- Use the code below to get the plot.
- The datasets used to plot these figures also need to be cnQECe.txt files (how to do this is highlighted above).

![ ](/readme_images/cap_fade_ce_code.png)![ ](/readme_images/cap_fade_with_ce.png)

#### **capacity_fade**

- This function will plot a series of cell datasets with discharge capacity vs cycle number.
- Use the below code to get your plot.
- Again, if you wish to have the same colours for the same datasets (linking to other types of plots such as rate capability) ensure to number your files in order within the folder path which is being used.

![alt text](/readme_images/cap_fade_comp_code.png)
![alt text](/readme_images/cap_fade_comparison.png)

#### **vc_cycle_comparison**

- This is a very useful funtion which will plot a single charge/discharge cycle.
- The data required to plot this file requires individual cycles to be extracted from the VC (voltage-capacity) plot on neware or biologic (remember on biologic cycle 1 is actually cycle 0. So if you want to compare a whole series of cells you need to take cycle 49 from biologic and cycle 50 from neware). Once you have extracted e.g. the 50th cycle, copy the data into a spreadsheet. Do this for every data set you wish to plot in the same figure. Save the file as a .csv (note the the order of each cell data. This must match the order of the active masses in the active_mass_list.)

![alt text](/readme_images/cycle_comp_spreadsheet.png)

- In the figure above you can see in row 1 column C starts with 'Capacity' not 'Spec. Cap' like in columns A & E. Do not worry about biologic not exporting the specific capacity whilst neware does - this is dealt with in the code and you just need to manually put in each active mass using active_mass_list. When putting these values into the list ensure they are in the same order as your exported cycle data (otherwise your specific capacity will be incorrect).
- Use the below code ensuring to add the legend_labels in the same order as the active_mass_list values.

![alt text](/readme_images/cycle_comp_code.png)

![alt text](/readme_images/cycle_comparison.png)

- You can use this same code for any cycle comparison data set. The way that each charge/discharge curve is not connected with a line at the top of the figure is because a scatter plot is being used. A line plot can be used as an alternative  but you may need to go through the datasets manually to modify them.

### **dQdVPlotting**

### **For Biologic datasets use the following functions:** 

#### **_get_file_list()**

- This function (same as above in rate capability) allows the code to read through all the files within a folder path. We need this in order to use multiple .txt .csv files and collate the data into one dQdV plot.

#### **dqdv_mulitple_cycles**

-This function requires you to extract individual cycle datasets from Biologic and collate them into a specific folder. Then the code checks the folder path and will plot all the datasets in the folder in the order that they sit in the folder (ordering your files in the correct order is key here).
-The data is plotted as a scatter plot.

![alt text](/readme_images/dqdv_multiple_cycles_code.png)
![alt text](/readme_images/dqdv_mulitple_cycles.png)

#### **dqdv_single_cycle**

-This function plots a single cycle of a cell as a scatter plot (the dataset for this has been extracted from Biologic data as a .csv or .txt file).

![alt text](/readme_images/dqdv_single_cycle_code.png)
![alt text](/readme_images/dqdv_single_cycle.png)

#### **Additional capability**

- In the template dQdV_plotting.ipynb notebook there is also a simple plotting function which allows you to plot the dQdV plot for every cycle of a cell and also every cycle can be plotted in a different colour too. To do this you just need to extract the dQdV data set for a cell as a .csv or .txt file and in the file_path for that dataset. This is more useful just to check your dataset looks the same on python as it does on the Biologic EC-lab software platforms.

### **For Neware datasets sue the below functions for dQ/dV plotting**
#### **dqdv_single_cycle_neware**

- This function does the same as the above but is specific to neware data sets. Input your file path into the dqdv notebook. You can change the figure size, title, fonts and x and y axes like usual. Please ensure that the legend label is also entered.

![alt text](/readme_images/dqdv-single-neware-code.png)
![alt text](/readme_images/dqdv-example-neware-single.png)

#### **dqdv_multiple_cycles_neware**

- This function again uses a folder path directory instead of an individual file path. For this function, ensure that the number of legend labels matches the number and order of the files listed inside the folder path.

![alt text](/readme_images/dqdv-neware-multiple-code.png)
![alt text](/readme_images/dqdv-multiple-neware-fig.png)

- There are several other functions which allow you to plot every cycle in one go. To use these 2 functions (dqdv_all_cycles_neware & dqdv_all_cycles_neware_colour). When you are exporting your dataset from the filtered .ndax file, in the 'Recording layer' of the 'Custom report settings' tabes ensure that you also select 'Cycle Index' in the tick box table (as well as 'Voltage' and 'dQ/dV') and change your circulation range to the full range of cycles that you would like to plot on the figure.

![alt text](/readme_images/dqdv-neware-all-cycles-export.png)


### **GCDPlotting**

This class allows plotting of every single galvanostatic charge and discharge (GCD) cycle of a cell.

First in the voltage_capacity_plotting.ipynb notebook (in the templates folder) you need to process your dataframe which requires use of the ProcessDataframe class mentioned previously.

#### **gcd_single_dataset**

- This function allows you to plot every cycle of a cell. You must locate the file_path and enter the active mass of your material (in order for the specific capacity to be calculated and plotted in the figure).

![alt text](/readme_images/gcd_single_dataset_code.png)
![alt text](/readme_images/gcd_single_dataset.png)

#### **gcd_color_grad**

- This function is very similar to the above except it incorpates a seaborn colour scheme going from a light to dark colour to show the capacity fade which occurs on cycling. 

![alt text](/readme_images/gcd_color_grad_code.png)
![alt text](/readme_images/GCD_colour.png)

#### **specific_cycle_plot_neware**

- This function is used on Neware data sets to plot every cycle. It also incorporates a seaborn colour scheme which allows colour fade to show for capacity fade occurring during cycling.

![alt text](/readme_images/code_specific_cycle_plot_neware.png)
![alt text](/readme_images/GCD_single_neware_fig.png)

#### **gcd_neware**

- This function is used on Neware data sets to plot every cycle. It also incorporates a seaborn colour scheme which allows colour fade to show for capacity fade occurring during cycling.

![alt text](/readme_images/code_GCD_Neware.png)
![alt text](/readme_images/GCD_Neware.png)
