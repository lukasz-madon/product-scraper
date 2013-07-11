from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from oxygen.items import OxygenProduct
from scrapy import log
import time


class OxygenSpider(CrawlSpider):
    name = "oxygen_spider"
    allowed_domains = ["oxygenboutique.com"]
    start_urls = ["http://www.oxygenboutique.com"]
    accessories = set(["hats", "sunglasses"])
    jewlery = set(["bracelet", "earrings", "necklace", "ring"])
    rules = (
        Rule(SgmlLinkExtractor(allow=(".*aspx$",), deny=(".*GetImage.*")),
             callback="parse_elem", follow=True),
    )

    def parse_elem(self, response):
        hxs = HtmlXPathSelector(response)
        item = OxygenProduct()
        item["code"] = response.url[30:-5]
            #id is URL without the extension and domain

        description = hxs.select(
            '//*[@id="accordion"]/div[1]/text()').extract()
        item["description"] = description[
            0].strip().replace("\r\n", "") if description else ""

        designer = hxs.select(
            '//*[@id="ctl00_ContentPlaceHolder1_AnchorDesigner"]/text()').extract()
        item["designer"] = designer[0].strip() if designer else ""

        price = 0
        sale_discount = 0
        price_before_num = 0
        price1 = self.get_price(
            hxs.select('//*[@id="container"]/div[2]/span/text()').extract())
        if price1 is not None:
            price = price1
        price2 = self.get_price(
            hxs.select('//*[@id="container"]/div[3]/span/text()').extract())
        if price2 is not None:
            price = price2
        price_before1 = hxs.select(
            '//*[@id="container"]/div[3]/span/span[1]/span/text()').extract()
        discounted_price1 = hxs.select(
            '//*[@id="container"]/div[3]/span/span[2]/text()').extract()
        price_dis1 = self.get_price_and_disc(price_before1, discounted_price1)
        if price_dis1 is not None:
            price, sale_discount = price_dis1
        price_before2 = hxs.select(
            '//*[@id="container"]/div[2]/span/span[1]/span/text()').extract()
        discounted_price2 = hxs.select(
            '//*[@id="container"]/div[2]/span/span[2]/text()').extract()
        price_dis2 = self.get_price_and_disc(price_before2, discounted_price2)
        if price_dis2 is not None:
            price, sale_discount = price_dis2
        item["price"] = price
        item["sale_discount"] = sale_discount

        item["gender"] = "F"  # Assuming is only for girls
        image_urls = []
        hrefs = hxs.select('//*[@id="thumbnails-container"]//td/a/@href')
        for href in hrefs:
            img_url = href.extract()
            image_urls.append(OxygenSpider.start_urls[0] + img_url)
        item["image_urls"] = image_urls

        name = hxs.select('//*[@id="breadcrumbs_2"]/text()').extract()
        item["name"] = "".join(name).strip()
        item["raw_color"] = ""  # no color
        item["source_url"] = response.url

        stock_status = {}
        options = hxs.select(
            '//*[@id="ctl00_ContentPlaceHolder1_ddlSize"]/*/text()').extract()
        for option in options[1:]:
            size = option.split()[0]
            if "Sold Out" in option:
                stock_status[size] = 1
            else:
                stock_status[size] = 3

        item["stock_status"] = stock_status
        item["last_updated"] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime())

        item_type = "A"
        item_name = item["name"].lower().split()
        for curr_item in item_name:
            if "shoes" == curr_item:
                item_type = "S"
            elif "bags" == curr_item:
                item_type = "B"
            elif curr_item in self.jewlery:
                item_type = "J"
            elif curr_item in self.accessories:
                item_type = "R"

        item["type"] = item_type
        return item

    def price_to_number(self, price):
        price_str = "".join(price)
        return float(price_str) / 100.0

    def get_price(self, elem):
        if len(elem) > 0:
            price_lst = filter(
                lambda x: x.isdigit(), elem[0].replace(u'\xa3', ''))
            if len(price_lst) > 0:
                return self.price_to_number(price_lst)
            else:
                return None

    def get_price_and_disc(self, price, disc):
        if len(price) > 0:
            price_before_number = filter(
                lambda x: x.isdigit(), price[0].replace(u'\xa3', ''))
            discounted_price_number = filter(
                lambda x: x.isdigit(), disc[0].replace(u'\xa3', ''))
            if len(price_before_number) > 0:
                price_before_num = self.price_to_number(price_before_number)
                price = self.price_to_number(discounted_price_number)
                sale_discount = price / price_before_num
                return (price, sale_discount)
        return None
