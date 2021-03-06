import json 
import pandas as pd
from pandas.io import sql
from sqlalchemy import create_engine
import datetime
import copy

date = "19990331"

sql1 = "SELECT * from fx where a = 'USD' or b = 'USD' and (day != 20000806 or day != 20010607) and day > 20140101  order by a, b, day limit 500000"


sqlfx = "SELECT * from fx where (day != 20000806 and day != 20010607 and day != 20050507) and day > " + date + " order by a, b, day limit 500000"

sqlgd1 = "select day, sum(SumArticles)/norm from gdecon2 where (Actor1Code = 'IGOEU' or Actor2Code = 'IGOEU') and day > " + date + " group by day order by day limit 100000"

sqlgd2 = "select day, sum(SumArticles)/norm from gdecon2 where (Actor1Code = 'GBR' or Actor2Code = 'GBR') and day > " + date + " group by day order by day limit 100000"

sqlgd3 = "select day, sum(SumArticles)/norm from gdecon2 where (Actor1Code = 'CHE' or Actor2Code = 'CHE') and day > " + date + " group by day order by day limit 100000"


sqlgd4 = "select day, sum(SumArticles)/norm from gdecon2 where (Actor1Code = 'USA' and (Actor2Code = 'EUR' or Actor2Code = 'IGOEU' or Actor2Code = 'DEU' or Actor2Code = 'GRC')) and day > " + date + " group by day order by day limit 100000"

sqlgd5 = "select day, sum(SumArticles)/norm from gdecon2 where (Actor1Code = 'USA' or Actor2Code = 'USA') and day > " + date + " group by day order by day limit 100000"



#sqlall = "select day, sum(SumArticles)/norm from gdecon1 where (Actor1Code = 'IGOEU' or Actor2Code = 'IGOEU') and day > 20100301 group by day order by day join"



engine = create_engine('mysql://root:cms001@localhost/test', echo=True)
cnx = engine.raw_connection()
df = pd.read_sql(sqlfx, cnx)
gdf = pd.read_sql(sqlgd4, cnx)
#af = pd.read_sql(sql1, cnx)
#a_pairs = pd.read_sql(sqlall, cnx)
#print pairs

#print df
#print gdf

AUDUSD = df[(df.a == 'AUD') & (df.b == 'USD')]
EURUSD = df[(df.a == 'EUR') & (df.b == 'USD')]
GBPUSD = df[(df.a == 'GBP') & (df.b == 'USD')]
USDCAD = df[(df.a == 'USD') & (df.b == 'CAD')]
USDCHF = df[(df.a == 'USD') & (df.b == 'CHF')]
USDJPY = df[(df.a == 'USD') & (df.b == 'JPY')]
EURJPY = df[(df.a == 'EUR') & (df.b == 'JPY')]
AUDJPY = df[(df.a == 'AUD') & (df.b == 'JPY')]
EURGBP = df[(df.a == 'EUR') & (df.b == 'GBP')]
EURCHF = df[(df.a == 'EUR') & (df.b == 'CHF')]
GBPJPY = df[(df.a == 'GBP') & (df.b == 'JPY')]
AUDCHF = df[(df.a == 'AUD') & (df.b == 'CHF')]


upairs = [AUDUSD, EURUSD, GBPUSD, USDCAD, USDCHF, USDJPY, EURJPY, EURGBP, EURCHF, GBPJPY, AUDCHF]

opy = copy.deepcopy(upairs)

for p in upairs:
    p['day'] = [datetime.datetime.combine(datetime.date(int(str(time)[0:4]), int(str(time)[4:6]), int(str(time)[6:])), datetime.time()) for time in p['day']]
    p[['day']] = p[['day']].astype('datetime64[ns]')
    #p = p.set_index('day')
    #print p

"""
for p in a_pairs:
    p['day'] = [datetime.datetime.combine(datetime.date(int(str(time)[0:4]), int(str(time)[4:6]), int(str(time)[6:])), datetime.time()) for time in p['day']]
    p[['day']] = p[['day']].astype('datetime64[ns]')
    #p = p.set_index('day')
    print p
"""

for p in opy:
    p['day'] = [datetime.datetime.combine(datetime.date(int(str(time)[0:4]), int(str(time)[4:6]), int(str(time)[6:])), datetime.time()) for time in p['day']]
    p[['day']] = p[['day']].astype('datetime64[ns]')
    #p = p.set_index('day')
    #print p



#print upairs[0].dtypes
#print upairs[5].dtypes

rows_list = []


"""
for i in range(len(upairs) -1):
   for j in range(len(upairs)):
      if i == j: continue
      if j < i: continue
      #a_pairs[j].columns = ['day', 'av', 'x', 'y']
      opy[j].columns = ['day', 'av', 'x', 'y'] 
      join = pd.merge(upairs[i], opy[j], left_index=False, right_index=False)
      #print join.a.ix[4], join.b.ix[4]
      #print join.x.ix[4], join.y.ix[4]
      corr = join.av.corr(join.avg)
      #print corr
      try:
         dict1 = {'pair1': str(join.a.ix[52] + join.b.ix[52]), 'pair2': str(join.x.ix[52] + join.y.ix[52]), 'corr': corr}

         rows_list.append(dict1)
      except:
         continue


corrs = pd.DataFrame(rows_list)
corrs = corrs.sort(['corr'])
print corrs
"""
gdf.columns = ['day', 'ratio']

gdf['day'] = [datetime.datetime.combine(datetime.date(int(str(time)[0:4]), int(str(time)[4:6]), int(str(time)[6:])), datetime.time()) for time in gdf['day']]
gdf[['day']] = gdf[['day']].astype('datetime64[ns]')


#print gdf
rows_list2 = []

start = 100000


class Player():
    
    def __init__(self, cash):
        self.cash = cash
        self.portfolio = {} 

    def buy(self, price, order, sid):
        if (self.cash <= 0):
            print "you're broke"
            
        else:
            cost = price*order
            if cost > self.cash:
               print "not enough cash for transaction"


            else:
                self.cash -= cost
                try:
                    self.portfolio[sid][0] += order
                    self.portfolio[sid][1] = self.portfolio[sid][0]*price
                    self.portfolio[sid][2] += cost
                    self.portfolio[sid][3] = price

                except:
                    self.portfolio[sid] = [order, cost, cost, price, 0]
            

    def evalall(self):
        keys = self.portfolio.keys()
        results = {}
        for k in keys:
            results[k] = self.evaluate(self.portfolio[k][3], k)

        return results



    def evaluate(self, price, sid):
        try:
            
            self.portfolio[sid][1] = self.portfolio[sid][0]*price
            self.portfolio[sid][3] = price
            self.portfolio[sid][4] = self.portfolio[sid][1] - self.portfolio[sid][2]
            val = self.portfolio[sid]

            return [[sid], val]

        except:
            return
       
print "%%%"
nikhil = Player(100000)
bt = []

for i in range(len(upairs)):

    join = pd.merge(upairs[i], gdf, left_index=False, right_index=False)
    join = join.set_index('day')

    if (join.a.ix[4] != 'EUR' or join.b.ix[4] != 'USD'):
        continue

    #print join
    j = join.itertuples()
    for a in join.itertuples():
        price = a[1]
        if str(join.b.ix[4]) != 'USD':
                price = 1/price

        sid = str(join.a.ix[4] + join.b.ix[4])

        if (a[4] > 0.003): 
            #print a[0], a[1], a[4]
            
            sid = str(join.a.ix[4] + join.b.ix[4])
            nikhil.buy(price, 100, sid)

        table = [str(a[0])]
        eva = nikhil.evaluate(price, sid)
        print eva
        try:
            for lis in eva:
                for item in lis:
                    table.append(item) 
        
        except:
            continue

        print table
         
        #t.append(str(a[0]))
        bt.append(table)
        

    out = nikhil.evalall()
    for key in out.keys():
        print out[key]
        
    output = json.dumps(bt)
        

            


"""
    corr = join.ratio.corr(join.avg)
    try:
         dict1 = {'pair': str(join.a.ix[4] + join.b.ix[4]), 'corr': corr}

         rows_list2.append(dict1)
    except:
        continue    


corrs2 = pd.DataFrame(rows_list2)
#print corrs2
corrs2 = corrs2.sort(['corr'])
print corrs2
      #print join.avg.corr(join.av)

      #print join.head()



#upairs[5].columns = ['day', 'av', 'x', 'y']
""" 
