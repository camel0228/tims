class MemCache:
    
    def __init__(self):
        self.cache = {} 
        self.max_cache_size = 10000
        self.cache['CURRENCY'] = {}
    
    def __contains__(self, key): 
        return key in self.cache
    
    def updateCurrency(self, key, value): 
        self.cache['CURRENCY'][key] = value
    
    @property
    def size(self): 
        return len(self.cache)