import json
import requests
import csv 
import time

class tickersFinancialCrawler:

    def __init__ (self):
        self.session = requests.Session()
        self.tickersListNames = []
        self.dictTickersDetailsList = []
        self.final_tickers_dict_list = []

    def _go_tickers(self,url):
        tickersRequest = requests.get(url)
        #assert tickersRequest.status_code == 200
        #time.sleep(12)
        return tickersRequest
        
    def _get_tickers(self,tickersRequest):
        dictTickers = json.loads(tickersRequest.text)
        return dictTickers

    def _go_ticker_details(self,i):
        tickerDetailsRequest = requests.get("https://api.polygon.io/v1/meta/symbols/"+str(i)+"/company?&apiKey=fXeNsEuF5_RYIgNgFae7LsdpGSz_jAxn").text
        #assert tickerDetailsRequest.status_code == 200
        #time.sleep(12)
        return tickerDetailsRequest

    def _get_ticker_details(self,tickerDetailsRequest):
        dictTickersDetails = json.loads(tickerDetailsRequest)
        return dictTickersDetails    

    def _get_next_cursor(self,ticker_next_request):
        print(ticker_next_request.status_code) # status code la requete = 401 => OK
        if ticker_next_request.status_code == 200:  
            next_tickers_result = json.loads(ticker_next_request.text)
            tickers = next_tickers_result["results"]
            return tickers
        else:
            return None   

    def _go_stock_financials_details(self,companyTicker):
        stockFinancialsRequest = requests.get("https://api.polygon.io/v2/reference/financials/"+str(companyTicker)+"?limit=3&type=T&apiKey=fXeNsEuF5_RYIgNgFae7LsdpGSz_jAxn")
        #assert stockFinancialsRequest.status_code == 200
        #time.sleep(12)
        return stockFinancialsRequest
    
    def _get_stock_financials_details(self,stockFinancialsRequest):
        dictstockFinancials = json.loads(stockFinancialsRequest.text)
        return dictstockFinancials

    def _go_aggregates_details(self,companyTicker):
        url = "https://api.polygon.io/v2/aggs/ticker/"+str(companyTicker)+"/range/1/week/2020-08-19/2021-08-19?adjusted=true&sort=asc&limit=120&apiKey=fXeNsEuF5_RYIgNgFae7LsdpGSz_jAxn"
        aggreagatesRequests = requests.get(url)
        #assert aggreagatesRequests.status_code == 200
        #time.sleep(12)
        print(url)
        return aggreagatesRequests
    
    def _get_aggregates_details(self,aggreagatesRequests):
        dictAggregates = json.loads(aggreagatesRequests.text) # sous la forme {.... results:{ {v:..}, {v:..}, {v:..} }}
        return dictAggregates   
  
    def _import_features_into_csv(self,final_tickers_dict_list):
        with open("C:\\Users\\CYTech Student\\AppData\\Local\\Programs\\Python\\Python39\\Scripts\\tickersInformation.csv",'w', encoding='utf-8') as tickerInfo:
            featuresNames = ["Id","ticker","name","market","locale","Active", "currency_name", "cik", "composite_figi", "share_class_figi", "last_updated_utc",
            'logo', 'listdate', 'bloomberg', 'figi', 'lei', 'sic', 'country', 'industry', 'sector', 'marketcap', 'employees', 'phone', 'ceo', 'url', 'description', 'exchange', 'name', 'symbol', 'exchangeSymbol', 'hq_address', 'hq_state', 'hq_country', 'type', 'updated']
            writer = csv.DictWriter(tickerInfo, fieldnames=featuresNames)    
            writer.writeheader()
            print(len(final_tickers_dict_list)) #taille de  1000
            print(final_tickers_dict_list)
            for ticker in final_tickers_dict_list:
                writer.writerow({'Id': ticker.get("Id"),'ticker' : ticker.get('tickerName'),'name': ticker.get('name'),'market':  ticker.get('market'),'locale':  ticker.get('locale'),'Active':  ticker.get('Active'),'currency_name':  ticker.get('currency_name'), 'cik': ticker.get('cik'), 'composite_figi':  ticker.get('composite_figi'), 'share_class_figi': ticker.get('share_class_figi') , 'last_updated_utc': ticker.get('last_updated_utc'),
                'logo': ticker.get("logo"), 'listdate': ticker.get("listdate"), 'bloomberg' :ticker.get("bloomberg"), 'figi' :ticker.get("fig"), 'lei' :ticker.get("lei"), 'sic' :ticker.get("si"), 'country' :ticker.get("country"), 'industry' :ticker.get("industry"), 'sector' :ticker.get("secto"), 'marketcap' :ticker.get("marketca"), 'employees' :ticker.get("employee"), 'phone' :ticker.get("phone"), 'ceo' :ticker.get("ce"), 'url' :ticker.get("ur"), 'description' :ticker.get("description"), 'exchange' :ticker.get("exchange"), 'name' :ticker.get("name"), 'symbol' :ticker.get("symbol"), 'exchangeSymbol' :ticker.get("exchangeSymbol"), 'hq_address' :ticker.get("hq_address"), 'hq_state' :ticker.get("hq_state"), 'hq_country' :ticker.get("hq_country"), 'type' :ticker.get("type"), 'updated' :ticker.get("update")})
                
    def execute(self,financialCrawler):
        
        counter = 0
        firstUrl = "https://api.polygon.io/v3/reference/tickers?active=true&sort=ticker&order=asc&limit=1000&apiKey=fXeNsEuF5_RYIgNgFae7LsdpGSz_jAxn"
        ticker_request = financialCrawler._go_tickers(firstUrl)
        tickers_result = financialCrawler._get_tickers(ticker_request)
        tickers = tickers_result["results"]

        for ticker in tickers: # remplissage du ticker dict pour la premiere page 
            print(counter)
            ticker_dict = {}
            print(ticker)
            ticker_dict.update(Id= counter ,tickerName=ticker.get('ticker'),name = ticker.get('name'), market=ticker.get('market'), locale = ticker.get('locale'), Active = ticker.get('active'), currency_name = ticker.get('currency_name'), cik = ticker.get('cik'), composite_figi = ticker.get('composite_figi'), share_class_figi = ticker.get('share_class_figi') , last_updated_utc = ticker.get('last_updated_utc'))
            tickerDetailsRequest = financialCrawler._go_ticker_details(ticker.get('ticker'))
            dictTickerDetails = financialCrawler._get_ticker_details(tickerDetailsRequest)
            ticker_dict.update( logo = dictTickerDetails.get("logo"), listdate = dictTickerDetails.get("listdate"), bloomberg = dictTickerDetails.get("bloomberg"), fig = dictTickerDetails.get("figi"), lei = dictTickerDetails.get("lei"), si = dictTickerDetails.get("sic"), country = dictTickerDetails.get("country"), industry = dictTickerDetails.get("industry"), secto = dictTickerDetails.get("lsector"), marketca = dictTickerDetails.get("marketcap"), employee = dictTickerDetails.get("employees"), phone = dictTickerDetails.get("phone"), ce = dictTickerDetails.get("ceo"), ur = dictTickerDetails.get("url"), description = dictTickerDetails.get("description"), exchange = dictTickerDetails.get("exchange"), name = dictTickerDetails.get("name"), symbol = dictTickerDetails.get("symbol"), exchangeSymbol = dictTickerDetails.get("exchangeSymbol"), hq_address = dictTickerDetails.get("hq_adress"), hq_state = dictTickerDetails.get("hq_state"), hq_country = dictTickerDetails.get("hq_country"), type = dictTickerDetails.get("type"), update = dictTickerDetails.get("updated"))
            counter=counter+1
            self.final_tickers_dict_list.append(ticker_dict)
            """ if counter == 2:
                break """

        next_url = tickers_result["next_url"]
        #print(next_url) #OK verification de l'url pour voir si ma requete est fonctionnelle ou pas

        if requests.get(next_url).status_code == 200:

            ticker_next_request = financialCrawler._go_tickers(next_url)
            tickers_next = financialCrawler._get_next_cursor(ticker_next_request)

            if tickers_next != None:
                _has_next_page = True
                print("Ticker is different of 'None'")
                for ticker in tickers: # remplissage du ticker dict pour la premiere page 
                    print(counter)
                    ticker_dict = {}
                    print(ticker)
                    ticker_dict.update(Id= counter ,tickerName=ticker.get('ticker'),name = ticker.get('name'), market=ticker.get('market'), locale = ticker.get('locale'), Active = ticker.get('active'), currency_name = ticker.get('currency_name'), cik = ticker.get('cik'), composite_figi = ticker.get('composite_figi'), share_class_figi = ticker.get('share_class_figi') , last_updated_utc = ticker.get('last_updated_utc'))
                    tickerDetailsRequest = financialCrawler._go_ticker_details(ticker.get('ticker'))
                    dictTickerDetails = financialCrawler._get_ticker_details(tickerDetailsRequest)
                    ticker_dict.update( logo = dictTickerDetails.get("logo"), listdate = dictTickerDetails.get("listdate"), bloomberg = dictTickerDetails.get("bloomberg"), fig = dictTickerDetails.get("figi"), lei = dictTickerDetails.get("lei"), si = dictTickerDetails.get("sic"), country = dictTickerDetails.get("country"), industry = dictTickerDetails.get("industry"), secto = dictTickerDetails.get("lsector"), marketca = dictTickerDetails.get("marketcap"), employee = dictTickerDetails.get("employees"), phone = dictTickerDetails.get("phone"), ce = dictTickerDetails.get("ceo"), ur = dictTickerDetails.get("url"), description = dictTickerDetails.get("description"), exchange = dictTickerDetails.get("exchange"), name = dictTickerDetails.get("name"), symbol = dictTickerDetails.get("symbol"), exchangeSymbol = dictTickerDetails.get("exchangeSymbol"), hq_address = dictTickerDetails.get("hq_adress"), hq_state = dictTickerDetails.get("hq_state"), hq_country = dictTickerDetails.get("hq_country"), type = dictTickerDetails.get("type"), update = dictTickerDetails.get("updated"))
                    counter=counter+1
                    self.final_tickers_dict_list.append(ticker_dict)
            else:
                _has_next_page = False
                print("Ticker is equal to 'None'")

            counter = 3 # pour connaitre le nombre de page prise

            while _has_next_page == True:
                print("I am in "+str(counter)+"next_url")
                tickers_next = financialCrawler._get_next_cursor(ticker_next_request)
                for ticker in tickers: # remplissage du ticker dict pour la premiere page 
                    print(counter)
                    ticker_dict = {}
                    print(ticker)
                    ticker_dict.update(Id= counter ,tickerName=ticker.get('ticker'),name = ticker.get('name'), market=ticker.get('market'), locale = ticker.get('locale'), Active = ticker.get('active'), currency_name = ticker.get('currency_name'), cik = ticker.get('cik'), composite_figi = ticker.get('composite_figi'), share_class_figi = ticker.get('share_class_figi') , last_updated_utc = ticker.get('last_updated_utc'))
                    tickerDetailsRequest = financialCrawler._go_ticker_details(ticker.get('ticker'))
                    dictTickerDetails = financialCrawler._get_ticker_details(tickerDetailsRequest)
                    ticker_dict.update( logo = dictTickerDetails.get("logo"), listdate = dictTickerDetails.get("listdate"), bloomberg = dictTickerDetails.get("bloomberg"), fig = dictTickerDetails.get("figi"), lei = dictTickerDetails.get("lei"), si = dictTickerDetails.get("sic"), country = dictTickerDetails.get("country"), industry = dictTickerDetails.get("industry"), secto = dictTickerDetails.get("lsector"), marketca = dictTickerDetails.get("marketcap"), employee = dictTickerDetails.get("employees"), phone = dictTickerDetails.get("phone"), ce = dictTickerDetails.get("ceo"), ur = dictTickerDetails.get("url"), description = dictTickerDetails.get("description"), exchange = dictTickerDetails.get("exchange"), name = dictTickerDetails.get("name"), symbol = dictTickerDetails.get("symbol"), exchangeSymbol = dictTickerDetails.get("exchangeSymbol"), hq_address = dictTickerDetails.get("hq_adress"), hq_state = dictTickerDetails.get("hq_state"), hq_country = dictTickerDetails.get("hq_country"), type = dictTickerDetails.get("type"), update = dictTickerDetails.get("updated"))
                    counter=counter+1
                    self.final_tickers_dict_list.append(ticker_dict)
                next_url = tickers_result["next_url"]
                ticker_next_request = requests.get(next_url)
        else:
            pass 

        final_tickers_dict_list = self.final_tickers_dict_list
        financialCrawler._import_features_into_csv(final_tickers_dict_list)

def main():
    financialCrawler = tickersFinancialCrawler()
    financialCrawler.execute(financialCrawler)

if __name__ == "__main__":
    main()