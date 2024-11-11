

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import Optional, Tuple

class PreProcessingXRD:
    def __init__(
            self,
            dataset_name: Optional [str] = "",
            file_path: Optional[str] = "",
    ):
        self.dataset_name = dataset_name
        self.file_path = file_path

    def process_asc_df(self) -> pd.DataFrame:
        df = pd.read_csv(self.file_path)

        #x = df[:,0]
        y_calc = df[:,1]
        y_obs = df[:,2]
        diff = y_calc - y_obs
        fourth_column = df.pop()
        df.insert(3, 'diff', fourth_column)
        
        return df