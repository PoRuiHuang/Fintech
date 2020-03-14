import numpy as np

def myOptimAction(priceMat, transFeeRate):
    # Explanation of my approach:
    # 1. Technical indicator used: DP
    '''
    Step 1: 因為我們知道全部天的價格，故最大化收益都是ALL SELL或ALL BUY
    Step 2: 每天確認完Cash的MAX後，確認是否要買其他股票。
    step 3: 最後由最後一天的Cash，透過DP去找尋應該買那一支股票最好，透過STEP2所跑的結果，便能找出最佳股票之選擇，進行全買或全賣

    '''
    # default
    cash = 1000
    daystrade = np.size(priceMat,0) # 日期天數
    stock_amount = np.size(priceMat,1) # 股票數  
    stockHolding = np.zeros(stock_amount)  # Mat of stock holdings
    actionMat = []  # An k-by-4 action matrix which holds k transaction records, each row of [d,a,b,z] represents a transaction record
    max_cash = np.zeros(daystrade) # 這裡數字有0~4，0 for保留前一天之cash，1-4為最適化之股票代號
    stock_sit = np.zeros((daystrade,stock_amount)) #1= 購入，0 = 保留
    sell_price = np.zeros((daystrade,stock_amount)) #未扣除transFeeRate之售價
    

    for day in range(daystrade) :
        dayPrices = priceMat[day]  #4支股票每天之價格
        
        if day == 0:#第一天需要初始化
            stockHolding = cash*(1-transFeeRate)/dayPrices
            for i in range(stock_amount):
                stock_sit[0][i] = 1
                sell_price[0][i] = cash
            continue
            
        #判斷cash    
        for stock in range(stock_amount) :# 四支股票的cash
            todayPrice = dayPrices[stock]  #紀錄今天價格
            
            cash_criterion = todayPrice * (1 - transFeeRate) * stockHolding[stock]
            if cash < cash_criterion:# 該賣出股票
                sell_price[day][stock] = cash_criterion/(1 - transFeeRate)
                cash = cash_criterion
                max_cash[day] = stock + 1
        
        #判斷stock
        for stock in range(stock_amount) :# 分別跑四支股票的stock
            todayPrice = dayPrices[stock]  #當天之價格
            
            #買入一檔股票之判斷
            stock_criterion = (cash*(1 - transFeeRate) / todayPrice)
            if stockHolding[stock] < stock_criterion:
                stockHolding[stock] = stock_criterion
                stock_sit[day,stock] = 1
                buy = False
                for i in range (stock_amount):
                    if sell_price[day][i] != 0:
                        buy = True
                        sell_price[day][stock] = sell_price[day][i]
                        break
                if buy == False: 
                    sell_price[day][stock] = cash
    
    #回推每天的交易
    buy_stock = False
    from_stock = 3
    for ic in range(daystrade - 1, -1, -1) :
        if buy_stock == True:
            if stock_sit[ic][from_stock - 1] == 1: #use cash to buy the stock
                buy_stock = False
                from_stock = int(from_stock)
                action = [ic, -1, from_stock - 1, sell_price[ic][from_stock-1]*100]  #因有誤差 故放大數據 反正是為了ALL IN的判斷
                actionMat.insert(0, action)
                
        if buy_stock == False:
            if max_cash[ic] != 0: #sell the stock for cash
                buy_stock = True
                from_stock = int(max_cash[ic])
                action = [ic, from_stock - 1, -1, sell_price[ic][from_stock-1]*100] #因有誤差 故放大數據 反正是為了ALL IN的判斷
                actionMat.insert(0, action)
    return actionMat
