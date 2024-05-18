#################################
# Contains functions for many different 
# multi-winner methods
#################################
import csv
import numpy as np
import random as rand
from itertools import combinations

class mw_elections:
    
    
    def __init__(self, name):
        self.name = name
        self.ballots, self.cand_num, self.seat_num = self.get_ballots(self.name)
    
    
    #####################################
    ## read csv files from mggg/scot-elex
    #####################################
    def get_ballots(self, name):
        bottom=False
        with open(name, encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0
            for row in csv_reader:
                if row[0][0]=='0':
                    if len(row[0])==1 or row[0][1]!='.':
                        bottom = True
                ## First row contains information about number of candidates and seats
                if line_count == 0:
                    indx = row[0].index(' ')
                    cand_num = int(row[0][:indx])
                    seat_num = int(row[0][indx:])
                    ballots = {}
                    
                ## Each row has number of votes, list of candidates, and then 0
                if line_count>0 and not bottom:
                    ballot_str = row[0]
                    indx = ballot_str.index(' ')
                    ballot_num = float(ballot_str[:indx])
                    ballot_list = []
                    for x in ballot_str[indx:].split():
                        if x !='0':
                            ballot_list.append(int(x))
                    ballot = tuple(ballot_list)
                    if ballot in ballots:
                        ballots[ballot] += ballot_num
                    else:
                        ballots[ballot] = ballot_num
            
                line_count += 1
        
        ## return dictionary of ballots and number of candidates and seats
        return ballots, cand_num, seat_num


    #######################
    ## standard scottish STV
    #######################
    def scot_stv(self):
        stv_ballots = self.ballots.copy()
        remaining = list(range(1,self.cand_num+1))
        elected = []
        removed = []
        ballot_total = 0
        for ballot in stv_ballots:
            ballot_total += stv_ballots[ballot]
        quota = int(ballot_total/(self.seat_num+1)) + 1
    
        ## each iteration removes a candidate by electing the candidate
        ## that surpasses quota or removing the weakest remaining candidate
        while remaining:
            ## Count how many first place votes each candidate has
            vote_counts = []
            for cand in remaining:
                votes = 0
                for ballot in stv_ballots:
                    if ballot[0]==cand:
                        votes+=stv_ballots[ballot]
                vote_counts.append(votes)
            
            ## only go through computations if more candidates need to be elected
            if len(elected)<self.seat_num:
                ## only go through computations if more candidates need to be removed
                if len(elected)+len(remaining)>self.seat_num:
                    ## a candidate has quota, so elect the top candidate remaining
                    if max(vote_counts)>=quota:
                        indx = vote_counts.index(max(vote_counts))
                        removed_frac = quota/vote_counts[indx]
                        elected.append(remaining.pop(indx))
                        new_winner = elected[-1]
                        
                        ## make new ballots that don't rank new_winner
                        new_ballots = {}
                        for ballot in stv_ballots:
                            if ballot[0] == new_winner:
                                stv_ballots[ballot] = stv_ballots[ballot]*(1-removed_frac)
                            if ballot != (new_winner,):
                                new_ballot = tuple(x for x in ballot if x!=new_winner)
                                if new_ballot in new_ballots:
                                    new_ballots[new_ballot] += stv_ballots[ballot]
                                else:
                                    new_ballots[new_ballot] = stv_ballots[ballot]
                        stv_ballots = new_ballots
                        
                    ## no candidate makes quota, so remove the worst candidate remaining
                    else:
                        indx = vote_counts.index(min(vote_counts))
                        removed.append(remaining.pop(indx))
                        new_loser = removed[-1]
                        
                        ## make new ballots that don't rank new_loser
                        new_ballots = {}
                        for ballot in stv_ballots:
                            if ballot != (new_loser,):
                                new_ballot = tuple(x for x in ballot if x!=new_loser)
                                if new_ballot in new_ballots:
                                    new_ballots[new_ballot] += stv_ballots[ballot]
                                else:
                                    new_ballots[new_ballot] = stv_ballots[ballot]
                        stv_ballots = new_ballots
    
                ## if every candidate that is left needs to win a seat, elect them
                ## in the order of first place votes
                else:
                    indx = vote_counts.index(max(vote_counts))
                    elected.append(remaining.pop(indx))
                    
            ## if all seats have been filled, remove all remaining candidates
            ## in the order of first place votes
            else:
                indx = vote_counts.index(min(vote_counts))
                removed.append(remaining.pop(indx))
    
        ## return the candidates that were elected and the candidates that were removed
        return elected, removed
    
    
    ########################################
    ## Adaptive Quota STV (aka modified stv)
    ########################################
    def aq_stv(self):
        stv_ballots = self.ballots.copy()
        remaining = list(range(1,self.cand_num+1))
        elected = []
        removed = []
        ballot_total = 0
        for ballot in stv_ballots:
            ballot_total += stv_ballots[ballot]

        ## each iteration determines how many ballots are left, computes the quota
        ## and either elects or removes a candidate
        while remaining:
            vote_counts = []
            for cand in remaining:
                votes = 0
                for ballot in stv_ballots:
                    if ballot[0]==cand:
                        votes+=stv_ballots[ballot]
                vote_counts.append(votes)
            quota = int(sum(vote_counts)/(self.seat_num+1-len(elected))) + 1
            
            ## only go through computations if more candidates need to win seats
            if len(elected)<self.seat_num:
                ## only go through computations if more candidates need to be removed
                if len(elected)+len(remaining)>self.seat_num:
                    ## candidate makes quota, elect best candidate
                    if max(vote_counts)>=quota:
                        indx = vote_counts.index(max(vote_counts))
                        removed_frac = quota/vote_counts[indx]
                        elected.append(remaining.pop(indx))
                        new_winner = elected[-1]
                        ## make new ballots without new_winner
                        new_ballots = {}
                        for ballot in stv_ballots:
                            if ballot[0] == new_winner:
                                stv_ballots[ballot]=stv_ballots[ballot]*(1-removed_frac)
                            if ballot != (new_winner,):
                                new_ballot = tuple(x for x in ballot if x!=new_winner)
                                if new_ballot in new_ballots:
                                    new_ballots[new_ballot] += stv_ballots[ballot]
                                else:
                                    new_ballots[new_ballot] = stv_ballots[ballot]
                        stv_ballots = new_ballots
                        
                    ## no candidate makes quota, remove worst candidate 
                    else:
                        indx = vote_counts.index(min(vote_counts))
                        removed.append(remaining.pop(indx))
                        new_loser = removed[-1]
                        ## make new ballots without new_loser
                        new_ballots = {}
                        for ballot in stv_ballots:
                            if ballot != (new_loser,):
                                new_ballot = tuple(x for x in ballot if x!=new_loser)
                                if new_ballot in new_ballots:
                                    new_ballots[new_ballot] += stv_ballots[ballot]
                                else:
                                    new_ballots[new_ballot] = stv_ballots[ballot]
                        stv_ballots = new_ballots
                
                ## if every candidate that is left needs to win a seat, elect them
                ## in the order of first place votes
                else:
                    indx = vote_counts.index(max(vote_counts))
                    elected.append(remaining.pop(indx))
            
            ## if all seats have been filled, remove all remaining candidates
            ## in the order of first place votes
            else:
                # print('Remaining candidates lose by default')
                indx = vote_counts.index(min(vote_counts))
                removed.append(remaining.pop(indx))

        ## return the candidates that were elected and the candidates that were removed
        return elected, removed
    
    
    ##############################
    ## Meek STV
    ##############################
    def meek_stv(self):
        hopeful = list(range(1,self.cand_num+1))
        elected = []
        excluded = []
        weights = [1 for _ in range(self.cand_num)]

        total_votes = 0
        for ballot in self.ballots:
            total_votes += self.ballots[ballot]
            
        ## At each stage, either elect or exclude candidates
        while hopeful:
            if len(elected)<self.seat_num:
                if len(elected) + len(hopeful) > self.seat_num:
                    cand_votes, weights, quota = self.get_cand_weights(weights, elected, max_error = 0.001)
                    cands_elect = [cand for cand in hopeful if cand_votes[cand-1]>=quota]
                    ## elect hopefuls that surpass quota
                    if cands_elect:
                        for cand in cands_elect:
                            elected.append(cand)
                            hopeful.remove(cand)
                        ## edge case if we accidentally elected one too many candidates
                        if len(elected)>self.seat_num:
                            cands_elect_votes = [cand_votes[cand-1] for cand in cands_elect]
                            min_votes = min(cands_elect_votes)
                            if cands_elect_votes.count(min_votes) == 1:
                                elected.remove(cands_elect[cands_elect_votes.index(min_votes)])
                            else:
                                min_cands = [cand for cand in cands_elect if cand_votes[cand-1] == min_votes]
                                elected.remove(rand.choice(min_cands))
                    ## exclude candidate(s) with the fewest votes
                    else:
                        hopeful_votes = [cand_votes[cand-1] for cand in hopeful]
                        losers = [cand for cand in hopeful if cand_votes[cand-1] == min(hopeful_votes)]
                        for cand in losers:
                            excluded.append(cand)
                            hopeful.remove(cand)
                            weights[cand-1] = 0
                
                else:
                    ## elect all hopeful candidates in order of current votes
                    cand_votes, weights, quota = self.get_cand_weights(weights, elected, max_error = 0.001)
                    hopeful_votes = [cand_votes[cand-1] for cand in hopeful]
                    while hopeful:
                        indx = hopeful_votes.index(max(hopeful_votes))
                        elected.append(hopeful.pop(indx))
            
            else:
                # exclude all hopeful candidates in order of current votes
                cand_votes, weights, quota = self.get_cand_weights(weights, elected, max_error = 0.001)
                hopeful_votes = [cand_votes[cand-1] for cand in hopeful]
                while hopeful:
                    indx = hopeful_votes.index(min(hopeful_votes))
                    excluded.append(hopeful.pop(indx))
        
        return elected, excluded


    ##################################################
    ## helper function that computes candidate weights 
    ## for Meek STV
    ##################################################
    def get_cand_weights(self, weights, elected, max_error):
        ## count votes with initial weights
        cand_votes = [0 for _ in range(self.cand_num)]
        total_votes = 0
        excess_votes = 0
        for ballot in self.ballots:
            ballot_count = self.ballots[ballot]
            total_votes += ballot_count
            ## frac keeps track of how much of a ballot reaches the next candidate in line
            frac = 1
            for cand in ballot:
                cand_votes[cand-1] += ballot_count*weights[cand-1]*frac
                frac *= 1-weights[cand-1]
                ## no more candidates get votes if frac = 0
                if frac == 0:
                    break
            excess_votes += ballot_count * frac
        quota = (total_votes - excess_votes) / (self.seat_num + 1)
        error = sum([np.abs(cand_votes[cand-1]-quota) for cand in elected])
        
        ## update weights until convergence of weights
        while error > max_error:
            ## update the weights for all elected candidates
            for cand in elected:
                weights[cand-1] = weights[cand-1]*quota/cand_votes[cand-1]
            ## recount votes
            cand_votes = [0 for _ in range(self.cand_num)]
            excess_votes = 0
            for ballot in self.ballots:
                ballot_count = self.ballots[ballot]
                ## frac keeps track of how much of a ballot reaches the next candidate in line
                frac = 1
                for cand in ballot:
                    cand_votes[cand-1] += ballot_count*weights[cand-1]*frac
                    frac *= 1-weights[cand-1]
                    ## no more candidates get votes if frac = 0
                    if frac == 0:
                        break
                excess_votes += ballot_count * frac
            quota = (total_votes - excess_votes) / (self.seat_num + 1)
            error = sum([np.abs(cand_votes[cand-1]-quota) for cand in elected])
        
        return cand_votes, weights, quota
    
    ###############################
    ## CPO-STV
    ###############################
    def cpo_stv(self):
        ## Determine certain winners and enumerate all outcomes
        full_cand_votes = [0 for _ in range(self.cand_num)]
        for ballot in self.ballots:
            ballot_count = self.ballots[ballot]
            cand = ballot[0]
            full_cand_votes[cand-1] += ballot_count

        total_votes = sum(full_cand_votes)
        quota = (total_votes) / (self.seat_num + 1)

        certain_winners = [cand for cand in range(1,self.cand_num+1) if full_cand_votes[cand-1]>=quota]
        uncertain_winners = [cand for cand in range(1,self.cand_num+1) if cand not in certain_winners]
        uncertain_num = self.seat_num - len(certain_winners)

        outcomes = list(combinations(uncertain_winners, uncertain_num))
        for i in range(len(outcomes)):
            outcomes[i] = certain_winners + list(outcomes[i])
        outcomes_comp_matrix = np.zeros((len(outcomes), len(outcomes)))

        ## scan through each pair of outcomes
        for i in range(len(outcomes)):
            for j in range(i+1, len(outcomes)):

                ## run outcome comparison
                outcome_A = outcomes[i]
                outcome_B = outcomes[j]
                outcome_A.sort()
                outcome_B.sort()
                intersection = [cand for cand in outcome_A if cand in outcome_B]
                union = [cand for cand in range(1, self.cand_num+1) if cand in outcome_A or cand in outcome_B]
                
                ## transfer votes from candidates that are not in union using meek stv
                elected = []
                weights = [0 for cand in range(self.cand_num)]
                for cand in union:
                    weights[cand-1] = 1
                cand_votes = [0 for _ in range(self.cand_num)]
                excess_votes = 0
                for ballot in self.ballots:
                    ballot_count = self.ballots[ballot]
                    ## frac keeps track of how much of a ballot reaches the next candidate in line
                    frac = 1
                    for cand in ballot:
                        cand_votes[cand-1] += ballot_count*weights[cand-1]*frac
                        frac *= 1-weights[cand-1]
                        ## no more candidates get votes if frac = 0
                        if frac == 0:
                            break
                    excess_votes += ballot_count * frac
                quota = (total_votes - excess_votes) / (self.seat_num + 1)
                
                ## candidates in the intersection have excess votes transferred
                if intersection:
                    int_votes = [cand_votes[cand-1] for cand in intersection]
                    ## transfer excess votes until no candidate in intersection has more than quota
                    while max(int_votes)>quota+0.001:
                        surplus_cand = intersection[int_votes.index(max(int_votes))]
                        elected.append(surplus_cand)
                        ## determine new weights
                        cand_votes, weights, quota = self.get_cand_weights(weights, elected, max_error = 0.001)
                        int_votes = [cand_votes[cand-1] for cand in intersection]
                     
                points_A = sum([cand_votes[cand-1] for cand in outcome_A])
                points_B = sum([cand_votes[cand-1] for cand in outcome_B])
                
                outcomes_comp_matrix[i,j] = points_A
                outcomes_comp_matrix[j,i] = points_B

        ## Look for condorcet winner or determine minimax winner
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
            
        return outcomes[win_set], condorcet
    
    
    ##########################
    ## Chamberlin-Courant Rule
    ##########################
    def cham_cour(self, model):
        ## enumerate all possible winner sets
        outcomes = list(combinations(list(range(1, self.cand_num+1)), self.seat_num))
        outcome_points = []

        for outcome in outcomes:
            points = 0
            for ballot in self.ballots:
                cands_ranked = False
                ## for each ballot, go through the candidates until finding 
                ## one in outcome
                for pos, cand in enumerate(ballot):
                    if cand in outcome:
                        points += (self.cand_num - 1 - pos)*self.ballots[ballot]
                        cands_ranked = True
                        break
                ## In the optimistic model, add points if the truncated ballot
                ## does not have any candidates in outcome
                if model == 'OM' and not cands_ranked:
                    points += self.cand_num - 1 - len(ballot)
            outcome_points.append(points)
            
        return outcomes[outcome_points.index(max(outcome_points))] 
    
    
    ################################
    ## Greed Chamberlin-Courant Rule
    ################################
    def greedy_cham_cour(self, model):
        hopeful = list(range(1, self.cand_num+1))
        elected = []
        
        ## Each round, add the candidate that improves scores the most
        while len(elected)<self.seat_num:
            ## add each hopeful candidate to the elected candidates
            outcomes = [elected + [cand] for cand in hopeful]
            outcome_points = []
            for outcome in outcomes:
                points = 0
                for ballot in self.ballots:
                    cands_ranked = False
                    ## for each ballot, go through the candidates until finding 
                    ## one in outcome
                    for pos, cand in enumerate(ballot):
                        if cand in outcome:
                            points += (self.cand_num - 1 - pos)*self.ballots[ballot]
                            cands_ranked = True
                            break
                    ## In the optimistic model, add points if the truncated ballot
                    ## does not have any candidates in outcome
                    if model == 'OM' and not cands_ranked:
                        points += self.cand_num - 1 - len(ballot)
                outcome_points.append(points)
            
            indx = outcome_points.index(max(outcome_points))
            elected.append(hopeful.pop(indx))
            
        return elected
    
    
    
    
    
    
    
    
    
    