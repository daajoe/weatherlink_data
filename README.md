# WeatherLink Data to CSV
Format and log new [WeatherLink](http://www.weatherlink.com/) data to a local
CSV file.

## Purpose

1. WeatherLink only stores a fixed amount of archive data for each station, so
you are guaranteed to lose data eventually if you do not back it up. For 
example, my account holds up to 10240 records; a new record is added every 30
minutes, so it can only keep the most recent 213 days worth of data.
2. On the web service, data is stored in 52 byte records with a
lot of unnecessary data (e.g. soil temperature and leaf wetness are useless
if you do not have the right equipment on your weather station). This program
formats and stores just the data you want in a CSV. 

## Setup
Two files are needed for the program to function:

1. A `.weatherlink` file in your home directory with your weatherlink.com
account name on the first line, password on the second line, and a 
comma-separated list of fields that you want to exclude from the CSV 
(on as many additional lines as needed). A list of all of the field names 
is in the progdata.py file.
Your dotfile might look like this:
```
ACCOUNT
PASSWORD
soil_moist1, soil_moist2, soil_moist3, soil_moist4
```
2. A CSV file. By default, the program expects `weatherlink.csv` in your home
directory -- simply create an empty file. You can use `f FILENAME`
or `--file=FILENAME` as an argment to specify a different file.


Note: designed for data format Rev "B" (which is used in Davis firmware 
dated after 4/24/02). Support for older firmware may be added in the future.

## Data Format
Check out explanations of each field of the data format (Rev "B") in 
[the manufacturer's PDF](http://www.davisnet.com/support/weather/download/VantageSerialProtocolDocs_v261.pdf#page=32).

Field                      | Offset | Size | Dash Val 
---------------------------|--------|------|---------
Date Stamp                 | 0      | 2    | N/A 
Time Stamp                 | 2      | 2    | N/A
Outside Temperature        | 4      | 2    | 32767
High Out Temperature       | 6      | 2    | -32768
Low Out Temperature        | 8      | 2    | 32767
Rainfall                   | 10     | 2    | 0
High Rain Rate             | 12     | 2    | 0
Barometer                  | 14     | 2    | 0
Solar Radiation            | 16     | 2    | 32767
Number of Wind Samples     | 18     | 2    | 0
Inside Temperature         | 20     | 2    | 32767
Inside Humidity            | 22     | 1    | 255
Outside Humidity           | 23     | 1    | 255
Average Wind Speed         | 24     | 1    | 255
High Wind Speed            | 25     | 1    | 0
Direction of Hi Wind Speed | 26     | 1    | 255
Prevailing Wind Direction  | 27     | 1    | 255
Average UV Index           | 28     | 1    | 255
ET                         | 29     | 1    | 0
High Solar Radiation       | 30     | 2    | 0
High UV Index              | 32     | 1    | 0
Forecast Rule              | 33     | 1    | 193
Leaf Temperature           | 34     | 2    | 255
Leaf Wetnesses             | 36     | 2    | 255
Soil Temperatures          | 38     | 4    | 255
Download Record Type       | 42     | 1    | N/A
Extra Humidities           | 43     | 2    | 255
Extra Temperatures         | 45     | 3    | 32767 (typo?)
Soil Moistures             | 48     | 4    | 255
