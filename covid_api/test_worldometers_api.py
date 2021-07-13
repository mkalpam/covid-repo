import requests


def test_get_country_wise_covid_summary_status_code():
    res = requests.get("http://127.0.0.1:5000/get_country_wise_covid_summary/", json={'country': ['abc', 'USA']})
    assert res.status_code == 200


def test_get_country_wise_covid_summary_size():
    res = requests.get("http://127.0.0.1:5000/get_country_wise_covid_summary/", json={'country': ['abc', 'USA']})
    assert len(res.json()) == 2


def test_get_country_wise_covid_summary_country_check():
    res = requests.get("http://127.0.0.1:5000/get_country_wise_covid_summary/", json={'country': ['India', 'USA']})
    assert res.json()[0]['Country Name'] == 'India'
    assert res.json()[1]['Country Name'] == 'USA'


def test_get_country_wise_covid_summary_non_exist_country():
    res = requests.get("http://127.0.0.1:5000/get_country_wise_covid_summary/", json={'country': ['abc', 'USA']})
    assert res.json()[0]['abc'] == 'No Data available for this country'


def test_get_country_wise_covid_summary_string_query_param():
    res = requests.post("http://127.0.0.1:5000/get_country_wise_covid_summary/", json={'country': 'USA'})
    assert res.json()[0]['Country Name'] == 'USA'
