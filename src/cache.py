#Problem Statement
#Implement and compare three cache eviction policies on the same request sequence:
#FIFO (First-In, First-Out)
#LRU (Least Recently Used)
#OPTFF (Belady’s Farthest-in-Future, optimal offline)
#You will also complete a short written component, including a proof that OPTFF is optimal.
#You are given:
#A cache of capacity ( k )
#A sequence of ( m ) requests ( r_1, r_2,.., r_m )
#For each request:
#If the item is already in the cache, this is a hit.
#Otherwise, this is a miss. Insert the item:
#If the cache is not full, simply insert it.
#If the cache is full, evict one item according to the policy.
#Eviction Policies
#FIFO: Evict the item that has been in the cache the longest.
#LRU: Evict the item whose most recent access time is the oldest.
#OPTFF: Among items currently in the cache, evict the one whose next request occurs farthest in the future (or never occurs again).

import sys
#python3 cache.py input.in
if len(sys.argv) != 2:
    print("Usage: python3 cache.py <input_file>")
    sys.exit(1)
#Input Format
#Your program must read input from a file with the following format:
#k m
#r1 r2 r3 ... rm
#Where:
#( k ) = cache capacity ( ( k >= 1 ) )
# ( m ) = number of requests
# ( r_1, .., r_m ) = sequence of integer IDs
with open(sys.argv[1], 'r') as f:
    parts = f.read().split()
k = int(parts[0])
m = int(parts[1])
requests = list(map(int, parts[2:]))
if len(requests) != m:
    print("Error: Number of requests does not match m")
    sys.exit(1)
#FIFO: Evict the item that has been in the cache the longest.
fifo_cache = []
fifo_order = []
fifo_misses = 0
#cache full, remove the page sitting in the cache the longest
for page in requests:
    if page in fifo_cache:
        continue
    fifo_misses += 1
    #still space -> add the page
    if len(fifo_cache) < k:
        fifo_cache.append(page)
        fifo_order.append(page)
    else:
        #cache full, remove the page sitting in the cache the longest
        oldest_page = fifo_order.pop(0)
        fifo_cache.remove(oldest_page)
        fifo_cache.append(page)
        fifo_order.append(page)
#LRU: Evict the item whose most recent access time is the oldest.
lru_cache = []
last_used = {}
lru_misses = 0
for i in range(len(requests)):
    page = requests[i]
    #page alr in cache -> update last used time
    if page in lru_cache:
        last_used[page] = i
        continue
    lru_misses += 1
    if len(lru_cache) < k:
        lru_cache.append(page)
        last_used[page] = i
    else:
        #page whose last use is smallest
        #evict the least recently used page
        page_to_remove = lru_cache[0]
        for p in lru_cache:
            if last_used[p] < last_used[page_to_remove]:
                page_to_remove = p
        lru_cache.remove(page_to_remove)
        del last_used[page_to_remove]
        lru_cache.append(page)
        last_used[page] = i
#OPTFF: Among items currently in the cache, evict the one whose next request occurs farthest in the future (or never occurs again).
optff_cache = []
optff_misses = 0
for i in range(len(requests)):
    page = requests[i]
    if page in optff_cache:
        continue #hit
    optff_misses += 1
    if len(optff_cache) < k:
        optff_cache.append(page)
    else:
        page_to_remove = None
        farthest_next_use = -1
        #check each page current in cache
        for old_page in optff_cache:
            next_use = -1
            for j in range(i + 1, len(requests)):
                #look ahead in the request seq
                if requests[j] == old_page:
                    next_use = j
                    break
            if next_use == -1: 
                #never appear again -> remove this page
                page_to_remove = old_page
                break
            if next_use > farthest_next_use:
                #otherwise keep track of the page with the farthest next use
                farthest_next_use = next_use
                page_to_remove = old_page
        optff_cache.remove(page_to_remove)
        optff_cache.append(page)
# Output Format
# Your program must output:
#FIFO  : <number_of_misses>
#LRU   : <number_of_misses>
#OPTFF : <number_of_misses>
print(f"FIFO  : {fifo_misses}")
print(f"LRU   : {lru_misses}")
print(f"OPTFF : {optff_misses}")
