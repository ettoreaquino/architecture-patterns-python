#!/bin/sh
gunicorn -w 1 -b "0.0.0.0:9080" -t 300 src.falcon_app:app
