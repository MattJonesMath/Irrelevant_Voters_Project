from elections_class import mw_elections as mwe
import time

election = mwe('edinburgh_2022_ward5.csv')

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

start_time = time.time()
print('###################')
print('Meek STV Results')
print(election.meek_stv())
print(f'Time: {time.time()-start_time}')

start_time = time.time()
print('###################')
print('Chamberlin-Courant Results')
print(election.cham_cour('OM'))
print(f'Time: {time.time()-start_time}')

start_time = time.time()
print('###################')
print('Greedy Chamberlin-Courant Results')
print(election.greedy_cham_cour('OM'))
print(f'Time: {time.time()-start_time}')

start_time = time.time()
print('###################')
print('CPO-STV Results')
print(election.cpo_stv())
print(f'Time: {time.time()-start_time}')


