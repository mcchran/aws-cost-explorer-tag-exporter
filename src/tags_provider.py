from abc import ABC, abstractmethod
from retry import retry
from utils import dict_product as get_dict_product

import json
import requests

class AbstractTagsProvider(ABC):
    @abstractmethod
    def get_service_tags(self):
        pass
    

class HttpTagsProvider(AbstractTagsProvider):
    def __init__(self, tags_url):
        self.tags_url = tags_url
        self.service_tags = {}
    
    @retry(
        attempts=100,
        max_delay=4000,
    )
    def __fetch_service_tag_map_lists(self):
        return json.loads(requests.get(self.tags_url).text)
    
    def __refresh_service_tags(self):
        service_tag_map_lists = self.__fetch_service_tag_map_lists()
        self.service_tags = {}
        for service in service_tag_map_lists:
            self.service_tags[service] = get_dict_product(
                service_tag_map_lists[service]
            )

        # self.logger.info(f"Total number of filters: {sum(len(service_tags) for service_tags in self.service_tags)}")
    
    def get_service_tags(self):
        self.__refresh_service_tags()
        return self.service_tags