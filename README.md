# address-parser microservice
A REST endpoint consuming an address string and returning a json with address fields:

    curl -X POST "http://127.0.0.1:5000/parse" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"address\": \"5760 Teredo St., Sechelt, BC, Canada, VON 3A0\"}"
    {
        "city": "Sechelt",
        "state": "BC",
        "street_address": "5760, Teredo St.",
        "postcode": "VON 3A0",
        "country": "Canada",
    },

## Use Locally

1. Install libpostal
2. Instal deps with `pipenv install && pipenv shell`
3. Run flask application `export FLASK_APP=api.py && flask run`
4. Test at http://127.0.0.1:5000/swagger-ui/