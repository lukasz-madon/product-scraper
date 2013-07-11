from twisted.internet import task
from twisted.internet import reactor
import os

timeout = 60.0 * 20  # 20 mins

print "Starting oxygen spider with 20min timeout..."
os.chdir("oxygen")

def crawl():
    os.system("scrapy crawl oxygen_spider")

l = task.LoopingCall(crawl)
l.start(timeout)

reactor.run()
