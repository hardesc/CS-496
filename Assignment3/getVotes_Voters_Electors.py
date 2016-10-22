import json
import sys
import random
from pprint import pprint


voterID_list = []

all_state_classes = []
all_district_classes = []
all_electoral_classes = []

income_list = [
    '0 - $15,000', 
    '$15,001 - $30,000', 
    '$30,001 - $50,000', 
    '$50,001 - $75,000', 
    '$75,001 - $100,000', 
    '$100,001 - $150,000', 
    '$150,001 - $200,000', 
    '$200,001+'
    ]

ethnicity_list = [
    'White', 
    'Black', 
    'Hispanic', 
    'Asian', 
    'Native American', 
    'Pacific Islander', 
    'Other'
    ]

education_lvl_list = [
    'GED', 
    'HS Diploma', 
    'Some college', 
    'Bachelor\'s Degree', 
    'Postgraduate Degree', 
    'PhD'
    ]

candidate_list = [
    'Hillary Clinton', 
    'Donald Trump', 
    'Gary Johnson', 
    'Jill Stein', 
    'Other'
    ]

issues_list = [
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
    states_list = json.load(states_data)
    
with open('districts.json') as districts_data:
    districts_list = json.load(districts_data)







def json_read_test():
    print "\n\n--------------------TESTING JSON DATA READ-------------------\n\n"
    pprint(states_list)
    pprint(districts_list)
    
class Electoral_College():
    def __init__(self, elector_id, state, candidate_list):
        self.evoter_id = elector_id
        self.state = state
        self.candidate = random.randint(0, len(candidate_list) - 1)
        all_electoral_classes.append(self)
        
    def db_decode_candidate(self):
        if type(self.candidate) is int:
            self.candidate = candidate_list[self.candidate]
        
    def db_encode_candidate(self):
        if type(self.candidate) is str:
            self.candidate = candidate_list.index(self.candidate)        

class District():
    def __init__(self, district, state, all_district_classes):
        self.number = district['Number']
        self.state = state
        self.voters = []
        all_district_classes.append(self)
        
    def print_District(self):
        sys.stdout.write("Number = %d\nState = %s\n" % (self.number, self.state.abbr))

class State():
    def __init__(self, state, all_state_classes):
        self.abbr = state['state']
        self.quant_districts = state['Quant_Districts']
        self.quant_registered = state['Quant_Registered']
        self.quant_electors = self.quant_districts + 2
        self.districts = []
        self.electors = []
        all_state_classes.append(self)
        
    def set_Districts(self, all_district_classes):
        self.districts = [district for district in all_district_classes if district.state.abbr == self.abbr]
            
    def set_Electoral_College(self, all_electoral_classes):
        self.electors = [elector for elector in all_electoral_classes if elector.state.abbr == self.abbr]
        
    def print_State(self):
        sys.stdout.write("abbr = %s\nquant_districts = %d\nquant_registered = %d\nquant_electors = %d\n" % (self.abbr, self.quant_districts, self.quant_registered, self.quant_electors))
        sys.stdout.write("Districts: ")
        print [district.number for district in self.districts]
        sys.stdout.write("Electors: ")
        print [elector.evoter_id for elector in self.electors]
        
def generate_all_states(states_list, all_state_classes):
    for state in states_list:
        State(state, all_state_classes)
        
def generate_all_districts(districts_list, all_state_classes, all_districts_classes):
    
    for state in all_state_classes:
        for district in districts_list:
            if district['state'] == state.abbr:
                District(district, state, all_districts_classes)
        state.set_Districts(all_districts_classes)  
                
def generate_all_electoral_college(all_electoral_classes, all_state_classes, candidate_list):
    for state in all_state_classes:
        for i in range(1, state.quant_electors + 1):
            Electoral_College(i, state, candidate_list)
        state.set_Electoral_College(all_electoral_classes)

def display_all_states(all_states_classes):
    for state in all_states_classes:
        print "\n"
        state.print_State()
        
def display_all_districts(all_districts_classes):
    for district in all_districts_classes:
        print "\n"
        district.print_District()

seed = random.seed()

"""
Voters
-------
Voter_ID
Party
Age
Sex
Income_Lvl
Ethnicity
Education_Lvl
"""
class Voter():
    def __init__(self, voterID_list, income_list, ethnicity_list, education_lvl_lst):
        self.id = 0
        while self.id in voterID_list or self.id == 0:
            self.id = random.randrange(100000)
        
        self.party = random.choice(['D', 'R', 'G', 'L', 'I', 'O'])
        self.age = random.randrange(18, 105)
        self.sex = random.choice(['M', 'F'])
        self.income_lvl = random.randint(0, len(income_list) - 1)
        self.ethnicity = random.sample([ i for i in range(len(ethnicity_list))], random.randint(1, len(ethnicity_list)))#pick a random combination of ethnicities
        self.education_lvl = random.randint(0, len(education_lvl_list) - 1)
        
        voterID_list.append(self.id)
        
    def print_Voter(self):
        sys.stdout.write("id = %d\nparty = %c\nage = %d\nsex = %c\nincome_lvl = %s\nethnicity = %s\neducation_lvl = %s\n\n" % (self.id, self.party, self.age, self.sex, self.income_lvl, self.ethnicity, self.education_lvl))
    
    def db_decode_income(self):
        if type(self.income_lvl) is int:
            self.income_lvl = income_list[self.income_lvl]
        
    def db_encode_income(self):
        if type(self.income_lvl) is str:
            self.income_lvl = income_list.index(self.income_lvl)

    def db_decode_ethnicity(self):
        if type(self.ethnicity[0]) is int:
            for i, ethnicity in enumerate(self.ethnicity):
                self.ethnicity[i] = ethnicity_list[ethnicity]
        
    def db_encode_ethnicity(self):
        if type(self.ethnicity[0]) is str:
            for i, ethnicity in enumerate(self.ethnicity):
                self.ethnicity[i] = ethnicity_list.index(ethnicity)
            
    def db_decode_education_lvl(self):
        if type(self.education_lvl) is int:
            self.education_lvl = education_lvl_list[self.education_lvl]
        
    def db_encode_education_lvl(self):
        if type(self.education_lvl) is str:
            self.education_lvl = education_lvl_list.index(self.education_lvl)
            
    def db_decode_all(self):
        self.db_decode_income()
        self.db_decode_ethnicity()
        self.db_decode_education_lvl()
        
    def db_encode_all(self):
        self.db_encode_income()
        self.db_encode_ethnicity()
        self.db_encode_education_lvl()

#just a simple test of the basic Voter stuff
def test_Voter():
    print "\n\n------------TESTING VOTER CLASS-----------------------\n\n"
    for i in range(0, 10):
        a_voter = Voter(voterID_list, income_list, ethnicity_list, education_lvl_list)
        sys.stdout.write("%d.)" % (i))
        a_voter.print_Voter()
        
        a_voter.db_decode_all()
        sys.stdout.write("%d.)" % (i))
        a_voter.print_Voter()
        
        a_voter.db_encode_all()
        sys.stdout.write("%d.)" % (i))
        a_voter.print_Voter()
    
"""    
Votes
----------
Voter_Key
Candidate
Issues
Dist_Key
State_Key
""" 
class Vote():
    def __init__(self, voter_id, candidate_list, issues_list, states_list, districts_list):
        self.voter_id = voter_id
        self.candidate = random.randint(0, len(candidate_list) - 1)
        self.issues = random.sample([ i for i in range(len(issues_list))], random.randint(1, len(issues_list)))#pick a random combination of issues
        self.state = random.choice(states_list)['state']
        self.district = random.choice([ x for x in districts_list if x['state'] == self.state])['Number']
        
    def db_decode_candidate(self):
        if type(self.candidate) is int:
            self.candidate = candidate_list[self.candidate]
        
    def db_encode_candidate(self):
        if type(self.candidate) is str:
            self.candidate = candidate_list.index(self.candidate)

    def db_decode_issues(self):
        if type(self.issues[0]) is int:
            for i, issue in enumerate(self.issues):
                self.issues[i] = issues_list[issue]
        
    def db_encode_issues(self):
        if type(self.issues[0]) is str:
            for i, issue in enumerate(self.issues):
                self.issues[i] = issues_list.index(issue)
                
    def db_decode_all(self):
        self.db_decode_candidate()
        self.db_decode_issues()
        
    def db_encode_all(self):
        self.db_encode_candidate()
        self.db_encode_issues()
        
    def print_Vote(self):
        sys.stdout.write("voter_id = %d\ncandidate = %s\nissues = %s\nstate = %s\ndistrict = %d\n\n" % (self.voter_id, self.candidate, self.issues, self.state, self.district))

        
def test_Vote(VoterID_List):
    print "\n\n------------TESTING VOTE CLASS-----------------------\n\n"
    for i in range(0, 10):
        a_vote = Vote(VoterID_List[i], candidate_list, issues_list, states_list, districts_list)
        sys.stdout.write("%d.)" % (i))
        a_vote.print_Vote()
        
        a_vote.db_decode_all()
        sys.stdout.write("%d.)" % (i))
        a_vote.print_Vote()
        
        a_vote.db_encode_all()
        sys.stdout.write("%d.)" % (i))
        a_vote.print_Vote()
        
"""        
test_Voter()
test_Vote(voterID_list)
print voterID_list
"""

generate_all_states(states_list, all_state_classes)
generate_all_districts(districts_list, all_state_classes, all_district_classes)
generate_all_electoral_college(all_electoral_classes, all_state_classes, candidate_list)

"""----------------------------------------END---------------------------------------------"""