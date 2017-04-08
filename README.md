# trainpos.oxyfi.com

## Setup
1. Rename local_example.py to local.py.
2. Change ip and port in local.pu to your ip and port.
3. Change the Auth base64 string and if you want you can put the username and password in the dicst as in the 
   example but it ns not used by the server.
4. Start the server by runnign ./run.sh

## Usage
Listen with websocket:
ws://trainpos.oxyfi.com/trafiklab/v1/listen?key=<your key>
wss://trainpos.oxyfi.com/trafiklab/v1/listen?key=<your key>

## Data frames:

### Example:
$GPRMC,054031.0,A,6238.017143,N,01755.565469,E,0.0,208.2,080417,0.0,E,A*00,,62008.trains.se,,17405.public.trains.se@2017-04-08;17405.internal.trains.se@2017-04-08,oxyfi

### Field ,  

|No Field|Example|Explanation|
|------|---|---|
| 1  |RMC|   | 
| 2  |   |   |   
| 3  |   |   |   
| 4  |   |   |   
| 5  |   |   |   
| 6  |   |   |  
| 7  |   |   |   
| 8  |   |   |   
| 9  |   |   |   
| 10 |   |   |   
| 11 |   |   |   
| 12 |   |   |   
| 13 |   |   |   
| 14 |   |   |   
| 15 |   |   |   
| 16 |   |   |   
| 17 |   |   |   
| 18 |   |   |  
1. RMC Recommended	Minimum	sentence	C
2. 142937 Fix	taken	at	14:29:37 UTC
3. A Status	A=active	or	V=Void
4. 5948.7028 Latitude	59 deg	48.7028'	
5. N Latitude	hemisphere	N	for	northern	and	S	for	southern	
6. 01307.9771 Longitude	13 deg	07.9771'	
7. E Longitude	direction,	E	for	east	of	the	meridian	0° and	W	for	west	
8. 49.53 Speed	over ground	in	knots
9. 349.7 Track	angle	in	degrees	True
10. 101212 Date	– 10th of	December	2012
11. 1.8 Magnetic	Variation
12. E Magnetic	deviation	direction,	E	for	east	of	the	meridian	0° and	W	for	west
13. *3A The	checksum	data,	always	begins	with	*
14. n/a Not	used
15. 1421.trains.se Identifies	the	vehicle,	1421	in	this	case	(Värmlandstrafik)
16. n/a Not	use S.id 6
17. 8955.public.trains.se@2012-12-10;8957.public.trains.se@2012-12-10
    Train	identities	concatenated	with	semicolon	if	more	than	one	is	present.	
    See	more	details	about	how	this	string	is	built	up	in section	3.1.
18. oxyfi Data	origin
