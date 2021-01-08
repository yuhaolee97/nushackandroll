import googlemaps

api_key = 'AIzaSyC3FjZU8SGXBVUj5p4mymMcvFcpNr_hyec'

gmaps = googlemaps.Client(key = api_key)

photo_reference = "ATtYBwJHh94FHtVM4LbQJGbvjofLbQyHTVIpZfRlsr9C4diDkc_EGrAQtO_bhDw4psxjyXh2cmtS192MkMzMMui-9sF4jdVIvxTvxoqteqsUdGxvqrZArb2cBEBO-4SPK9Y_AmJj-Ox6hBxpdK5-sMxHe57zy6k-8IGqsD7_SGWLT8_IKT5J"
maxwidth = 1600

raw_image_data = gmaps.places_photo(photo_reference = photo_reference, max_width = maxwidth) #400 - 1600 (max)
 
imgfile = open('hi.jpg', 'wb')

for chunk in raw_image_data:
    if chunk:
        imgfile.write(chunk)
imgfile.close()