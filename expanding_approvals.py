# expanding approvals election

import csv
from tabulate import tabulate
from itertools import chain, combinations, permutations
import math
import random as rand
import numpy as np


bottom=False
# with open('east_ayrshire_2012_ward5.csv', encoding="utf8") as csv_file:
with open('falkirk_2017_ward3.csv', encoding="utf8") as csv_file:
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

################################
# run expanding approvals 
################################

# ##### find strict priority ordering
# # compute rank vectors
# rank_vectors = []
# for cand in range(1, cand_num+1):
#     cand_vector = [0 for _ in range(cand_num)]
#     for ballot in ballots:
#         if cand in ballot:
#             indx = ballot.index(cand)
#             for nindx in range(indx, cand_num):
#                 cand_vector[nindx] += ballots[ballot]
#     # print(cand_vector)
#     rank_vectors.append(cand_vector)

# priority_ordering = list(range(1,cand_num+1))
# priority_ordering.sort(key = lambda cand: rank_vectors[cand-1], reverse=True)
            
# print(f'Priority ordering: {priority_ordering}')

##### run expanding approvals
ballot_weights = ballots.copy()
remaining = list(range(1, cand_num+1))
elected = []
j = 0

total_votes = 0
for ballot in ballot_weights:
    total_votes += ballot_weights[ballot]
quota = total_votes/(seat_num+1) + 1/(cand_num+1)*(np.floor(total_votes/(seat_num+1)) + 1 - total_votes/(seat_num+1))
# print(quota)

while len(elected)<seat_num:
    cand_votes = [0 for _ in range(cand_num)]
    for ballot in ballot_weights:
        ballot_num = ballot_weights[ballot]
        for cand in ballot[:j+1]:
            cand_votes[cand-1] += ballot_num
    # print(cand_votes)
    
    possible_winners = [cand for cand in remaining if cand_votes[cand-1] > quota]
    if possible_winners or j >= cand_num-2:
        # winner = priority_ordering[min([priority_ordering.index(cand) for cand in possible_winners])]
        
        remaining_votes = [cand_votes[cand-1] for cand in remaining]
        winner = remaining[remaining_votes.index(max(remaining_votes))]
        
        remaining.remove(winner)
        elected.append(winner)
        
        supporters = []
        support_vote = 0
        for ballot in ballot_weights:
            if winner in ballot[:j+1]:
                supporters.append(ballot)
                support_vote += ballot_weights[ballot]
        
        payment_frac = (support_vote - quota)/support_vote
        for ballot in supporters:
            ballot_weights[ballot] *= payment_frac
    
    else:
        j+=1
    
print('####################')
print(f'Final candidates: {elected}')
print('####################')