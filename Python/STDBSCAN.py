import math
from datetime import timedelta
from geopy.distance import great_circle
"""
INPUTS:
    df={o1,o2,...,on} Set of objects
    spatial_threshold = Maximum geographical coordinate (spatial) distance value
    temporal_threshold = Maximum non-spatial distance value
    min_neighbors = Minimun number of points within Eps1 and Eps2 distance
OUTPUT:
    C = {c1,c2,...,ck} Set of clusters
"""
def ST_DBSCAN(df, spatial_threshold, temporal_threshold, min_neighbors):
    cluster_label = 0
    NOISE = -999999
    UNMARKED = 777777
    stack = []

    logging = len(df)

    # initialize each point with unmarked
    df['cluster'] = UNMARKED

    print "Size: %d" % (len(df))
    # for each point in database
    for index, point in df.iterrows():
        #print point
        if df.loc[index]['cluster'] == UNMARKED:
            neighborhood = retrieve_neighbors(index, df, spatial_threshold, temporal_threshold)
            #print "neighborhood %d" %len(neighborhood)

            if len(neighborhood) < min_neighbors:
                df.set_value(index, 'cluster', NOISE)
                logging-=1
                print logging

            else: # found a core point
                cluster_label = cluster_label + 1
                df.set_value(index, 'cluster', cluster_label)# assign a label to core point
                logging-=1
                print logging

                for neig_index in neighborhood: # assign core's label to its neighborhood
                    df.set_value(neig_index, 'cluster', cluster_label)
                    stack.append(neig_index) # append neighborhood to stack
                    logging-=1
                    print logging

                while len(stack) > 0: # find new neighbors from core point neighborhood
                    current_point_index = stack.pop()
                    new_neighborhood = retrieve_neighbors(current_point_index, df, spatial_threshold, temporal_threshold)

                    if len(new_neighborhood) >= min_neighbors: # current_point is a new core
                        for neig_index in new_neighborhood:
                            neig_cluster = df.loc[neig_index]['cluster']
                            if (neig_cluster != NOISE) & (neig_cluster == UNMARKED):
                                # TODO: verify cluster average before add new point
                                df.set_value(neig_index, 'cluster', cluster_label)
                                logging-=1
                                print logging
                                stack.append(neig_index)


    return df


def retrieve_neighbors(index_center, df, spatial_threshold, temporal_threshold): #lista de indices vizinhos
    neigborhood = []

    center_point = df.loc[index_center]

    # filter by time
    min_time = center_point['DATATIME'] - timedelta(minutes = temporal_threshold)
    max_time = center_point['DATATIME'] + timedelta(minutes = temporal_threshold)
    df = df[(df['DATATIME'] >= min_time) & (df['DATATIME'] <= max_time)]
    #print "{} {} {} ".format(min_time, center_point['date_time'], max_time)

    # filter by distance
    for index, point in df.iterrows():
        if index != index_center:
            distance = great_circle((center_point['LATITUDE'], center_point['LONGITUDE']), (point['LATITUDE'], point['LONGITUDE'])).meters
            if distance <= spatial_threshold:
                neigborhood.append(index)

    return neigborhood
