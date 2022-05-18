# https://googlemaps.github.io/google-maps-services-python/docs/
# https://developers.google.com/maps/documentation/places/web-service/search-nearby#maps_http_places_nearbysearch-py
import googlemaps

output = open("api.txt", "w")

key_word = input("Please input the keyword you want to search.")
API_KEY = "AIzaSyCI17Ct--r9YoWoZri3xciKl74D3u0jfeM"

gmaps = googlemaps.Client(key=API_KEY)
geocode_result = gmaps.geocode("花蓮縣壽豐鄉大學路二段1號")
# print(geocode_result)
loc = geocode_result[0]["geometry"]["location"]
places = gmaps.places_nearby(keyword=key_word, location=loc, radius=2500)
print(places, file=output)
print("總共有", len(places["results"]), "個地點", sep="")

index = 0
while index < len(places["results"]):
    print(places["results"][index]["name"], file=output)
    print("評價:", places["results"][index]["rating"], sep="", file=output)
    print("地址:", places["results"][index]["vicinity"], sep="", file=output)
    print("絕對位置:", places["results"][index]["geometry"]
          ["location"], sep="", file=output)
    print("", file=output)
    index += 1
