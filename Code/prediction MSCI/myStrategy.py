import numpy as np
def myStrategy(dailyOhlcvFile, minutelyOhlcvFile, openPrice):
	global EMAS
	global EMAL
	global DIF
	global MACD
	global OSC_y
	global OSC_t
	global comp
	Eshort = 12
	Elong  = 130
	MA_day = 9
	EMAS   = 0
	EMAL   = 0
	DIF    = 0
	MACD   = 0
	OSC_t  = 0
	OSC_y  = 0
	comp   = 0
	for i in range(Eshort): #12 -> 0~11
		EMAS = EMAS + (dailyOhlcvFile['high'][i] + dailyOhlcvFile['low'][i] + 2*dailyOhlcvFile['close'][i])/4
    #     total = total + dailyOhlcvFile['close'][i]
	EMAS = EMAS/Eshort
	# print(EMAS)
	for i  in range(Eshort,Elong):#14 -> 12~25
		EMAS = (1-2/(1+Eshort))*EMAS + 2/(1+Eshort)*(dailyOhlcvFile['high'][i] + dailyOhlcvFile['low'][i] + 2*dailyOhlcvFile['close'][i])/4

	# for i  in range(Eshort+1,len(dailyOhlcvFile['close'])):
	# 	EMAS = (1-2/(1+Eshort))*EMAS + 2/(1+Eshort)*(dailyOhlcvFile['high'][i-1] + dailyOhlcvFile['low'][i-1] + 2*dailyOhlcvFile['close'][i-1])/4
	# print('EMAS: ',EMAS)

	for i in range(Elong):#26 -> 0~25
		EMAL = EMAL + (dailyOhlcvFile['high'][i] + dailyOhlcvFile['low'][i] + 2*dailyOhlcvFile['close'][i])/4
    #     total = total + dailyOhlcvFile['close'][i]
	EMAL = EMAL/Elong
	# print(EMAL)
	DIF = EMAS-EMAL
	# print(DIF)

	for i  in range(Elong,Elong+MA_day-1): #8 -> 26~33
		EMAS = (1-2/(1+Eshort))*EMAS + 2/(1+Eshort)*(dailyOhlcvFile['high'][i] + dailyOhlcvFile['low'][i] + 2*dailyOhlcvFile['close'][i])/4
		EMAL = (1-2/(1+Elong))*EMAL + 2/(1+Elong)*(dailyOhlcvFile['high'][i] + dailyOhlcvFile['low'][i] + 2*dailyOhlcvFile['close'][i])/4
		DIF = DIF + (EMAS-EMAL)

	MACD = DIF/MA_day
	# print(MACD)

	for i  in range(Elong+ MA_day-1,len(dailyOhlcvFile['close'])-1):
		EMAS = (1-2/(1+Eshort))*EMAS + 2/(1+Eshort)*(dailyOhlcvFile['high'][i] + dailyOhlcvFile['low'][i] + 2*dailyOhlcvFile['close'][i])/4
		EMAL = (1-2/(1+Elong))*EMAL + 2/(1+Elong)*(dailyOhlcvFile['high'][i] + dailyOhlcvFile['low'][i] + 2*dailyOhlcvFile['close'][i])/4
		DIF = EMAS-EMAL
		MACD = (MA_day-1)/(MA_day+1)*MACD + (1-(MA_day-1)/(MA_day+1))*DIF
	OSC_y = DIF - MACD
	# print(DIF)
	# print(MACD)

	# print(OSC_y)

	for i  in range(len(dailyOhlcvFile['close'])-1,len(dailyOhlcvFile['close'])):
		EMAS = (1-2/(1+Eshort))*EMAS + 2/(1+Eshort)*(dailyOhlcvFile['high'][i] + dailyOhlcvFile['low'][i] + 2*dailyOhlcvFile['close'][i])/4
		EMAL = (1-2/(1+Elong))*EMAL + 2/(1+Elong)*(dailyOhlcvFile['high'][i] + dailyOhlcvFile['low'][i] + 2*dailyOhlcvFile['close'][i])/4
		DIF = EMAS-EMAL
		MACD = (MA_day-1)/(MA_day+1)*MACD + (1-(MA_day-1)/(MA_day+1))*DIF
	OSC_t = DIF - MACD
	# print(OSC_t)

	comp = OSC_t-OSC_y
	# print(DIF)
	# print(MACD)
	# print("OSC: ", OSC_t)
	# print("comparison: ",comp)
	if OSC_t > 0:
		if OSC_y < 0:
			return 1
		elif OSC_y > 0:
			if comp > 15:
				# print("OSC_t-OSC_y: ",comp)
				# print("b")
				return -1#1=0<-1
			else:
				# print("c")
				return 0#1<0=-1
		else:
			# print("d")
			return 0#nothing
	elif OSC_t < 0:
		if OSC_y > 0:
			# print("e")
			return -1#-1
		elif OSC_y < 0:
			if comp > 0:
				if comp >6:
					# print("OSC_y: ", OSC_y)
					# print("OSC_t-OSC_y: ",comp)
					# print("f")
					return 1#1
				else:
					return 0
			else:
				return 1
		else:
			# print("h")
			return 0#nothing
	else:
		return 0

	# return 1
	# print(EMAS-EMAL)