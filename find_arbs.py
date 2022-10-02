import numpy as np
import time
import fuzzywuzzy
import unibet_scrape, paf_scrape, betsson_scrape

from multiprocessing.pool import ThreadPool as Pool

def test_f(l, i):
    l.append(i)

sites = ['https://www.unibet.com/betting/sports/filter/football/all/matches',
         'https://www.paf.com/en/betting#/filter/football/all/all/all/matches',
         'https://www.betsson.com/en/sportsbook/football']
names = ['Unibet', 'Paf', 'Betsson']
foos = [unibet_scrape.football_matches, paf_scrape.football_matches, betsson_scrape.football_matches]

# Category, 
matches = [[], [], [], [], [], []]
all_site_matches = []
# Create matches list for all sites
for i in range(0, len(sites)):
    all_site_matches.append(matches)

pool_size = len(sites)
pool = Pool(pool_size)

for site, foo, site_matches in zip(sites, foos, all_site_matches):
    pool.apply_async(foo, args=(site, site_matches))

pool.close()
pool.join()

for site_matches in all_site_matches:
    print(np.array(site_matches).shape)
