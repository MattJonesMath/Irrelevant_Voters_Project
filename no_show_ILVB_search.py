import csv
import os
import pandas as pd
import ast


#############################
# Check ILVB anomalies to see if they are no show paradoxes
#############################
anom_data = pd.read_csv("C:/Users/mijones/Documents/GitHub/Irrelevant_Voters_Project/anomaly_data_l10_w3.csv")
election_data = pd.read_csv("C:/Users/mijones/Documents/GitHub/Irrelevant_Voters_Project/election_results.csv", index_col='Election')

lxn_method = 'Expanding Approvals OM'
for i in range(len(anom_data)):
    if isinstance(anom_data.at[i, lxn_method +' - Losing Voter Bloc Anomaly'], str):
        
        new_win_set = set(ast.literal_eval(anom_data.at[i, lxn_method +' - Losing Voter Bloc Anomaly']))
        removed_ballots = ast.literal_eval(anom_data.at[i, lxn_method +' - Removed Loser Ballots'])
        
        old_win_set = set(ast.literal_eval(election_data[lxn_method+' Winners'][anom_data.at[i, 'Election']]))
        new_winners = new_win_set-old_win_set
        old_winners = old_win_set-new_win_set
        
        if len(new_winners)>1:
            print('multiple winner changes')
            print(anom_data.at[i, 'Election'])
            # breakhere
            
        for nw in new_winners:
            break
        for ow in old_winners:
            break
        # nw = new_winners[0]
        # ow = old_winners[0]
        
        no_show = True
        for ballot in removed_ballots:
            if (nw not in ballot and ow not in ballot):
                no_show = False
                break

        if no_show:
            print(anom_data.at[i, 'Election'])