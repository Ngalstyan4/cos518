from lru_cache import BackendCache
from hyperbolic import HyperbolicCache
from ycsb_zipf import YCSB_Zipfian
import numpy as np

def test_cache(cache_size, max_items, zipf_param, item_count, method):
    Z = YCSB_Zipfian(max_items, zipf_param)
    if method == "LRU":
        cache = BackendCache(cache_size, "LRU")
    elif method == "Hyper":
        cache = HyperbolicCache(cache_size, 64)

    cnt_hits = 0
    cnt_miss = 0
    for i in range(0, item_count):
        next_key = 1 + Z.get_next(np.random.random())[0]
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
    policy="LRU"
    test_cache(100,   10000, zipf_param, 10000, policy)
    test_cache(1000,  10000, zipf_param, 10000, policy)
    test_cache(10000, 10000, zipf_param, 10000, policy)
    #test_cache(10000, 100000, zipf_param, 100000, policy)
    policy="Hyper"
    test_cache(100,   10000, zipf_param, 10000, policy)
    test_cache(1000,  10000, zipf_param, 10000, policy)
    test_cache(10000, 10000, zipf_param, 10000, policy)

test_policy1(1.01)
test_policy1(1.1)
test_policy1(1.5)
test_policy1(1.9)
