import pandas as pd
import numpy as np

class PantryDat():
    """
    Create and parse pantry data
    """
    def __init__(self,path:str):
        """
        Read the pantry file
        """
        self.df=None


    def _parse(self,path):
        """
        Parses the excel spreadsheet and combines it into one large dataframe
        """
        sheets=pd.read_excel(io=path,sheet_name=None)
        
        self._combine(sheets)

    def _combine(self,sheets):
        """
        Combines sheets into one large data frame
        """
        for page in sheets.value:
            if not df:
                df=page
            else:
                pass

    def _pick_up_fix(self,sheets):
        """
        Changes the pick up dates to timestamps
        """
        for sheet in sheets
        return sheets




