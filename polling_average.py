import sys  
import time
import csv
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
from lxml import html 

class Render(QWebPage):  
    def __init__(self, url):  
        self.app = QApplication(sys.argv)  
        QWebPage.__init__(self)  
        self.loadFinished.connect(self._loadFinished)  
        self.mainFrame().load(QUrl(url))  
        self.app.exec_()  
  
    def _loadFinished(self, result):  
        self.frame = self.mainFrame()  
        self.app.quit()  

url = 'http://projects.fivethirtyeight.com/2016-election-forecast/national-polls/'
while(True):
    r = Render(url)  
    result = r.frame.toHtml()
    tree = html.fromstring(result)
    table = tree.xpath('//*[@id="cardsets"]/div[53]/div/div[4]/div[2]/div/table/tbody/tr[7]')
    data = [ele.text for ele in table[0]]
    imestamp = time.time()
    with open('polling_average.csv', 'a') as out:
        writer = csv.writer(out)
        writer.writerow([timestamp, float(data[2].strip('%'))/100.0,
            float(data[3].strip('%'))/100.0,
            float(data[4].strip('%'))/100.0])
    sleep(7200)
