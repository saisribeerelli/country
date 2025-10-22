from django.shortcuts import render
import requests

# Create your views here.
def index(request):
    form = True
    data = ""
    l = []
    if request.method == "POST":
        country = request.POST.get('country')
        print(country)
        form = False
        data = requests.get(f"https://restcountries.com/v3.1/name/{country}").json()
        # print(data)
        # main_l = []
        for i in data:
            d = {}
            d.setdefault("name",i['name']['common'])
            d.setdefault("official", i['translations'].get('hin', {}).get('official', i['name']['official']))
            d.setdefault("code", i['cca3'])
            d.setdefault("independent", i.get('independent', 'Unknown'))
            d.setdefault("currency", ", ".join([v['name'] for v in i.get('currencies', {}).values()]) if i.get('currencies') else "Not available")
            d.setdefault("calling_code", "+{}".format(i['idd']['root'].replace("+", "") + i['idd']['suffixes'][0]) if i.get('idd') else "Not available")
            d.setdefault("capital", i.get('capital', ['Unknown'])[0])
            d.setdefault("alt_spellings", ", ".join(i.get('altSpellings', [])))
            d.setdefault("region", i.get('region', 'Unknown'))
            d.setdefault("subregion", i.get('subregion', 'Unknown'))
            d.setdefault("languages", ", ".join(i.get('languages', {}).values()))
            d.setdefault("latlng", f"{i['latlng'][0]}, {i['latlng'][1]}")
            d.setdefault("borders", ", ".join(i.get('borders', [])) if i.get('borders') else "No borders")
            d.setdefault("area", i.get('area', 'Unknown'))
            d.setdefault("flag", i['flags']['png'])
            d.setdefault("coat_of_arms", i.get('coatOfArms', {}).get('png', ''))
            d.setdefault("map", i['maps']['googleMaps'])
            d.setdefault("population", i.get('population', 'Unknown'))
            d.setdefault("timezone", ", ".join(i.get('timezones', [])))
            if i.get('timezones'):
                try:
                    tz = pytz.timezone(i['timezones'][0])
                    d["current_time"] = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
                except:
                    d["current_time"] = "Unavailable"
            else:
                d["current_time"] = "Unavailable"

            d.setdefault("continent", ", ".join(i.get('continents', [])))
            d.setdefault("start_of_week", i.get('startOfWeek', 'Unknown'))

            # d.setdefault("maps",i['maps']['googleMaps'])
            # d.setdefault("flag",i['flags']['png'])
            # d.setdefault("alt",i['altSpellings'])
            # d.setdefault("cap",i['capital'])


            l.append(d)
        print(l)
    context = {
        'data':data,
        'form':form,
        'l':l
    }
    return render(request,'index.html',context)

