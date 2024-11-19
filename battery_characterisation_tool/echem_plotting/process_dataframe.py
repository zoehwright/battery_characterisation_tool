import pandas as pd
from typing import Optional
import numpy as np


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
            indexes = df.index[df[header] > 4.29875].tolist()
            column_index = df.columns.get_loc(header)
            spec_capacity_header = df.columns[column_index-1]
            df[[header, spec_capacity_header]] = df.iloc[:, [column_index, column_index-1]].drop(index=indexes)
        
        return df
        
    def process_dqdv_neware(self,
                            file_path,
                            df) -> pd.DataFrame:
        df = pd.read_csv(file_path, header=1)
        