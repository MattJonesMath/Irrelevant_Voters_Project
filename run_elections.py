from elections_class import mw_elections as mwe
import time

election = mwe('argyll_bute_2022_ward4.csv                                                   ')

start_time = time.time()
print('###################')
print('Scottish STV Results')
print(election.scot_stv())
print(f'Time: {time.time()-start_time}')

start_time = time.time()
print('###################')
print('Adaptive Quota STV Results')
print(election.aq_stv())
print(f'Time: {time.time()-start_time}')

# start_time = time.time()
# print('###################')
# print('Meek STV Results')
# print(election.meek_stv())
# print(f'Time: {time.time()-start_time}')

# start_time = time.time()
# print('###################')
# print('Chamberlin-Courant Results')
# print(election.cham_cour())
# print(f'Time: {time.time()-start_time}')

# start_time = time.time()
# print('###################')
# print('Greedy Chamberlin-Courant Results')
# print(election.greedy_cham_cour())
# print(f'Time: {time.time()-start_time}')

# start_time = time.time()
# print('###################')
# print('Expanding Approvals Results')
# print(election.expanding_approvals())
# print(f'Time: {time.time()-start_time}')

# start_time = time.time()
# print('###################')
# print('CPO-STV Results')
# print(election.cpo_stv())
# print(f'Time: {time.time()-start_time}')


