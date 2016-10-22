import sys
import random
from lists import Lists

L = Lists()
#L.json_read_test()
 

seed = random.seed()

class Electoral_College():
    def __init__(self, elector_id, state, theLists):
        self.evoter_id = elector_id
        self.state = state
        self.candidate = random.randint(0, len(theLists.candidate_list) - 1)
        theLists.all_electoral_classes.append(self)
        
    def db_decode_candidate(self, theLists):
        if type(self.candidate) is int:
            self.candidate = theLists.candidate_list[self.candidate]
        
    def db_encode_candidate(self, theLists):
        if type(self.candidate) is str:
            self.candidate = theLists.candidate_list.index(self.candidate)        

class District():
    def __init__(self, district, state, theLists):
        self.number = district['Number']
        self.state = state
        self.voters = []
        theLists.all_district_classes.append(self)
        
    def print_District(self):
        sys.stdout.write("Number = %d\nState = %s\n" % (self.number, self.state.abbr))

class State():
    def __init__(self, state, theLists):
        self.abbr = state['state']
        self.quant_districts = state['Quant_Districts']
        self.quant_registered = state['Quant_Registered']
        self.quant_electors = self.quant_districts + 2
        self.districts = []
        self.electors = []
        theLists.all_state_classes.append(self)
        
    def set_Districts(self, theLists):
        self.districts = [district for district in theLists.all_district_classes if district.state.abbr == self.abbr]
            
    def set_Electoral_College(self, theLists):
        self.electors = [elector for elector in theLists.all_electoral_classes if elector.state.abbr == self.abbr]
        
    def print_State(self):
        sys.stdout.write("abbr = %s\nquant_districts = %d\nquant_registered = %d\nquant_electors = %d\n" % (self.abbr, self.quant_districts, self.quant_registered, self.quant_electors))
        sys.stdout.write("Districts: ")
        print [district.number for district in self.districts]
        sys.stdout.write("Electors: ")
        print [elector.evoter_id for elector in self.electors]
        
def generate_all_states(theLists):
    for state in theLists.states_list:
        State(state, theLists)
        
def generate_all_districts(theLists):
    
    for state in theLists.all_state_classes:
        for district in theLists.districts_list:
            if district['state'] == state.abbr:
                District(district, state, theLists)
        state.set_Districts(theLists)  
                
def generate_all_electoral_college(theLists):
    for state in theLists.all_state_classes:
        for i in range(1, state.quant_electors + 1):
            Electoral_College(i, state, theLists)
        state.set_Electoral_College(theLists)

def display_all_states(theLists):
    for state in theLists.all_state_classes:
        print "\n"
        state.print_State()
        
def display_all_districts(theLists):
    for district in theLists.all_district_classes:
        print "\n"
        district.print_District()



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
    def __init__(self, theLists):
        self.id = 0
        while self.id in theLists.voterID_list or self.id == 0:
            self.id = random.randrange(100000)
        
        self.party = random.choice(['D', 'R', 'G', 'L', 'I', 'O'])
        self.age = random.randrange(18, 105)
        self.sex = random.choice(['M', 'F'])
        self.income_lvl = random.randint(0, len(theLists.income_list) - 1)
        self.ethnicity = random.sample([ i for i in range(len(theLists.ethnicity_list))], random.randint(1, len(theLists.ethnicity_list)))#pick a random combination of ethnicities
        self.education_lvl = random.randint(0, len(theLists.education_lvl_list) - 1)
        
        theLists.voterID_list.append(self.id)
        
    def print_Voter(self):
        sys.stdout.write("id = %d\nparty = %c\nage = %d\nsex = %c\nincome_lvl = %s\nethnicity = %s\neducation_lvl = %s\n\n" % (self.id, self.party, self.age, self.sex, self.income_lvl, self.ethnicity, self.education_lvl))
    
    def db_decode_income(self, theLists):
        if type(self.income_lvl) is int:
            self.income_lvl = theLists.income_list[self.income_lvl]
        
    def db_encode_income(self, theLists):
        if type(self.income_lvl) is str:
            self.income_lvl = theLists.income_list.index(self.income_lvl)

    def db_decode_ethnicity(self, theLists):
        if type(self.ethnicity[0]) is int:
            for i, ethnicity in enumerate(self.ethnicity):
                self.ethnicity[i] = theLists.ethnicity_list[ethnicity]
        
    def db_encode_ethnicity(self, theLists):
        if type(self.ethnicity[0]) is str:
            for i, ethnicity in enumerate(self.ethnicity):
                self.ethnicity[i] = theLists.ethnicity_list.index(ethnicity)
            
    def db_decode_education_lvl(self, theLists):
        if type(self.education_lvl) is int:
            self.education_lvl = theLists.education_lvl_list[self.education_lvl]
        
    def db_encode_education_lvl(self, theLists):
        if type(self.education_lvl) is str:
            self.education_lvl = theLists.education_lvl_list.index(self.education_lvl)
            
    def db_decode_all(self, theLists):
        self.db_decode_income(theLists)
        self.db_decode_ethnicity(theLists)
        self.db_decode_education_lvl(theLists)
        
    def db_encode_all(self, theLists):
        self.db_encode_income(theLists)
        self.db_encode_ethnicity(theLists)
        self.db_encode_education_lvl(theLists)

#just a simple test of the basic Voter stuff
def test_Voter(theLists):
    print "\n\n------------TESTING VOTER CLASS-----------------------\n\n"
    for i in range(0, 10):
        a_voter = Voter(theLists)
        sys.stdout.write("%d.)" % (i))
        a_voter.print_Voter()
        
        a_voter.db_decode_all(theLists)
        sys.stdout.write("%d.)" % (i))
        a_voter.print_Voter()
        
        a_voter.db_encode_all(theLists)
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
    def __init__(self, voter_id, theLists):
        self.voter_id = voter_id
        self.candidate = random.randint(0, len(theLists.candidate_list) - 1)
        self.issues = random.sample([ i for i in range(len(theLists.issues_list))], random.randint(1, len(theLists.issues_list)))#pick a random combination of issues
        self.state = random.choice(theLists.states_list)['state']
        self.district = random.choice([ x for x in theLists.districts_list if x['state'] == self.state])['Number']
        
    def db_decode_candidate(self, theLists):
        if type(self.candidate) is int:
            self.candidate = theLists.candidate_list[self.candidate]
        
    def db_encode_candidate(self, theLists):
        if type(self.candidate) is str:
            self.candidate = theLists.candidate_list.index(self.candidate)

    def db_decode_issues(self, theLists):
        if type(self.issues[0]) is int:
            for i, issue in enumerate(self.issues):
                self.issues[i] = theLists.issues_list[issue]
        
    def db_encode_issues(self, theLists):
        if type(self.issues[0]) is str:
            for i, issue in enumerate(self.issues):
                self.issues[i] = theLists.issues_list.index(issue)
                
    def db_decode_all(self, theLists):
        self.db_decode_candidate(theLists)
        self.db_decode_issues(theLists)
        
    def db_encode_all(self, theLists):
        self.db_encode_candidate(theLists)
        self.db_encode_issues(theLists)
        
    def print_Vote(self):
        sys.stdout.write("voter_id = %d\ncandidate = %s\nissues = %s\nstate = %s\ndistrict = %d\n\n" % (self.voter_id, self.candidate, self.issues, self.state, self.district))

        
def test_Vote(theLists):
    print "\n\n------------TESTING VOTE CLASS-----------------------\n\n"
    for i in range(0, 10):
        a_vote = Vote(theLists.voterID_list[i], theLists)
        sys.stdout.write("%d.)" % (i))
        a_vote.print_Vote()
        
        a_vote.db_decode_all(theLists)
        sys.stdout.write("%d.)" % (i))
        a_vote.print_Vote()
        
        a_vote.db_encode_all(theLists)
        sys.stdout.write("%d.)" % (i))
        a_vote.print_Vote()
        
"""        
test_Voter()
test_Vote(voterID_list)
print voterID_list
"""



"""
generate_all_states(L)
generate_all_districts(L)
generate_all_electoral_college(L)


display_all_states(L)
display_all_districts(L)


test_Voter(L)
test_Vote(L)
"""
"""----------------------------------------END---------------------------------------------"""