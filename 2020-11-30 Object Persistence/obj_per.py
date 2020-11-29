'''
    File name: obj_per.py
    Author: Henry Letton
    Date created: 2020-11-29
    Python Version: 3.8.3
    Desciption: Demo some object persistance methods
'''

#%% Move to folder
import os

# Store old directory in case you need to return
old_dir = os.getcwd()
print(old_dir)

new_dir = "C:\\Users\\henry\\OneDrive\\Documents\\Python\\Code-Club\\2020-11-30 Object Persistence"
os.chdir(new_dir)

#%% Store python object on computer
import pickle

# Pickle Rick!
test_dict = {
    "date": "2017-08-06",
    "numb": 23,
    "full name": "Rich Sanchez",
    "yes_or_no": True}

# Write dictionary to disk
with open('store_dict.pkl', 'wb') as output_:
    pickle.dump(test_dict, output_, pickle.HIGHEST_PROTOCOL)

# Read dictionary from disk
with open('store_dict.pkl', 'rb') as input_:
    test_dict2 = pickle.load(input_)

#%% Store as csv
import pandas as pd

# Paint it black
fav_cols = {'colour': ['black','charcoal','midnight','obsidian','salmon pink'],
            'rank': [1,2,3,4,5]}
fav_cols_df = pd.DataFrame(data = fav_cols)

fav_cols_df.to_csv("favourite colours.csv")

#%% Store in online MySQL database
import mysql.connector
import pandas as pd
from getpass import getpass

# User inputs login credentials
username = input("Enter user name: ") #u235764393_HL
password = getpass("Enter password: ")

# Connect to database
conn = mysql.connector.connect(user=username, 
                              password=password,
                              host='sql134.main-hosting.eu',
                              database='u235764393_HLDB')

cursor = conn.cursor() # Keeps track of where we are in database

# Create table in not exist
try:
    cursor.execute("CREATE TABLE Test_Colours (colour TEXT, rank INT)")
except:
    print("Test_Colours table already exists")
    
# Insert rows
for idx in range(fav_cols_df.shape[0]):
    insert = f"""INSERT INTO Test_Colours (colour, rank) VALUES 
                ('{fav_cols_df['colour'][idx]}', {fav_cols_df['rank'][idx]})"""
                
    print(insert)
    
    cursor.execute(insert)

conn.commit() # Changes need to be comitted

# Check return dataframe is the same as origional
fav_cols_df_sql = pd.read_sql_query("SELECT * FROM Test_Colours", conn)

# Get complete list of tables from dataase
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

# Drop test table to keep database tidy
cursor.execute("DROP TABLE IF EXISTS Test_Colours")

# Close database connection
conn.close()





