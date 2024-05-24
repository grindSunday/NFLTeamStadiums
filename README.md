# NFLTeamStadiums
A simple python class that scrapes Wikipedia for NFL stadium data and provides methods for easy access

## Pre-requisites
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/): `pip install beautifulsoup4`
- [fake-useragent](https://github.com/fake-useragent/fake-useragent): `pip install fake-useragent`

## Installation and Creating an Instance
1. Clone or download the repository
```bash
git clone https://github.com/your-username/NFLTeamStadiums.git
```

2. Import the class in your code
```python
from nflTeamStadiums import NFLTeamStadiums
```

3. Instantiate the class
```python 
nfl_stadiums = NFLTeamStadiums()
```

## Methods

### get_stadium_by_team
```
lions_stadium = nfl_stadiums.get_stadium_by_team("lions")
print(lions_stadium)

# results
{
    "name": "Ford Field",
    "capacity": 65000,
    "imgUrl": "https://en.wikipedia.org//wiki/File:Packers_at_Lions_Dec_2020_(50715608723).jpg",
    "city": "Detroit, Michigan",
    "surface": "FieldTurf CORE[18]",
    "roofType": "Fixed",
    "teams": [
        "Detroit Lions"
    ],
    "yearOpened": "2002",
    "sharedStadium": false,
    "currentTeams": [
        "DET"
    ]
}
```

### get_list_of_stadium_names
```
stadium_names = nfl_stadiums.get_list_of_stadium_names()
print(stadium_names[:5])

# results
['Acrisure Stadium', 'Allegiant Stadium', 'Arrowhead Stadium', 'AT&T Stadium', 'Bank of America Stadium']
```

## Data Source
This package scrapes data from Wikipedia.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

Wikipedia content is accessed through this class upon instantiation. Wikipedia content is licensed under 
the Creative Commons Attribution-ShareAlike 3.0 Unported License. For more details on the terms of use, 
please refer to the Wikimedia Foundation's Terms of Use:
https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use