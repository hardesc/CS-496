import webapp2
import os
import json

class BaseHandler(webapp2.RequestHandler):

    def get(self):
        url_dict = {
            'post_requests' : {
                'load_states_and_districts_url' : 'https://cs496-assignment3-148322.appspot.com/admin?fill_all=True',
                'generate_random_votes_url' : 'https://cs496-assignment3-148322.appspot.com/admin?fill_votes=True&num={number_of_votes_to_generate}'
            },
            'get_requests' : {
                "vote_count_url" : "https://cs496-assignment3-148322.appspot.com/votes/all",
                "single_vote_url" : "https://cs496-assignment3-148322.appspot.com/votes/{vote_key}",
                "voter_count_url" : "https://cs496-assignment3-148322.appspot.com/voters/all",
                "single_voter_url" : "https://cs496-assignment3-148322.appspot.com/voters/{voter_key}",
                "states_url" : "https://cs496-assignment3-148322.appspot.com/states/all",
                "single_state_url" : "https://cs496-assignment3-148322.appspot.com/states/{state_key}",
                "districts_url" : "https://cs496-assignment3-148322.appspot.com/districts/all",
                "single_district_url" : "https://cs496-assignment3-148322.appspot.com/districts/{district_key}",
                "single_state_url" : "https://cs496-assignment3-148322.appspot.com/states/{state_key}|{state_abbr}",
                "all_districts_by_district_number_url" : "https://cs496-assignment3-148322.appspot.com/districts/{district_number}",
                "all_districts_by_state_url" : "https://cs496-assignment3-148322.appspot.com/districts/state/{state_key}|{state_abbr}",
                "all_electors_url" : "https://cs496-assignment3-148322.appspot.com/electors/all",
                "elector_count_url" : "https://cs496-assignment3-148322.appspot.com/electors/count",
                "single_elector_url" : "https://cs496-assignment3-148322.appspot.com/electors/{elector_key}"
            },
            'put_requests' : {
                "edit_vote_url" : "https://cs496-assignment3-148322.appspot.com/votes/{vote_key}{?voter_key,candidate,issues,state_key,dist_key}"
            },
            'delete_requests' : {
                "delete_all_url" : 'https://cs496-assignment3-148322.appspot.com/admin?nuke=True'
            }
        }
        self.response.write(json.dumps(url_dict, indent=4))
        
        