import requests
import json
import pytz
from datetime import datetime
import re

### Time format convert for non-standard format, e.g. ISO8601, use regex to extract standard time info from a non-standard time format, 
### then fill date and hour info into two variables from two regex group, finally return data according to whether it needs to be extracted or not.
def time_format(timestamp, extract=None):
	re_pattern = r"(\d{4}[-]\d{2}[-]\d{2}).*(\d{2}[:]\d{2}[:]\d{2}).*"
	re_matched_results = re.match(re_pattern, timestamp)
	re_group_year = re_matched_results.group(1)
	re_group_month = re_matched_results.group(2)
	while extract:
		return(re_group_year, re_group_month)
	else:
		re_extracted_timestamp = '{} {}.000000'.format(re_group_year, re_group_month)
		return(re_extracted_timestamp)

## Convert Timezone from UTC to Shanghai
def tzconvert(timestamp):
	old_timezone = pytz.timezone("UTC")
	new_timezone = pytz.timezone("Asia/Shanghai")
	localized_timestamp = old_timezone.localize(timestamp)
	new_timezone_timestamp = localized_timestamp.astimezone(new_timezone)
	return(new_timezone_timestamp)

### API RELATED INFORMATION
API_KEY = '{{YOUR AIRVISUAL API KEY}}'
COUNTRY = 'China'
STATE = 'Shanghai'
CITY = 'Shanghai'
URL = 'https://api.airvisual.com/v2/city?city={}&state={}&country={}&key={}'.format(CITY, STATE, COUNTRY, API_KEY)

### Request AirVisual Data through its API
r = requests.get(URL)
url_text = r.text
converted_dict = json.loads(url_text)

### Current pollution conditions
pollution_ts = converted_dict["data"]["current"]["pollution"]["ts"]
pollution_aqius = converted_dict["data"]["current"]["pollution"]["aqius"]
pollution_mainus = converted_dict["data"]["current"]["pollution"]["mainus"]
pollution_aqicn = converted_dict["data"]["current"]["pollution"]["aqicn"]
pollution_maincn = converted_dict["data"]["current"]["pollution"]["maincn"]

### Current weather conditions
weather_ts = converted_dict["data"]["current"]["weather"]["ts"]
weather_tp = converted_dict["data"]["current"]["weather"]["tp"]
weather_pr = converted_dict["data"]["current"]["weather"]["pr"]
weather_hu = converted_dict["data"]["current"]["weather"]["hu"]
weather_ws = converted_dict["data"]["current"]["weather"]["ws"]
weather_wd = converted_dict["data"]["current"]["weather"]["wd"]

# Convert ISO8601 format to Standard UTC
pollution_datetime_object = datetime.strptime(time_format(pollution_ts), '%Y-%m-%d %H:%M:%S.%f')
weather_datetime_object = datetime.strptime(time_format(weather_ts), '%Y-%m-%d %H:%M:%S.%f')

### Date information compare
pollution_date = time_format(str(tzconvert(pollution_datetime_object)), 1)[0]
pollution_hours = time_format(str(tzconvert(pollution_datetime_object)), 1)[1]
weather_date = time_format(str(tzconvert(weather_datetime_object)), 1)[0]
weather_hours = time_format(str(tzconvert(weather_datetime_object)), 1)[1]

## Output information retrieved from AirVisual API
print("({}) Last weather info update: {} {}, Temperature: {}°C, Humidity: {}%, Wind speed: {}m/s, Wind direction: {}°, Atmospheric pressure: {}hPa.".format(CITY, weather_date, weather_hours, weather_tp, weather_hu, weather_ws, weather_wd, weather_pr))
print("({}) Last pollution info update: {} {}, AQI US: {} with main pollutant: {}, AQI CN: {} with main pollution: {}.".format(CITY, pollution_date, pollution_hours, pollution_aqius, pollution_mainus, pollution_aqicn, pollution_maincn))
