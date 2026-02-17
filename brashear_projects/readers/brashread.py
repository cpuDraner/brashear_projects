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
        self._parse(path)


    def _parse(self,path):
        """
        Parses the excel spreadsheet and combines it into one large dataframe
        """
        sheets=pd.read_excel(io=path,sheet_name=None)
        mapper={
            'Client ID':'id',
            'CLIENT ID':'id2',
            'Timestamp':'timestamp',
            'Zipcode':'zip',
            'Gender (Head of Household)':'gender',
            'What age group does the client belong to? Head of Household)':'age_group',
            'Does this person have a Proxy (Delegate picking up food)?':'proxy',
            'Family Size':'family_size',
            'Pets':'pets',
            'Did you receive food last month? ':'food_last_month',
            'Which date will you pick up? ':'pick_up_date',
            'Continue for new registration':'new_reg',
            ' (Date of Birth) Head of Household':'dob',
            'Current/Highest Education Level (Head of Household)':'education',
            'Race':'race',	
            'Ethnicity':'ethnicity',
            'What is the total # Females in the Household':'num_female',
            'What is the total # Males in the Household?':'num_male',
            'What is the total Monthly  Household Income? (Combined Gross Monthly For all Income Types and Members with Income)':'house_income',
            'Income sources for all household members?(check all that apply)l':'income_resources',
            'Work Status':'work_status',
            'Military Status':'military_status',
            'Please check if any of the following apply to the Head of Household.  (check all that apply)':'house_head_list',
            'Do you have Health Insurance? ':'health_insurance',
            'If you answered "Yes" to the previous question,  What type of health insurance do you have?  (check all that apply)':'health_insurance_type',
            'Gender (Other Adult 1)':'gender_oa1',
            'Date of Birth (Other Adult 1)':'dob_oa1',
            'What age group does the other adult 1 belong to? ':'age_group_oa1',
            'Race (Other Adult 1)':'race_oa1',
            'Current/Highest Education Level (Other Adult 1)':'education_oa1',
            'Do you have Medical Benefits? Other Adult 1':'medical_benifits_oa1', 
            'If you answered "Yes" to the previous question,  What type of Medical Benefits do you have?  (check all that apply)':'medical_ben_kind_oa1',
            'Please check if any of the following apply to Other Adult 1  (Check all that apply)':'oa1_list',
            'Gender (Other Adult 2)':'gender_oa2',
            'Date of Birth (Other Adult 2)':'dob_oa2',
            'What age group does the client belong to? ':'age_group_oa2',
            'Current/Highest Education Level (Other Adult 2)':'education_oa2',
            'Please check if any of the following apply tother Adult 2  (Check all that apply)':'oa2_list',
            'Gender (Other Adult 3)':'gender_oa3',
            'Date of Birth (Other Adult 3)':'dob_oa3',
            'What age group does the client belong to?  2':'age_group_oa3',
            'Current/Highest Education Level (Other Adult 3)':'education_oa3',	
            'Please check if any of the following apply to Other Adult 3  (Check all that apply)':'oa3_list',
            'Gender (Child 1)':'gender_c1',
            'D.O.B. (Child 1 )':'dob_c1',
            'What age group does the client belong to?  3':'age_group_c1',
            'Current Grade Level in School (Child 1)':'education_c1',
            'Disabled? (Child 1) ':'disabled_c1',
            'Gender (Child 2 )':'gender_c2',
            'D.O.B. (Child 2 )':'dob_c2',
            'What age group does the client belong to?  4':'age_group_c2',
            'Current Grade Level in School (Child 2)':'education_c2',
            'Disabled? (Child 2)':'diabled_c2',
            'D.O.B. (Child 3 )':'dob_c3',
            'What age group does the client belong to?  5':'age_group_c3',
            'Gender (Child 3)':'gender_c3',
            'Current Grade Level in School (Child 3)':'education_c3',
            'Disabled? (Child 3)':'disabled_c3',
            'D.O.B. (Child 4 )':'dob_c4',
            'What age group does the client belong to?  6':'age_group_c4',
            'Child 4 Gender':'gender_c4',
            'Current Grade Level in School (Child 4)':'education_c4',
            'Disabled? (Child 4)':'diabled_c4',
            'D.O.B. (Child 5 )':'dob_c5',
            'What age group does the client belong to?  7':'age_group_c5',
            'Gender (Child 5)':'gender_c5',
            'Current Grade Level in School (Child 5)':'education_c5',
            'Disabled? (Child 5 )':'disabled_c5',
            'D.O.B. (Child 6) ':'dob_c6',
            'What age group does the client belong to?  8':'age_group_c6',
            'Gender (Child 6)':'gender_c6',
            'Current Grade Level in School (Child 6)':'education_c6',
            'Disabled? (Child 6) ':'disabled_c6',
            'Who is completing this form? ':'form_completer',
            'Comments':'comments',
            'Staff Name':'staff_name'
        }

        self.df=self._combine(sheets)
        self.df=self.df.rename(columns=mapper)[mapper.values()]

        return self.df


    def _combine(self,sheets):
        """
        Combines sheets into one large data frame
        """
        df=None
        for page in sheets.values():
            if isinstance(df,pd.DataFrame):
                df=pd.concat([df,page])
            else:
                df=page
        return df
    
    def _date_fix(self,sheets):
        """
        Changes the pick up dates to timestamps
        """
        for sheet in sheets:
            pass
        return sheets
    
if __name__ == '__main__':
    # This is for debugging
    Dat = PantryDat('C:/sockdrawer/brashear_projects/data/pantry_data.xlsx')




