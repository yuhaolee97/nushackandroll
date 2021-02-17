# Project Title
Meet & Eat

NUS Hack and Roll 2021 Submission: Done collaboratively with Aw Khai Loong and Richard Ng.

## Motivation
We have on many occasions faced difficulty in settling on a fair location for a group meetup given that we reside in different parts of Singapore. This often leads to some members of the group having travel times much longer than necessary. In the context of fighting COVID-19, there is also newfound importance in practicing social distancing when eating out. We were unable to find any web service that takes in multiple starting addresses and returns the optimal restaurants based on travel time and crowd avoidance, so we decided to create one!

Meet & Eat takes in multiple starting addresses and intelligently determines the most optimal restaurants for a group meetup based on travel time and crowd level/cuisine preferences.

## Tech/framework used
We used an extensive technology stack to develop the Meet & Eat webservice. Python/Flask was the ideal language for the backend given that our project dealt a lot with data. We made good use of python’s extensive libraries such as scikitlearn for machine learning, BeautifulSoup for web scraping and plotly for visualization. We also used different APIs and datasets in tandem to collect meaningful data. For instance, we retrieved restaurant details such as the geographic coordinates and photo by parsing the restaurant names that we scraped from the web to the Google Maps Place Details API. These details were then parsed into the Best Time API to retrieve forecasted crowd levels. The frontend portion of the project was constructed using HTML, CSS and Javascript.

## Features
With the inputted addresses, Meet & Eat will first find the geographic midpoint by converting the addresses to latitude longitude coordinates through the Google Maps Geocoding API. However, this midpoint could end up in an unpractical location such as within a reservoir or in a place devoid of restaurants.

To meaningfully overcome this issue, we needed a creative solution involving a lot of data and converting it into something useful. We scraped for over 1300 restaurants in Singapore and their cuisines. This data was expanded to include the restaurants’ address, the main photo, and geographic coordinates through the Google Maps Details API. The sizable number of restaurants coordinates were used as the unlabeled dataset for unsupervised machine learning to generate 50 clusters of restaurants using k-means clustering. Each cluster is a meaningful vicinity for users to explore for good restaurants. Meet & Eat then finds the closest 4 centroids of restaurants to the users’ geographic midpoint.

However, the most geographically central location does not account for public transport infrastructure and travel time. This is why we narrowed down to 4 of the closest centroids to then calculate the sum of travel times from the users’ addresses to each centroid, using the Google Maps Distance Matrix API. The centroid with the smallest travel time sum is selected. Users will then be presented with the list of restaurants from that centroid and provided with meaningful information such as the restaurant’s crowd level throughout the day. This is particularly useful in the context of COVID-19, allowing users to pick from uncrowded restaurants and timings to better practice safe social distancing. Users are also provided with numerical and graphic statistics of the search, the restaurants’ cuisines and picture, and a link to the restaurant’s google maps search result.

## Possible Improvements
Extend Meet & Eat onto different platforms such as dedicated iOS/Android applications or as a Telegram/Discord bot, as well as deploy Meet & Eat onto a dedicated server.

## License
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

MIT © Lee Yu Hao, Aw Khai Loong, Richard Ng