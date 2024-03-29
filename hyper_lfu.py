import random

#Priority function = #accesses/lifetime in cache

class HyperLFUCache:
    def __init__(self, capacity, sample_size):
        self.capacity = capacity
        self.store_dict = {}
        self.key_costs = {}
        self.key_access_cnt = {}
        self.key_insert_time = {}
        self.sample_size = sample_size
        self.time = 0
        self.first_eviction = 1

    def put(self, key, value, cost):
        if len(self.store_dict.keys()) >= self.capacity:
            if self.first_eviction == 1:
                self.first_eviction = 0
                print("First eviction", self.time)
            evict_key = self.find_key_to_evict()
            del self.store_dict[evict_key]
            del self.key_costs[evict_key]
            del self.key_access_cnt[evict_key]
            del self.key_insert_time[evict_key]
        self.store_dict[key] = value
        self.key_costs[key] = cost+1
        self.key_access_cnt[key] = 1
        self.key_insert_time[key] = self.time
        self.time += 1 
	#Increment all lifetime counters by 1 for this timestep
        #for k in self.key_lifetime.keys():
        #    self.key_lifetime[k] += 1
        #self.print_cache()

    def get(self, key):
        value = None
        ret_val = 0
        if key in self.store_dict.keys():
            value = self.store_dict[key]
            self.key_access_cnt[key] += 1
            ret_val = 1
        else:
            ret_val = 0
            #print("Cache miss", key)
        #Increment all lifetime counters by 1 for this timestep
        #for k in self.key_lifetime.keys():
        #    self.key_lifetime[k] += 1
        #self.print_cache()
        self.time += 1
        return ret_val

    def find_key_to_evict(self):
        sample = random.sample(self.store_dict.keys(), min(len(self.store_dict.keys()), self.sample_size))
        priority_dict = {}
        for k in sample:
            priority_dict[k] = self.key_access_cnt[k]
        return min(priority_dict, key=priority_dict.get)
        

    def print_cache(self):
        #print(self.store_dict)
        priority_dict = {}
        for k in self.store_dict:
            priority_dict[k] = float(self.key_access_cnt[k])/(self.time - self.key_insert_time[k])
        print("Priority:", priority_dict) 
def hyper_test():
    cache = HyperbolicCache(5, 3)
    for i in range(100):
        cache.put(i, 0, 0)
        cache.put(1000, 0, 0)

    cache.print_cache()

#hyper_test()
