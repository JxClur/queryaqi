import requests
import json
import pytz
from datetime import datetime
import re
import sys

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

### Retrive data from IQAir and format it with json module
def url_data_format(URL):
	payload={}
	files={}
	headers = {}
	r = requests.request("GET", URL, headers=headers, data=payload, files=files)
	return(json.loads(r.text))

### Main module aims to separate part of data and re-arrange, finally print and archive
def main(URL):
	data_receive = url_data_format(URL)
	pollution_ts = data_receive["data"]["current"]["pollution"]["ts"]
	pollution_aqius = data_receive["data"]["current"]["pollution"]["aqius"]
	pollution_mainus = data_receive["data"]["current"]["pollution"]["mainus"]
	pollution_aqicn = data_receive["data"]["current"]["pollution"]["aqicn"]
	pollution_maincn = data_receive["data"]["current"]["pollution"]["maincn"]

	weather_ts = data_receive["data"]["current"]["weather"]["ts"]
	weather_tp = data_receive["data"]["current"]["weather"]["tp"]
	weather_pr = data_receive["data"]["current"]["weather"]["pr"]
	weather_hu = data_receive["data"]["current"]["weather"]["hu"]
	weather_ws = data_receive["data"]["current"]["weather"]["ws"]
	weather_wd = data_receive["data"]["current"]["weather"]["wd"]

	pollution_datetime_object = datetime.strptime(time_format(pollution_ts), '%Y-%m-%d %H:%M:%S.%f')
	weather_datetime_object = datetime.strptime(time_format(weather_ts), '%Y-%m-%d %H:%M:%S.%f')

	pollution_date = time_format(str(tzconvert(pollution_datetime_object)), 1)[0]
	pollution_hours = time_format(str(tzconvert(pollution_datetime_object)), 1)[1]
	weather_date = time_format(str(tzconvert(weather_datetime_object)), 1)[0]
	weather_hours = time_format(str(tzconvert(weather_datetime_object)), 1)[1]

	content_print = "\r\n({}) Last weather info update: {} {}, Temperature: {}°C, Humidity: {}%, Wind speed: {}m/s, Wind direction: {}°, Atmospheric pressure: {}hPa. \r\n({}) Last pollution info update: {} {}, AQI US: {} with main pollutant: {}, AQI CN: {} with main pollution: {}.\r\n\r\n".format(CITY, weather_date, weather_hours, weather_tp, weather_hu, weather_ws, weather_wd, weather_pr, CITY, pollution_date, pollution_hours, pollution_aqius, pollution_mainus, pollution_aqicn, pollution_maincn)
	print(content_print)

	f = open("{}.txt".format(pollution_date), "a")
	f.write(content_print)
	f.close()

if __name__ == "__main__":
	API_KEY = {{API_KEY}}
	COUNTRY = 'China'
	STATE = 'Jiangsu'
	# CITY = 'Shanghai'
	CITY = input("Please tell me which city you'd like to know in {}:".format(STATE))
	URL = 'https://api.airvisual.com/v2/city?city={}&state={}&country={}&key={}'.format(CITY, STATE, COUNTRY, API_KEY)
	main(URL)