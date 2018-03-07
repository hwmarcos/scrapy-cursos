# -*- coding: utf-8 -*-
import scrapy

from courses.items import CoursesItem, VeducaItemLoader


class VeducaSpider(scrapy.Spider):
    name = 'veduca'
    start_urls = ['https://veduca.org/cursos/']

    def parse(self, response):
        course_list = response.xpath("//div[contains(@class, 'course-list')]//a")
        for course_item in course_list:
            url = course_item.xpath(".//@href").extract_first()
            url = 'https://veduca.org%s' % url
            yield scrapy.Request(
                url=url, callback=self.parse_detail
            )
        next_page = response.xpath("//span[contains(@class, 'next')]/a/@href").extract_first()
        if next_page:
            self.log('************************************* Página Atual: %s' % next_page)
            url = 'https://veduca.org%s' % next_page
            yield scrapy.Request(
                url=url, callback=self.parse
            )

    def parse_detail(self, response):
        loader = VeducaItemLoader(CoursesItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('title', '//*[contains(@class, "course-title")]/text()')
        loader.add_xpath('headline', '//*[contains(@class, "course-subtitle")]/text()')
        loader.add_xpath('instructors', '//*[contains(@class, "author-name")]/text()')
        loader.add_xpath('lectures', '//a[contains(@class, "item")]/@href')
        loader.add_xpath('instructors_description', '//div[contains(@class, "bio")]/div/div/div/div/div[2]')
        yield loader.load_item()
