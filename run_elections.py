from elections_class import mw_elections as mwe
import time

election = mwe("C:/Users/mijones/Documents/Datasets/full_scot_data/7_cands/clackmannanshire_2022_ward4.csv")

start_time = time.time()
print('###################')
print('Scottish STV Results')
print(election.scot_stv())
print(f'Time: {time.time()-start_time}')

# start_time = time.time()
# print('###################')
# print('Adaptive Quota STV Results')
# print(election.aq_stv())
# print(f'Time: {time.time()-start_time}')

start_time = time.time()
print('###################')
print('Meek STV Results')
print(election.meek_stv())
print(f'Time: {time.time()-start_time}')

start_time = time.time()
print('###################')
print('Chamberlin-Courant Results')
election.model = 'OM'
print(election.cham_cour())

election.model = 'PM'
print(election.cham_cour())
print(f'Time: {time.time()-start_time}')

# start_time = time.time()
# print('###################')
# print('Greedy Chamberlin-Courant Results')
# print(election.greedy_cham_cour())
# print(f'Time: {time.time()-start_time}')

start_time = time.time()
print('###################')
print('Expanding Approvals Results')
print(election.expanding_approvals())
print(f'Time: {time.time()-start_time}')

# start_time = time.time()
# print('###################')
# print('CPO-STV Results')
# print(election.cpo_stv())
# print(f'Time: {time.time()-start_time}')

start_time = time.time()
print('###################')
print('Expanding Approvals OM Results')
print(election.expanding_approvals_om())
print(f'Time: {time.time()-start_time}')





# #############
# ## run specific election with removed ballots
# #############

# election = mwe("C:/Users/mijones/Documents/Datasets/full_scot_data/9_cands/fife_2017_ward12.csv")
# method = election.expanding_approvals_om
# # election.model = 'OM'

# print(method())

# removed_ballots = {(6,): 58}


# for ballot in removed_ballots:
#     election.ballots[ballot] -= removed_ballots[ballot]

# print(method())



























