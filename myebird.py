import time
import sys
import subprocess
from pathlib import Path

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'pandas'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'ebird-api'])

import pandas as pd
from ebird.api import get_visits, get_checklist

observations = []
metadata = []
#this is a file that has your eBird  API key in it
path = Path(__file__).parent / "../keys.txt"
keyFile = path.open()
consumer_key = keyFile.readline().rstrip()
#1ST entry HAS TO BE VALID CHECKLIST

#EXAMPLE IF YOU HAVE A TEXT FILE WHERE EACH LINE IS A CHECKLIST ID
#with open('output2.txt') as f:
#    lines = f.read().splitlines()

#EXAMPLE IF YOU HAVE A CSV WHERE EACH RECORD HAS A CHECKLIST ID IN A COLUMN LABELED 'checklistID'
#df = pd.read_csv("checklist_data.csv")
#mylist = df['checklistID'].tolist()
#lines = list(dict.fromkeys(mylist))

lines = ['S64365393','S64365715', 'S64366020', 'S64366484', 'S64366945', 'S64367258', 'S64367912', 'S64368195', 'S64368532', 'S64368970', 'S64369341', 'S64369837']

for check in lines:
    time.sleep(0.5)
    try:
        checklist = get_checklist(consumer_key, check)
        observations.extend(checklist['obs'])
        metadata.append(checklist.copy())
    except:
        filler = metadata[0]
        filler = {k: None for k, v in filler.items()}
        metadata.append(filler.copy())
        continue


# Convert the list of dictionaries to a pandas dataframe
obs_df = pd.DataFrame(observations)
metadata_df = pd.DataFrame(metadata)
metadata_df['subId'] = lines 

# Export the dataframe to a csv file
obs_df.to_csv("observations_test.csv", index=False)
metadata_df.to_csv("metadata_test.csv", index=False)