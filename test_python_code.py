class DataProcessor:
    def __init__(self, config):
        self.config = config
        self.data_cache = {}
    
    def process_data(self, input_data):
        """Process incoming data with transformations"""
        if not input_data:
            return None
        
        # Apply transformations
        transformed = self.transform(input_data)
        
        # Cache results
        self.data_cache[hash(str(input_data))] = transformed
        
        return transformed
    
    def transform(self, data):
        """Transform data based on configuration"""
        if self.config.get('normalize'):
            data = self.normalize(data)
        
        if self.config.get('filter'):
            data = self.filter_data(data)
        
        return data
    
    def normalize(self, data):
        """Normalize data values"""
        # Simple normalization logic
        return [x / max(data) if max(data) > 0 else 0 for x in data]
    
    def filter_data(self, data):
        """Filter out invalid data points"""
        return [x for x in data if x is not None and x > 0]
    
    def get_statistics(self):
        """Get processing statistics"""
        return {
            'processed_items': len(self.data_cache),
            'cache_size': len(self.data_cache)
        }