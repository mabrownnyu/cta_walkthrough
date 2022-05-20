'''
Author MB
Date: May 19, 2022

This python script creates a Flask API to return primary winners from a local file
`primary_results.json`

Assumption that the primary results are formatted like:
{
    "state":{
        "county":{
            "party_1":{
                "candidate_1 ":votes,
                "candidate_2":votes
            },
            "party_2":{
                "candidate_1":votes,
                "candidate_2":votes,
                "candidate_3":votes
            }
        }
    }
}

'''

# imports
import json

from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd

# start flask app
app = Flask(__name__)
api = Api(app)

class County(Resource):
    '''
    class for the county endpoint
    '''
    def get(self):
        # parse parameters for county and state
        parser = reqparse.RequestParser()
        parser.add_argument('state', required=True)
        parser.add_argument('county', required=True)
        args = parser.parse_args()

        # read local file of JSON data of primary results
        data = json.load(open('primary_results.json', 'r'))

        # parse url args from arg parser into variables
        state = args['state']
        county = args['county']

        # check that the state is in the data, return 404 if not
        if state not in set(data.keys()):
            return {
                'message': f"{state} not in primary results."
            }, 404

            # check that the county is in that state as well, return 404 if not
            if county not in set(data[state].keys()):
                return {
                    'message': f"{county} not in {state} primary results."
                }, 404

        # get the list of county candidates for the state/county requested
        county_candidates = data[state][county]

        # init the winners payload to return to the user
        winners = {}

        # iterate through each of the parties in the county dictionary
        for party, candidates in county_candidates.items():
            # set the max votes/winning candidate to -1 and none respectively
            # note this code does assume that there is not a tie/runoff
            max_votes = -1
            winning_candidate = None

            # for each of the candidates, check and see if they have more max_votes
            # than the previous highest votes. if so, assign that candidate to be the winner
            for candidate, votes in candidates.items():
                if votes > max_votes:
                    winning_candidate = candidate
                    max_votes = votes

            # after iterating through all the candidates, add the winning candidate
            # to the dictionary paylod
            winners[party] = winning_candidate

        # return data and OK status to the end user
        return {'data': winners}, 200

class State(Resource):
    '''
    class for the state endpoint
    '''
    def get(self):
        # parse parameters for county and state
        parser = reqparse.RequestParser()
        parser.add_argument('state', required=True)
        args = parser.parse_args()

        # read local file of JSON data of primary results
        data = json.load(open('primary_results.json', 'r'))

        # parse url args from arg parser into variables
        state = args['state']

        # check that the state is in the data, return 404 if not
        if state not in set(data.keys()):
            return {
                'message': f"{state} not in primary results."
            }, 404

        # get the list of county candidates for the state/county requested
        state_candidates = data[state]

        # init the winners payload to return to the user
        winners = {}

        # iterate through each of the counties in the state dictionary
        for county, county_candidates in state_candidates.items():
            # create empty dict for county
            winners[county] = {}
            # iterate through each of the parties in the county dictionary
            for party, candidates in county_candidates.items():
                # set the max votes/winning candidate to -1 and none respectively
                # note this code does assume that there is not a tie/runoff
                max_votes = -1
                winning_candidate = None

                # for each of the candidates, check and see if they have more max_votes
                # than the previous highest votes. if so, assign that candidate to be the winner
                for candidate, votes in candidates.items():
                    if votes > max_votes:
                        winning_candidate = candidate
                        max_votes = votes

                # after iterating through all the candidates, add the winning candidate
                # to the dictionary paylod
                winners[county][party] = winning_candidate

        # return data and OK status to the end user
        return {'data': winners}, 200

class All(Resource):
    '''
    class for the all endpoint
    '''
    def get(self):
        # read local file of JSON data of primary results
        data = json.load(open('primary_results.json', 'r'))

        # init the winners payload to return to the user
        winners = {}

        for state, state_candidates in data.items():
            # create empty dict for state
            winners[state] = {}

            # iterate through each of the counties in the state dictionary
            for county, county_candidates in state_candidates.items():
                # create empty dict for county
                winners[state][county] = {}
                # iterate through each of the parties in the county dictionary
                for party, candidates in county_candidates.items():
                    # set the max votes/winning candidate to -1 and none respectively
                    # note this code does assume that there is not a tie/runoff
                    max_votes = -1
                    winning_candidate = None

                    # for each of the candidates, check and see if they have more max_votes
                    # than the previous highest votes. if so, assign that candidate to be the winner
                    for candidate, votes in candidates.items():
                        if votes > max_votes:
                            winning_candidate = candidate
                            max_votes = votes

                    # after iterating through all the candidates, add the winning candidate
                    # to the dictionary paylod
                    winners[state][county][party] = winning_candidate

        # return data and OK status to the end user
        return {'data': winners}, 200

# add endpoints to API
api.add_resource(County, '/county')
api.add_resource(State, '/state')
api.add_resource(All, '/all')

if __name__ == '__main__':
    # run the flask app
    app.run()
