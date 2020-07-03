import unittest
from models import Personhood, Authority, Requirement, Team

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
        
        



class TestPersonhood(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.a, self.b, self.c = Personhood('a'), Personhood('b'), Personhood('c')
        self.r = Requirement()
        conditions = ['True', 'p.get("x") < 10']
        # be sure to add variables like x with p.get and inner quotes
        self.r.setup('and', conditions)
    def test_grant_authority(self):
        """ grant another user the authority to perform func on self """
        self.assertTrue(self.a.grant_authority_over_self('f', self.b.id, self.r))
    def test_has_authority_do(self):
        p = {'action': 'f', 'over_whom': self.b.id, 'x': 5}
        print(self.a.id, self.b.id, self.c.id)
        self.assertTrue(self.b.has_authority_do(p))
        self.assertFalse(self.c.has_authority_do(p))
        p = {'action': 'other', 'over_whom': self.a.id, 'x': 5}
        self.assertFalse(self.b.has_authority_do(p))
    def test_use_granted_authority(self):
        self.assertTrue(self.b.f(self.a.id, 5))
        self.assertTrue(self.a.grant_authority_over_self('f', [self.a, self.b.id], self.r))
        p = {'action': 'f', 'over_whom': self.a.id, 'x': 5}
        self.assertTrue(self.b.has_authority_do(p))
        self.assertFalse(self.c.has_authority_do(p))
        self.assertTrue(self.a.grant_authority_over_self('f', self.c, self.r))
        self.assertTrue(self.c.has_authority_do(p))
    def test_grant_authority_again(self):
        """ attemp to grant an authority already grantable over self """
        self.assertFalse(self.a.grant_authority_over_self('f', self.b.id, self.r))
    def test_grant_authority_new_weilded_by(self):
        """ grant an existing authority to a new weilded_by """
        self.a = Personhood('a')
        self.user4 = Personhood('user4')
        self.assertTrue(self.a.grant_authority_over_self('f', self.user4.id, self.r))
        p = {'action': 'f', 'over_whom': self.a.id, 'x': 5}
        self.assertTrue(self.user4.has_authority_do(p))
        p = {'action': 'f', 'over_whom': self.a.id, 'x': 15}
        self.assertFalse(self.user4.has_authority_do(p))
        p = {'action': 'other', 'over_whom': self.a.id, 'x': 5}
        self.assertFalse(self.user4.has_authority_do(p))
    def test_grant_meta_authority(self):
        self.a, self.b, self.c = Personhood('a'), Personhood('b'), Personhood('c')
        self.meta_grantor = Personhood('meta_grantor')
        self.meta_receiver = Personhood('meta_receiver')
        self.assertTrue(self.meta_grantor.grant_meta_authority_over_self('f', self.meta_receiver, [self.a.id, self.b.id], self.r))
        self.assertTrue(self.meta_grantor.grant_meta_authority_over_self('f', self.meta_receiver, [self.a.id, self.b.id, self.c.id], self.r))
        p = {'action': 'f', 'over_whom': self.meta_grantor.id}
        self.assertFalse(self.meta_receiver.has_authority_do(p))
        self.r.setup('and', ['True'])
        self.assertTrue(self.meta_receiver.has_authority_grant_over_other('f', self.a.id, self.meta_grantor.id, self.r))
        self.assertFalse(self.a.has_authority_do(p))
        self.assertTrue(self.meta_receiver.grant_authority_over_other('f', [self.a.id, self.b.id], self.meta_grantor, self.r))
        self.assertTrue(self.meta_receiver.grant_authority_over_other('f', self.c, self.meta_grantor, self.r))
        self.assertTrue(self.a.has_authority_do(p))
        self.assertTrue(self.b.has_authority_do(p))
        self.assertTrue(self.c.has_authority_do(p))
        self.assertTrue(self.c.f(self.meta_grantor.id, 10))
        self.assertTrue(self.c.grant_meta_authority_over_self('f', self.meta_receiver, [self.a.id, self.b.id], self.r))
        p = {'action': 'f', 'over_whom': self.c.id}
        self.assertFalse(self.b.has_authority_do(p))
        self.assertTrue(self.meta_receiver.grant_authority_over_other('f', self.b, self.c, self.r))
        self.assertTrue(self.b.has_authority_do(p))
        self.assertFalse(self.b.grant_meta_authority_over_self('grant_meta_authority_over_self', self.meta_receiver, [self.a.id, self.b.id], self.r))
        self.assertFalse(self.b.grant_meta_authority_over_self('grant_meta_authority_over_self', self.meta_receiver, [self.a.id, self.b.id], self.r))
        self.assertFalse(self.b.grant_meta_authority_over_self('nonexistent', self.meta_receiver, [self.a.id, self.b.id], self.r))
    def test_request_join_team(self):
        self.t1 = Team('t1')
        self.a.request_join_team(self.t1)
        self.assertTrue(self.a.id in self.t1.invitations)
        self.assertFalse(self.a.id in self.t1.membership)
        self.t1.invite_member(self.a)
        self.assertTrue(self.a.id in self.t1.membership)

class TestTeams(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.a, self.b, self.c = Personhood('a'), Personhood('b'), Personhood('c')
        self.r = Requirement()
        conditions = ['True', 'over_whom in Team.every["t2"].membership']
        # be sure to add variables like x with p.get and inner quotes
        self.r.setup('and', conditions)
        self.t1, self.t2, self.t3 = Team('t1'), Team('t2'), Team('t3')
    def test_invitation(self):
        self.t1.invite_member(self.a)
        print('a invitations:')
        print(self.a.invitations)
        print('members:')
        self.assertTrue(self.a.request_join_team(self.t1))
        self.assertTrue(self.c.request_join_team(self.t1.id))
        self.assertTrue(self.a.id in self.t1.membership)
    def test_auths_over_members(self):
        self.auth = Authority(None)  
        self.auth.action = 'f'
        self.auth.weilded_by = self.t1.id
        self.auth.requirement = self.r
        self.auth.over_whom = [self.c.id]
        self.t1.auths_over_members.append(self.auth)
        Authority.print_every()
        self.a.request_join_team(self.t1)
        self.t1.invite_member(self.a)
        Authority.print_every()
        print([Personhood.every[each].name for each in self.t1.membership])
