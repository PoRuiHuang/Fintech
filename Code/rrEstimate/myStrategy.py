def myStrategy(pastPriceVec, currentPrice, stockType):
	# Explanation of my approach:
	# 1. Technical indicator used: MACD
	# 2. if OSC > alpha/20 且柱狀趨勢在0以上變長 ==> buy
	#    if OSC < beta/20 且柱狀趨勢在0以下變長 ==> sell
	# 3. Modifiable parameters: EMAshort, EMAlong, alpha, beta, gamma for MACD
	# 4. Use exhaustive search to obtain these parameter values (as shown in bestParamByExhaustiveSearch.py)
	
	import numpy as np
	# stockType='SPY', 'IAU', 'LQD', 'DSI'
	# Set parameters for different stocks
	paramSetting={	'SPY': {'EMAshort':17,'EMAlong':26,'alpha':4, 'beta':-23, 'gamma':15},
					'IAU': {'EMAshort':10,'EMAlong':29,'alpha':4, 'beta':-2 , 'gamma':7},
					'LQD': {'EMAshort':8,'EMAlong':31,'alpha':10, 'beta':-14, 'gamma':12},
					'DSI': {'EMAshort':13,'EMAlong':23,'alpha':5, 'beta':-27, 'gamma':15},}

	EMAshort = paramSetting[stockType]['EMAshort']
	EMAlong = paramSetting[stockType]['EMAlong']
	alpha = paramSetting[stockType]['alpha']
	beta = paramSetting[stockType]['beta']
	gamma = paramSetting[stockType]['gamma']

	action=0		# action=1(buy), -1(sell), 0(hold), with 0 as the default action
	dataLen=len(pastPriceVec)		# Length of the data vector
	global EMAS
	global EMAL
	global MACD
	global Temp
	global DIF
	DIF = []
	if dataLen<EMAshort:
		return action;
	elif dataLen==EMAshort:
		EMAS = np.mean(pastPriceVec)
		return action;
	else:
		EMAS = (1-(2/(1+EMAshort)))*EMAS + (2/(1+EMAshort))*pastPriceVec[-1]


	if dataLen<EMAlong:
		return action;

	elif dataLen==EMAlong:
		EMAL = np.mean(pastPriceVec)
		return action;
	else:
		EMAL = (1-(2/(1+EMAlong)))*EMAL + (2/(1+EMAlong))*pastPriceVec[-1]

	count = dataLen - EMAlong

	if count >=0 and count <gamma -1 :
		DIF.append(EMAS - EMAL)
		return action;
	elif count ==gamma -1:
		DIF.append(EMAS - EMAL)
		MACD = np.mean(DIF)	
	else: 
		DIF.append(EMAS - EMAL)
		MACD = MACD*(1-2/(gamma+1)) + DIF[-1]*2/(gamma+1)

	OSC =  DIF[-1] - MACD

	#上面為MACD的基本操作
	#下面為篩選買賣條件；調整alpha及beta來決定買賣基準
	if OSC > alpha/20:		
		if Temp -OSC >0:
			action=1
		else:
			action=-1
	elif OSC < beta/20:	
		if Temp -OSC >0:
			action=1
		else:
			action=-1
	else:
		action = 0
	Temp = OSC
	return action
