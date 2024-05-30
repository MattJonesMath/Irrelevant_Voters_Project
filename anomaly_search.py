#######################################
## Run all scottish elections
## Save winners for each method in file
#######################################
from elections_class import mw_elections as mwe
import os
import csv
import sys


def loser_anomaly_search(file_name, method_indx):
    full_lxn = mwe(file_name)
    method_functions_full = [full_lxn.scot_stv, full_lxn.aq_stv, full_lxn.meek_stv, full_lxn.cham_cour, full_lxn.greedy_cham_cour, full_lxn.expanding_approvals, full_lxn.cpo_stv]
    lxn_method_full = method_functions_full[method_indx]
    full_results = lxn_method_full()
    winners = full_results[0]
    losers = full_results[1]

    lxn = mwe('')
    lxn.cand_num = full_lxn.cand_num
    lxn.seat_num = full_lxn.seat_num
    method_functions = [lxn.scot_stv, lxn.aq_stv, lxn.meek_stv, lxn.cham_cour, lxn.greedy_cham_cour, lxn.expanding_approvals, lxn.cpo_stv]
    lxn_method = method_functions[method_indx]

    remove_fracs = [i/10 for i in range(10,0,-1)]
    # remove_fracs = [1]
    for loser in reversed(losers):
        keep_set = set(winners + [loser])
        for frac in reversed(remove_fracs):
            excluded_ballots = {}
            mod_ballots = {}
            for ballot in full_lxn.ballots:
                count = full_lxn.ballots[ballot]
                if set(ballot).intersection(keep_set):
                    mod_ballots[ballot] = count
                else:
                    excluded_ballots[ballot] = frac * count
                    mod_ballots[ballot] = (1-frac) * count
            lxn.ballots = mod_ballots
            new_winners = lxn_method()[0]
            if loser in new_winners:
                return new_winners, excluded_ballots
    return [], {}


def loser_anomaly_search_whole_ballots(file_name, method_indx):
    full_lxn = mwe(file_name)
    method_functions_full = [full_lxn.scot_stv, full_lxn.aq_stv, full_lxn.meek_stv, full_lxn.cham_cour, full_lxn.greedy_cham_cour, full_lxn.expanding_approvals, full_lxn.cpo_stv]
    lxn_method_full = method_functions_full[method_indx]
    full_results = lxn_method_full()
    winners = full_results[0]
    losers = full_results[1]

    lxn = mwe('')
    lxn.cand_num = full_lxn.cand_num
    lxn.seat_num = full_lxn.seat_num
    method_functions = [lxn.scot_stv, lxn.aq_stv, lxn.meek_stv, lxn.cham_cour, lxn.greedy_cham_cour, lxn.expanding_approvals, lxn.cpo_stv]
    lxn_method = method_functions[method_indx]

    remove_fracs = [i/10 for i in range(10,0,-1)]
    # remove_fracs = [1]
    for loser in reversed(losers):
        keep_set = set(winners + [loser])
        for frac in reversed(remove_fracs):
            excluded_ballots = {}
            mod_ballots = {}
            for ballot in full_lxn.ballots:
                count = full_lxn.ballots[ballot]
                if set(ballot).intersection(keep_set):
                    mod_ballots[ballot] = count
                else:
                    excluded_ballots[ballot] = int(frac * count)
                    mod_ballots[ballot] = count - int(frac * count)
            lxn.ballots = mod_ballots
            new_winners = lxn_method()[0]
            if loser in new_winners:
                return new_winners, excluded_ballots
    return [], {}


def winner_anomaly_search(file_name, method_indx):
    full_lxn = mwe(file_name)
    method_functions_full = [full_lxn.scot_stv, full_lxn.aq_stv, full_lxn.meek_stv, full_lxn.cham_cour, full_lxn.greedy_cham_cour, full_lxn.expanding_approvals, full_lxn.cpo_stv]
    lxn_method_full = method_functions_full[method_indx]
    full_results = lxn_method_full()
    winners = full_results[0]
    losers = full_results[1]

    lxn = mwe('')
    lxn.cand_num = full_lxn.cand_num
    lxn.seat_num = full_lxn.seat_num
    method_functions = [lxn.scot_stv, lxn.aq_stv, lxn.meek_stv, lxn.cham_cour, lxn.greedy_cham_cour, lxn.expanding_approvals, lxn.cpo_stv]
    lxn_method = method_functions[method_indx]

    win_lose_pairs = []
    for winner in reversed(winners):
        for loser in reversed(losers):
            win_lose_pairs.append([winner,loser])

    for pair in win_lose_pairs:
        winner = pair[0]
        loser = pair[1]
        
        # print(winner, loser)
        
        # determine which candidates help winner the most
        winner_keeper_balance = {cand:0 for cand in winners if cand!=winner}
        for ballot in full_lxn.ballots:
            count = full_lxn.ballots[ballot]
            for cand in winner_keeper_balance.keys():
                if cand in ballot:
                    cand_indx = ballot.index(cand)
                    if winner in ballot:
                        winner_indx = ballot.index(winner)
                    else:
                        winner_indx = len(ballot)
                    if loser in ballot:
                        loser_indx = ballot.index(loser)
                    else:
                        loser_indx = len(ballot)
                    if cand_indx < min([winner_indx, loser_indx]):
                        if winner_indx < loser_indx:
                            winner_keeper_balance[cand] += count
                        if loser_indx < winner_indx:
                            winner_keeper_balance[cand] -= count
        
        # print(winner_keeper_balance)
        
        winners_by_support = sorted(list(winner_keeper_balance.keys()), key = lambda cand: winner_keeper_balance[cand], reverse=True)
        # print(winners_by_support)
        
        for i in range(1,len(winners_by_support)+1):
            winners_to_remove = set(winners_by_support[:i])
            excluded_ballots = {}
            mod_ballots = {}
            for ballot in full_lxn.ballots:
                count = full_lxn.ballots[ballot]
                if set(ballot).union(winners_to_remove) != winners_to_remove:
                    mod_ballots[ballot] = count
                else:
                    excluded_ballots[ballot] = count
            lxn.ballots = mod_ballots
            new_winners = lxn_method()[0]
            if winner not in new_winners:
                return new_winners, excluded_ballots
            
    return [], {}
    



###################################
## Chose which elections to run
###################################
run_scottish = True
run_adapt_quota = True
run_meek = True
run_cham_cour = True
run_greedy_cham_cour = True
run_expand_app = True
run_cpo_stv = False
###################################
###################################

which_methods = [run_scottish, run_adapt_quota, run_meek, run_cham_cour, run_greedy_cham_cour, run_expand_app, run_cpo_stv]
losing_voters_headers = ['Scottish STV - Losing Voter Bloc Anomaly', 'AQ STV - Losing Voter Bloc Anomaly', 'Meek STV - Losing Voter Bloc Anomaly', 'Chamberlin-Courant - Losing Voter Bloc Anomaly', 'Greedy Chamberlin-Courant - Losing Voter Bloc Anomaly', 'Expanding Approvals - Losing Voter Bloc Anomaly', 'CPO STV - Losing Voter Bloc Anomaly']
removed_losing_ballot_headers = ['Scottish STV - Removed Loser Ballots', 'AQ STV - Removed Loser Ballots', 'Meek STV - Removed Loser Ballots', 'Chamberlin-Courant - Removed Loser Ballots', 'Greedy Chamberlin-Courant - Removed Loser Ballots', 'Expanding Approvals - Removed Loser Ballots', 'CPO STV - Removed Loser Ballots']
winning_voters_headers = ['Scottish STV - Winning Voter Bloc Anomaly', 'AQ STV - Winning Voter Bloc Anomaly', 'Meek STV - Winning Voter Bloc Anomaly', 'Chamberlin-Courant - Winning Voter Bloc Anomaly', 'Greedy Chamberlin-Courant - Winning Voter Bloc Anomaly', 'Expanding Approvals - Winning Voter Bloc Anomaly', 'CPO STV - Winning Voter Bloc Anomaly']
removed_winning_ballot_headers = ['Scottish STV - Removed Winner Ballots', 'AQ STV - Removed Winner Ballots', 'Meek STV - Removed Winner Ballots', 'Chamberlin-Courant - Removed Winner Ballots', 'Greedy Chamberlin-Courant - Removed Winner Ballots', 'Expanding Approvals - Removed Winner Ballots', 'CPO STV - Removed Winner Ballots']
csv_headers = ['Election']
for i in range(7):
    if which_methods[i]:
        csv_headers.append(losing_voters_headers[i])
        csv_headers.append(removed_losing_ballot_headers[i])
        csv_headers.append(winning_voters_headers[i])
        csv_headers.append(removed_winning_ballot_headers[i])
        
        
## create list of file names for all scottish elections
file_names = {}
for folder_name in os.listdir('../full_scot_data'):
    # if '5_cands' in folder_name:
    if 'cands' in folder_name:
        for name in os.listdir(f'../full_scot_data/{folder_name}'):
            file_name = '../full_scot_data/'+folder_name+'/'+name
            file_names[name] = file_name
            
anomaly_results = [{'Election': name} for name in file_names]

# file_names = {'argyll_bute_2022_ward4.csv':'../full_scot_data/11_cands/argyll_bute_2022_ward4.csv'}

print('### Searching for Losing Voter Bloc Anomalies ###')
loser_anomaly_count = [0 for i in range(7)]
for election_num, name in enumerate(file_names):

    sys.stdout.write('\r')
    sys.stdout.write(f'Election {election_num+1}/{len(file_names)}' + '    ' + name + '                                     ')
    sys.stdout.flush()
    
    election_dict = anomaly_results[election_num]
    # election_dict['Election'] = name
    for method_indx in range(7):
        if which_methods[method_indx]:
            # new_win_set, removed_ballots = loser_anomaly_search(file_names[name], method_indx)
            new_win_set, removed_ballots = loser_anomaly_search_whole_ballots(file_names[name], method_indx)
            if new_win_set:
                loser_anomaly_count[method_indx] += 1
                election_dict[losing_voters_headers[method_indx]] = new_win_set
                election_dict[removed_losing_ballot_headers[method_indx]] = removed_ballots
    # anomaly_results.append(election_dict)
sys.stdout.write('\r')
print(f'Loser Anomalies Found: {loser_anomaly_count}                                ')



print('### Searching for Winning Voter Bloc Anomalies ###')
winner_anomaly_count = [0 for i in range(7)]
for election_num, name in enumerate(file_names):

    sys.stdout.write('\r')
    sys.stdout.write(f'Election {election_num+1}/{len(file_names)}' + '    ' + name + '                                     ')
    sys.stdout.flush()
    
    election_dict = anomaly_results[election_num]
    # election_dict['Election'] = name
    for method_indx in range(7):
        if which_methods[method_indx]:
            new_win_set, removed_ballots = winner_anomaly_search(file_names[name], method_indx)
            if new_win_set:
                winner_anomaly_count[method_indx] += 1
                election_dict[winning_voters_headers[method_indx]] = new_win_set
                election_dict[removed_winning_ballot_headers[method_indx]] = removed_ballots
    # anomaly_results.append(election_dict)
sys.stdout.write('\r')
print(f'Winner Anomalies Found: {winner_anomaly_count}                                ')


## Write results to csv file
with open('anomaly_data_full_ballots.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
    writer.writeheader()
    for election in anomaly_results:
        writer.writerow(election)


zero_anomaly_count = 0
for anomaly in anomaly_results:
    if len(anomaly)==1:
        zero_anomaly_count += 1

print(f'{zero_anomaly_count} elections with no election anomalies')






################################
## test individual election
## for testing purposes
#################################
# file_name = file_names['argyll_bute_2022_ward4.csv']
# method_indx = 0


#########################
## loser voter blocs
#########################
# full_lxn = mwe(file_name)
# method_functions_full = [full_lxn.scot_stv, full_lxn.aq_stv, full_lxn.meek_stv, full_lxn.cham_cour, full_lxn.greedy_cham_cour, full_lxn.expanding_approvals, full_lxn.cpo_stv]
# lxn_method_full = method_functions_full[method_indx]
# full_results = lxn_method_full()
# winners = full_results[0]
# losers = full_results[1]

# loser_cooccur_scores = [0 for loser in losers]
# for ballot in full_lxn.ballots:
#     ballot_num = full_lxn.ballots[ballot]
#     if set(ballot).intersection(set(winners)):
#         for i, cand in enumerate(losers):
#             if cand in ballot:
#                 loser_cooccur_scores[i] += ballot_num

# lxn = mwe('')
# lxn.cand_num = full_lxn.cand_num
# lxn.seat_num = full_lxn.seat_num
# method_functions = [lxn.scot_stv, lxn.aq_stv, lxn.meek_stv, lxn.cham_cour, lxn.greedy_cham_cour, lxn.expanding_approvals, lxn.cpo_stv]
# lxn_method = method_functions[method_indx]

# remove_fracs = [i/100 for i in range(100,0,-1)]
# for loser in reversed(losers):
#     keep_set = set(winners + [loser])
#     for frac in remove_fracs:
#         excluded_ballots = {}
#         mod_ballots = {}
#         for ballot in full_lxn.ballots:
#             count = full_lxn.ballots[ballot]
#             if set(ballot).intersection(keep_set):
#                 mod_ballots[ballot] = count
#             else:
#                 excluded_ballots[ballot] = frac * count
#                 mod_ballots[ballot] = (1-frac) * count
#         lxn.ballots = mod_ballots
#         new_winners = lxn_method()[0]
#         if loser in new_winners:
#             print(loser)
#             print(new_winners)
#             print(frac)
#             print(excluded_ballots)
#             break


# ########################
# ## winner voter blocs
# ########################
# full_lxn = mwe(file_name)
# method_functions_full = [full_lxn.scot_stv, full_lxn.aq_stv, full_lxn.meek_stv, full_lxn.cham_cour, full_lxn.greedy_cham_cour, full_lxn.expanding_approvals, full_lxn.cpo_stv]
# lxn_method_full = method_functions_full[method_indx]
# full_results = lxn_method_full()
# winners = full_results[0]
# losers = full_results[1]

# lxn = mwe('')
# lxn.cand_num = full_lxn.cand_num
# lxn.seat_num = full_lxn.seat_num
# method_functions = [lxn.scot_stv, lxn.aq_stv, lxn.meek_stv, lxn.cham_cour, lxn.greedy_cham_cour, lxn.expanding_approvals, lxn.cpo_stv]
# lxn_method = method_functions[method_indx]

# win_lose_pairs = []
# for winner in reversed(winners):
#     for loser in reversed(losers):
#         win_lose_pairs.append([winner,loser])

# for pair in win_lose_pairs:
#     winner = pair[0]
#     loser = pair[1]
    
#     # print(winner, loser)
    
#     # determine which candidates help winner the most
#     winner_keeper_balance = {cand:0 for cand in winners if cand!=winner}
#     for ballot in full_lxn.ballots:
#         count = full_lxn.ballots[ballot]
#         for cand in winner_keeper_balance.keys():
#             if cand in ballot:
#                 cand_indx = ballot.index(cand)
#                 if winner in ballot:
#                     winner_indx = ballot.index(winner)
#                 else:
#                     winner_indx = len(ballot)
#                 if loser in ballot:
#                     loser_indx = ballot.index(loser)
#                 else:
#                     loser_indx = len(ballot)
#                 if cand_indx < min([winner_indx, loser_indx]):
#                     if winner_indx < loser_indx:
#                         winner_keeper_balance[cand] += count
#                     if loser_indx < winner_indx:
#                         winner_keeper_balance[cand] -= count
    
#     # print(winner_keeper_balance)
    
#     winners_by_support = sorted(list(winner_keeper_balance.keys()), key = lambda cand: winner_keeper_balance[cand], reverse=True)
#     # print(winners_by_support)
    
#     for i in range(1,len(winners_by_support)+1):
#         winners_to_remove = set(winners_by_support[:i])
#         excluded_ballots = {}
#         mod_ballots = {}
#         for ballot in full_lxn.ballots:
#             count = full_lxn.ballots[ballot]
#             if set(ballot).union(winners_to_remove) != winners_to_remove:
#                 mod_ballots[ballot] = count
#             else:
#                 excluded_ballots[ballot] = count
#         lxn.ballots = mod_ballots
#         new_winners = lxn_method()[0]
#         if set(new_winners)!=set(winners):
#             print(winner)
#             print(loser)
#             print(new_winners)
#             print(excluded_ballots)
#             break

















