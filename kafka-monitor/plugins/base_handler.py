class BaseHandler:
    '''
        Base handler for handling incoming request in kafka
    '''
    schema = "None"
    def setup(self):
        '''
            Setup handler
        '''
        if self.schema == "None":
            raise NotImplementedError("Please specify a schema for the kafka monitor")
    
    def handle(self):
        '''
            Handle a valid incoming request
        '''
        raise NotImplementedError("Please implement a handle method for your handler")