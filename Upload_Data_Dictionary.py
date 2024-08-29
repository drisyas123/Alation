import os
import pandas as pd
import requests
import json
from dotenv import load_dotenv
import tkinter as tk
from tkinter import filedialog
import Map_Target_to_Source as mpts
import warnings 
warnings.filterwarnings("ignore")


load_dotenv()

ALATION_API_TOKEN = os.getenv('API_TOKEN')
BASEURL = os.getenv('BASE_URL')

# input the data dictionary file to be executed
inputFileName = ""
while inputFileName == "":
   print("Please select the Data Dictionary file: ")
   root = tk.Tk() 
   inputFileName = filedialog.askopenfilename()
   
   if inputFileName == "":
      print("Please select a valid Data Dictionary file.")

data_dict_df = pd.read_csv(inputFileName)
print("The data dictionary selected: ",inputFileName)

# input the business file to be executed
businessFileName = ""
while businessFileName == "":
   print("Please select the business file: ")
   root = tk.Tk() 
   businessFileName = filedialog.askopenfilename()
   
   if businessFileName == "":
      print("Please select a valid business file.")

business_df = pd.read_excel(businessFileName)
print("The business file selected: ",businessFileName)
merged_df = pd.merge(data_dict_df, business_df[['Source Key', 'Suggested business term']],
                     left_on='key', right_on='Source Key', how='left')

merged_df['business term'] = merged_df['Suggested business term']
merged_df.loc[merged_df['al_datadict_item_properties'].str.split(';',expand=True)[1]!='otype=attribute', 'business term'] = "_"
merged_df = merged_df.drop(columns=['Source Key','Suggested business term'])

root = tk.Tk()

print("Please save the updated Data Dictionary file")
    # Open save file dialog
file_path = filedialog.asksaveasfilename(initialfile="updated_datadictionary",defaultextension=".csv", 
                                             filetypes=[("CSV files", "*.csv"), 
                                                        ("All files", "*.*")])
root.destroy()

if file_path:
   merged_df.to_csv(file_path, index=False)
   print(f"DataFrame saved to {file_path}")
else:
   print("Save operation cancelled.")

alationDCUpdate = input("Map to suggested terms in Alation (Y/N)?: ")
if alationDCUpdate.upper() == "Y":
   # Alation Data Catalog Base URL, Access Token and required endpoint headers
   # No trailing slash for base_url
   headers = {'Token': ALATION_API_TOKEN, 'accept': 'application/json'}

   payload = {'overwrite_values': 'true'}

   # Set the full or relative path to the desired data dictionary file
   # Make sure to change the text/csv value based on the type of file you are uploading, either text/csv or text/tsv
   dd_file_name = file_path
   files = {'file': (dd_file_name, open(dd_file_name, 'r'), 'text/csv')}

   # api_url for a data source as the target object, change the ID value to the ID of the data source
   api_url = BASEURL + '/integration/v1/data_dictionary/table/4/upload/'

   # print(api_url)
   response = requests.request("PUT", api_url, headers=headers, data=payload, files=files, verify=False)
   task_details = response.json()
   print(task_details)
   # print(json.dumps(task_details, indent=2))

   # Get the task ID for the request, use it to monitor the task until it is completed
   task_id = task_details['task']['id']
   get_url = BASEURL + '/integration/v1/data_dictionary/tasks/' + task_id
   # print(get_url)

   x = 1
   while True:
      get_response = requests.request("GET", get_url, headers=headers)
      task_status = get_response.json()
      status = task_status['status']
      print("Task Status " + str(x) + ": " + status, end='\r')
      x += 1
      if status == 'SUCCEEDED':
         print("                              ")
         break
   print(json.dumps(task_status, indent=2))