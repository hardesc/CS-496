import json
from pprint import pprint

class Lists():
    def __init__(self):

        self.voterID_list = []
        self.all_state_classes = []
        self.all_district_classes = []
        self.all_electoral_classes = []
        self.all_vote_classes = []
        self.all_voter_classes = []
        
        self.income_list = [
            '0 - $15,000', 
            '$15,001 - $30,000', 
            '$30,001 - $50,000', 
            '$50,001 - $75,000', 
            '$75,001 - $100,000', 
            '$100,001 - $150,000', 
            '$150,001 - $200,000', 
            '$200,001+'
            ]
        
        self.ethnicity_list = [
            'White', 
            'Black', 
            'Hispanic', 
            'Asian', 
            'Native American', 
            'Pacific Islander', 
            'Other'
            ]
        
        self.education_lvl_list = [
            'GED', 
            'HS Diploma', 
            'Some college', 
            'Bachelor\'s Degree', 
            'Postgraduate Degree', 
            'PhD'
            ]
        
        self.candidate_list = [
            'Hillary Clinton', 
            'Donald Trump', 
            'Gary Johnson', 
            'Jill Stein', 
            'Other'
            ]
        
        self.issues_list = [
            'The Economy',
            'National Defense',
            'Education',
            'Income Inequality',
            'The Environment',
            'Terrorism',
            'Social Justice',
            'The Supreme Court',
            'Gun Control',
            'Government Overreach',
            'Health Care',
            'Corruption'
            ]
        
        with open('states.json') as states_data:
            self.states_list = json.load(states_data)
            
        with open('districts.json') as districts_data:
            self.districts_list = json.load(districts_data)

    def json_read_test(self):
        print "\n\n--------------------TESTING JSON DATA READ-------------------\n\n"
        pprint(self.states_list)
        pprint(self.districts_list)