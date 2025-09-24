## exhaustive search of small election

from elections_class import mw_elections as mwe
import time
import copy
import os
import sys





# election = mwe('../full_scot_data/5_cands/east_ayrshire_2012_ward5.csv')

# wins = set(election.scot_stv()[0])

# loser_ballots = []
# loser_ballot_counts = []
# for ballot in election.ballots.keys():
#     if not wins.intersection(ballot):
#         loser_ballots.append(ballot)
#         loser_ballot_counts.append(int(election.ballots[ballot]))
        

# total_subsets = 1
# for count in loser_ballot_counts:
#     total_subsets *= (count+1)
# print(total_subsets)


# ballot_changes_old = [[]]
# for count in loser_ballot_counts:
#     ballot_changes_new = []
#     for i in range(count+1):
#         for x in ballot_changes_old:
#             ballot_changes_new.append(x+[i])
#     ballot_changes_old = ballot_changes_new

# for j, changes in enumerate(ballot_changes_new):
#     print(j)
#     for i, ballot in enumerate(loser_ballots):
#         election.ballots[ballot] = changes[i]
        
#     if set(election.scot_stv()[0]) != wins:
#         print('changes')
#         break




## create list of file names for all scottish elections
file_names = {}
for folder_name in os.listdir('../full_scot_data'):
    # print(folder_name)
    if '5_cands' in folder_name:
        for name in os.listdir(f'../full_scot_data/{folder_name}'):
            # print(file_name)
            file_name = '../full_scot_data/'+folder_name+'/'+name
            
            File=open(file_name,'r', encoding='utf-8')
            lines=File.readlines()
            
            if '5 3' in lines[0]:
                file_names[name] = file_name
 
    
 
## ILVB exhaustive search
start_time = time.time()
election_results = []
for election_num, name in enumerate(file_names):
    print()
    print(f'Election {election_num+1}/{len(file_names)}')
    
    election = mwe(file_names[name])

    wins = set(election.cham_cour()[0])

    loser_ballots = []
    loser_ballot_counts = []
    for ballot in election.ballots.keys():
        if not wins.intersection(ballot):
            loser_ballots.append(ballot)
            loser_ballot_counts.append(int(election.ballots[ballot]))
            

    total_subsets = 1
    for count in loser_ballot_counts:
        total_subsets *= (count+1)
    print(f'Total election count = {total_subsets}')


    ballot_changes_old = [[]]
    for count in loser_ballot_counts:
        ballot_changes_new = []
        for i in range(count+1):
            for x in ballot_changes_old:
                ballot_changes_new.append(x+[i])
        ballot_changes_old = ballot_changes_new

    for j, changes in enumerate(ballot_changes_new):
        sys.stdout.write('\r')
        sys.stdout.write(str(j))
        sys.stdout.flush()
        for i, ballot in enumerate(loser_ballots):
            election.ballots[ballot] = changes[i]
            
        if set(election.cham_cour()[0]) != wins:
            print('ILVB violation in ' + name)
            break
    
print(f'Total time = {time.time() - start_time}')






# ## IWVB exhaustive search
# start_time = time.time()
# election_results = []
# for election_num, name in enumerate(file_names):
#     print()
#     print(f'Election {election_num+1}/{len(file_names)}')
    
#     election = mwe(file_names[name])

#     wins = election.scot_stv()[0]
#     losers = [cand for cand in range(1,6) if cand not in wins]
    
#     win_sets = [[wins[0]], [wins[1]], [wins[2]], [wins[0],wins[1]], [wins[0], wins[2]], [wins[1], wins[2]], wins]

#     print(wins)
#     print(win_sets)
    
#     for win_set in win_sets:
#         print(win_set)
#         keep_cands = set(losers).union(win_set)
#         winner_ballots = []
#         winner_ballot_counts = []
#         for ballot in election.ballots.keys():
#             if not keep_cands.intersection(ballot):
#                 winner_ballots.append(ballot)
#                 winner_ballot_counts.append(int(election.ballots[ballot]))
        
#         print(winner_ballots)
        
#         total_subsets = 1
#         for count in winner_ballot_counts:
#             total_subsets *= (count+1)
#         print(f'Total election count = {total_subsets}')
        
#         ballot_changes_old = [[]]
#         for count in winner_ballot_counts:
#             ballot_changes_new = []
#             for i in range(count+1):
#                 for x in ballot_changes_old:
#                     ballot_changes_new.append(x+[i])
#             ballot_changes_old = ballot_changes_new
            
#         print(len(ballot_changes_old))
    
#     breakhere
#     loser_ballots = []
#     loser_ballot_counts = []
#     for ballot in election.ballots.keys():
#         if not wins.intersection(ballot):
#             loser_ballots.append(ballot)
#             loser_ballot_counts.append(int(election.ballots[ballot]))
            

#     total_subsets = 1
#     for count in loser_ballot_counts:
#         total_subsets *= (count+1)
#     print(f'Total election count = {total_subsets}')


#     ballot_changes_old = [[]]
#     for count in loser_ballot_counts:
#         ballot_changes_new = []
#         for i in range(count+1):
#             for x in ballot_changes_old:
#                 ballot_changes_new.append(x+[i])
#         ballot_changes_old = ballot_changes_new

#     for j, changes in enumerate(ballot_changes_new):
#         sys.stdout.write('\r')
#         sys.stdout.write(str(j))
#         sys.stdout.flush()
#         for i, ballot in enumerate(loser_ballots):
#             election.ballots[ballot] = changes[i]
            
#         if set(election.scot_stv()[0]) != wins:
#             print('ILVB violation in ' + name)
#             break
    
# print(f'Total time = {time.time() - start_time}')