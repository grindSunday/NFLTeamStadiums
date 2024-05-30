# NFLTeamStadiums
A simple python class that provides easy access to NFL stadium data.

This class utilizes the Wikipedia API to retrieve NFL stadium data and provides methods for easy 
access to the same. Stadium data is fairly static, so by default, this class will save the data retrieved from 
Wikipedia locally for subsequent uses for quicker access and less load on Wikipedia. See the below documentation 
for details on basic usage.

## Pre-requisites
- [requests](https://pypi.org/project/requests/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

```
pip install beautifulsoup4
pip install requests
```

## Installation and Creating an Instance
1. Clone or download the repository 
2. Import the class in your code
3. Instantiate the class
```
git clone https://github.com/your-username/NFLTeamStadiums.git
from nflTeamStadiums import NFLTeamStadiums

# Use one of the below to instantiante the class
nfl_stadiums = NFLTeamStadiums()                    # will use local cache if available and print to console
nfl_stadiums = NFLTeamStadiums(use_cache=False)     # will retrieve data from wikipedia and overwrite local cache
nfl_stadiums = NFLTeamStadiums(verbose=False)       # will turn off console printing
```

## Methods

### get_stadium_by_team
```
nfl_stadiums.get_stadium_by_team("lions")
```

#### results:
```json
{
    "name": "Ford Field",
    "capacity": 65000,
    "imgUrl": "https://en.wikipedia.org/wiki/File:Packers_at_Lions_Dec_2020_(50715608723).jpg",
    "city": "Detroit, Michigan",
    "surface": "FieldTurf CORE",
    "roofType": "Fixed",
    "teams": [
        "Detroit Lions"
    ],
    "yearOpened": 2002,
    "sharedStadium": false,
    "currentTeams": [
        "DET"
    ],
    "coordinates": {
        "lat": 42.34,
        "lon": -83.04555556,
        "primary": "",
        "globe": "earth"
    }
}
```

### calculate_distance_between_stadiums
```
distance_in_miles = nfl_stadiums.calculate_distance_between_stadiums('lions', 'chiefs')
```


### get_list_of_stadium_names
```
nfl_stadiums.get_list_of_stadium_names()
```

#### results:
```
['Acrisure Stadium', 'Allegiant Stadium', 'Arrowhead Stadium', 'AT&T Stadium', 'Bank of America Stadium' ...]
```

## Data Source
This package utilizes data from Wikipedia. The core page is 
[here](https://en.wikipedia.org/wiki/List_of_current_NFL_stadiums).


You are responsible for how you use the data. Wikipedia content is licensed under 
the Creative Commons Attribution-ShareAlike 3.0 Unported License. For more details on the terms of use, 
please refer to the [Wikimedia Foundation's Terms of Use](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use).


## License
This project is licensed under the MIT License. See the LICENSE file for details.

