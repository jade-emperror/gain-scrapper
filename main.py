import os
import requests,csv
from bs4 import BeautifulSoup
url='https://www.moneycontrol.com/stocks/marketstats/nse-gainer/all-companies_-2/'
response_= requests.get(url)
soup = BeautifulSoup(response_.text, 'html.parser')
table=soup.find_all("div",class_="bsr_table hist_tbl_hm")
header=['Symbol','High','Low','Last Price','Prev Close','Change','Gain%','Volume5','Volume10','Volume30','Volume','Lower Circuit','Upper Circuit','VWAP','P/E','P/B']
rows=table[0].find_all("tr")
data=[header]
for row in rows[1:]:
    td=row.find_all("td")
    symbol=row.find('div',class_='PA10')
    if(symbol!=None):
        symbol=symbol.find('span').string 
        if(symbol!=None):
                symbol=' '.join(str(symbol).split(' ')[:2])
                cells=row.find_all("td")
                vol=str(row.find('td',class_='vol')).split('</div>') #fetches the volume section of the row
                vol=vol[4].split('<span id="tt05">')[0]#from that volume is segregated
                if(not vol.isnumeric()):
                    vol=vol[:-5]
                #storing values for better readabilty
                high,low,lastprice,prevclose=cells[1].string,cells[2].string,cells[3].string,cells[4].string
                change,gainper=cells[5].string,cells[6].string
                #volumes
                volume5,volume10,volume30=cells[9].string,cells[11].string,cells[13].string
                lc,uc,pb,pe=cells[29].string,cells[28].string,cells[19].string,cells[18].string
                vwap=cells[30].string
    #Row format=['Symbol','High','Low','Last Price','Prev Close','Change','Gain%','Volume5','Volume10','Volume30','Volume','Lower Circuit','Upper Circuit','VWAP','SMA','Deliverable','P/E','P/B']
                data.append([symbol,high,low,lastprice,prevclose,change,gainper,volume5,volume10,volume30,vol,lc,uc,vwap,pe,pb])
with open('output.csv','a',newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)
print("csv file exported succesfully at "+str(os.getcwd())+"\\output.csv")