import sqlite3                        # Database
import time                           # For sleep
import yahooDataObject
import Pyro4

f = time.strftime("%d/%m/%Y")
h = time.strftime("%H:%M:%S")
fecha = "'" + f + "'"
hora = "'" + h + "'"

conn = sqlite3.connect('masterDB.db') # Create connection
c = conn.cursor() # Create cursor

class MasterProgram:
    def __init__(self, a_socket):
        self._objList = [yahooDataObject.yahooDataObject('GOOG'), 
                                            yahooDataObject.yahooDataObject('AAPL'),
                                            yahooDataObject.yahooDataObject('IBM'),
                                            yahooDataObject.yahooDataObject('MSFT'),
                                            yahooDataObject.yahooDataObject('TOSHBF'),
                                            yahooDataObject.yahooDataObject('SNE'),
                                            yahooDataObject.yahooDataObject('2357.TW'),
                                            yahooDataObject.yahooDataObject('LNVGY'),
                                            yahooDataObject.yahooDataObject('ITX.MC'),
                                            yahooDataObject.yahooDataObject('SAN'),
                                            yahooDataObject.yahooDataObject('FB'),
                                            yahooDataObject.yahooDataObject('IDR.MC')]

    def dataBase(self):
        # c.execute('''DROP TABLE IF EXISTS stocks''')        
        c.execute('CREATE TABLE if not EXISTS stocks (symbol text, last text, xdate text, change text, high text, low text, vol text, send text)')
    
    def getBootTime(self):
        return hora
    
    def doWork(self):
        for obj in self._objList:
            c = conn.cursor()
            obj.updateYahooStockQuoteWeb()
            valores = obj.D
            
            query = 'INSERT INTO stocks (symbol, last, xdate, change, high, low, vol, send) VALUES (:symbol, :last, :date, :change, :high, :low, :vol, 1);'
            c.execute(query, valores)
            print c.fetchall()
            conn.commit()

daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(MasterProgram)
ns.register("master.boot.time", uri)

print ("Master Booted")
daemon.requestLoop()
