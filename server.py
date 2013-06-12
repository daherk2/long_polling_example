# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask.ext import restful

import os
import time
from datetime import datetime


app = Flask(__name__)
api = restful.Api(app)


@app.route('/')
def index():
    return render_template('index.html')


class DataUpdate(restful.Resource):

    def _is_updated(self, request_time):
        """
        Returns if resource is updated or it's the first
        time it has been requested.
        args:
            request_time: last request timestamp
        """
        last_change = os.stat('data.txt').st_mtime
        app.config['first_time'] = False
        return last_change > request_time

    def get(self):
        """
        Returns 'data.txt' content when the resource has
        changed after the request time
        """
        request_time = time.time()
        while not self._is_updated(request_time):
            time.sleep(0.5)
        content = ''
        with open('data.txt') as data:
            content = data.read()
        return {'content': content,
                'date': datetime.now().strftime('%Y/%m/%d %H:%M:%S')}


class Data(restful.Resource):

    def get(self):
        content = ''
        with open('data.txt') as data:
            content = data.read()
        return {'content': content}


api.add_resource(DataUpdate, '/data-update')
api.add_resource(Data, '/data')


if __name__ == '__main__':
    app.run(port=5000, debug=True)