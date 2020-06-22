import unittest
from models import Member, Authority, Requirement, Authorities



class TestRequirement(unittest.TestCase):
    def setUp(self):
        self.r = Requirement()
        self.r2 = Requirement()
        self.r3 = Requirement()
    def test_setup_fail(self):
        self.conditions1 = ['True', 'False']
        self.assertFalse(self.r.setup('or', 'True'))
        self.assertFalse(self.r.setup('ljdsljk', ['True']))
        self.assertFalse(self.r.setup('and', self.r2))    
    def test_setup_pass(self):
        self.assertTrue(self.r.setup('or', ['True']))
        self.assertTrue(self.r.setup('and', []))
        self.assertTrue(self.r.setup('and', [self.r2, self.r3]))

    def test_setup_and_fail(self):
        self.conditions1 = ['True', 'False']
        self.r.setup('and', self.conditions1)
        self.assertFalse(self.r.validate({}))
    def test_setup_and_pass(self):
        self.conditions2 = ['True', 'True']
        self.r.setup('and', self.conditions2)
        self.assertTrue(self.r.validate({}))
    def test_setup_or_fail(self):
        self.conditions1 = ['False', 'False']
        self.r.setup('or', self.conditions1)
        self.assertFalse(self.r.validate({}))
    def test_setup_or_pass(self):
        self.conditions2 = ['True', 'False']
        self.r.setup('or', self.conditions2)
        self.assertTrue(self.r.validate({}))
    def test_requirement_validate(self):
        self.r.setup('and', ['p.get("x") < 10'])
        p = {'x': 5}
        self.assertTrue(self.r.validate(p))
        p = {'x': 11}
        self.assertFalse(self.r.validate(p))
    def test_is_same(self):
        self.r.setup('and', ['p.get("x") < 10'])
        self.r2.setup('and', ['p.get("x") < 10'])
        self.assertTrue(self.r.is_same(self.r2))
        
        



class TestMember(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.user1, self.user2 = Member('user1'), Member('user2')
        self.user3 = Member('user3')
        self.r = Requirement()
        conditions = ['True', 'p.get("x") < 10']
        # be sure to add variables like x with p.get and inner quotes
        self.r.setup('and', conditions)
    def test_grant_authority(self):
        """ grant another user the authority to perform func on self """
        self.assertTrue(self.user1.grant_authority_over_self('f', self.user2.id, self.r).id)
    def test_has_authority(self):
        p = {'action': 'f', 'over_whom': self.user1.id, 'x': 5}
        print(self.user1.id, self.user2.id, self.user3.id)
        self.assertTrue(self.user2.has_authority(p))
        self.assertFalse(self.user3.has_authority(p))
    def test_use_granted_authority(self):
        self.assertTrue(self.user2.f(self.user1.id, 5))
    def test_grant_authority_again(self):
        """ attemp to grant an authority already granted over self """
        self.assertFalse(self.user1.grant_authority_over_self('f', self.user2.id, self.r))
    def test_grant_authority_new_weilded_by(self):
        """ grant an existing authority to a new weilded_by """
        '''
        self.assertTrue(self.user1.grant_authority_over_self('f', self.user3.id, self.r))
        '''
        

