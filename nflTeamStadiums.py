from custom_libs import requestsCommon as rC
from custom_libs.teamLists import city_short, alt_city_short, long, mascots, mascots_short


class NFLTeamStadiums:
    """
    This class scrapes from wikipedia main page:
    https://en.wikipedia.org/wiki/List_of_current_NFL_stadiums

    And various pages linked to on the main page.
    """
    def __init__(self):
        self.data = list()

        self._main_url = 'https://en.wikipedia.org/wiki/List_of_current_NFL_stadiums'
        self._team_lists = [city_short, alt_city_short, long, mascots, mascots_short]
        self._get_data()

    def _get_data(self):
        soup = rC.get_soup(self._main_url, add_user_agent=True)

        # find heading above table
        heading = soup.find(id='List_of_current_stadiums')

        if not heading:
            print("ERROR: Could not scrape wikipedia correctly. The sections may have been updated.")
            return None

        # find second table under heading
        next_ele = heading.next_element
        table_count = 0
        table_element = None
        while next_ele and table_count <= 1:
            next_ele = next_ele.next_element
            if next_ele.name == 'table':
                if table_count == 1:
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

    def get_list_of_stadium_names(self):
        """
        Use to get the names of all NFL stadiums

        :return: list() of str()
        """
        return [x['name'] for x in self.data]


def main():
    # Test code
    nfl_stadiums = NFLTeamStadiums()
    stadium_names = nfl_stadiums.get_list_of_stadium_names()
    print(stadium_names[:5])


if __name__ == '__main__':
    main()
