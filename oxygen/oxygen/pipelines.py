import json
import requests
from scrapy import log


class OxygenPipeline(object):

    def process_item(self, item, spider):
        if self.is_data_valid(item):
            data = dict(item)
            data["__type__"] = "Product"
            r = requests.put(
                "http://127.0.0.1:5000/rest/products/", data=json.dumps(data),
                headers={"content-type": "application/json"})
            log.msg("Result " + r.content, level=log.INFO)
        else:
            log.msg("Data invalid " + item["code"], level=log.WARNING)
        return item

    def is_data_valid(self, item):
        is_valid = True
        if not item["description"]:
            is_valid = False
        if not item["designer"]:
            is_valid = False
        if item["price"] == 0:
            is_valid = False
        if not item["image_urls"]:
            is_valid = False
        if not item["name"]:
            is_valid = False
        if not item["stock_status"]:
            is_valid = False
        return is_valid
