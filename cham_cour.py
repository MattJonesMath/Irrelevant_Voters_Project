# Chamberlin Courant election

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


######
# run cham cour
######
start_time = time.time()

# print(f'Number of candidates: {cand_num}')
# print(f'Number of seats: {seat_num}')

##### Enumerate all outcomes
outcomes = list(combinations(list(range(1, cand_num+1)),seat_num))
outcome_points = []
for outcome in outcomes:
    points = 0
    for ballot in ballots:
        cands_ranked = False
        for pos, cand in enumerate(ballot):
            if cand in outcome:
                points += (cand_num - 1 - pos)*ballots[ballot]
                cands_ranked = True
                break
        ## optimistic model
        if not cands_ranked:
            points += cand_num - 1 - len(ballot)
    outcome_points.append(points)
    
print(outcomes[outcome_points.index(max(outcome_points))])



################
## greedy version
################

hopeful = list(range(1, cand_num+1))
elected = []

while len(elected)<seat_num:
    outcomes = [elected + [cand] for cand in hopeful]
    
    outcome_points = []
    for outcome in outcomes:
        points = 0
        for ballot in ballots:
            cands_ranked = False
            for pos, cand in enumerate(ballot):
                if cand in outcome:
                    points += (cand_num - 1 - pos)*ballots[ballot]
                    cands_ranked = True
                    break
            ## optimistic model
            if not cands_ranked:
                points += cand_num - 1 - len(ballot)
        outcome_points.append(points)
    
    indx = outcome_points.index(max(outcome_points))
    elected.append(hopeful.pop(indx))
    
print(elected)
    
    
                

