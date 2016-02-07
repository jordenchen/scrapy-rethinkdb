from scrapy.item import Item
from scrapy.exceptions import NotConfigured

from scrapy_rethinkdb.driver import RethinkDBDriver


class RethinkDBPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        """Gets settings for the pipeline from the crawler.
        @param crawler: crawler
        """
        settings = crawler.settings

        # get relevant settings for the pipeline
        connection_settings = settings.get('RETHINKDB_CONNECTION', {})
        table_mapping = settings.get('RETHINKDB_TABLE_MAPPING', None)
        insert_options = settings.get('RETHINKDB_INSERT_OPTIONS', {})

        # creates driver instance
        driver = RethinkDBDriver(connection_settings)

        return cls(driver, table_mapping, insert_options)

    def __init__(self, driver, table_mapping, insert_options):
        """Rethinkdb pipeline for Scrapy processed items.

        @param driver: rethinkdb driver
        @param table_mapping: table mapping, item -> table name
        @param insert_options: options to be used when inserting documents

        @raises NotConfigured: if any of the constructor arguments wasn't
        supplied.
        """

        # check if driver not provided
        if not driver:
            raise NotConfigured("Driver not provided.")
        else:
            self.driver = driver

        # check if table mapping provided
        if not table_mapping:
            raise NotConfigured("The variable RETHINKDB_TABLE_MAPPING is not defined in settings.py")
        elif not isinstance(table_mapping, dict):
            raise NotConfigured("The variable RETHINKDB_TABLE_MAPPING shall be specified as dictionary: item -> table")
        
        # get table references from driver
        self.table_mapping = dict()
        for item in table_mapping:
                self.table_mapping[item] = self.driver.get_table(table_mapping[item]) 

        # check if insert options not provided
        if insert_options is None:
            raise NotConfigured("Insert options not provided.")
        else:
            self.insert_options = insert_options

    def process_item(self, item, spider):
        """Processes item.

        @param item: the item scraped
        @param spider: the spider which scraped the item
        @returns Item to be processed by the next pipelines (if any).
        """
        if not isinstance(item, Item):
            spider.log.msg('Item not valid for RethinkDBPipeline <%s>. '
                           'Ignoring item.' % item,
                           level=spider.log.WARNING)
            return item

        self.before_insert(item)
        document = self.get_document(item)

        insert_stmt = self.table_mapping[item.__class__.__name__].insert(document, **self.insert_options)
        insert_result = self.driver.execute(insert_stmt)
        self.after_insert(item, insert_result)

        return item

    def get_document(self, item):
        """Gets document from the item. By default returns the attribute
        _values from the item.

        @param item: the item scraped
        @returns Document that represents the item.
        """
        return item # ._values

    def before_insert(self, item):
        """
        Extension point to change the item/ drop it before inserting it in
        the database.

        @param item: the item scraped
        """
        pass

    def after_insert(self, item, insert_result):
        """
        Extension point to change the item/ drop it with the result from
        inserting it in the database.

        @param item: the item scraped
        @param insert_result: result from insert
        """
        pass
