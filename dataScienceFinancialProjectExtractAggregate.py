import json
import requests
import csv 
import time

class StockFinancialsCrawler:

    def __init__ (self):
        self.session = requests.Session()
        self.final_stock_financials_tickers_list = []
        self.final_stock_financials_dict_list = []

    def _go_tickers(self,url):
        tickersRequest = requests.get(url)
        assert tickersRequest.status_code == 200
        time.sleep(12)
        return tickersRequest
        
    def _get_tickers(self,tickersRequest):
        dictTickers = json.loads(tickersRequest.text)
        return dictTickers

    def _go_ticker_details(self,i):
        tickerDetailsRequest = requests.get("https://api.polygon.io/v1/meta/symbols/"+str(i)+"/company?&apiKey=fXeNsEuF5_RYIgNgFae7LsdpGSz_jAxn").text
        assert tickerDetailsRequest.status_code == 200
        time.sleep(12)
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
        assert stockFinancialsRequest.status_code == 200
        time.sleep(12)
        return stockFinancialsRequest
    
    def _get_stock_financials_details(self,stockFinancialsRequest):
        dictstockFinancials = json.loads(stockFinancialsRequest.text)
        return dictstockFinancials

    def _go_aggregates_details(self,companyTicker):
        url = "https://api.polygon.io/v2/aggs/ticker/"+str(companyTicker)+"/range/1/week/2020-08-19/2021-08-19?adjusted=true&sort=asc&limit=120&apiKey=fXeNsEuF5_RYIgNgFae7LsdpGSz_jAxn"
        aggreagatesRequests = requests.get(url)
        assert aggreagatesRequests.status_code == 200
        time.sleep(12)
        print(url)
        return aggreagatesRequests
    
    def _get_aggregates_details(self,aggreagatesRequests):
        dictAggregates = json.loads(aggreagatesRequests.text) # sous la forme {.... results:{ {v:..}, {v:..}, {v:..} }}
        return dictAggregates   

    def _import_features_into_csv(self,final_stock_financials_dict_list):
        with open("C:\\Users\\CYTech Student\\AppData\\Local\\Programs\\Python\\Python39\\Scripts\\financialsInformation.csv",'w', encoding='utf-8') as financialsInfo:
            featuresNames = ["Id","tickerId", "ticker","period","calendar_date","report_period","updated","date_key","accumulated_other_comprehensive_income","assets","assets_current","assets_non_current","book_value_per_share","capital_expenditure","cash_and_equivalents","cash_and_equivalents_usd","cost_of_revenue","consolidated_income"
            ,"current_ratio","debt_to_equity_ratio","debt","debt_current","debt_non_current","debt_usd","deferred_revenue","depreciation_amortization_and_accretion","deposits","dividend_yield","dividends_per_basic_common_share","earning_before_interest_taxes","earnings_before_interest_taxes_depreciation_amortization","ebitda_margin","earnings_before_interest_taxes_depreciation_amortization_usd",
            "earning_before_interest_taxes_usd","earnings_before_tax","earnings_per_basic_share","earnings_per_diluted_share","earnings_per_basic_share_usd","shareholders_equity","shareholders_equity_usd","enterprise_value","enterprise_value_over_ebit","enterprise_value_over_ebita","free_cash_flow","free_cash_flow_per_share",
            "foreign_currency_usd_exchange_rate","gross_profit","gross_margin","goodwill_and_intangible_assets","interest_expense","invested_capital","inventory","investments","investments_current","investments_non_current","total_liabilities","current_liabilities","liabilities_non_current","market_capitalization","net_cash_flow",
            "net_cash_flow_business_acquisitions_disposals","issuance_equity_shares","issuance_debt_securities","payment_dividends_other_cash_distributions","net_cash_flow_from_financing","net_cash_flow_from_investing","net_cash_flow_investment_acquisitions_disposals","net_cash_flow_from_operations","effect_of_exchange_rate_changes_on_cash","net_income",
            "net_income_common_stock","net_income_common_stock_usd","net_loss_income_from_discontinued_operations","net_income_to_non_controlling_interests","profit_margin","operating_expenses","operating_income","trade_and_non_trade_payables","payout_ratio","price_to_book_value","price_earnings","price_to_earnings_ratio","property_plant_equipment_net",
            "preferred_dividends_income_statement_impact","share_price_adjusted_close","price_sales","price_to_sales_ratio","trade_and_non_trade_receivables","accumulated_retained_earnings_deficit","revenues","revenues_usd","research_and_development_expense","return_on_sales","share_based_compensation","selling_general_and_administrative_expense","share_factor",
            "shares","weighted_average_shares","weighted_average_shares_diluted","sales_per_share","tangible_asset_value","tax_assets","income_tax_expense","tax_liabilities","tangible_assets_book_value_per_share","working_capital"]

            writer = csv.DictWriter(financialsInfo, fieldnames=featuresNames)    
            writer.writeheader()
            countId = 0
            countTickerId = 1
            print("in the import method before the loop:"+str(len(final_stock_financials_dict_list)))
            print(final_stock_financials_dict_list) # sous la forme { {..,results:[ {}{}{}] }, {..,results:[ {}{}{}] }, {..,results:[ {}{}{}] } }
            for ticker in final_stock_financials_dict_list:
                print("##########################")
                print(ticker)
                for i in range(0,len(ticker)):
                    writer.writerow({ 
                            "Id": countId
                            ,"tickerId": countTickerId
                            ,"ticker":ticker["results"][i]["ticker"]
                            ,"period":ticker["results"][i]["period"]
                            ,"calendar_date":ticker["results"][i]["calendarDate"]
                            ,"report_period":ticker["results"][i]["reportPeriod"]
                            ,"updated":ticker["results"][i]["updated"]
                            ,"date_key":ticker["results"][i]["dateKey"]
                            ,"accumulated_other_comprehensive_income":ticker["results"][i]["accumulatedOtherComprehensiveIncome"]
                            ,"assets":ticker["results"][i]["assets"]
                            ,"assets_current":ticker["results"][i]["assetsCurrent"]
                            ,"assets_non_current":ticker["results"][i]["assetsNonCurrent"]
                            ,"book_value_per_share":ticker["results"][i]["bookValuePerShare"]
                            ,"capital_expenditure":ticker["results"][i]["capitalExpenditure"]
                            ,"cash_and_equivalents":ticker["results"][i]["cashAndEquivalents"]
                            ,"cash_and_equivalents_usd":ticker["results"][i]["cashAndEquivalentsUSD"]
                            ,"cost_of_revenue":ticker["results"][i]["costOfRevenue"]
                            ,"consolidated_income":ticker["results"][i]["consolidatedIncome"]
                            ,"current_ratio":ticker["results"][i]["currentRatio"]
                            ,"debt_to_equity_ratio":ticker["results"][i]["debtToEquityRatio"]
                            ,"debt":ticker["results"][i]["debt"]
                            ,"debt_current":ticker["results"][i]["debtCurrent"]
                            ,"debt_non_current":ticker["results"][i]["debtNonCurrent"]
                            ,"debt_usd":ticker["results"][i]["debtUSD"]
                            ,"deferred_revenue":ticker["results"][i]["deferredRevenue"]
                            ,"depreciation_amortization_and_accretion":ticker["results"][i]["depreciationAmortizationAndAccretion"]
                            ,"deposits":ticker["results"][i]["deposits"]
                            ,"dividend_yield":ticker["results"][i]["dividendYield"]
                            ,"dividends_per_basic_common_share":ticker["results"][i]["dividendsPerBasicCommonShare"]
                            ,"earning_before_interest_taxes":ticker["results"][i]["earningBeforeInterestTaxes"]
                            ,"earnings_before_interest_taxes_depreciation_amortization":ticker["results"][i]["earningsBeforeInterestTaxesDepreciationAmortization"]
                            ,"ebitda_margin":ticker["results"][i]["EBITDAMargin"]
                            ,"earnings_before_interest_taxes_depreciation_amortization_usd":ticker["results"][i]["earningsBeforeInterestTaxesDepreciationAmortizationUSD"]
                            ,"earning_before_interest_taxes_usd":ticker["results"][i][ "earningBeforeInterestTaxesUSD"]
                            ,"earnings_before_tax":ticker["results"][i]["earningsBeforeTax"]
                            ,"earnings_per_basic_share":ticker["results"][i]["earningsPerBasicShare"]
                            ,"earnings_per_diluted_share":ticker["results"][i]["earningsPerDilutedShare"]
                            ,"earnings_per_basic_share_usd":ticker["results"][i]["earningsPerBasicShareUSD"]
                            ,"shareholders_equity":ticker["results"][i]["shareholdersEquity"]
                            ,"shareholders_equity_usd":ticker["results"][i][ "shareholdersEquityUSD"]
                            ,"enterprise_value":ticker["results"][i]["enterpriseValue"]
                            ,"enterprise_value_over_ebit":ticker["results"][i]["enterpriseValueOverEBIT"]
                            ,"enterprise_value_over_ebita":ticker["results"][i]["enterpriseValueOverEBITDA"]
                            ,"free_cash_flow":ticker["results"][i]["freeCashFlow"]
                            ,"free_cash_flow_per_share":ticker["results"][i]["freeCashFlowPerShare"]
                            ,"foreign_currency_usd_exchange_rate":ticker["results"][i]["foreignCurrencyUSDExchangeRate"]
                            ,"gross_profit":ticker["results"][i]["grossProfit"]
                            ,"gross_margin":ticker["results"][i]["grossMargin"]
                            ,"goodwill_and_intangible_assets":ticker["results"][i]["goodwillAndIntangibleAssets"]
                            ,"interest_expense":ticker["results"][i]["interestExpense"]
                            ,"invested_capital":ticker["results"][i]["investedCapital"]
                            ,"inventory":ticker["results"][i]["inventory"]
                            ,"investments":ticker["results"][i]["investments"]
                            ,"investments_current":ticker["results"][i]["investmentsCurrent"]
                            ,"investments_non_current":ticker["results"][i]["investmentsNonCurrent"]
                            ,"total_liabilities":ticker["results"][i]["totalLiabilities"]
                            ,"current_liabilities":ticker["results"][i]["currentLiabilities"]
                            ,"liabilities_non_current":ticker["results"][i]["liabilitiesNonCurrent"]
                            ,"market_capitalization":ticker["results"][i]["marketCapitalization"]
                            ,"net_cash_flow":ticker["results"][i]["netCashFlow"]
                            ,"net_cash_flow_business_acquisitions_disposals":ticker["results"][i]["netCashFlowBusinessAcquisitionsDisposals"]
                            ,"issuance_equity_shares":ticker["results"][i]["issuanceEquityShares"]
                            ,"issuance_debt_securities":ticker["results"][i]["issuanceDebtSecurities"]
                            ,"payment_dividends_other_cash_distributions":ticker["results"][i]["paymentDividendsOtherCashDistributions"]
                            ,"net_cash_flow_from_financing":ticker["results"][i]["netCashFlowFromFinancing"]
                            ,"net_cash_flow_from_investing":ticker["results"][i]["netCashFlowFromInvesting"]
                            ,"net_cash_flow_investment_acquisitions_disposals":ticker["results"][i]["netCashFlowInvestmentAcquisitionsDisposals"]
                            ,"net_cash_flow_from_operations":ticker["results"][i]["netCashFlowFromOperations"]
                            ,"effect_of_exchange_rate_changes_on_cash":ticker["results"][i]["effectOfExchangeRateChangesOnCash"]
                            ,"net_income":ticker["results"][i]["netIncome"]
                            ,"net_income_common_stock":ticker["results"][i][ "netIncomeCommonStock"]
                            ,"net_income_common_stock_usd":ticker["results"][i]["netIncomeCommonStockUSD"]
                            ,"net_loss_income_from_discontinued_operations":ticker["results"][i]["netLossIncomeFromDiscontinuedOperations"]
                            ,"net_income_to_non_controlling_interests":ticker["results"][i]["netIncomeToNonControllingInterests"]
                            ,"profit_margin":ticker["results"][i]["profitMargin"]
                            ,"operating_expenses":ticker["results"][i]["operatingExpenses"]
                            ,"operating_income":ticker["results"][i]["operatingIncome"]
                            ,"trade_and_non_trade_payables":ticker["results"][i]["tradeAndNonTradePayables"]
                            ,"payout_ratio":ticker["results"][i]["payoutRatio"]
                            ,"price_to_book_value":ticker["results"][i]["priceToBookValue"]
                            ,"price_earnings":ticker["results"][i]["priceEarnings"]
                            ,"price_to_earnings_ratio":ticker["results"][i]["priceToEarningsRatio"]
                            ,"property_plant_equipment_net":ticker["results"][i]["propertyPlantEquipmentNet"]
                            ,"preferred_dividends_income_statement_impact":ticker["results"][i]["preferredDividendsIncomeStatementImpact"]
                            ,"share_price_adjusted_close":ticker["results"][i]["sharePriceAdjustedClose"]
                            ,"price_sales":ticker["results"][i]["priceSales"]
                            ,"price_to_sales_ratio":ticker["results"][i]["priceToSalesRatio"]
                            ,"trade_and_non_trade_receivables":ticker["results"][i]["tradeAndNonTradeReceivables"]
                            ,"accumulated_retained_earnings_deficit":ticker["results"][i]["accumulatedRetainedEarningsDeficit"]
                            ,"revenues":ticker["results"][i]["revenues"]
                            ,"revenues_usd":ticker["results"][i][ "revenuesUSD"]
                            ,"research_and_development_expense":ticker["results"][i]["researchAndDevelopmentExpense"]
                            ,"return_on_sales":ticker["results"][i]["returnOnSales"]
                            ,"share_based_compensation":ticker["results"][i]["shareBasedCompensation"]
                            ,"selling_general_and_administrative_expense":ticker["results"][i]["sellingGeneralAndAdministrativeExpense"]
                            ,"share_factor":ticker["results"][i]["shareFactor"]
                            ,"shares":ticker["results"][i]["shares"]
                            ,"weighted_average_shares":ticker["results"][i]["weightedAverageShares"]
                            #,"weighted_average_shares_diluted":ticker["results"][i]["weightedAverageSharesDiluted"] #weightedAverageSharesDiluted
                            ,"sales_per_share":ticker["results"][i]["salesPerShare"]
                            ,"tangible_asset_value":ticker["results"][i]["tangibleAssetValue"]
                            ,"tax_assets":ticker["results"][i]["taxAssets"]
                            ,"income_tax_expense":ticker["results"][i]["incomeTaxExpense"]
                            ,"tax_liabilities":ticker["results"][i]["taxLiabilities"]
                            ,"tangible_assets_book_value_per_share":ticker["results"][i]["tangibleAssetsBookValuePerShare"]
                            ,"working_capital":ticker["results"][i]["workingCapital"]
                        })
                countId += 1
                countTickerId += 1
        
    def _import_features_into_dataBase(self,final_stock_financials_dict_list):

        countTickerId = 0

        for ticker in final_stock_financials_dict_list:
                print("##########################")
                for i in range(0,len(ticker)):
                    { 
                            "tickerId": countTickerId
                            ,"ticker":ticker["results"][i]["ticker"]
                            ,"periode":ticker["results"][i]["period"]
                            ,"calendar_date":ticker["results"][i]["calendarDate"]
                            ,"report_periode":ticker["results"][i]["reportPeriod"]
                            ,"updated":ticker["results"][i]["updated"]
                            ,"date_key":ticker["results"][i]["dateKey"]
                            ,"accumulated_other_comprehensive_income":ticker["results"][i]["accumulatedOtherComprehensiveIncome"]
                            ,"assets":ticker["results"][i]["assets"]
                            ,"assets_current":ticker["results"][i]["assetsCurrent"]
                            ,"assets_non_current":ticker["results"][i]["assetsNonCurrent"]
                            ,"book_value_per_share":ticker["results"][i]["bookValuePerShare"]
                            ,"capital_expenditure":ticker["results"][i]["capitalExpenditure"]
                            ,"cash_and_equivalents":ticker["results"][i]["cashAndEquivalents"]
                            ,"cash_and_equivalents_usd":ticker["results"][i]["cashAndEquivalentsUSD"]
                            ,"cost_of_revenue":ticker["results"][i]["costOfRevenue"]
                            ,"consolidated_income":ticker["results"][i]["consolidatedIncome"]
                            ,"current_ratio":ticker["results"][i]["currentRatio"]
                            ,"debt_to_equity_ratio":ticker["results"][i]["debtToEquityRatio"]
                            ,"debt":ticker["results"][i]["debt"]
                            ,"debt_current":ticker["results"][i]["debtCurrent"]
                            ,"debt_non_current":ticker["results"][i]["debtNonCurrent"]
                            ,"debt_usd":ticker["results"][i]["debtUSD"]
                            ,"deferred_revenue":ticker["results"][i]["deferredRevenue"]
                            ,"depreciation_amortization_and_accretion":ticker["results"][i]["depreciationAmortizationAndAccretion"]
                            ,"deposits":ticker["results"][i]["deposits"]
                            ,"dividend_yield":ticker["results"][i]["dividendYield"]
                            ,"dividends_per_basic_common_share":ticker["results"][i]["dividendsPerBasicCommonShare"]
                            ,"earning_before_interest_taxes":ticker["results"][i]["earningBeforeInterestTaxes"]
                            ,"earnings_before_interest_taxes_depreciation_amortization":ticker["results"][i]["earningsBeforeInterestTaxesDepreciationAmortization"]
                            ,"ebitda_margin":ticker["results"][i]["EBITDAMargin"]
                            ,"earnings_before_interest_taxes_depreciation_amortization_usd":ticker["results"][i]["earningsBeforeInterestTaxesDepreciationAmortizationUSD"]
                            ,"earning_before_interest_taxes_usd":ticker["results"][i][ "earningBeforeInterestTaxesUSD"]
                            ,"earnings_before_tax":ticker["results"][i]["earningsBeforeTax"]
                            ,"earnings_per_basic_share":ticker["results"][i]["earningsPerBasicShare"]
                            ,"earnings_per_diluted_share":ticker["results"][i]["earningsPerDilutedShare"]
                            ,"earnings_per_basic_share_usd":ticker["results"][i]["earningsPerBasicShareUSD"]
                            ,"shareholders_equity":ticker["results"][i]["shareholdersEquity"]
                            ,"shareholders_equity_usd":ticker["results"][i][ "shareholdersEquityUSD"]
                            ,"enterprise_value":ticker["results"][i]["enterpriseValue"]
                            ,"enterprise_value_over_ebit":ticker["results"][i]["enterpriseValueOverEBIT"]
                            ,"enterprise_value_over_ebita":ticker["results"][i]["enterpriseValueOverEBITDA"]
                            ,"free_cash_flow":ticker["results"][i]["freeCashFlow"]
                            ,"free_cash_flow_per_share":ticker["results"][i]["freeCashFlowPerShare"]
                            ,"foreign_currency_usd_exchange_rate":ticker["results"][i]["foreignCurrencyUSDExchangeRate"]
                            ,"gross_profit":ticker["results"][i]["grossProfit"]
                            ,"gross_margin":ticker["results"][i]["grossMargin"]
                            ,"goodwill_and_intangible_assets":ticker["results"][i]["goodwillAndIntangibleAssets"]
                            ,"interest_expense":ticker["results"][i]["interestExpense"]
                            ,"invested_capital":ticker["results"][i]["investedCapital"]
                            ,"inventory":ticker["results"][i]["inventory"]
                            ,"investments":ticker["results"][i]["investments"]
                            ,"investments_current":ticker["results"][i]["investmentsCurrent"]
                            ,"investments_non_current":ticker["results"][i]["investmentsNonCurrent"]
                            ,"total_liabilities":ticker["results"][i]["totalLiabilities"]
                            ,"current_liabilities":ticker["results"][i]["currentLiabilities"]
                            ,"liabilities_non_current":ticker["results"][i]["liabilitiesNonCurrent"]
                            ,"market_capitalization":ticker["results"][i]["marketCapitalization"]
                            ,"net_cash_flow":ticker["results"][i]["netCashFlow"]
                            ,"net_cash_flow_business_acquisitions_disposals":ticker["results"][i]["netCashFlowBusinessAcquisitionsDisposals"]
                            ,"issuance_equity_shares":ticker["results"][i]["issuanceEquityShares"]
                            ,"issuance_debt_securities":ticker["results"][i]["issuanceDebtSecurities"]
                            ,"payment_dividends_other_cash_distributions":ticker["results"][i]["paymentDividendsOtherCashDistributions"]
                            ,"net_cash_flow_from_financing":ticker["results"][i]["netCashFlowFromFinancing"]
                            ,"net_cash_flow_from_investing":ticker["results"][i]["netCashFlowFromInvesting"]
                            ,"net_cash_flow_investment_acquisitions_disposals":ticker["results"][i]["netCashFlowInvestmentAcquisitionsDisposals"]
                            ,"net_cash_flow_from_operations":ticker["results"][i]["netCashFlowFromOperations"]
                            ,"effect_of_exchange_rate_changes_on_cash":ticker["results"][i]["effectOfExchangeRateChangesOnCash"]
                            ,"net_income":ticker["results"][i]["netIncome"]
                            ,"net_income_common_stock":ticker["results"][i][ "netIncomeCommonStock"]
                            ,"net_income_common_stock_usd":ticker["results"][i]["netIncomeCommonStockUSD"]
                            ,"net_loss_income_from_discontinued_operations":ticker["results"][i]["netLossIncomeFromDiscontinuedOperations"]
                            ,"net_income_to_non_controlling_interests":ticker["results"][i]["netIncomeToNonControllingInterests"]
                            ,"profit_margin":ticker["results"][i]["profitMargin"]
                            ,"operating_expenses":ticker["results"][i]["operatingExpenses"]
                            ,"operating_income":ticker["results"][i]["operatingIncome"]
                            ,"trade_and_non_trade_payables":ticker["results"][i]["tradeAndNonTradePayables"]
                            ,"payout_ratio":ticker["results"][i]["payoutRatio"]
                            ,"price_to_book_value":ticker["results"][i]["priceToBookValue"]
                            ,"price_earnings":ticker["results"][i]["priceEarnings"]
                            ,"price_to_earnings_ratio":ticker["results"][i]["priceToEarningsRatio"]
                            ,"property_plant_equipment_net":ticker["results"][i]["propertyPlantEquipmentNet"]
                            ,"preferred_dividends_income_statement_impact":ticker["results"][i]["preferredDividendsIncomeStatementImpact"]
                            ,"share_price_adjusted_close":ticker["results"][i]["sharePriceAdjustedClose"]
                            ,"price_sales":ticker["results"][i]["priceSales"]
                            ,"price_to_sales_ratio":ticker["results"][i]["priceToSalesRatio"]
                            ,"trade_and_non_trade_receivables":ticker["results"][i]["tradeAndNonTradeReceivables"]
                            ,"accumulated_retained_earnings_deficit":ticker["results"][i]["accumulatedRetainedEarningsDeficit"]
                            ,"revenues":ticker["results"][i]["revenues"]
                            ,"revenues_usd":ticker["results"][i][ "revenuesUSD"]
                            ,"research_and_development_expense":ticker["results"][i]["researchAndDevelopmentExpense"]
                            ,"return_on_sales":ticker["results"][i]["returnOnSales"]
                            ,"share_based_compensation":ticker["results"][i]["shareBasedCompensation"]
                            ,"selling_general_and_administrative_expense":ticker["results"][i]["sellingGeneralAndAdministrativeExpense"]
                            ,"share_factor":ticker["results"][i]["shareFactor"]
                            ,"shares":ticker["results"][i]["shares"]
                            ,"weighted_average_shares":ticker["results"][i]["weightedAverageShares"]
                            ,"sales_per_share":ticker["results"][i]["salesPerShare"]
                            ,"tangible_asset_value":ticker["results"][i]["tangibleAssetValue"]
                            ,"tax_assets":ticker["results"][i]["taxAssets"]
                            ,"income_tax_expense":ticker["results"][i]["incomeTaxExpense"]
                            ,"tax_liabilities":ticker["results"][i]["taxLiabilities"]
                            ,"tangible_assets_book_value_per_share":ticker["results"][i]["tangibleAssetsBookValuePerShare"]
                            ,"working_capital":ticker["results"][i]["workingCapital"]
                        }
                countTickerId += 1

    def execute(self,stock_financials_crawler):
        
        counter = 0
        firstUrl = "https://api.polygon.io/v3/reference/tickers?active=true&sort=ticker&order=asc&limit=1000&apiKey=fXeNsEuF5_RYIgNgFae7LsdpGSz_jAxn"
        ticker_request = stock_financials_crawler._go_tickers(firstUrl)
        tickers_result = stock_financials_crawler._get_tickers(ticker_request)
        tickers = tickers_result["results"]

        for ticker in tickers: # remplissage du ticker dict pour la premiere page avec les ticker names à reutiliser pour stocks fianancials  
            print(counter)
            ticker_dict = {}
            print(ticker.get('ticker'))
            ticker_dict.update(tickerName=ticker.get('ticker'))
            self.final_stock_financials_tickers_list.append(ticker_dict)
            counter+=1
            """ if counter == 2:
                break """

        next_url = tickers_result["next_url"]
        #print(next_url) #OK verification de l'url pour voir si ma requete est fonctionnelle ou pas

        if requests.get(next_url).status_code == 200:

            ticker_next_request = stock_financials_crawler._go_tickers(next_url)
            tickers_next = stock_financials_crawler._get_next_cursor(ticker_next_request)

            if tickers_next != None:
                _has_next_page = True
                print("Ticker is different of 'None'")
                for ticker in tickers_next: # première boucle for pour l'initialisation du premier next_url
                        print(counter)
                        ticker_dict = {}
                        print(tickers_next)
                        ticker_dict.update(tickerName=tickers_next.get('ticker'))
                        self.final_stock_financials_tickers_list.append(ticker_dict)
                        counter+=1
            else:
                _has_next_page = False
                print("Ticker is equal to 'None'")

            counter = 3 # pour connaitre le nombre de page prise

            while _has_next_page == True:
                print("I am in "+str(counter)+"next_url")
                tickers_next = stock_financials_crawler._get_next_cursor(ticker_next_request)
                for ticker in tickers_next: 
                    print(counter)
                    print(ticker)
                    ticker_dict.update(tickerName=tickers_next.get('ticker'))
                    self.final_stock_financials_tickers_list.append(ticker_dict)
                    counter+=1
                next_url = tickers_result["next_url"]
                ticker_next_request = requests.get(next_url)
        else:
            pass    

        for company in self.final_stock_financials_tickers_list:
            stockFinancialsRequest = stock_financials_crawler._go_stock_financials_details(company["tickerName"])
            """ DEBUGGER
            print(stockFinancialsRequest.text)
            print("#######################")
            print(requests.get("https://api.polygon.io/v2/reference/financials/A?limit=3&type=T&apiKey=fXeNsEuF5_RYIgNgFae7LsdpGSz_jAxn").text) """
            dictstockFinancials = stock_financials_crawler._get_stock_financials_details(stockFinancialsRequest)
            print(dictstockFinancials)
            self.final_stock_financials_dict_list.append(dictstockFinancials)
            print("in the loop:"+str(len(self.final_stock_financials_dict_list))) # TAILLE DE LIST = 1000

        print("after the loop"+str(len(self.final_stock_financials_dict_list))) # TAILLE DE LIST = 1000
        final_stock_financials_dict_list = self.final_stock_financials_dict_list
        stock_financials_crawler._import_features_into_csv(final_stock_financials_dict_list)

def main():
        stock_financials_crawler = StockFinancialsCrawler()
        stock_financials_crawler.execute(stock_financials_crawler)

if __name__ == "__main__":
    main()


