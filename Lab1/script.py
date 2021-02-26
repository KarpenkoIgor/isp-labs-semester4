from datetime import datetime
import pytz
  
city_list = ['Europe/Minsk', 'Asia/Tokyo', 'Europe/Berlin','Australia/Sydney', 'America/New_York', 'America/Buenos_Aires']
for  city in city_list:
    city_name = city.split('/')
    city_name[-1] = city_name[-1].replace('_',' ')
    print(f"Time in {city_name[-1]} :", datetime.now(pytz.timezone(city)).strftime("%a %H:%M:%S"))