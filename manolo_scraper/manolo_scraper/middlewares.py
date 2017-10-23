from scrapy.conf import settings


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = settings.get('HTTP_PROXY')
        if proxy:
            request.meta['proxy'] = proxy
