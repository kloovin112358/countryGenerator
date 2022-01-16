from flask import Flask, render_template, jsonify
import csv
from random import randint
from bisect import bisect_left

app = Flask(__name__, static_url_path='/static')

"""
on startup, we want to load the data from the CSV file
data is provided courtesy of Worldometer:
https://www.worldometers.info/world-population/population-by-country/

the format of the CSV data is in the following form:
col 1: country name
col 2: population in 2020
col 3: cumulative population. We are going to draw from this value when 
selecting a random number. For example, if we select the number 2,500,200,352,
this would correspond to India, which is given values 1,439,323,777 to 2,819,328,161
"""
WORLD_POP = 7795232630
# the population dict is in the following format:
# {
#   cumulative_population1: [country_name, population],
#   cumulative_population2: ...,
#   ...
# }
POP_DICT = {}
POP_DICT_KEYS = []

@app.before_first_request
def loadCSVData():
    with open('Country_Populations.csv') as csvfile:
        countryReader = csv.reader(csvfile, delimiter=',')
        # skip the header row
        next(countryReader)
        # now loop through each row in the CSV
        for row in countryReader:
            POP_DICT[int(row[2])] = [row[0], int(row[1]), int(row[1]) / WORLD_POP]
            POP_DICT_KEYS.append(int(row[2]))

@app.route('/')
def index():
    return render_template('index.html')

# implementation borrowed from
# https://www.geeksforgeeks.org/binary-search-bisect-in-python/
def BinarySearch(a, x):
    i = bisect_left(a, x)
    if i:
        return i
    return 0

@app.route('/generate')
def generate_country():

    randomInt = randint(1, WORLD_POP)

    # now that we have a random integer value of a person, we
    # have to search through the population dictionary in order to find
    # the country this corresponds to
    # we will use bisection search
    res = BinarySearch(POP_DICT_KEYS, randomInt)
    
    # the response is in the format:
    # [country_name, country_pop, % of world pop]
    countryList = POP_DICT[POP_DICT_KEYS[res]]

    return jsonify(countryList=countryList)