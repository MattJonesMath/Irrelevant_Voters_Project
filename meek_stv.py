# Meek STV election

import csv
from tabulate import tabulate
from itertools import chain, combinations, permutations
import math
import random as rand
import numpy as np


def get_cand_weights(weights, elected, max_error):
    # count votes with initial weights
    cand_votes = [0 for _ in range(cand_num)]
    excess_votes = 0
    for ballot in ballots:
        ballot_count = ballots[ballot]
        frac = 1
        for cand in ballot:
            cand_votes[cand-1] += ballot_count*weights[cand-1]*frac
            frac *= 1-weights[cand-1]
        excess_votes += ballot_count * frac
    quota = (total_votes - excess_votes) / (seat_num + 1)
    error = sum([np.abs(cand_votes[cand-1]-quota) for cand in elected])
    
    # update weights for elected candidates
    while error > 0.001:
        for cand in elected:
            weights[cand-1] = weights[cand-1]*quota/cand_votes[cand-1]
        cand_votes = [0 for _ in range(cand_num)]
        excess_votes = 0
        for ballot in ballots:
            ballot_count = ballots[ballot]
            frac = 1
            for cand in ballot:
                cand_votes[cand-1] += ballot_count*weights[cand-1]*frac
                frac *= 1-weights[cand-1]
            excess_votes += ballot_count * frac
        quota = (total_votes - excess_votes) / (seat_num + 1)
        error = sum([np.abs(cand_votes[cand-1]-quota) for cand in elected])
    
    return cand_votes, weights, quota


bottom=False
# with open('east_ayrshire_2012_ward5.csv', encoding="utf8") as csv_file:
# with open('falkirk_2017_ward3.csv', encoding="utf8") as csv_file:
# with open('edinburgh_2022_ward5.csv', encoding="utf8") as csv_file:
with open('aberdeenshire_2012_ward1.csv', encoding="utf8") as csv_file:
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
            print(f'There are {cand_num} candidates and {seat_num} seats.')
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


######
# run meek stv
######

# print(f'Number of candidates: {cand_num}')
# print(f'Number of seats: {seat_num}')

hopeful = list(range(1,cand_num+1))
elected = []
excluded = []
weights = [1 for _ in range(cand_num)]

total_votes = 0
for ballot in ballots:
    total_votes += ballots[ballot]
    
stage = 0

while hopeful:
    if len(elected)<seat_num:
        if len(elected) + len(hopeful) > seat_num:
            stage += 1
            print('##################')
            print(f'Stage {stage}')
            print(f'Filling seat {len(elected)+1}')
            
            # # count votes with initial weights
            # cand_votes = [0 for _ in range(cand_num)]
            # excess_votes = 0
            # for ballot in ballots:
            #     ballot_count = ballots[ballot]
            #     frac = 1
            #     for cand in ballot:
            #         cand_votes[cand-1] += ballot_count*weights[cand-1]*frac
            #         frac *= 1-weights[cand-1]
            #     excess_votes += ballot_count * frac
            # quota = (total_votes - excess_votes) / (seat_num + 1)
            # error = sum([np.abs(cand_votes[cand-1]-quota) for cand in elected])
            
            # # update weights for elected candidates
            # while error > 0.001:
            #     for cand in elected:
            #         weights[cand-1] = weights[cand-1]*quota/cand_votes[cand-1]
            #     cand_votes = [0 for _ in range(cand_num)]
            #     excess_votes = 0
            #     for ballot in ballots:
            #         ballot_count = ballots[ballot]
            #         frac = 1
            #         for cand in ballot:
            #             cand_votes[cand-1] += ballot_count*weights[cand-1]*frac
            #             frac *= 1-weights[cand-1]
            #         excess_votes += ballot_count * frac
            #     quota = (total_votes - excess_votes) / (seat_num + 1)
            #     error = sum([np.abs(cand_votes[cand-1]-quota) for cand in elected])
                
            cand_votes, weights, quota = get_cand_weights(weights, elected, max_error = 0.001)
            
            print(f'Candidate votes: {cand_votes}')
            print(f'Weights: {weights}')
            # print(f'Excess votes: {excess_votes}')
            # print(f'Quota: {quota}')
            
            # elect hopefuls that surpass quota
            cands_elect = [cand for cand in hopeful if cand_votes[cand-1]>=quota]
            if cands_elect:
                print(f'Electing candidates: {cands_elect}')
                for cand in cands_elect:
                    elected.append(cand)
                    hopeful.remove(cand)
                if len(elected)>seat_num:
                    cands_elect_votes = [cand_votes[cand-1] for cand in cands_elect]
                    min_votes = min(cands_elect_votes)
                    if cands_elect_votes.count(min_votes) == 1:
                        elected.remove(cands_elect[cands_elect_votes.index(min_votes)])
                    else:
                        min_cands = [cand for cand in cands_elect if cand_votes[cand-1] == min_votes]
                        elected.remove(rand.choice(min_cands))
            else:
                hopeful_votes = [cand_votes[cand-1] for cand in hopeful]
                losers = [cand for cand in hopeful if cand_votes[cand-1] == min(hopeful_votes)]
                print(f'Excluding candidates: {losers}')
                for cand in losers:
                    excluded.append(cand)
                    hopeful.remove(cand)
                    weights[cand-1] = 0
        
        else:
            # elect all hopeful candidates
            cand_votes, weights, quota = get_cand_weights(weights, elected, max_error = 0.001)
            hopeful_votes = [cand_votes[cand-1] for cand in hopeful]
            while hopeful:
                indx = hopeful_votes.index(max(hopeful_votes))
                elected.append(hopeful.pop(indx))
    
    else:
        # exclude all hopeful candidates
        
        cand_votes, weights, quota = get_cand_weights(weights, elected, max_error = 0.001)
        hopeful_votes = [cand_votes[cand-1] for cand in hopeful]
        while hopeful:
            indx = hopeful_votes.index(min(hopeful_votes))
            excluded.append(hopeful.pop(indx))
            hopeful_votes.pop(indx)
                
    
print('####################')
print(f'Final candidates: {elected}')
print('####################')