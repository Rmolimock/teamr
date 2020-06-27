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
        self.grant_f, self.take_f = Member('grant_f'), Member('take_f')
        self.no_f = Member('user3')
        self.r = Requirement()
        conditions = ['True', 'p.get("x") < 10']
        # be sure to add variables like x with p.get and inner quotes
        self.r.setup('and', conditions)
    def test_grant_authority(self):
        """ grant another user the authority to perform func on self """
        self.assertTrue(self.grant_f.grant_authority_over_self('f', self.take_f.id, self.r).id)
    def test_has_authority(self):
        self.grant_f, self.take_f, self.no_f = Member('grant_f'), Member('take_f'), Member('no_f')
        p = {'action': 'f', 'over_whom': self.take_f.id, 'x': 5}
        print(self.grant_f.id, self.take_f.id, self.no_f.id)
        self.assertTrue(self.take_f.has_authority(p))
        self.assertFalse(self.no_f.has_authority(p))
        p = {'action': 'other', 'over_whom': self.grant_f.id, 'x': 5}
        self.assertFalse(self.take_f.has_authority(p))
    def test_use_granted_authority(self):
        self.assertTrue(self.take_f.f(self.grant_f.id, 5))
        self.u1, self.u2, self.u3 = Member('u1'), Member('u2'), Member('u3')
        self.user1 = Member('user1')
        self.assertTrue(self.user1.grant_authority_over_self('f', [self.u1, self.u2.id], self.r))
        p = {'action': 'f', 'over_whom': self.user1.id, 'x': 5}
        self.assertTrue(self.u2.has_authority(p))
        self.assertFalse(self.u3.has_authority(p))
        self.assertTrue(self.user1.grant_authority_over_self('f', self.u3, self.r))
        self.assertTrue(self.u3.has_authority(p))
    def test_grant_authority_again(self):
        """ attemp to grant an authority already grantable over self """
        self.assertFalse(self.grant_f.grant_authority_over_self('f', self.take_f.id, self.r))
    def test_grant_authority_new_weilded_by(self):
        """ grant an existing authority to a new weilded_by """
        self.user1 = Member('user1')
        self.user4 = Member('user4')
        self.assertTrue(self.user1.grant_authority_over_self('f', self.user4.id, self.r))
        p = {'action': 'f', 'over_whom': self.user1.id, 'x': 5}
        self.assertTrue(self.user4.has_authority(p))
        p = {'action': 'f', 'over_whom': self.user1.id, 'x': 15}
        self.assertFalse(self.user4.has_authority(p))
        p = {'action': 'other', 'over_whom': self.user1.id, 'x': 5}
        self.assertFalse(self.user4.has_authority(p))
    def test_grant_meta_authority(self):
        self.u1, self.u2, self.u3 = Member('u1'), Member('u2'), Member('u3')
        self.meta_grantor = Member('meta_grantor')
        self.meta_receiver = Member('meta_receiver')
        self.assertTrue(self.meta_grantor.grant_meta_authority_over_self('f', self.meta_receiver, [self.u1.id, self.u2.id], self.r))
        self.assertTrue(self.meta_grantor.grant_meta_authority_over_self('f', self.meta_receiver, [self.u1.id, self.u2.id, self.u3.id], self.r))
        p = {'action': 'f', 'over_whom': self.meta_grantor.id}
        self.assertFalse(self.meta_receiver.has_authority(p))
        self.r.setup('and', ['True'])
        self.assertTrue(self.meta_receiver.has_authority_grant_over_other('f', self.u1.id, self.meta_grantor.id, self.r))
        self.assertFalse(self.u1.has_authority(p))
        self.assertTrue(self.meta_receiver.grant_authority_over_other('f', [self.u1.id, self.u2.id], self.meta_grantor, self.r))
        self.assertTrue(self.u1.has_authority(p))
