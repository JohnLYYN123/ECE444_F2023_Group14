from flask import Blueprint, jsonify, render_template, request
from pathlib import Path
import os
import sys

sys.path.append(os.path.abspath('..'))
from ..Models.SearchModel import SearchModel

search = Blueprint(url_prefix="/search")

class SearchController:
    @search.route('/find_event', methods=["GET"])
    def find_event(self):
        event_json = request.get_json()
        event_name = event_json.get('event_name')

        if not event_name:
            return jsonify({"code": 401, "msg": "empty event name", "data": []})

        if len(event_name) > 200:
            return jsonify({"code": 401, "msg": "event name too long", "data": []})

        data = SearchModel.find_event(event_name)
        return jsonify({"code": 200, "msg": "OK", "data": data})
