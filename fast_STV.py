###############################################
# Determine how often scottish elections 
# break the indifference to non-voters property
############################################### 

import csv
from tabulate import tabulate
from itertools import chain, combinations, permutations
import math
import random as rand
import os
import multiprocessing
import copy

def stv(ballots, cand_num, seat_num):
    remaining = list(range(1,cand_num+1))
    elected = []
    removed = []
    ballot_total = 0
    for ballot in ballots:
        ballot_total += ballots[ballot]
    quota = int(ballot_total/(seat_num+1)) + 1

    while remaining:
        vote_counts = []
        for cand in remaining:
            votes = 0
            for ballot in ballots:
                if ballot[0]==cand:
                    votes+=ballots[ballot]
            vote_counts.append(votes)
        # print(vote_counts)
        
        if len(elected)<seat_num:
            if len(elected)+len(remaining)>seat_num:
                # print(f'Filling seat {len(elected)+1}')
                
                if max(vote_counts)>=quota:
                    indx = vote_counts.index(max(vote_counts))
                    removed_frac = quota/vote_counts[indx]
                    # print(f'Candidate {remaining[indx]} wins seat')
                    elected.append(remaining.pop(indx))
                    new_winner = elected[-1]
                    # new_ballot_list = create_ballot_list(remaining, len(remaining))
                    # new_ballot_counts = [0 for _ in new_ballot_list]
                    new_ballots = {}
                    for ballot in ballots:
                        if ballot[0] == new_winner:
                            ballots[ballot]= ballots[ballot]*(1-removed_frac)
                        if ballot != (new_winner,):
                            new_ballot = tuple(x for x in ballot if x!=new_winner)
                            if new_ballot in new_ballots:
                                new_ballots[new_ballot] += ballots[ballot]
                            else:
                                new_ballots[new_ballot] = ballots[ballot]
                    
                    ballots = new_ballots
                    
                else:
                    indx = vote_counts.index(min(vote_counts))
                    # print(f'Candidate {remaining[indx]} is removed')
                    removed.append(remaining.pop(indx))
                    new_loser = removed[-1]
                    
                    new_ballots = {}
                    for ballot in ballots:
                        if ballot != (new_loser,):
                            new_ballot = tuple(x for x in ballot if x!=new_loser)
                            if new_ballot in new_ballots:
                                new_ballots[new_ballot] += ballots[ballot]
                            else:
                                new_ballots[new_ballot] = ballots[ballot]
                    
                    ballots = new_ballots

            else:
                # print('Remaining candidates win by default')
                indx = vote_counts.index(max(vote_counts))
                elected.append(remaining.pop(indx))
        else:
            # print('Remaining candidates lose by default')
            indx = vote_counts.index(min(vote_counts))
            removed.append(remaining.pop(indx))

    return elected, removed

def mstv(ballots, cand_num, seat_num):
    remaining = list(range(1,cand_num+1))
    elected = []
    removed = []
    ballot_total = 0
    for ballot in ballots:
        ballot_total += ballots[ballot]
    # quota = int(ballot_total/(seat_num+1)) + 1

    while remaining:
        vote_counts = []
        for cand in remaining:
            votes = 0
            for ballot in ballots:
                if ballot[0]==cand:
                    votes+=ballots[ballot]
            vote_counts.append(votes)
        # print(vote_counts)
        quota = int(sum(vote_counts)/(seat_num+1-len(elected))) + 1
        
        if len(elected)<seat_num:
            if len(elected)+len(remaining)>seat_num:
                # print(f'Filling seat {len(elected)+1}')
                
                if max(vote_counts)>=quota:
                    indx = vote_counts.index(max(vote_counts))
                    removed_frac = quota/vote_counts[indx]
                    # print(f'Candidate {remaining[indx]} wins seat')
                    elected.append(remaining.pop(indx))
                    new_winner = elected[-1]
                    # new_ballot_list = create_ballot_list(remaining, len(remaining))
                    # new_ballot_counts = [0 for _ in new_ballot_list]
                    new_ballots = {}
                    for ballot in ballots:
                        if ballot[0] == new_winner:
                            ballots[ballot]= ballots[ballot]*(1-removed_frac)
                        if ballot != (new_winner,):
                            new_ballot = tuple(x for x in ballot if x!=new_winner)
                            if new_ballot in new_ballots:
                                new_ballots[new_ballot] += ballots[ballot]
                            else:
                                new_ballots[new_ballot] = ballots[ballot]
                    
                    ballots = new_ballots
                    
                else:
                    indx = vote_counts.index(min(vote_counts))
                    # print(f'Candidate {remaining[indx]} is removed')
                    removed.append(remaining.pop(indx))
                    new_loser = removed[-1]
                    
                    new_ballots = {}
                    for ballot in ballots:
                        if ballot != (new_loser,):
                            new_ballot = tuple(x for x in ballot if x!=new_loser)
                            if new_ballot in new_ballots:
                                new_ballots[new_ballot] += ballots[ballot]
                            else:
                                new_ballots[new_ballot] = ballots[ballot]
                    
                    ballots = new_ballots

            else:
                # print('Remaining candidates win by default')
                indx = vote_counts.index(max(vote_counts))
                elected.append(remaining.pop(indx))
        else:
            # print('Remaining candidates lose by default')
            indx = vote_counts.index(min(vote_counts))
            removed.append(remaining.pop(indx))

    return elected, removed


def get_ballots(name):
    bottom=False
    with open(name, encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            # print(row)
            if row[0][0]=='0':
                if len(row[0])==1 or row[0][1]!='.':
                    bottom = True
    
            if line_count == 0:
                indx = row[0].index(' ')
                cand_num = int(row[0][:indx])
                seat_num = int(row[0][indx:])
                # print(f'There are {cand_num} candidates and {seat_num} seat(s).')
                ballots = {}
                
            if line_count>0 and not bottom:
                ballot_str = row[0]
                indx = ballot_str.index(' ')
                ballot_num = float(ballot_str[:indx])
                ballot_list = []
                for x in ballot_str[indx:].split():
                    if x !='0':
                        ballot_list.append(int(x))
                # print(f'There are {ballot_num} ballots of form {ballot}')
                ballot = tuple(ballot_list)
                if ballot in ballots:
                    ballots[ballot] += ballot_num
                else:
                    ballots[ballot] = ballot_num
    
            line_count += 1
    
    return ballots, cand_num, seat_num

def get_ballots_non_voters(name, keeper_candidates):
    bottom=False
    with open(name, encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            # print(row)
            if row[0][0]=='0':
                if len(row[0])==1 or row[0][1]!='.':
                    bottom = True
    
            if line_count == 0:
                indx = row[0].index(' ')
                cand_num = int(row[0][:indx])
                seat_num = int(row[0][indx:])
                # print(f'There are {cand_num} candidates and {seat_num} seat(s).')
                ballots = {}
                
            if line_count>0 and not bottom:
                ballot_str = row[0]
                indx = ballot_str.index(' ')
                ballot_num = float(ballot_str[:indx])
                ballot_list = []
                for x in ballot_str[indx:].split():
                    if x !='0':
                        ballot_list.append(int(x))
                # print(f'There are {ballot_num} ballots of form {ballot}')
                ballot = tuple(ballot_list)
                if set(ballot_list).intersection(set(keeper_candidates)):
                    if ballot in ballots:
                        ballots[ballot] += ballot_num
                    else:
                        ballots[ballot] = ballot_num
    
            line_count += 1
    
    return ballots, cand_num, seat_num

def run_stv(name):
    ballots, cand_num, seat_num = get_ballots(name)
    elected, removed = stv(ballots, cand_num, seat_num)
    return elected, removed

def run_stv_keepers(name, keeper_candidates):
    ballots, cand_num, seat_num = get_ballots_non_voters(name, keeper_candidates)
    elected, removed = stv(ballots, cand_num, seat_num)
    return elected, removed

def run_mstv(name):
    ballots, cand_num, seat_num = get_ballots(name)
    elected, removed = mstv(ballots, cand_num, seat_num)
    return elected, removed

def count_loser_ballots(name, keeper_candidates):
    loser_ballots_count = []
    bottom=False
    with open(name, encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            # print(row)
            if row[0][0]=='0':
                if len(row[0])==1 or row[0][1]!='.':
                    bottom = True
    
            if line_count == 0:
                indx = row[0].index(' ')
                cand_num = int(row[0][:indx])
                seat_num = int(row[0][indx:])
                # print(f'There are {cand_num} candidates and {seat_num} seat(s).')
                ballots = {}
                
            if line_count>0 and not bottom:
                ballot_str = row[0]
                indx = ballot_str.index(' ')
                ballot_num = float(ballot_str[:indx])
                ballot_list = []
                for x in ballot_str[indx:].split():
                    if x !='0':
                        ballot_list.append(int(x))
                # print(f'There are {ballot_num} ballots of form {ballot}')
                if not set(ballot_list).intersection(set(keeper_candidates)):
                    loser_ballots_count.append(ballot_num)
            line_count += 1
    
    return loser_ballots_count

###############
# single election
###############
# name = './full_scot_data/5_cands/east_ayrshire_2012_ward5.csv'

# ballots, cand_num, seat_num = get_ballots(name)
# winners, losers = stv(ballots, cand_num, seat_num)
# print(winners, losers)

# keepers = winners + [losers[-1]]

# ballots, cand_num, seat_num = get_ballots_non_voters(name, keepers)
# winners, losers = stv(ballots, cand_num, seat_num)
# print(winners, losers)

###############
# check for inv violations on all elections
# all elections
###############
# linv_violations = []
# winv_violations = []
# for folder_name in os.listdir('./full_scot_data'):
#     print(folder_name)
#     if 'cands' in folder_name:
#     # if folder_name[0] in [3,4,5,6,7,8]:
#         for file_name in os.listdir(f'./full_scot_data/{folder_name}'):
#             print(file_name)
#             name = './full_scot_data/'+folder_name+'/'+file_name
#             # print(name)
#             winners, losers = run_stv(name)
#             # print(winners, losers)
            
#             for loser in losers:
#                 keepers = winners + [loser]
#                 linv_winners, linv_losers = run_stv_keepers(name, keepers)
#                 if set(winners)!=set(linv_winners):
#                     linv_violations.append(name)
#                     break
            
            # keepers = winners + [losers[-1]]
            # linv_winners, linv_losers = run_stv_keepers(name, keepers)
            # # print(linv_winners, linv_losers)
            # if not set(winners)==set(linv_winners):
            #     # print('LINV violation')
            #     linv_violations.append(name)
            # for i in range(1,len(winners)):
            #     keepers = winners[i:]+losers
            #     winv_winners, winv_losers = run_stv_keepers(name,keepers)
            #     if not set(winners[i:]).issubset(set(winv_winners)):
            #         # print('WINV violation')
            #         winv_violations.append(name)
            #         break


################
# compare stv to mstv on all elections
################
# stv_mstv_diff = []
# for folder_name in os.listdir('./full_scot_data'):
#     print(folder_name)
#     if 'cands' in folder_name:
#         for file_name in os.listdir(f'./full_scot_data/{folder_name}'):
#             print(file_name)
#             name = './full_scot_data/'+folder_name+'/'+file_name
#             stv_win, stv_lose = run_stv(name)
#             mstv_win, mstv_lose = run_mstv(name)
            
#             if set(stv_win)!=set(mstv_win):
#                 stv_mstv_diff.append(name)

######################
# count how many possible removals there are
# for the brute force approach
######################
brute_force_counts = []
for folder_name in os.listdir('./full_scot_data'):
    print(folder_name)
    if 'cands' in folder_name:
    # if folder_name[0] in [3,4,5,6,7,8]:
        for file_name in os.listdir(f'./full_scot_data/{folder_name}'):
            print(file_name)
            name = './full_scot_data/'+folder_name+'/'+file_name
            # print(name)
            winners, losers = run_stv(name)
            loser_ballots = count_loser_ballots(name, winners)
            count = 1
            for ballot in loser_ballots:
                count *= ballot
            brute_force_counts.append(count)
