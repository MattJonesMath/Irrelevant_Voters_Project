############################
# confirm that all identified anomalies
# actually work out
############################
from elections_class import mw_elections as mwe
import csv
import os
import copy
import sys
import ast

## load list of all found anomalies
anomaly_data = []
with open('anomaly_data_6.01.csv', encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_reader:
        ## First row contains information about number of candidates and seats
        if line_count == 0:
            headers = row.copy()
            
        ## Each row has number of votes, list of candidates, and then 0
        if line_count>0:
            election_data = {}
            for i, header in enumerate(headers):
                election_data[header] = row[i]
            anomaly_data.append(election_data)
    
        line_count += 1


## create list of file names for all scottish elections
file_names = {}
for folder_name in os.listdir('../full_scot_data'):
    if 'cands' in folder_name:
        for name in os.listdir(f'../full_scot_data/{folder_name}'):
            file_name = '../full_scot_data/'+folder_name+'/'+name
            file_names[name] = file_name


found_errors = []
for election_num, election in enumerate(anomaly_data):
    
    sys.stdout.write('\r')
    sys.stdout.write(f'Election {election_num+1}/{len(file_names)}')
    sys.stdout.flush()
    
    name = election['Election']
    anomalies = [[key, election[key]] for key in election.keys() if 'Ballots' in key and election[key]!='']
    lxn = mwe(file_names[name])
    full_ballots = copy.deepcopy(lxn.ballots)
    
    for anomaly in anomalies:
        anomaly_type = anomaly[0]
        removed_ballots = ast.literal_eval(anomaly[1])
        if 'Scottish' in anomaly_type:
            method = lxn.scot_stv
        elif 'AQ' in anomaly_type:
            method = lxn.aq_stv
        elif 'Meek' in anomaly_type:
            method = lxn.meek_stv
        elif '(OM)' in anomaly_type and 'Greedy' not in anomaly_type:
            method = lxn.cham_cour
        elif '(OM)' in anomaly_type and 'Greedy' in anomaly_type:
            method = lxn.greedy_cham_cour
        elif '(PM)' in anomaly_type and 'Greedy' not in anomaly_type:
            method = lxn.cham_cour
            lxn.model = 'PM'
        elif '(PM)' in anomaly_type and 'Greedy' in anomaly_type:
            method = lxn.greedy_cham_cour   
            lxn.model = 'PM'
        elif 'Expanding' in anomaly_type:
            method = lxn.expanding_approvals
        else:
            print(f'Error: {anomaly}')
        
        lxn.ballots = copy.deepcopy(full_ballots)
        winners, losers = method()
        removed_cands = []
        for ballot in removed_ballots:
            lxn.ballots[ballot] -= removed_ballots[ballot]
            for cand in ballot:
                if cand not in removed_cands:
                    removed_cands.append(cand)
        new_winners, new_losers = method()
        
        if set(winners).intersection(new_losers)-set(removed_cands):
            pass
        else:
            found_errors.append([name, anomaly])
        
        

if not found_errors:
    print('No errors found!')
else:
    print(f'Found {len(found_errors)} errors')




