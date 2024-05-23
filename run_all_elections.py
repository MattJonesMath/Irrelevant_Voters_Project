#######################################
## Run all scottish elections
## Save winners for each method in file
#######################################
from elections_class import mw_elections as mwe
import os
import csv


###################################
## Chose which elections to run
###################################
run_scottish = True
run_adapt_quota = True
run_meek = True
run_cham_cour = True
run_greedy_cham_cour = True
run_expand_app = True
run_cpo_stv = True
###################################
###################################

which_methods = [run_scottish, run_adapt_quota, run_meek, run_cham_cour, run_greedy_cham_cour, run_expand_app, run_cpo_stv]
headers = ['Scottish STV Winners', 'Adaptive Quota STV Winners', 'Meek STV Winners', 'Chamberlin-Courant Winners', 'Greedy Chamberlin-Courant Winners', 'Expanding Approvals Winners', 'CPO-STV Winners']
csv_headers = ['Election']
for i in range(len(which_methods)):
    if which_methods[i]:
        csv_headers.append(headers[i])
        
## create list of file names for all scottish elections
file_names = {}
for folder_name in os.listdir('../full_scot_data'):
    # print(folder_name)
    if 'cands' in folder_name:
        for name in os.listdir(f'../full_scot_data/{folder_name}'):
            # print(file_name)
            file_name = '../full_scot_data/'+folder_name+'/'+name
            file_names[name] = file_name
 
## Run all the chosen methods on all the scottish elections
election_results = []
for name in file_names:
    print(name)
    election_dict = {}
    election_dict['Election'] = name
    election = mwe(file_names[name])
    if run_scottish:
        election_dict[headers[0]] = election.scot_stv()[0]
    if run_adapt_quota:
        election_dict[headers[1]] = election.aq_stv()[0]
    if run_meek:
        election_dict[headers[2]] = election.meek_stv()[0]
    if run_cham_cour:
        election_dict[headers[3]] = election.cham_cour('OM')
    if run_greedy_cham_cour:
        election_dict[headers[4]] = election.greedy_cham_cour('OM')
    if run_expand_app:
        election_dict[headers[5]] = election.expanding_approvals()
    if run_cpo_stv:
        election_dict[headers[6]] = election.cpo_stv()[0]
        
    election_results.append(election_dict)

## Write results to csv file
with open('election_results.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
    writer.writeheader()
    for election in election_results:
        writer.writerow(election)