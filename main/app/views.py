import json
from django.shortcuts import render
import requests

# Create your views here.
fin_List = []


def home(request):
    if request.method == 'POST':
        travel_With = request.POST['travellingWith']
        origin = request.POST['currentLocation']
        num_Days = request.POST['days']
        places_List = ['Mumbai', 'Jaisalmer', 'Kochi', 'Udaipur', 'Manali',
                       'Chennai', 'Kolkata', 'Bengaluru', 'Amritsar', 'Nainital', 'Goa']
        coords = []
        places_List.append(origin)
        for i in places_List:
            url1 = f"https://maps.googleapis.com/maps/api/geocode/json?address={i}&key=AIzaSyBc3tvk8dfja8r0ABh65c-14YZJula3wXs"
            json_Response = requests.post(url1).json()
            coords.append(json_Response['results']
                          [0]['geometry']['location']['lat'])
            coords.append(json_Response['results']
                          [0]['geometry']['location']['lng'])
        dist = []

        for i in range(0, len(coords)-3, 2):
            url2 = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={coords[-2]},{coords[-1]}&destinations={coords[i]},{coords[i+1]}&key=AIzaSyBc3tvk8dfja8r0ABh65c-14YZJula3wXs"
            json_Response = requests.post(url2).json()
            dist.append(json_Response['rows'][0]['elements'][0]['distance']['text'].split(
                ' ', 1)[0].replace(',', ''))
        for i in range(0, len(dist)):
            if int(num_Days) >= 10:
                if int(dist[i]) >= 1200:
                    fin_List.append(places_List[i])
            elif int(num_Days) >= 5:
                if int(dist[i]) >= 700 and int(dist[i]) < 1200:
                    fin_List.append(places_List[i])
            else:
                if int(dist[i]) >= 250 and int(dist[i]) < 700:
                    fin_List.append(places_List[i])

        dictt, l = {}, []
        for i in fin_List:
            l = query_api(i, travel_With)
            dictt[i] = l
            final1 = dictt
            print(dictt)

        return render(request, 'app/itinerary.html', {'cities': fin_List, 'final1': final1, 'days': num_Days})
    return render(request, 'app/index.html')


def about(request):
    return render(request, 'app/about.html')


def explore(request):
    return render(request, 'app/explore.html')


def itinerary(request):
    return render(request, 'app/itinerary.html')


final1 = {}
dict_per_place = {}

place = ''


def query_api(place, option):
    print(fin_List)
    places_list_name = []
    finale = []
    places_list_add = []
    url = 'https://api.foursquare.com/v2/venues/explore'
    count = 0
    i = 0

    cat = {
        "friends": ['4bf58dd8d48988d182941735', '4d4b7104d754a06370d81259'],
        "family": ['4bf58dd8d48988d181941735'],
        "kids": ['4bf58dd8d48988d131941735',  '52e81612bcbc57f1066b79e7', '52e81612bcbc57f1066b79ea'],
        "partner": ['4bf58dd8d48988d17f941735', '52e81612bcbc57f1066b79ec', '4d4b7105d754a06377d81259'],
        "senior": ['4bf58dd8d48988d131941735']
    }

    params = dict(
        client_id='HC2LQMRSPYBNYNW4SJZA1TPYEWVIEFOPXXPJXKKY2J0ALPIC',
        client_secret='RI0VEO3OAXJIE2JB40HND1KSUI1VU0DXZMW4RXFU4ZB2WNHU',
        near=place,  # Take from Google maps
        v="20180323",
        limit=5,
        radius="50000"
    )

    for i in range(0, 1):
        params['categoryId'] = cat[option]
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)

        # dict_per_place['query'] = data['meta']['venue']['name']
        # place = data['response']['groups']
       # dict_per_place['summary'] = data['venue']['name']
        # dict_per_place['formattedAddress'] = data['venue']['formattedAddress']
        # places_list.append(dict_per_place)
        # print(places_list)
        groups = data['response']['groups']
        main_data = groups[0]['items'][0]['venue']
        places_list_name.append(main_data['name'])
        # places_list_add.append(main_data['location']['address'])
        main_data = groups[0]['items'][1]['venue']
        places_list_name.append(main_data['name'])
        # places_list_add.append(main_data['location']['address'])
        main_data = groups[0]['items'][2]['venue']
        places_list_name.append(main_data['name'])
        # places_list_add.append(main_data['location']['address'])

        # print(main_data)
        # print(" seperate \n")
        # dict_per_place['query'] = main_data['name']
        # dict_per_place['formattedAddress'] = main_data['location']['formattedAddress']
        # places_list.append(dict_per_place)

    finale = places_list_name
    return finale
