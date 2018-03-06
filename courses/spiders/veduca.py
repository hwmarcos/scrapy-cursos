# -*- coding: utf-8 -*-
import scrapy
from courses.items import CoursesItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class VeducaSpider(scrapy.Spider):
    name = 'veduca'
    start_urls = ['https://veduca.org/p/cursos/']

    def parse(self, response):
        course_list = response.xpath("//div[contains(@class, 'course-list')]//a")
        for course_item in course_list:
            url = course_item.xpath(".//@href").extract_first()
            url = 'https://veduca.org%s' % url
            yield scrapy.Request(
                url=url, callback=self.parse_detail
            )

    def parse_detail(self, response):
        loader = ItemLoader(CoursesItem(), response=response)
        loader.default_output_processor = TakeFirst()
        loader.add_value('url', response.url)
        loader.add_xpath('title', '//*[contains(@class, "course-title")]/text()')
        loader.add_xpath('headline', '//*[contains(@class, "course-subtitle")]/text()')
        loader.add_xpath('instructors', '//*[contains(@class, "author-name")]/text()')
        loader.add_xpath('lectures', '//a[contains(@class, "item")]/@href')
        yield loader.load_item()
