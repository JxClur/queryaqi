# queryaqi

## Query AQI information
This script aims to query the AQI information of a city using AirVisual API<br />
Change the value of the variable 'CITY' if you want it to display the city you interest.

## Core idea behind the script
### Retrieve AQI and weather info from AirVisual API
- Call AirVisual API with requests module
- Transform string type to dictionary type for the output data with json module
<br />

### Time zone conversion
Because the time zone which AirVisual API uses is UTC, in order to convert it to the time zone we are currently living in, <br />
we can use pytz module to make the change.<br />

### Print or return the value you want
Finally we have to put all pieces together to make the task.
