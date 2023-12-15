# petlebi_scrapy.py
import scrapy
from ..items import PetlebiItem

class PetlebiSpider(scrapy.Spider):
    name = "petlebi"
    allowed_domains = ["petlebi.com"]
    start_urls = ["https://www.petlebi.com"]

    custom_setting ={
        'FRREDS':{
            'petlebi_products.json':{'format': 'json', 'overwrite':True} ,
        }
    }
    custom_settings = {
        'CONCURRENT_REQUESTS': 6,
        #'DOWNLOAD_DELAY': 2,
    }
    output_data = []

    def parse(self, response):
        # Extract all links on the page
        links = response.css("div.wstheading.clearfix a")


        # Follow each valid link and continue the crawling
        for link in links:
            first_page_link = f"{link.attrib['href']}?page=1"
            yield response.follow(url=first_page_link, callback=self.parse_product_page)

    def parse_product_page(self, response):
        # Extract product data
        next_page_url = response.css("#pagination_area ul li:last-child a::attr(href)").extract_first()

        products = response.css("div.col-lg-4.col-md-4.col-sm-6.search-product-box")

        for product in products:
            product_link = product.css("a::attr(href)").extract_first()
            yield response.follow(url=product_link, callback=self.parse_products)

        # Follow the next page URL if available
        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse_product_page)

    def parse_products(self, response):
        petlebi_item = PetlebiItem()

        petlebi_item['product_url'] = response.url
        petlebi_item['product_name'] = response.css(".product-h1::text").get()
        petlebi_item['product_barcode'] = response.xpath("//*[@id='hakkinda']/div[2]/div[2]/text()").get()
        petlebi_item['product_image'] = response.css("div.row.product-detail-main .col-md-6.col-sm-5 a")[0].attrib["href"]
        petlebi_item['product_description'] = ''.join(response.css("div.tab-pane.active.show p::text").getall())
        petlebi_item['product_category'] = response.xpath("/html/body/div[3]/div[1]/div/div/div[1]/ol/li[3]/a/span/text()").get()
        petlebi_item['product_brand'] = response.css("div.row.mb-2.brand-line a::text").get()
        petlebi_item['product_new_price'] = response.css(".new-price::text").get()
        petlebi_item['product_old_price'] = response.css(".old-price::text").get()
        petlebi_item['product_stock'] = None
        petlebi_item['sku'] = None
        petlebi_item['product_ID'] = None

        yield petlebi_item
