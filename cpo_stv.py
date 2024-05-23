# CPO STV election

import csv
from tabulate import tabulate
from itertools import chain, combinations, permutations
import math
import random as rand
import numpy as np
import sys
import time

bottom=False
# with open('east_ayrshire_2012_ward5.csv', encoding="utf8") as csv_file:
# with open('falkirk_2017_ward3.csv', encoding="utf8") as csv_file:
with open('edinburgh_2022_ward5.csv', encoding="utf8") as csv_file:
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

##### worst case analysis loser ballots
# ballots = {}
# k = 2
# cand_num = 3*k
# seat_num = k
# for i in range(k):
#     ballots[(1+3*i, )] = 3
#     # ballots[(2+3*i, )] = 2
#     ballots[(3+3*i, )] = 5
#     ballots[(1+3*i, 2+3*i, 3+3*i)] = 5
#     ballots[(2+3*i, 3+3*i, 1+3*i)] = 3
#     ballots[(3+3*i, 1+3*i, 2+3*i)] = 2

##### worst case analysis winner ballots
# ballots = {}
# k = 3
# cand_num = 2*k
# seat_num = k
# ballots[(1, )] = 1000
# for i in range(k-1):
#     ballots[(1, i+2)] = 3
#     ballots[(i+2, )] = 8+i*0.09
# for i in range(k):
#     ballots[(k+i+1, )] = 10+i*0.1

ballots = {}
k = 3
cand_num = 2*k
seat_num = k
c = 10
ballots[(1, )] = 3*c
ballots[(1, 1+k)] = 1*c
ballots[(k+1, 1)] = 2*c
ballots[(1, 2+k)] = 1*c
ballots[(2+k, 1)] = 2*c
for i in range(2, k):
    ballots[(i, i+k)] = 2*c
    ballots[(i+k, i)] = 2*c
    ballots[(i, i+k+1)] = 2*c
    ballots[(i+k+1, i)] = 2*c
ballots[(k, 2*k)] = 2*c
ballots[(2*k, k)] = 2*c
ballots[(k, 1+k)] = 2*c
ballots[(1+k, k)] = 2*c

##### alt worst case analysis winner ballots
# ballots = {}
# k = 3
# cand_num = 1+2*(k-1)
# seat_num = k
# # ballots[(1, )] = 1000
# for i in range(k-1):
#     ballots[(1, 2+i)] = 20
#     ballots[(k+1+i, )] = 18


######
# run cpo stv
######
start_time = time.time()

# print(f'Number of candidates: {cand_num}')
# print(f'Number of seats: {seat_num}')

##### Enumerate all outcomes
full_cand_votes = [0 for _ in range(cand_num)]
for ballot in ballots:
    ballot_count = ballots[ballot]
    cand = ballot[0]
    full_cand_votes[cand-1] += ballot_count

total_votes = sum(full_cand_votes)
quota = (total_votes) / (seat_num + 1)

certain_winners = [cand for cand in range(1,cand_num+1) if full_cand_votes[cand-1]>=quota]
uncertain_winners = [cand for cand in range(1,cand_num+1) if cand not in certain_winners]
uncertain_num = seat_num - len(certain_winners)

outcomes = list(combinations(uncertain_winners, uncertain_num))
for i in range(len(outcomes)):
    outcomes[i] = certain_winners + list(outcomes[i])
outcomes_comp_matrix = np.zeros((len(outcomes), len(outcomes)))

for i in range(len(outcomes)):
    for j in range(i+1, len(outcomes)):

        ##### run outcome comparison
        outcome_A = outcomes[i]
        outcome_B = outcomes[j]
        outcome_A.sort()
        outcome_B.sort()
        print(f'Outcomes: {outcome_A}, {outcome_B}')
        # print(outcome_A, outcome_B)
        intersection = [cand for cand in outcome_A if cand in outcome_B]
        union = [cand for cand in range(1, cand_num+1) if cand in outcome_A or cand in outcome_B]
        
        
        # ##### scottish stv
        
        # new_ballots = {}
        # for ballot in ballots:
        #     count = ballots[ballot]
        #     new_ballot = []
        #     for cand in ballot:
        #         if cand in union:
        #             new_ballot.append(cand)
        #     if new_ballot:
        #         new_ballot = tuple(new_ballot)
        #         if new_ballot in new_ballots:
        #             new_ballots[new_ballot] += count
        #         else:
        #             new_ballots[new_ballot] = count
        #     else:
        #         new_ballot = (0, )
        #         if new_ballot in new_ballots:
        #             new_ballots[new_ballot] += count
        #         else:
        #             new_ballots[new_ballot] = count
                
        # cand_votes = [0 for _ in range(len(union))]
        # elected = []
        # for ballot in new_ballots:
        #     if ballot != (0, ):
        #         ballot_count = new_ballots[ballot]
        #         cand = ballot[0]
        #         cand_votes[union.index(cand)] += ballot_count
        
        # int_votes = [cand_votes[union.index(cand)] for cand in intersection]
        # while max(int_votes)>quota:
        #     surplus_cand = intersection[int_votes.index(max(int_votes))]
        #     # print(surplus_cand)
        #     frac = quota/cand_votes[union.index(surplus_cand)]
        #     reduced_ballots = {}
        #     for ballot in new_ballots:
        #         count = new_ballots[ballot]
        #         if surplus_cand in ballot:
        #             if ballot[0] == surplus_cand:
        #                 count *= (1-frac)
        #                 new_ballot = list(ballot)
        #                 new_ballot.remove(surplus_cand)
        #                 if not new_ballot:
        #                     new_ballot = (0, )
        #                 else:
        #                     new_ballot = tuple(new_ballot)
        #             else:
        #                 new_ballot = list(ballot)
        #                 new_ballot.remove(surplus_cand)
        #                 new_ballot = tuple(new_ballot)
        #         else:
        #             new_ballot = ballot
        #         if new_ballot in reduced_ballots:
        #             reduced_ballots[new_ballot] += count
        #         else:
        #             reduced_ballots[new_ballot] = count
        #     elected.append(surplus_cand)
        #     cand_votes = []
        #     for cand in union:
        #         if cand in elected:
        #             cand_votes.append(quota)
        #         else:
        #             votes = 0
        #             for ballot in reduced_ballots:
        #                 if ballot[0] == cand:
        #                     votes += reduced_ballots[ballot]
        #             cand_votes.append(votes)
        #     int_votes = [cand_votes[union.index(cand)] for cand in intersection]
        #     new_ballots = reduced_ballots
        
        
        
        
        ##### meek stv
        elected = []
        
        weights = [0 for cand in range(cand_num)]
        for cand in union:
            weights[cand-1] = 1
            
        cand_votes = [0 for _ in range(cand_num)]
        excess_votes = 0
        for ballot in ballots:
            ballot_count = ballots[ballot]
            frac = 1
            for cand in ballot:
                cand_votes[cand-1] += ballot_count*weights[cand-1]*frac
                frac *= 1-weights[cand-1]
                ## no more candidates get votes if frac = 0
                if frac == 0:
                    break
            excess_votes += ballot_count * frac
        quota = (total_votes - excess_votes) / (seat_num + 1)
        error = sum([np.abs(cand_votes[cand-1]-quota) for cand in elected])
        # print('###################')    
        # print('Initial votes')
        # print(f'Candidate votes: {cand_votes}')
        # print(f'Weights: {weights}')
        # print(f'Excess votes: {excess_votes}')
        # print(f'Quota: {quota}')
        
        if intersection:
            int_votes = [cand_votes[cand-1] for cand in intersection]
            while max(int_votes)>quota+0.001:
                surplus_cand = intersection[int_votes.index(max(int_votes))]
                if surplus_cand in elected:
                    print('ERROR')
                    sys.exit()
                # print(surplus_cand)
                elected.append(surplus_cand)
                
                ##### determine new weights
                cand_votes = [0 for _ in range(cand_num)]
                excess_votes = 0
                for ballot in ballots:
                    ballot_count = ballots[ballot]
                    frac = 1
                    for cand in ballot:
                        cand_votes[cand-1] += ballot_count*weights[cand-1]*frac
                        frac *= 1-weights[cand-1]
                        ## no more candidates get votes if frac = 0
                        if frac == 0:
                            break
                    excess_votes += ballot_count * frac
                quota = (total_votes - excess_votes) / (seat_num + 1)
                error = sum([np.abs(cand_votes[cand-1]-quota) for cand in elected])
                
                # print('###################')    
                # print(f'Electing candidate {surplus_cand}')
                # print(f'Candidate votes: {cand_votes}')
                # print(f'Weights: {weights}')
                # print(f'Excess votes: {excess_votes}')
                # print(f'Quota: {quota}')
                
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
                            ## no more candidates get votes if frac = 0
                            if frac == 0:
                                break
                        excess_votes += ballot_count * frac
                    quota = (total_votes - excess_votes) / (seat_num + 1)
                    error = sum([np.abs(cand_votes[cand-1]-quota) for cand in elected])
                  
                # print(f'New weights and votes')
                # print(f'Candidate votes: {cand_votes}')
                # print(f'Weights: {weights}')
                # print(f'Excess votes: {excess_votes}')
                # print(f'Quota: {quota}')
                
                int_votes = [cand_votes[cand-1] for cand in intersection]
            
        
        points_A = sum([cand_votes[cand-1] for cand in outcome_A])
        points_B = sum([cand_votes[cand-1] for cand in outcome_B])
        
        print(f'Scores: {points_A},{points_B}')
        # print(points_A, points_B)
        outcomes_comp_matrix[i,j] = points_A
        outcomes_comp_matrix[j,i] = points_B

##### Look for condorcet winner or minimax
condorcet = False
for win_set in range(len(outcomes)):
    winner = True
    for j in range(len(outcomes)):
        if outcomes_comp_matrix[win_set,j]<outcomes_comp_matrix[j,win_set]:
            winner = False
            break
    if winner:
        condorcet = True
        break

if not condorcet:
    worst_losses = []
    for outcome in range(len(outcomes)):
        scores = [outcomes_comp_matrix[outcome,i] - outcomes_comp_matrix[i,outcome] for i in range(len(outcomes))]
        worst_losses.append(min(scores))
    win_set = worst_losses.index(max(worst_losses))
    
print('#######################')
if condorcet:
    print('Condorcet winner:')
else:
    print('Minimax winner:')
print(outcomes[win_set])
print('#######################')



print(f'Total time: {time.time()-start_time}')

    
                
    
# print('####################')
# print(f'Final candidates: {elected}')
# print('####################')