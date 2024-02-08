import os
import shutil
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")
current_date_time = datetime.now()


try:
    os.chdir('..') # enters root directory
    root_dir = os.getcwd()  #gets root directory

    data_folder = os.path.join(root_dir,'data')
    os.chdir(data_folder)  #enters 'data' directory

    csv_folder = os.path.join(os.getcwd(),'csv',current_date)

    ### creating directory if doesnt exists
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder, exist_ok=True)
        print(f"Folder for the CSV file created")
    else:
        print(f"Folder already exists")
    ###
    
    ### copyng to local filesystem
    csv_file_path = os.path.join(csv_folder,f'order_details_{current_date}.csv')
    shutil.copy('order_details.csv',csv_file_path)

    print("File copy was done successfully")
except Exception as error:
    print("Error in getting csv file")