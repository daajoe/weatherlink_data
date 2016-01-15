# WeatherLink Data to CSV
Log [WeatherLink](http://www.weatherlink.com/) data to a local CSV file.

## Purpose and Use Case
There are two main purposes:
1. WeatherLink only stores a fixed amount of archive data for each station, so 
one can avoid losing older data. For example, my WeatherLink account holds onto 
10240 records, but a new one is added every 30 minutes, which means it 
only keeps the most recent 213 days worth of data.
2. Storing in a CSV makes it much easier to use cool tools like 
[D3](https://d3js.org/).

Important: designed for data format Rev "B" (which is used in firmware 
dated after 4/24/02. Will not work (yet) on older firmware.

## Data Format
Check out explanations of each field of the data format (called Rev "B") in 
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
Direction of Hi Wind Speed | 26     | 1    | 32767 (typo: 255)
Prevailing Wind Direction  | 27     | 1    | 32767 (typo: 255)
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
