import pandas as pd
from typing import Optional
import numpy as np
import os


class ProcessDataframe:
    def __init__(self):
        pass

    def check_file_header_present(self, 
                          file_path) -> int:
        if file_path.endswith(".txt"):
            with open(file_path, 'r') as file:
                # Read the first few lines to check for the specific header
                lines = file.readlines()
            # Define the header lines to check for
            header_lines = ["EC-Lab ASCII FILE\n"]

            # Check if the file starts with the specified header
            if lines[:1] == header_lines: 
                return 3
            else:
                return 0
        else:
            return 0

    def process_voltage_capacity_df(self,
                                    file_path,
                                    active_mass) -> pd.DataFrame:
            df = pd.read_csv(file_path, sep='\t', header=0)

            #shift column 'time/s' to first position
            first_column = df.pop('time/s')
            df.insert(0, 'time/s', first_column)

            third_column = df.pop('Ewe/V')
            df.insert(2, 'Ewe/V', third_column)

            fourth_column = df.pop('Capacity/mA.h')
            df.insert(3, 'Capacity/mA.h', fourth_column)

            #Remove unnamed:5 column
            df.pop('Unnamed: 5')

            #Add in additional column to calculate specific discharge capacity
            df.insert(4, "Specific Capacity mAh/g", True)

            #Calculate Specific Capacity Column
            df['Specific Capacity mAh/g'] = df['Capacity/mA.h']/active_mass

            #Remove ocv points (when external current =0)
            #df = df[df["I/mA"] != 0]
            df["charge_discharge"] = np.sign(df["I/mA"])

            return df
    
    def process_energy_fade_df(self, file_name, active_mass) -> list:
        """
        
        """
        import pdb
        #pdb.set_trace()
        if file_name.endswith(".txt"):
            # file_path = os.path.join(file_paths, file_name)
            
            # Get the corresponding active mass for this file
            active_mass = active_mass
            
            # Read the file
            df = pd.read_csv(file_name, sep='\t', header=0, encoding='unicode_escape')

            # Normalize column names (strip spaces & fix encoding issues)
            df.columns = df.columns.str.strip()

            # Ensure required columns exist
            required_cols = {"cycle number", "Energy discharge/W.h"} #"Q discharge/mA.h", 
            missing_cols = required_cols - set(df.columns)

            if missing_cols:
                raise KeyError(f"Missing columns in dataset for {file_name}: {missing_cols}")
            if "Energy discharge/mW.h/g" not in df.columns:
            # Calculate Specific Energy
                df["Energy discharge/mW.h/g"] = df["Energy discharge/W.h"] * 1000 / active_mass
            
            #df.insert(8, "Energy discharge/mWh/g", True)

            # Add a unique identifier to the DataFrame (filename or index)
            df['filename'] = file_name

        return df
        
    def process_energy_fade_df_list(self, file_paths, active_mass_list) -> pd.DataFrame:
        df = pd.DataFrame(index=range(250))  # Ensure consistency with capacity fade
        # Check the active mass list and number of file paths is the same

        assert len(active_mass_list) == len(file_paths)
        
        for i, (file_path, active_mass) in enumerate(zip(file_paths, active_mass_list)):
            df_temp = self.process_energy_fade_df(file_path, active_mass)

            # Print available columns for debugging
            print(f"File {i}: {file_paths[i]}")
            print("Available columns:", df_temp.columns.tolist())

            # Check if required columns exist
            if "cycle number" in df_temp.columns and "Energy discharge/mW.h/g" in df_temp.columns:
                df[f"cycle number_{i}"] = df_temp["cycle number"]
                df[f"Spec. Energy(mWh/g)_{i}"] = df_temp["Energy discharge/mW.h/g"]
            else:
                print(f"Skipping file {file_paths[i]} due to missing columns.")
        
        print("Final DataFrame columns:", df.columns.tolist())  # Debugging
        return df
    
    def process_capacity_fade_df(self,
                                file_path,
                                active_mass) -> pd.DataFrame:
        if file_path.endswith(".txt"):    
            df = pd.read_csv(file_path, sep='\t', header=0, encoding= 'unicode_escape')
            df = df[["cycle number", "Q discharge/mA.h", "Efficiency/%"]]
            #Calculate Specific Capacity Column
            df['Specific Discharge Capacity mAh/g'] = df['Q discharge/mA.h']/active_mass
        else:
            df = pd.read_csv(file_path, header=0)
            df = df[["Cycle Index", "DChg. Spec. Cap.(mAh/g)", "Chg.-DChg. Eff"]]
            replace = {"Cycle Index": "cycle number",
                       "DChg. Spec. Cap.(mAh/g)": "Specific Discharge Capacity mAh/g",
                       "Chg.-DChg. Eff": "Efficiency/%",
                       }
            df.rename(columns=replace, inplace=True)
        return df
    
    def process_capacity_fade_df_list(self,
                                file_paths,
                                active_mass_list) -> pd.DataFrame:
        df = pd.DataFrame(index=range(250))
        for i, active_mass in enumerate(active_mass_list):
            df_temp = self.process_capacity_fade_df(file_paths[i], active_mass)
            df[f"cycle number_{i}"] = df_temp["cycle number"]
            df[f"Specific Discharge Capacity mAh/g_{i}"] = df_temp["Specific Discharge Capacity mAh/g"]

        return df
    
    def process_vc_cycle_comparison_df(self,
                                        file_path,
                                        active_mass_list) -> pd.DataFrame:
         
        df = pd.read_csv(file_path, header=0)
        df_headers = df.columns.tolist()
        df_headers = [column for column in df_headers if column.startswith("Cap")]
        for i, header in enumerate(df_headers):
            df[header] = df[header]/active_mass_list[i]
            df.rename(columns={header: "Specific_{header}g-1"})

        return df
    
    def remove_large_voltage_values(self,
                                    df) -> pd.DataFrame:
        df_headers = df.columns.tolist()
        df_headers = [column for column in df_headers if column.startswith(("Voltage", "Ewe"))]
        for header in df_headers:
            indexes = df.index[df[header] > 4.299].tolist()
            column_index = df.columns.get_loc(header)
            spec_capacity_header = df.columns[column_index-1]
            df[[header, spec_capacity_header]] = df.iloc[:, [column_index, column_index-1]].drop(index=indexes)
        
        return df
    
    def remove_large_voltage_values_2_4V(self,
                                    df) -> pd.DataFrame:
        df_headers = df.columns.tolist()
        df_headers = [column for column in df_headers if column.startswith(("Voltage", "Ewe"))]
        for header in df_headers:
            indexes = df.index[df[header] > 3.98].tolist()
            column_index = df.columns.get_loc(header)
            spec_capacity_header = df.columns[column_index-1]
            df[[header, spec_capacity_header]] = df.iloc[:, [column_index, column_index-1]].drop(index=indexes)
        
        return df
    
    def remove_ocv_voltage_values(self,
                                    df) -> pd.DataFrame:
        df_headers = df.columns.tolist()
        df_headers = [column for column in df_headers if column.startswith(("Voltage", "Ewe"))]
        for header in df_headers:
            indexes = df.index[df[header] < 1].tolist()
            column_index = df.columns.get_loc(header)
            spec_capacity_header = df.columns[column_index-1]
            df[[header, spec_capacity_header]] = df.iloc[:, [column_index, column_index-1]].drop(index=indexes)
        
        return df
        
    def process_dqdv_neware(self,
                            file_path,
                            df) -> pd.DataFrame:
        df = pd.read_csv(file_path, header=1)

    def process_dqdv_neware_zero_values(self,
                                        path,
                                        df) -> pd.DataFrame:
        df = pd.read_csv(path, header=0)
        df = df.loc[df['dQ/dV(mAh/V)'] != 0] 
        #print(df)
        return df

        