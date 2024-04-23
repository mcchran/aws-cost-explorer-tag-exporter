import os

class ConfigurationError(Exception):
    pass


class Config:
    
    COST_PROVISIONING = 1
    TAG_PROVISIONING = 2
    
    AVAILABLE_MODES = {
        "cost_provisioning": COST_PROVISIONING, 
        "tag_provisioning": TAG_PROVISIONING
    }
    
    def __init__(self):
        
        try:
            self.mode = self.AVAILABLE_MODES[
                os.environ.get("MODE", None).lower()
            ]
        except KeyError:
            raise ConfigurationError(f"Invalid mode please try adding one of the following: {self.AVAILABLE_MODES.keys()}")
        
        
        if self.mode == self.COST_PROVISIONING:                
            self.persistent_file_path = os.environ.get(
                "PERSISTENT_FILE", "metrics_store.json")
            try:
                assert os.path.exists(self.persistent_file_path)
            except AssertionError:
                raise ConfigurationError(f"File {self.persistent_file_path} does not exist.")
            

            self.tags_host = os.environ.get("TAGS_DISCOVERY_URL", "http://localhost:3000")
    
        if self.mode == self.TAG_PROVISIONING:
            self.tags_list = os.environ.get("TAGS_LIST", "team,service").split(",")
            
        self.schedule_minute = os.environ.get("SCHEDULE_MINUTE", 10)
        self.schedule_hour = os.environ.get("SCHEDULE_HOUR", 23)
    
        
    def is_cost_provisioning(self):
        return self.mode == self.COST_PROVISIONING
    
    def is_tag_provisioning(self):
        return self.mode == self.TAG_PROVISIONING
    