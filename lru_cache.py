
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.lru_queue = []
        self.store_dict = {}
        self.policy = "LRU"
        self.key_costs = {}
        self.walk_length = 10
    
    def put(self, key, value, cost):
        if len(self.store_dict.keys()) >= self.capacity:
            evict_key = self.find_key_to_evict()
            self.lru_queue.remove(evict_key)
            del self.store_dict[evict_key]
            #print("Evicted", evict_key)
        self.store_dict[key] = value
        self.lru_queue.append(key)
        self.key_costs[key] = cost

    def get(self, key):
        if key in self.store_dict.keys():
            value = self.store_dict[key]
            self.lru_queue.remove(key)
            self.lru_queue.append(key)
            return 1
        else:
            return 0

    def find_key_to_evict(self):
        if self.policy == "LRU":
            #return head of the queue
            return self.lru_queue[0]
        elif self.policy == "NetLRU":
            i = 0
            min_cost = self.key_costs[self.lru_queue[0]]
            min_idx = self.lru_queue[0]
            #print("Queue:", self.lru_queue)
            for item in self.lru_queue:
                if min_cost > self.key_costs[item]:
                    min_cost = self.key_costs[item]
                    min_idx = item
                i += 1
                if i == self.walk_length:
                    break
            #print("returning", min_idx)
            return min_idx

    def print_cache(self):
        print(self.store_dict)
        print(self.lru_queue)

def lru_test():
    cache = BackendCache(3, "LRU")
    cache.put(1, 0, 0)
    cache.put(2, 0, 0)
    cache.put(3, 0, 0)
    cache.get(2)
    cache.put(4, 0, 0)
    cache.get(1)
    cache.put(5, 0, 0)
    cache.put(6, 0, 0)
    cache.get(5)
    cache.print_cache()

def netlru_test():
    print("")
    cache = BackendCache(3, "NetLRU")
    cache.put(1, 0, 100)
    cache.put(2, 0, 0)
    cache.put(3, 0, 0)
    cache.get(2)
    cache.put(4, 0, 0)
    cache.get(1)
    cache.put(5, 0, 0)
    cache.put(6, 0, 0)
    cache.get(5)
    cache.print_cache()

#lru_test()
#netlru_test()
