# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import pymysql.cursors

from twisted.enterprise import adbapi


class TomorrowHeadlinePipeline(object):
    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):
        db_pool = adbapi.ConnectionPool('pymysql', host=settings['MYSQL_HOST'], port=settings['MYSQL_PORT'],
                                        db=settings['MYSQL_DB'], user=settings['MYSQL_USER'],
                                        password=settings['MYSQL_PASSWD'], charset='utf8',
                                        cursorclass=pymysql.cursors.DictCursor, use_unicode=True)
        return cls(db_pool)

    def process_item(self, item, spider):
        self.db_pool.runInteraction(self.do_insert, item)

    @staticmethod
    def parse_insert_sql(item):
        sql_template = 'insert into article(title, author, url, src, summary, content) values (%s, %s, %s, %s, %s, %s)'
        params = (item['title'], item['author'], item['url'],
                  item['src'], item['summary'], item['content'])

        return sql_template, params

    def do_insert(self, cursor, item):
        insert_sql, params = TomorrowHeadlinePipeline.parse_insert_sql(item)
        cursor.execute(insert_sql, params)
