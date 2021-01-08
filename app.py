from flask import Flask, request, render_template
import requests
import geocoder
from geopy import geocoders
import random
import logging
import pickle
import pandas as pd
import math
from collections import namedtuple, OrderedDict
import collections
import requests, json
import os
from dotenv import load_dotenv
from flask import redirect, url_for

api_key = 'AIzaSyC3FjZU8SGXBVUj5p4mymMcvFcpNr_hyec'

#python is great

app = Flask(__name__)

app.config["DEBUG"] = True


@app.route('/')
def my_form():
    return render_template('index.html')
 

@app.route('/results', methods=['POST'])
def my_form_post():
    latlong_df = pd.read_csv("./updatedlatlong.csv")

    lists = []
    # if request.form["address-1"] != null:
    if request.form['address-1']:
        text1 = request.form['address-1']
        lists.append(text1)
    if request.form['address-2']:
        text2 = request.form['address-2']
        lists.append(text2)
    if request.form['address-3']:
        text3 = request.form['address-3']
        lists.append(text3)
    if request.form['address-4']:
        text4 = request.form['address-4']
        lists.append(text4)
    if request.form['address-5']:
        text5 = request.form['address-5']
        lists.append(text5)
    
    
    coordinates_list = [] # list of their addresses 

    for i in lists:
        g = geocoders.GoogleV3(api_key)
        place, (latitude, longitude) = g.geocode(i)
        print(place)
        print(latitude)
        print(longitude)

        coordinates_list.append([latitude, longitude])
    print(coordinates_list)

    average = [sum(x)/len(x) for x in zip(*coordinates_list)]    
    print(average)

    km = pickle.load(open("save.pkl", "rb"))


    # coordinates 
    distance_dictionary = OrderedDict() # coordinates of centroid, distance from centroid to the middle 

    cluster_dictionary = {} #coordinates of centroid, centroid number

    Coordinates = namedtuple("Coordinates", ["latitude", "longitude"])
    counter = 0
    for x, y in km.cluster_centers_:
        comparison = math.sqrt((average[0] - x)**2 + (average[1] - y)**2)
        distance_dictionary[Coordinates(x, y)] = comparison
        cluster_dictionary[Coordinates(x, y)] = km.labels_[counter]
        counter += 1

    print(distance_dictionary)
    top_4_dictionaries = collections.Counter(distance_dictionary).most_common()[:-5:-1]


    top_4_dictionaries = dict(top_4_dictionaries)
    print(top_4_dictionaries)

    google_url ='https://maps.googleapis.com/maps/api/distancematrix/json?'
    minimum = 100000000000000000000000000
    import googlemaps
    reference = 0



    for key, value in top_4_dictionaries.items():
        sums = 0
        for j in coordinates_list:
            print(key.latitude)
            print(key.longitude)
            print(value)

        

            gmaps = googlemaps.Client(key = api_key)
            origins = []
            destinations = []

            origins.append(str(key.latitude) + ' ' + str(key.longitude))
            destinations.append(str(j[0]) + ' ' + str(j[1]))

            matrix = gmaps.distance_matrix(origins, destinations, mode = "transit")
            print(matrix)

            sums += matrix['rows'][0]['elements'][0]['distance']['value']

        if (minimum > sums):
            print(minimum)
            minimum = sums
            reference = Coordinates(key.latitude, key.longitude)

    print(cluster_dictionary[reference])
        
    return render_template("results.html")

    # filtered_df = latlong_df.loc[latlong_df['Clusters'] == centroid[0]]
    # print(filtered_df.head())
    # print(centroid)



    # print(centroid)

    # a = geocoder.google(text1)
    # a = a.latlng
    # b = geocoder.google(text2)
    # b = b.latlng
    # c = geocoder.google(text3)
    # c = c.latlng
    # d = geocoder.google(text4)
    # d = d.latlng
    # lists = []
    
    # lists.append(a)
    # lists.append(b)
    # lists.append(c)
    # lists.append(d)
    # return lists[0]

    # request_address = '%(text1)s , IN' % {'text1':text1}

    # https://maps.googleapis.com/maps/api/geocode/json?address=text1
    # processed_text = text.upper()
    # alert("HIIHI")
    # return request_address

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

    