from custom_libs import requestsCommon as rC
from custom_libs import osCommon as osC
from custom_libs import fileCommon as fC
from custom_libs.teamLists import city_short, alt_city_short, long, mascots, mascots_short


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
        self.verbose = verbose
        self._main_url = 'https://en.wikipedia.org/wiki/List_of_current_NFL_stadiums'
        self._raw_soup_file = osC.create_file_path_string(["resources", "rawSoup.txt"])
        self._parsed_soup_file = osC.create_file_path_string(["resources", "parsedSoup.json"])

        # Used to find current stadium table. Change this if wiki structure changes.
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

        # Get and clean data
        if use_cache:
            self._check_cache()

        if not self.data:
            self._get_current_stadium_data()
            self._add_normalized_current_team_to_data()
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
        soup = rC.get_soup(self._main_url, add_user_agent=True)
        fC.write_content_to_file(self._raw_soup_file, soup.prettify())

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

        for row in main_table_content[1:]:
            cells = row.find_all(['th', 'td'])
            name = cells[name_index].text.strip()
            img_url = f"https://en.wikipedia.org/{cells[img_index].find_all('a')[0].attrs['href']}"
            capacity = int(cells[capacity_index].text.replace(",", "").strip())
            city = cells[city_index].text.strip()
            surface = cells[surface_index].text.strip()
            roof_type = cells[roof_index].text.strip()
            teams = [x.text for x in cells[teams_index].find_all('a')]
            year_opened = cells[date_opened_index].text.strip()

            temp_dict = {
                "name": name,
                "capacity": capacity,
                "imgUrl": img_url,
                "city": city,
                "surface": surface,
                "roofType": roof_type,
                "teams": teams,
                "yearOpened": year_opened
                }

            self.data.append(temp_dict.copy())

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
    nfl_stadiums = NFLTeamStadiums()
    stadium_names = nfl_stadiums.get_list_of_stadium_names()
    det = nfl_stadiums.get_stadium_by_team('det')
    print(stadium_names[:5])
    print(det)


if __name__ == '__main__':
    main()
