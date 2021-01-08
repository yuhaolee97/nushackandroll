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
import numpy
import pandas
import plotly.graph_objs as go
import json

api_key = 'AIzaSyC3FjZU8SGXBVUj5p4mymMcvFcpNr_hyec'


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

    centroid = cluster_dictionary[reference]
    filename = "./images"

    filtered_df = latlong_df.loc[latlong_df['Clusters'] == centroid]
    # print(filtered_df.head())

    filename_lists = []
    map_titles = []
    restaurant_lists = []
    address_lists = []
    cusine_lists = []
    crowdlevel_lists = []

    counter = 0
    for row, col in filtered_df.iterrows():
        photo_reference = filtered_df['Photo_reference'][row]

        print(photo_reference)
        print(type(photo_reference))

        gmaps = googlemaps.Client(key = api_key)

        raw_image_data = gmaps.places_photo(photo_reference = photo_reference, max_width = 1600) #400 - 1600 (max)
        
        imgfile = open('./static/images/myImage' + str(counter) + '.jpg', 'wb')

        for chunk in raw_image_data:
            if chunk:
                imgfile.write(chunk)
        imgfile.close()
        filename_lists.append('images/myImage' + str(counter) + '.jpg')

        restaurant_lists.append(filtered_df['Restaurant'][row])
        address_lists.append(filtered_df['Address'][row])
        map_titles.append(filtered_df['Google_map_link'][row])
        cusine_lists.append(filtered_df['Cusines'][row])

        url = "https://besttime.app/api/v1/forecasts"

        params = {
            'api_key_private': 'pri_db35aee5b0a14d168d2c32a2f2e8891d',
            'venue_name': filtered_df['Restaurant'][row],
            'venue_address': filtered_df['Address'][row]
        }

        response = requests.request("POST", url, params=params)

        data = json.loads(response.text)


        hours = ["6AM","7AM","8AM", "9AM","10AM","11AM", "12PM","1PM","2PM", "3PM","4PM","5PM", "6PM","7PM","8PM","9PM","10PM","11PM", "12AM"]
        percent_fullness = data['analysis'][5]['day_raw'][:-5]
        print(percent_fullness)
        plotdata = [go.Bar(x = hours, y = percent_fullness)]
        fig = go.Figure(data=plotdata)
        fig.update_yaxes(range=[0, 100], color='lightgrey', showgrid=False)
        fig.update_layout(
            autosize=False,
            width=800,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        fig.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = ["9AM", "12PM", "3PM","6PM","9PM", "12AM"], showgrid=False, color='lightgrey'
            )
        )
        # fig.show()
        fig.write_image("./static/images/crowdlevel" + str(counter) + ".png")
        crowdlevel_lists.append('images/crowdlevel' + str(counter) + ".png")
        counter += 1

        if (counter == 2):
            break
    length = counter

        
    return render_template("results.html", centroid = centroid, filename = filename_lists, restaurant_lists = restaurant_lists, address_lists = address_lists, map_titles = map_titles, 
                        cusine_lists = cusine_lists, length = length, crowdlevel_lists = crowdlevel_lists)




    # request_address = '%(text1)s , IN' % {'text1':text1}

    # https://maps.googleapis.com/maps/api/geocode/json?address=text1
    # processed_text = text.upper()
    # return request_address

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

    