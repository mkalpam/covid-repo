import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

url = 'https://www.worldometers.info/coronavirus/'


def scrap_worldometers(country):
    """
    Scrape the url and filter required information out the text
    :param country:
    :return:
    """
    # Sending a HTTP GET request to a URL and fetch raw HTML text
    html_text = requests.get(url).text

    # Parse the html content
    soup = BeautifulSoup(html_text, 'html.parser')

    # Get the table having the id main_table_countries_today
    table = soup.find('table', attrs={'id': 'main_table_countries_today'})

    # Get the table headers
    table_headers = table.find('thead').select('th')

    # keeping all the header columns in a list
    headers_list = []
    for h in table_headers:
        headers_list.append(h.text)

    # to hold countries for which data to be retrieved
    countries = []
    # if single and string add it to countries list
    if not isinstance(country, list):
        countries.append(country)
    else:
        # add list of countries
        countries.extend(country)

    # to hold final countries information
    country_data = []

    # Handle multiple countries
    for c in countries:
        # getting the row for specific country
        if soup.find(lambda t: t.text.strip().lower() == str(c).lower()) is not None:
            country_row_data = soup.find(lambda t: t.text.strip().lower() == str(c).lower()).parent.select('td')

            values = []
            for row in country_row_data:
                values.append(row.text)

            # create list of dictionary contains each country covid information
            country_data.append(filter_and_process(dict(zip(headers_list, values))))
        # No country matches with the passed country name
        else:
            country_data.append({c: 'No Data available for this country'})
    return country_data


def replace_convert(txt):
    """
    Replace text which contains comma also seen '+' in some cases with none
    :param txt:
    :return: integer value of text
    """
    txt = txt.replace('+', '').replace(',', '')
    return int(txt.strip())


def filter_and_process(c_data):
    """
    Creating dict with required parameters
    :param c_data:
    :return: orderdict
    """
    # creating ordereddict to make the data stored in required order
    df = OrderedDict({'Country Name': c_data['Country,Other'], 'Total Cases': replace_convert(c_data['TotalCases']), 'Active Cases': replace_convert(c_data['ActiveCases']), 'Total Deaths': replace_convert(c_data['TotalDeaths'])})
    recovery_rate = (replace_convert(c_data['TotalRecovered'])/replace_convert(c_data['TotalCases']))*100
    population_infected = (replace_convert(c_data['TotalCases'])/replace_convert(c_data['Population']))*100
    df['Recovery Rate'] = recovery_rate
    df['% of Population Infected'] = population_infected
    return df



