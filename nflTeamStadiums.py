from custom_libs import requestsCommon as rC
from custom_libs import osCommon as osC
from custom_libs import fileCommon as fC
from custom_libs.teamLists import city_short, alt_city_short, long, mascots, mascots_short
import urllib.parse
import re


class NFLTeamStadiums:
    """
    This class scrapes from wikipedia main page:
    https://en.wikipedia.org/wiki/List_of_current_NFL_stadiums

    And various pages linked to on the main page.
    """
    def __init__(self, use_cache=True, verbose=True):
        """

        :param use_cache:   bool(), if True, the class will try to use cache from last time it scraped the web. Since
                            this data is fairly static, use_cache is on by default. Turn it off if you suspect
                            there were changes in the data to get the latest.
        """
        self.data = list()
        self._stadium_metadata = {}
        self.verbose = verbose

        # API Info
        self._header = {'User-Agent': 'NFLTeamStadiums/0.1 (https://github.com/grindSunday/NFLTeamStadiums)'}
        self._main_url = "https://en.wikipedia.org/w/api.php"

        # Project Structure
        self._resources_dir = osC.create_file_path_string(["resources"])
        self._raw_soup_file = osC.create_file_path_string(["resources", "rawSoup.txt"])
        self._parsed_soup_file = osC.create_file_path_string(["resources", "parsedSoup.json"])
        self._check_create_project_structure()

        # Used to find stadium table from HTML. Change this if wiki structure changes.
        self._current_stadiums_wiki_section_name = 'List_of_current_stadiums'
        self._current_stadiums_table_from_heading = 2

        # Used for team lookups
        self._teams_city_short = [x.lower() for x in city_short]
        self._teams_alt_city_short = [x.lower() for x in alt_city_short]
        self._teams_long = [x.lower() for x in long]
        self._teams_mascots = [x.lower() for x in mascots]
        self._teams_mascots_short = [x.lower() for x in mascots_short]
        self._team_lists = [self._teams_city_short, self._teams_alt_city_short, self._teams_long,
                            self._teams_mascots, self._teams_mascots_short]

        # Get the Data
        if use_cache:
            self._check_cache()

        if not self.data:
            self._get_current_stadium_data()
            self._add_normalized_current_team_to_data()
            self._add_stadium_coordinates_to_data()
            fC.dump_json_to_file(self._parsed_soup_file, self.data)

    def _check_print(self, print_txt):
        if self.verbose:
            print(print_txt)

    def _check_cache(self):

        raw_soup = fC.read_file_content(self._raw_soup_file)
        parsed_soup = fC.load_json_from_file(self._parsed_soup_file)

        if raw_soup == "" or parsed_soup == {}:
            self._check_print("INFO: No cache available. If this is first run this is normal.")
        else:
            self._check_print("INFO: Loaded data from cache. If the data needs to be refreshed, start the class with "
                              "parameter use_cache = False")
            self.data = parsed_soup

    def _get_current_stadium_data(self):

        def _clean_wiki_text(text_to_extract_from):
            text_to_extract_from = text_to_extract_from.strip()
            ref_bracket_loc = text_to_extract_from.find('[')
            return text_to_extract_from[:ref_bracket_loc] if ref_bracket_loc > -1 else text_to_extract_from

        # Parameters for the API request
        params = {
            "action": "parse",
            "page": "List of current NFL stadiums",
            "format": "json",
            "prop": "text"
        }

        # Make the API request
        self._check_print("INFO: Retrieving base stadium data from wikipedia")
        response = rC.basic_request(self._main_url, params=params, headers=self._header)
        data = response.json()

        # Extract the HTML content
        html_content = data['parse']['text']['*']

        # Parse the HTML content with BeautifulSoup
        soup = rC.get_soup_from_html_content(html_content)
        fC.write_content_to_file(self._raw_soup_file, str(soup))

        # find heading above table
        heading = soup.find(id=self._current_stadiums_wiki_section_name)

        if not heading:
            print("ERROR: Could not scrape wikipedia correctly. The sections may have been updated.")
            return None

        # find second table under heading
        next_ele = heading.next_element
        table_count = 1
        table_element = None
        while next_ele and table_count <= self._current_stadiums_table_from_heading:
            next_ele = next_ele.next_element
            if next_ele.name == 'table':
                if table_count == self._current_stadiums_table_from_heading:
                    table_element = next_ele
                    break
                else:
                    table_count = table_count + 1

        if not table_element:
            print("ERROR: Could not scrape wikipedia correctly. Could not find the stadium table.")
            return None

        # extract table contents
        main_table_content = table_element.find_all('tr')
        columns = [x.text.strip() for x in main_table_content[0].find_all('th')]

        # indices
        name_index = columns.index('Name')
        img_index = columns.index('Image')
        capacity_index = columns.index('Capacity')
        city_index = columns.index('Location')
        surface_index = columns.index('Surface')
        roof_index = columns.index('Roof type')
        teams_index = columns.index('Team(s)')
        date_opened_index = columns.index('Opened')

        index_count = 0
        for row in main_table_content[1:]:
            cells = row.find_all(['th', 'td'])
            name = _clean_wiki_text(cells[name_index].text)
            temp_url = cells[name_index].find_all('a')[0].attrs['href']
            title = urllib.parse.unquote(temp_url.rsplit('/', 1)[-1])
            self._stadium_metadata[title] = {}
            self._stadium_metadata[title]['name'] = name
            self._stadium_metadata[title]['url'] = f"https://en.wikipedia.org{temp_url}"
            self._stadium_metadata[title]['index'] = index_count
            img_url = f"https://en.wikipedia.org{cells[img_index].find_all('a')[0].attrs['href']}"
            capacity = _clean_wiki_text(cells[capacity_index].text.replace(",", ""))
            city = _clean_wiki_text(cells[city_index].text)
            surface = _clean_wiki_text(cells[surface_index].text)
            roof_type = _clean_wiki_text(cells[roof_index].text)
            teams = [_clean_wiki_text(x.text) for x in cells[teams_index].find_all('a')]
            year_opened = _clean_wiki_text(cells[date_opened_index].text)

            temp_dict = {
                "name": name,
                "capacity": int(capacity),
                "imgUrl": img_url,
                "city": city,
                "surface": surface,
                "roofType": roof_type,
                "teams": teams,
                "yearOpened": int(year_opened)
                }

            self.data.append(temp_dict.copy())
            index_count = index_count + 1

    def _add_normalized_current_team_to_data(self):
        """
        This function adds the 'sharedStadium' and 'currentTeams' data
        :return:
        """
        for stadium in self.data:
            found_current_teams = []
            for team in stadium['teams']:
                found_team = self._get_normalized_team(team)
                if found_team:
                    found_current_teams.append(found_team)

            stadium['sharedStadium'] = False if len(found_current_teams) == 1 else True
            stadium['currentTeams'] = found_current_teams.copy()

    def _add_stadium_coordinates_to_data(self):
        def _format_coordinates(coords):
            parts = coords.split('|')

            if len(parts) < 8:
                return "Invalid coordinates format"

            degrees_lat = parts[0] + '°'
            minutes_lat = parts[1] + '′'
            seconds_lat = parts[2] + '″'
            direction_lat = parts[3]

            degrees_lon = parts[4] + '°'
            minutes_lon = parts[5] + '′'
            seconds_lon = parts[6] + '″'
            direction_lon = parts[7]

            formatted_coords = f"{degrees_lat}{minutes_lat}{seconds_lat}{direction_lat} " \
                               f"{degrees_lon}{minutes_lon}{seconds_lon}{direction_lon}"
            return formatted_coords

        titles = [x for x in self._stadium_metadata]
        titles = '|'.join(titles)

        # API parameters to get the full HTML content
        params = {
            'action': 'query',
            'format': 'json',
            'prop': 'coordinates',
            'titles': titles
        }

        response = rC.basic_request(self._main_url, headers=self._header, params=params)
        if response.status_code != 200:
            self._check_print("ERROR: Could not complete the API request to get coordinates for stadiums")
            return None

        data = response.json()

        page_contents = {}

        # Process each page in the API response
        pages = data['query']['pages']
        for page_id, page_data in pages.items():
            title = page_data['title'].replace(" ", "_")
            if "coordinates" in page_data:
                coordinates = page_data["coordinates"][0]
            else:
                coordinates = None

            data_index = self._stadium_metadata[title]['index']
            self.data[data_index]['coordinates'] = coordinates


    def _check_create_project_structure(self):
        osC.check_create_directory(self._resources_dir)
        if not osC.check_if_file_exists(self._raw_soup_file):
            fC.create_blank_file(self._raw_soup_file)
        if not osC.check_if_file_exists(self._parsed_soup_file):
            fC.dump_json_to_file(self._parsed_soup_file, {})

    def _get_normalized_team(self, search_team):
        search_team = search_team.lower()
        for team_list in self._team_lists:
            if search_team in team_list:
                return self._teams_city_short[team_list.index(search_team)].upper()
        return None

    def get_list_of_stadium_names(self):
        """
        Use to get the names of all NFL stadiums

        :return: list() of str()
        """
        return [x['name'] for x in self.data]

    def get_stadium_by_team(self, team):
        """
        Provide the team you want stadium information for.

        :param team:    str(), team in which you want stadium information for. One of the following formats:
                        City + Mascot - e.g., Detroit Lions
                        Mascot - e.g., Lions
                        Team Abbreviation - e.g, DET

        :return:        dict(), JSON format of all available data for the given stadium for the provided team
        """

        team = self._get_normalized_team(team)
        if team is None:
            self._check_print("ERROR: The team you provided to get_stadium_by_team was not recognized. Try "
                              "one of the following formats:\n\n"
                              "City + Mascot - e.g., Detroit Lions\n"
                              "Mascot - e.g., Lions\n"
                              "Team Abbreviation - e.g, DET\n"
                              )
            return None

        teams = [x for x in self.data if team in x['currentTeams']]

        if len(teams) == 1:
            return teams[0]
        elif len(teams) > 1:
            self._check_print("WARNING: the team you provided plays at more than one stadium according to the data. "
                              "Both stadiums are returned in a list")
            return teams
        else:
            self._check_print("ERROR: the team you provided was recognized as a legitimate team, but there is no "
                              "data for them in the Wikipedia content.")
            return None


def main():
    # Test code
    nfl_stadiums = NFLTeamStadiums(use_cache=True)
    stadium_names = nfl_stadiums.get_list_of_stadium_names()
    lions_stadium = nfl_stadiums.get_stadium_by_team('detroit lions')
    print(stadium_names[:5])
    print(lions_stadium)


if __name__ == '__main__':
    main()
