from itemadapter import ItemAdapter
import mysql.connector


class PetlebiPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Strip leading and trailing spaces from all string fields
        for field_name, value in adapter.items():
            if isinstance(value, str):
                adapter[field_name] = value.strip()

        # Category & Product Type --> switch to lowercase
        lowercase_keys = ['product_category']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        # Remove '//' from the beginning of product_image
        adapter['product_image'] = adapter['product_image'].lstrip('/')

        # Remove space, 'TL', and convert to float for price fields
        price_keys = ['product_old_price', 'product_new_price']
        for price_key in price_keys:
            value = adapter.get(price_key)
            # Remove space and 'TL'
            value = value.replace(' ', '').replace('TL', '').replace(',', '')
            adapter[price_key] = float(value)

        return item


class SaveToMySQLPipline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='MyPassword77@',
            database='petlebi_create'
        )

        # create cursor, used to execute command
        self.cur = self.conn.cursor()

        # create petlebi_create table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS petlebi_create (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_url VARCHAR(255),
                product_name VARCHAR(255),
                product_barcode VARCHAR(255),
                product_image VARCHAR(255),
                product_description TEXT,
                product_category VARCHAR(255),
                product_brand VARCHAR(255),
                product_new_price DECIMAL(10, 2),
                product_old_price DECIMAL(10, 2),
                product_stock VARCHAR(255),
                sku VARCHAR(255),
                product_id VARCHAR(255)
            )
        """)

    def process_item(self, item, spider):
        # Insert petlebi table
        self.cur.execute("""
            INSERT INTO petlebi_create (
                product_url,
                product_name,
                product_barcode,
                product_image,
                product_description,
                product_category,
                product_brand,
                product_new_price,
                product_old_price,
                product_stock,
                sku,
                product_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item['product_url'],
            item['product_name'],
            item['product_barcode'],
            item['product_image'],
            item['product_description'],
            item['product_category'],
            item['product_brand'],
            item['product_new_price'],
            item['product_old_price'],
            item.get('product_stock') or None,
            item.get('sku') or None,
            item.get('product_id') or None
        ))

        # insert data to database
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # Close the cursor and connection when the spider is closed
        self.cur.close()
        self.conn.close()
