# Scrapy settings for oxygen project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'oxygen'

SPIDER_MODULES = ['oxygen.spiders']
NEWSPIDER_MODULE = 'oxygen.spiders'
ITEM_PIPELINES = [
    'oxygen.pipelines.OxygenPipeline',
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'oxygen (+http://www.yourdomain.com)'
