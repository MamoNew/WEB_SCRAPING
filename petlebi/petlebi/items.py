import scrapy

class PetlebiscraperclearItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class PetlebiItem(scrapy.Item):  # Change 'scrapy.item' to 'scrapy.Item'
    product_url = scrapy.Field()
    product_name = scrapy.Field()
    product_barcode = scrapy.Field()
    product_image = scrapy.Field()
    product_description = scrapy.Field()
    product_category = scrapy.Field()
    product_brand = scrapy.Field()
    product_new_price = scrapy.Field()
    product_old_price = scrapy.Field()
    product_stock = scrapy.Field()
    sku = scrapy.Field()
    product_ID = scrapy.Field()
