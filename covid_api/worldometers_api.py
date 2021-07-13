import json
from flask import Flask, request
import worldometers_info

# Flask instance
app = Flask(__name__)


@app.route('/get_country_wise_covid_summary/', methods=['POST', 'GET'])
def get_country_wise_covid_summary():
    input_json = request.get_json()
    countries = input_json['country']
    return json.dumps(worldometers_info.scrap_worldometers(countries), sort_keys=False)


if __name__ == "__main__":
    app.run(debug=True)