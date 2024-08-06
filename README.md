Code and results for "New Fairness Criteria for Truncated Ballots in Multi-Winner Ranked-Choice Elections" by Adam Graham-Squire, Matthew I. Jones, and David McCune

All csv files contain examples of ILVB and IWVB violations for each of the Scottish elections. The csv file names indicate the values for \sigma_\ell and \sigma_w that were used. 

The python files anomaly_search and anomaly_search_party_dynamics can be run to find violations.

run_elections and run_all_elections simply run the various election methods on the Scottish election data, and create the election_results_new.csv file, which lists winner sets under various election methods.

Finally, elections_class.py contains all the code that computes the winner set for all the different ballot profiles and election methods.
