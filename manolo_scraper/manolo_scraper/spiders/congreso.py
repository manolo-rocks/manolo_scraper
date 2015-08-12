import re
import math
import datetime
from datetime import timedelta

from scrapy import FormRequest, Request

from spiders import ManoloBaseSpider
from ..items import ManoloItem

from ..utils import make_hash


class CongresoSpider(ManoloBaseSpider):
    name = 'congreso'

    allowed_domains = ["regvisitas.congreso.gob.pe"]

    NUMBER_OF_PAGES_PER_PAGE = 10

    def start_requests(self):
        d1 = datetime.datetime.strptime(self.date_start, '%Y-%m-%d').date()
        d2 = datetime.date.today()
        delta = d2 - d1

        for i in range(delta.days + 1):
            my_date = d1 + timedelta(days=i)
            my_date_str = my_date.strftime("%d/%m/%Y")

            print("SCRAPING: %s" % my_date_str)

            # This initial request always hit the current page of the date.
            request = Request(url="http://regvisitas.congreso.gob.pe/regvisitastransparencia/",
                              meta={
                                  'current_page': 1,
                                  'date': my_date_str,
                                  'is_initial_request': 1
                              },
                              dont_filter=True,
                              callback=self.parse_pages)

            request.meta['date'] = my_date_str

            yield request

    def parse_pages(self, response):
        my_date_str = response.meta['date']
        is_initial_request = int(response.meta['is_initial_request'])

        if is_initial_request == 1:
            request = self._request_initial_date_page(response, my_date_str, self.parse_pages)
        else:
            # Parse Items
            items = self.parse(response)
            for item in items:
                yield item

            request = self._request_next_page(response, my_date_str, self.parse_pages)

        yield request

    def parse(self, response):

        for row in response.xpath('//table[@class="grid"]/tr'):

            data = row.xpath('td')
            full_name = ''

            try:
                full_name = data[2].xpath('./span/text()').extract()[0]
            except IndexError:
                pass

            if len(data) > 9 and full_name.strip():
                date_obj = datetime.datetime.strptime(response.meta['date'], '%d/%m/%Y')

                item = ManoloItem()
                item['full_name'] = ''
                item['id_document'] = ''
                item['id_number'] = ''
                item['institution'] = 'congreso'
                item['entity'] = ''
                item['reason'] = ''
                item['host_name'] = ''
                item['title'] = ''
                item['office'] = ''
                item['time_start'] = ''
                item['time_end'] = ''
                item['date'] = date_obj

                item['full_name'] = full_name

                try:
                    item['time_start'] = data[1].xpath('./span/text()').extract()[0].strip()
                except IndexError:
                    pass
                except:
                    pass

                try:
                    item['full_name'] = data[2].xpath('./span/text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['id_document'] = data[3].xpath('./span/text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['id_number'] = data[4].xpath('./span/text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['entity'] = data[5].xpath('./span/text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['reason'] = data[6].xpath('./span/text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['host_name'] = data[7].xpath('./span/text()').extract()[0].strip()
                except IndexError:
                    pass
                except:
                    pass

                try:
                    item['title'] = data[8].xpath('./span/text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['office'] = data[9].xpath('./span/text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['time_end'] = data[10].xpath('./span/text()').extract()[0].strip()
                except IndexError:
                    pass
                except:
                    pass

                item = make_hash(item)

                yield item

    def _get_number_of_pages(self, total_of_records):
        return int(math.ceil(total_of_records / float(self.NUMBER_OF_PAGES_PER_PAGE)))

    def _request_next_page(self, response, date_str, callback):
        current_page = int(response.meta['current_page'])

        try:
            total_string = response.css('#LblTotal').xpath('./text()').extract()[0]
        except:
            total_string = ''

        total = re.search(r'(\d+)', total_string)

        if total:

            # Deal with the next page.
            total = total.group(1)
            number_of_pages = self._get_number_of_pages(int(total))

            if current_page < number_of_pages:
                current_page += 1

                formdata = {
                    'TxtFecha': date_str,
                    'BtnBuscar': 'Buscar',
                    'LwVisitasCR$DpVisitasCR$ctl02$ctl00.x': '1',
                    'LwVisitasCR$DpVisitasCR$ctl02$ctl00.y': '1'
                }

                request = FormRequest.from_response(response,
                                                    formdata=formdata,
                                                    meta={'current_page': current_page},
                                                    dont_click=True,
                                                    dont_filter=True,
                                                    callback=callback
                )

                request.meta['date'] = date_str
                request.meta['current_page'] = current_page
                request.meta['is_initial_request'] = 0

                return request

    def _request_initial_date_page(self, response, date_str, callback):
        formdata = {
            'TxtFecha': date_str,
            'BtnBuscar': 'Buscar'
        }

        request = FormRequest.from_response(response,
                                            formdata=formdata,
                                            meta={'current_page': 1},
                                            dont_click=True,
                                            dont_filter=True,
                                            callback=callback
        )


        request.meta['date'] = date_str
        request.meta['is_initial_request'] = 0
        request.meta['current_page'] = 1

        return request
