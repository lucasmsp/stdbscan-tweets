# coding=UTF-8
#!/usr/bin/python

from datetime import datetime
import pandas as pd
import numpy as np
import re
import time
from STDBSCAN import *
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def parser_Tweet(line):
    #"id_tweet,timestamp,geo,tweet"
    fields = line.split(",")
    ID_TWEET = str(fields[0])
    DATATIME = datetime.strptime(fields[1], '%Y-%m-%d %H:%M:%S')
    lat_long=fields[2].split(" ")
    LATITUDE=float(lat_long[0])
    LONGITUDE=float(lat_long[1])

    return [ID_TWEET,DATATIME,LATITUDE,LONGITUDE]

def main():

    filename= "../Dataset/traffic_geo_marco_curitiba_filter.txt"

    df = pd.DataFrame([], columns=["ID_TWEET","DATATIME","LATITUDE","LONGITUDE"])

    for line in open(filename,"r"):
        df2 = pd.DataFrame([parser_Tweet(line)], columns=["ID_TWEET","DATATIME","LATITUDE","LONGITUDE"])
        df = df.append(df2, ignore_index=True)

    print df.head(5)

    spatial_threshold =  500   # em metros
    temporal_threshold = 60    # em minutos
    min_neighbors=5

    result_df = ST_DBSCAN(df, spatial_threshold, temporal_threshold, min_neighbors)
    print "Result - %d:" % len(result_df)

    output = "result_marco_d{0}_t{1}_n{2}.csv".format(spatial_threshold,temporal_threshold,min_neighbors)
    result_df.to_csv(output,sep='\t')


if __name__ == "__main__":
    sys.stdout = open('log.txt', 'w', 0)

    start = time.time()
    main()
    end = time.time()

    print "Time elapsed: %.2f secs" % ( end - start)
