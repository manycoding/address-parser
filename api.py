import os
from pathlib import Path
import re
from typing import *

from flask import Flask
from flask_apispec import FlaskApiSpec, use_kwargs, marshal_with, MethodResource
from flask_caching import Cache
from flask_restful import Resource, Api
from postal.parser import parse_address
from webargs import fields, validate
from webargs.flaskparser import parser, abort

DEBUG = os.environ.get("DEBUG", False)
config = {"DEBUG": DEBUG, "CACHE_TYPE": "simple", "CACHE_DEFAULT_TIMEOUT": 300}


app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
api = Api(app)
docs = FlaskApiSpec(app)


class Parse(MethodResource):
    @use_kwargs(
        {"address": fields.Str(required=True)}, locations=["json"],
    )
    def post(self, address: str) -> Tuple[Dict, int]:
        """Parse an address string
        Returns:
            A tuple of dict with message and results, and a status code.
            Result contains street address, city, zip
        """
        parsed = parse_address(address)

        return get_address(parsed), 200


class LibParse(MethodResource):
    @use_kwargs(
        {"address": fields.Str(required=True)}, locations=["json"],
    )
    def post(self, address: str) -> Tuple[Dict, int]:
        """Parse an address string with libpostal without any processing
        """
        return parse_address(address), 200


def get_address(i: List[Tuple[str]]) -> Optional[Dict[str, str]]:
    """Parse an incoming list from pypostal to a neat dict
    """
    if not i:
        return None
    results = {}
    for k, v in i:
        results.setdefault(v, []).append(k.title())
    address = dict()
    address["street_address"] = ", ".join(
        [
            get_first(results.get(f))
            for f in ["house_number", "building", "road", "unit"]
            if get_first(results.get(f))
        ]
    )
    address["city"] = get_first(results.get("city"))
    address["state"] = get_first(results.get("state")).upper()
    address["postcode"] = get_first(results.get("postcode")).upper()
    address["country"] = get_first(results.get("country"))
    return {k: v for k, v in address.items() if v}


def get_first(l: List[str]) -> str:
    if l:
        return l[0]
    return ""


@parser.error_handler
def handle_request_parsing_error(err, req, schema, error_status_code, error_headers):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    abort(error_status_code, errors=err.messages)


resources = [Parse, LibParse]
for r in resources:
    url = re.sub("(?!^)([A-Z]+)", r"_\1", r.__name__).lower()
    api.add_resource(r, f"/{url}")
    docs.register(r)

if __name__ == "__main__":
    app.run(debug=DEBUG)
