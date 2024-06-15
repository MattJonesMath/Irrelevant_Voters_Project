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
        if name != '':
            self.name = name
            self.ballots, self.cand_num, self.seat_num, self.parties = self.get_ballots(self.name)
        else:
            self.ballots = {}
            self.cand_num = 0
            self.seat_num = 0
        self.model = 'OM'
        
    
    #####################################
    ## read csv files from mggg/scot-elex
    #####################################
    def get_ballots(self, name):
        parties = []
        bottom=False
        with open(name, encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0
            for row in csv_reader:
                ## First row contains information about number of candidates and seats
                if line_count == 0:
                    indx = row[0].index(' ')
                    cand_num = int(row[0][:indx])
                    seat_num = int(row[0][indx:])
                    ballots = {}
                    
                ## Get party affiliations
                if bottom and len(parties)<cand_num:
                    line = row[0]
                    
                    if '(Con)' in line or '(C)' in line  or line[0:3]=='Con' or 'Conservative' in line:
                        parties.append('Con')
                    elif '(SNP)' in line or 'SNP' in line or 'Scottish National' in line:
                        parties.append('SNP')
                    elif '(Grn)' in line or 'Scottish Green' in line or line[0:3]=='Grn':
                        parties.append('Grn')
                    elif 'Scottish Unionist' in line or '(SU)' in line:
                        parties.append('SU')
                    elif '(Lab)' in line or 'Labour' in line or line[0:3]=='Lab':
                        parties.append('Lab')
                    elif '(LD)' in line or 'Liberal Democrat' in line or line[0:2]=='LD':
                        parties.append('LD')
                    elif '(Ind)' in line or 'Independent' in line or 'Ind' in line or line[0:3]=='Ind':
                        parties.append('Ind')
                    elif '(Libtn)' in line or 'Libertarian' in line:
                        parties.append('Libtn')
                    elif '(SC)' in line or 'Scottish Christian' in line or '(Chr)' in line:
                        parties.append('SC')
                    elif '(Sol)' in line or 'Solidarity' in line:
                        parties.append('Sol')
                    elif 'UKIP' in line or 'UK Independence' in line:
                        parties.append('UKIP')
                    elif 'SFP' in line or 'Scottish Family' in line:
                        parties.append('SFP')
                    elif 'TUSC' in line or 'Trade Unionist' in line:
                        parties.append('TUSC')
                    elif '(NF)' in line or 'National Front' in line:
                        parties.append('NF')
                    elif '(Soc)' in line or 'Scottish Trade Unionist and Socialist' in line or 'Scottish Socialist' in line or 'SSP' in line:
                        parties.append('Soc')
                    elif 'API' in line or 'ALBA' in line or 'Alba' in line:
                        parties.append('Alba')
                    elif '(SDP)' in line or 'Social Democratic' in line:
                        parties.append('SDP')
                    elif '(GF)' in line or 'Glasgow First' in line:
                        parties.append('Glasgow First')
                    elif 'Britannica' in line:
                        parties.append('Britannica')
                    elif '(Pir)' in line or 'Pirate' in line:
                        parties.append('Pir')
                    elif '(Comm)' in line or 'Communist' in line:
                        parties.append('Comm')
                    elif 'BNP' in line or 'British National Party' in line:
                        parties.append('BNP')
                    elif 'CPA' in line or 'Christian People' in line:
                        parties.append('CPA')
                    elif '(SSC)' in line or 'Scottish Senior' in line:
                        parties.append('SSC')
                    elif '(MVR)' in line or 'Monster Raving' in line:
                        parties.append('MVR')
                    elif 'Sovereignty' in line:
                        parties.append('Sovereignty')
                    elif 'Volt UK' in line:
                        parties.append('Volt UK')
                    elif 'Freedom Alliance' in line:
                        parties.append('Freedom Alliance')
                    elif 'Vanguard' in line:
                        parties.append('Vanguard')
                    elif '(SEFP)' in line:
                        parties.append('SEFP')
                    elif '(Lib)' in line or 'Liberal Party' in line:
                        parties.append('Liberal')
                    elif 'EDIA' in line or 'East Dunbartonshire' in line:
                        parties.append('EDIA')
                    elif 'Borders' in line:
                        parties.append('Scottish Borders')
                    elif 'EKA' in line or 'East Kilbride' in line:
                        parties.append('EKA')
                    elif 'CICA' in line:
                        parties.append('CICA')
                    elif 'Rubbish' in line:
                        parties.append('Rubbish')
                    elif 'British Unionist' in line:
                        parties.append('British Unionist')
                    elif 'OMG' in line:
                        parties.append('OMG')
                    elif 'WDCP' in line or 'West Dunbartonshire' in line or '(WDuns)' in line:
                        parties.append('WDuns')
                    else:
                        parties.append('Unknown')

                    
                    
                    
                    # if len(parties)<cand_num:
                    #     if '(' in row[0]:
                    #         indx = row[0].index('(')
                    #         nindx = row[0].index(')')
                    #         party = row[0][indx+1: nindx]
                    #         parties.append(party)
                    #     elif '"' in row[0]:
                    #         indxs = [i for i in range(len(row[0])) if row[0][i] == '"']
                    #         party = row[0][indxs[-2]+1: indxs[-1]]
                    #         parties.append(party)
                    #     else:
                    #         parties.append('None Listed')
                        
                if row[0][0]=='0':
                    if len(row[0])==1 or row[0][1]!='.':
                        bottom = True
                    
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
        return ballots, cand_num, seat_num, parties


    #######################
    ## standard scottish STV
    #######################
    def scot_stv(self):
        stv_ballots = self.ballots.copy()
        ## remaining is candidates that have not had excess redistributed
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
                
            
            # print('## next round ##')
            # print(remaining)
            # print(elected)
            # print(vote_counts)
            # print(quota)
            
            
            ## only go through computations if more candidates need to be elected
            if len(elected)<self.seat_num:
                ## only go through computations if more candidates need to be removed
                if len(elected)+len(remaining)>self.seat_num:
                    ## a candidate has quota, so elect the top candidate remaining
                    if max(vote_counts)>=quota:
                        
                        ## all that make surplus elected
                        for i in range(len(remaining)):
                            if vote_counts[i]>=quota and remaining[i] not in elected:
                                elected.append(remaining[i])
                        
                        ## redistribute votes for top winner
                        indx = vote_counts.index(max(vote_counts))
                        removed_frac = quota/vote_counts[indx]
                        new_winner = remaining[indx]
                        remaining.remove(new_winner)
                        
                        ## make new ballots that don't rank new_winner
                        new_ballots = {}
                        for ballot in stv_ballots:
                            ## take away ballots that support new_winner
                            if ballot[0] == new_winner:
                                stv_ballots[ballot] = stv_ballots[ballot]*(1-removed_frac)
                                
                            ## redistribute all excess votes to lower candidates that have not been elected
                            if ballot[0] == new_winner and set(ballot)-set(elected):
                                new_ballot = tuple(x for x in ballot if x not in elected)
                            ## votes for candidates that have been elected but are not new_winner are untouched except removing new_winner
                            elif ballot[0] in remaining and ballot[0] in elected:
                                new_ballot = tuple(x for x in ballot if x != new_winner)
                            ## all other votes remove all elected candidates
                            elif set(ballot)-set(elected):
                                new_ballot = tuple(x for x in ballot if x not in elected)
                            else:
                                new_ballot = []
        
                            if new_ballot:                                  
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
                if remaining[indx] in elected:
                    remaining.pop(indx)
                else:
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
        redistributed = 0
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
            ## recompute quota
            quota = int(sum(vote_counts)/(self.seat_num+1-redistributed)) + 1
            
            
            # print('## next round ##')
            # print(remaining)
            # print(elected)
            # print(vote_counts)
            # print(quota)
            
            
            ## only go through computations if more candidates need to win seats
            if len(elected)<self.seat_num:
                ## only go through computations if more candidates need to be removed
                if len(elected)+len(remaining)>self.seat_num:
                    ## candidate makes quota, elect best candidate
                    if max(vote_counts)>=quota:
                        
                        ## all that make surplus elected, only top has excess redistributed
                        for i in range(len(remaining)):
                            if vote_counts[i]>=quota and remaining[i] not in elected:
                                elected.append(remaining[i])
                        
                        ## top candidate has votes redistributed
                        indx = vote_counts.index(max(vote_counts))
                        removed_frac = quota/vote_counts[indx]
                        new_winner = remaining[indx]
                        remaining.remove(new_winner)
                        redistributed += 1

                        
                        ## make new ballots without new_winner
                        new_ballots = {}
                        for ballot in stv_ballots:
                            ## take away ballots that support new_winner
                            if ballot[0] == new_winner:
                                stv_ballots[ballot] = stv_ballots[ballot]*(1-removed_frac)
                                
                            ## redistribute all excess votes to lower candidates that have not been elected
                            if ballot[0] == new_winner and set(ballot)-set(elected):
                                new_ballot = tuple(x for x in ballot if x not in elected)
                            ## votes for candidates that have been elected but are not new_winner are untouched except removing new_winner
                            elif ballot[0] in remaining and ballot[0] in elected:
                                new_ballot = tuple(x for x in ballot if x != new_winner)
                            ## all other votes remove all elected candidates
                            elif set(ballot)-set(elected):
                                new_ballot = tuple(x for x in ballot if x not in elected)
                            else:
                                new_ballot = []
                                    
                            if new_ballot:                                  
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
                if remaining[indx] in elected:
                    remaining.pop(indx)
                else:
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
                    while hopeful:
                        hopeful_votes = [cand_votes[cand-1] for cand in hopeful]
                        indx = hopeful_votes.index(max(hopeful_votes))
                        elected.append(hopeful.pop(indx))
            
            else:
                # exclude all hopeful candidates in order of current votes
                cand_votes, weights, quota = self.get_cand_weights(weights, elected, max_error = 0.001)
                hopeful_votes = [cand_votes[cand-1] for cand in hopeful]
                while hopeful:
                    indx = hopeful_votes.index(min(hopeful_votes))
                    excluded.append(hopeful.pop(indx))
                    hopeful_votes.pop(indx)
        
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
            
        winner_set = outcomes[win_set]
        loser_set = [cand for cand in range(1,self.cand_num+1) if cand not in winner_set]
        
        return winner_set, loser_set, condorcet
    
    
    ##########################
    ## Chamberlin-Courant Rule
    ##########################
    def cham_cour(self):
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
                if self.model == 'OM' and not cands_ranked:
                    points += self.cand_num - 1 - len(ballot)
            outcome_points.append(points)
            
        winner_set = list(outcomes[outcome_points.index(max(outcome_points))])
        loser_set = [cand for cand in range(1,self.cand_num+1) if cand not in winner_set]
            
        return winner_set, loser_set
    
    
    ################################
    ## Greed Chamberlin-Courant Rule
    ################################
    def greedy_cham_cour(self):
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
                    if self.model == 'OM' and not cands_ranked:
                        points += self.cand_num - 1 - len(ballot)
                outcome_points.append(points)
            
            indx = outcome_points.index(max(outcome_points))
            elected.append(hopeful.pop(indx))
            
        return elected, hopeful
    
    
    ###############################
    ## Expanding Approvals
    ###############################
    def expanding_approvals(self):
        ballot_weights = self.ballots.copy()
        remaining = list(range(1, self.cand_num+1))
        elected = []
        j = 0

        total_votes = 0
        for ballot in ballot_weights:
            total_votes += ballot_weights[ballot]
        # quota = total_votes/(self.seat_num+1) + 1/(cand_num+1)*(np.floor(total_votes/(seat_num+1)) + 1 - total_votes/(seat_num+1))
        quota = total_votes/(self.seat_num+1)

        while len(elected)<self.seat_num:
            cand_votes = [0 for _ in range(self.cand_num)]
            for ballot in ballot_weights:
                ballot_num = ballot_weights[ballot]
                for cand in ballot[:j+1]:
                    cand_votes[cand-1] += ballot_num
            
            possible_winners = [cand for cand in remaining if cand_votes[cand-1] > quota]
            if possible_winners or j >= self.cand_num-2:
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
    
        return elected, remaining
    
    
    
    
    
    
    