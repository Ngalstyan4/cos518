from ycsb_zipf import *
import numpy as np
import subprocess as sp
from datetime import datetime
import random

def get_time_delta(time1, time2):
    tdelta = time2 - time1
    return (tdelta.seconds * 10**6) + tdelta.microseconds

def get_request(key, max_items, max_servers):
    cache_key_address = "10.0.0.1:3000/" + str(key)
    cache_get_command = ['curl', '-s', cache_key_address]

    p = sp.run(cache_get_command, stdout=sp.PIPE)
    end_time = datetime.now()
    ret_val = int(p.stdout)
    if ret_val == 1:
        return 1
    else:
        server_id = 2 + (key % max_servers) #int(max_servers*key/max_items)
        assert server_id <= 7
        server_key_address = "10.0.0." + str(server_id) + ':3000/' + str(key)      
        server_get_command = ['curl', '-s', server_key_address]
        p1 = sp.run(server_get_command, stdout=sp.PIPE)
        return 0

def put_request(key, cost):
    cache_key_address = "10.0.0.1:3000/" + str(key)
    cache_put_command = ['curl',  '-s', '-X', 'PUT', '-d' , "\"cost=" + str(cost) + "&value=0\"", cache_key_address]
    p2 = sp.run(cache_put_command, stdout=sp.PIPE)

def test_mininet(max_items, item_count, zipf_param, max_servers):
    Z = Accu_Zipfian(max_items, zipf_param)
    miss_count = 0
    total_get_time = 0
    total_miss_penalty = 0
    total_hit_time = 0
    hit_count = 0 
    all_items = [i for i in range(int(max_items/10))]

    for i in range(item_count + 1):
        if i % 100 == 0 and len(all_items):
            next_key = random.choice(all_items)
        else:
            next_key = 1 + Z.get_next(np.random.random())[0]
            if next_key in all_items:
                all_items.remove(next_key)
        start_time = datetime.now()
        cache_ret = get_request(next_key, max_items, max_servers)
        end_time = datetime.now()
        get_time = get_time_delta(start_time, end_time)/10**6

        #server_id = 2 + int(max_servers*next_key/max_items)
        if cache_ret == 0:
            miss_count += 1
            total_miss_penalty += get_time
            #print(server_id, "cache miss time:", get_time)
            put_request(next_key, get_time)
        else:
            hit_count += 1
            total_hit_time += get_time

        total_get_time += get_time
        if i != 0 and i % 500 == 0:
            miss_rate = float(miss_count/i)
            avg_miss_penalty = float(total_miss_penalty/miss_count)
            avg_get_time = float(total_get_time/i)
            avg_hit_time = float(total_hit_time/hit_count)
            print("Key space:", max_items, "Trials:", i, "zipf_param:", zipf_param, "max_servers:", max_servers, "Miss rate:", miss_rate, "Avg. miss penalty", avg_miss_penalty, "Avg. hit time", avg_hit_time, "Avg. get time", avg_get_time)
         
                
test_mininet(100000, 10000, 1.001, 4)

