from lru_cache import LRUCache
from hyperbolic import HyperbolicCache
from hyper_lfu import HyperLFUCache
from ycsb_zipf import *
import numpy as np
from matplotlib import pyplot as plt 
import random
from lfu import LFUCache

def get_zipf_keys(key_space, param, count, mapping):
    Z = Accu_Zipfian(key_space, param)
    keys = []
    for i in range(0, count):
        next_key = 1 + Z.get_next(np.random.random())[0]
        if next_key in mapping:
            keys.append(mapping[next_key])
        else:
            keys.append(next_key)
    return keys 

def draw_dyndistrb(max_items, count):
    rounds = int(count/100)
    top_k_lim = int(0.1*max_items)
    top_k_items = [i for i in range(1, top_k_lim)]
    key_space = max_items
    iter_count = int(count/rounds)
    zipf_param = 1.001
    workload = get_zipf_keys(key_space, zipf_param, iter_count, {})
    current_pop = 1 
    for i in range(1, rounds):
        next_pop = np.random.choice(top_k_items)
        while next_pop == current_pop:
            next_pop = np.random.choice(top_k_items)
        print("next_pop:", next_pop)
        next_batch = get_zipf_keys(key_space, zipf_param, iter_count, {}) #{current_pop:next_pop, next_pop:current_pop})
        workload.extend(next_batch)
        print(len(workload))
    return workload

    #count, bins, ignored = plt.hist(workload, bins=1000)
    #plt.yscale('log')
    #plt.xscale('log')
    #plt.show()


def draw_distrb(max_items, zipf_param, count):
    Z = Accu_Zipfian(max_items, zipf_param)
    keys = []
    for i in range(0, count):
        next_key = 1 + Z.get_next(np.random.random())[0]
        keys.append(next_key)
    hist=np.histogram(keys)
    plt.hist(keys, bins=max_items) 
    plt.yscale('log')
    plt.xscale('log')
    plt.show()
    print(hist)

#draw_distrb(10000, 1.001,  100000)
#draw_distrb(10000, 1.0001, 100000)
#draw_distrb(10000, 1.00001, 100000)

def test_dynworkload(workload, cache_size, max_items, zipf_param, item_count, method):
    if method == "LRU":
        cache = LRUCache(cache_size)
    elif method == "Hyper":
        cache = HyperbolicCache(cache_size, 64)
    elif method == "HyperLFU":
        cache = HyperLFUCache(cache_size, 100)
    elif method == "LFU":
        cache = LFUCache(cache_size)

    cnt_hits = 0
    cnt_miss = 0
    for i in range(0, item_count):
        next_key = workload[i]
        ret_val = cache.get(next_key)
        if ret_val == 1:
            cnt_hits += 1
        else:
            cnt_miss += 1
            cache.put(next_key, 0, 0)
    print(method, "Miss rate:", 100.0*cnt_miss/(cnt_hits+cnt_miss))


max_items =  100000
item_count= 1000000
workload = draw_dyndistrb(max_items, item_count)

sizes = [100, 1000, 10000, 100000]

for cache_size in sizes:
    print(cache_size)
    test_dynworkload(workload, cache_size, 100000, 1.001, item_count, "LFU")
    test_dynworkload(workload, cache_size, 100000, 1.001, item_count, "LRU")
    test_dynworkload(workload, cache_size, 100000, 1.001, item_count, "Hyper")
    test_dynworkload(workload, cache_size, 100000, 1.001, item_count, "HyperLFU")


def test_cache(cache_size, max_items, zipf_param, item_count, method):
    all_items = [i for i in range(int(max_items/10))]
    Z = Accu_Zipfian(max_items, zipf_param)
    if method == "LRU":
        cache = LRUCache(cache_size)
    elif method == "Hyper":
        cache = HyperbolicCache(cache_size, 64)
    elif method == "LFU":
        cache = LFUCache(cache_size)

    cnt_hits = 0
    cnt_miss = 0
    for i in range(0, item_count):
        if i % 100 == 0:
            next_key = random.choice(all_items)
        else:
            next_key = 1 + Z.get_next(np.random.random())[0]
            #if next_key in all_items:
            #    all_items.remove(next_key)
        ret_val = cache.get(next_key)
        if ret_val == 1:
            #found in cache
            cnt_hits += 1
        else:
            #cache-miss
            cnt_miss += 1
            cache.put(next_key, 0, 0)
    print(method, "Miss rate:", 100.0*cnt_miss/(cnt_hits+cnt_miss))

def test_policy1(zipf_param):
    print("Zipf_param:", zipf_param)
    policy="LFU"
    #test_cache(100,   100000, zipf_param, 20000, policy)
    test_cache(1000,  100000, zipf_param, 50000, policy)
    test_cache(10000, 100000, zipf_param, 50000, policy)
    #test_cache(10000, 100000, zipf_param, 100000, policy)
    policy="Hyper"
    #test_cache(100,   100000, zipf_param, 20000, policy)
    test_cache(1000,  100000, zipf_param, 50000, policy)
    test_cache(10000, 100000, zipf_param, 50000, policy)

#test_policy1(1.001)
#test_policy1(1.1)
#test_policy1(1.5)
#test_policy1(1.9)
