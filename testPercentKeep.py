import os

for currentPercent in range(0,50,5):
	list = []
	for i in range(25):
		output = os.popen('python3 GeoGame.py -g -pk '+str(float(currentPercent+.001)/100)).read()
		num = -1
		try:
			num=int(output)
		except ValueError:
			pass
		if num!= -1:
			list += [num]
	list.sort()
	print(currentPercent,": ",list[int(len(list)/2)])