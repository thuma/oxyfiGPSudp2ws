# trainpos.oxyfi.com

## Setup
1. Rename local_example.py to local.py.
2. Change ip and port in local.pu to your ip and port.
3. Change the Auth base64 string and if you want you can put the username and password in the dicst as in the 
   example but it ns not used by the server.
4. Start the server by runnign ./run.sh

## Usage
Listen with websocket:

ws://trainpos.oxyfi.com/trafiklab/v1/listen?key=your-key

wss://trainpos.oxyfi.com/trafiklab/v1/listen?key=your-key

## Data frames:
The data is fomated in the nmea standard $GPRMC (Recommended minimum specific GPS/Transit data) more information is avaialble at [http://aprs.gids.nl/nmea/#rmc](http://aprs.gids.nl/nmea/#rmc), there is also some aditional data added after the $GPRMC string with information about the train and data.

### Example:
$GPRMC,054031.0,A,6238.017143,N,01755.565469,E,0.0,208.2,080417,0.0,E,A*00,,62008.trains.se,,17405.public.trains.se@2017-04-08;17405.internal.trains.se@2017-04-08,oxyfi

### Fields 

|No Field|Example|Explanation|
|------|---|---|
| 1  |$GPRMC|Minimum sentence	C.| 
| 2  |142937.0|Fix taken at 14:29:37 UTC.|   
| 3  |A|Status A=active or V=Void.|   
| 4  |5948.7028|Latitude 59 deg 48.7028 minutes (59 + 60/48,7028 = 59.8117 deg)|   
| 5  |N|N Latitude hemisphere	N for northern and S for southern.|   
| 6  |01307.9771|Longitude 013 deg 07.9771' (13 + 60/7.9771 = 13.13295 deg).|  
| 7  |E|Longitude direction, E for east of the meridian 0° and for west.|   
| 8  |49.53| Speed over ground in	 knots (1 knot =  1,852 km/h).|   
| 9  |349.7|Direction angle in degrees.|   
| 10 |101212|Date – 10th of December 2012|   
| 11 |1.8|Magnetic Variation|   
| 12 |E| Magnetic deviation direction, E for east of the meridian 0° and W for west|   
| 13 |*3A| The checksum data, always begins with *|   
| 14 |n/a|Not used|   
| 15 |1421.trains.se|Identifies the vehicle, 1421 in this case (Värmlandstrafik)|   
| 16 |n/a|Not used|   
| 17 |8955.public.trains.se@2012-12-10;8957.public.trains.se@2012-12-10|Train identities concatenated with semicolon if more than one is present. Empty if train is not in traffic.|   
| 18 |oxyfi|Data origin| 

## Checksum
The checksum field that starts with '*' and two hex digits representing an 8 bit exclusive OR of all characters between, but not including, the '$' and '*'.

## Libs
JS: https://www.npmjs.com/package/nmea-0183
Python: https://github.com/Knio/pynmea2
Java: http://nmealib.sourceforge.net/
Ruby: https://github.com/ifreecarve/nmea_plus
GO: https://github.com/buxtronix/golang/blob/master/nmea/src/nmea/gprmc.go
C#: https://github.com/amezcua/GPS-NMEA-Parser/blob/master/C%23/GPRMCGpsSentence.cs
C: https://github.com/jacketizer/libnmea, http://nmea.sourceforge.net/



