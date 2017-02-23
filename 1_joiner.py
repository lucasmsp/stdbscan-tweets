# coding=UTF-8
#!/usr/bin/python

fileresult = "Python/result_marco_d500_t60_n5.csv"
fileData = "Dataset/traffic_geo_marco_curitiba_filter.txt"
fileoutput = "output"

f = open(fileresult,"r")
cluster = {}
for line in f:
	fields = line.split("\t")
	c = int(fields[4])
	if c > 0:
		cluster[fields[0]]= c
f.close()

f  = open(fileData,"r")
f1 = open(fileoutput,"w")

for line in f:
	fields = line.split(",")
	if fields[0] in cluster:
		f1.write(str(cluster[fields[0]])+","+line)


f.close()
f1.close()
