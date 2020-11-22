import os

print("Completely Random:")
for i in range(100):
	os.system('python3 NoGeneticGeoGame.py -g')

print("Genetic Algorithm:")
for i in range(100):
	os.system('python3 GeoGame.py -g')