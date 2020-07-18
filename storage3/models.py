#!/usr/bin/env python3
from uuid import uuid4
from typing import List


class Requirement():
    """
    Requirements Class
    """
    def __init__(self):
        self.id = uuid4()
        self.__conditions = []
        self.__operator = ''
    @property
    def conditions(self):
        return self.__conditions
    @property
    def operator(self):
        return self.__operator
    def is_same(self, requirement):
        """ check if str conditions are same for now. Reqs too in future """
        for each in requirement.conditions:
            if type(each) == str:
                if not each in self.conditions:
                    return False
        for each in self.conditions:
            if type(each) == str:
                if not each in requirement.conditions:
                    return False
        return True
    def setup(self, operator: str, conditions: List) -> bool:
        """
        Instantiate the operator (str) and conditions (list).
        """
        if (not type(operator) == str) or (not type(conditions) == list):
            return False
        allowed_operators = ['and', 'or']
        if not operator in allowed_operators:
            return False
        for each in conditions:
            if not type(each) == str and not type(each) == Requirement:
                return False
        self.__operator = operator
        self.__conditions = conditions
        return True
    def validate(self, current_parameters: dict) -> bool:
        """
        Determine if the requirement is valid.
        """
        if self.operator == 'and':
            return self.and_operator(current_parameters)
        if self.operator == 'or':
            return self.or_operator(current_parameters)
        return False
    def and_operator(self, current_parameters):
        """
        Validates true if all conditions are true.
        """
        p = current_parameters
        if not 'requirement' in p:
            p['requirement'] = self
        for condition in self.conditions:
            if type(condition) == str:
                try:
                    if not eval(condition):
                        return False
                except Exception:
                    return False
            elif type(condition) == Requirement:
                if not condition.validate(p):
                    return False
        return True
    def or_operator(self, current_parameters):
        """
        Validates true if any conditions are true.
        """
        p = current_parameters
        if not 'requirement' in p:
            p['requirement'] = self
        for condition in self.conditions:
            if type(condition) == str:
                try:
                    if eval(condition):
                        return True
                except Exception:
                    return False
            elif type(condition) == Requirement:
                if condition.validate(p):
                    return True
        return False


class Authority():
    """
    Authority Class
    """
    every = []
    def __init__(self, original_grantor):
        self.id = str(uuid4())
        self.weilded_by = []
        self.over_whom = ''
        self.grantors = []
        self.__original_grantor = original_grantor
        self.action = ''
        self.grantable_action = ''
        self.requirement = Requirement()
        Authority.every.append(self)
    @property
    def original_grantor(self):
        return self.__original_grantor
    def print_self(self):
        print(self.action)
        print("OG")
        print(Personhood.every[self.original_grantor].name)
        print(self.requirement.conditions)
        print("WB")
        for each in self.weilded_by:
            print(Personhood.every[each].name)
        print("OV WHOM")
        for each in self.over_whom:
            print(Personhood.every[each].name)
    @classmethod
    def print_every(cls):
        print("\nAuthorities:\n")
        for auth in Authority.every:
            print('action:')
            print('   ', auth.action)
            print('over whom:')
            if type(auth.over_whom) == list:
                for u_id in auth.over_whom:
                    print('   ', Personhood.every[u_id].name)
            else:
                print('   ', Personhood.every[auth.over_whom].name)
            print('weilded by:')
            if type(auth.weilded_by) == list:
                for u_id in auth.weilded_by:
                    if u_id == '*':
                        print('    *')
                        continue
                    print('   ', Personhood.every[u_id].name)
            else:
                print(Personhood.every[auth.weilded_by].name)
            print('original grantor')
            if auth.original_grantor:
                print('   ', Personhood.every[auth.original_grantor].name)
            print('grantable action')
            print('   ', auth.grantable_action if hasattr(auth, 'grantable_action') else 'no grantable action')
            print('grantors:')
            for each in auth.grantors:
                print(Personhood.every[each].name)
            print()
        for k, mem in Personhood.every.items():
            print(mem.name, '\n', mem.id)
    








class Personhood():
    """
    personhood Class
    """
    every = {}
    def __init__(self, name):
        self.name = name
        self.id = str(uuid4())
        Personhood.every[self.id] = self
        Personhood.nonsharables = ['grant_authority_over_self', 'grant_meta_authority_over_self']
        self.invitations = {}
        self.teams = {}
    def revoke_authority(self, action, weilded_by, requirement):
        """ revoke a previously granted authority """
        if isinstance(weilded_by, Personhood):
            weilded_by = weilded_by.id
        elif not type(weilded_by) == str:
            print('weilded_by must be a str or instance of Personhood')
            return False
        for i in range(len(Authority.every)):
            auth = Authority.every[i]
            if (action == auth.action and weilded_by in auth.weilded_by
               and (self.id in auth.grantors or self.id == auth.original_grantor)
               and requirement.is_same(auth.requirement)):
                if self.id == auth.original_grantor or self.id in auth.original_grantor:
                    del Authority.every[i]
                    del auth
                    print('auth deleted')
                    return True
                for i in range(len(auth.grantors)):
                    if auth.grantors[i] == self.id:
                        del auth.grantors[i]
                if len(auth.grantors) == 0:
                    del Authority.every[i]
                    del auth
                    return True
                for i in range(len(auth.over_whom)):
                    if auth.over_whom[i] == self.id:
                        del auth.over_whom[i]
                        return True
        return False
    def has_authority_do(self, parameters):
        """ verify user has the authority to perform an action """
        p = parameters
        action = p['action']
        over_whom = p['over_whom']
        if type(over_whom) == Personhood:
            over_whom = over_whom.id
        if type(over_whom) == str and over_whom == self.id:
            return True
        if type(over_whom) == list and len(over_whom) == 0 and over_whom == self.id:
            return True
        elif not type(over_whom) == str:
            print('over_whom must be an id or Member obj')
        for auth in Authority.every:
            if (auth.action == action and (self.id in auth.weilded_by or '*' in auth.weilded_by) and
               over_whom in auth.over_whom and auth.requirement.validate(p)):
                return True
        return False
    def request_join_team(self, team):
        """
        requesting to join a team means granting the membership level
        authorities of that team to that team over self
        """
        if type(team) == str:
            try:
                team = Team.every[team]
            except KeyError:
                return False
        elif not isinstance(team, Team):
            return False
        p = {'action': 'request_join_team', 'over_whom': team.id}
        if not self.has_authority_do(p):
            return False
        # if team has already invited self, join team
        if team.id in self.invitations:
            team.membership[self.id] = self
            self.teams[team.id] = team
            del self.invitations[team.id]
            return True
        # otherwise, request to join
        team.invitations[self.id] = self
        return True
    def f(self, over_whom, x=None):
        if isinstance(over_whom, Personhood):
            over_whom = over_whom.id
        p = {'action': 'f', 'over_whom': over_whom, 'x': x}
        if not self.has_authority_do(p):
            print('no auth!')
            return False
        else:
            if type(over_whom) == str:
                print(self.name, 'performed the action over', Personhood.every[over_whom].name)
            elif type(over_whom) == Personhood:
                print(self.name, 'performed the action over', over_whom.name)
            return True
    def has_authority_grant_from_self(self, action):
        """
        Verify action is a method of self.__class__
        """
        return True if (action in self.__class__.__dict__
                       and action not in Personhood.nonsharables
                       and callable(eval('self.' + action))) else False
    def grant_authority_over_self(self, action, weilded_by, requirement):
        if not self.has_authority_grant_from_self(action):
            return False
        for auth in Authority.every:
            if (auth.action == action and self.id in auth.over_whom
               and requirement.is_same(auth.requirement)):
                added = []
                print('Authority already exists: ', auth.id)
                if type(weilded_by) == list:
                    for each in weilded_by:
                        if type(each) == str:
                            if not each in auth.weilded_by:
                                auth.weilded_by.append(each)
                                added.append(each)
                                print(Personhood.every[each].name, 'added to weilded_by')
                            else:
                                print(Personhood.every[each].name, 'already has that auth')
                        elif type(each) == Personhood:
                            if not each.id in auth.weilded_by:
                                auth.weilded_by.append(each.id)
                                added.append(each.id)
                                print(each.name, 'added to weilded_by')
                elif type(weilded_by) == Personhood:
                    if not weilded_by.id in auth.weilded_by:
                        auth.weilded_by.append(weilded_by.id)
                        added.append(weilded_by.id)
                        print(weilded_by.name, 'added to weilded_by')
                    else:
                        print(weilded_by.name, 'already has that auth')
                        return False
                elif type(weilded_by) == str:
                    if not weilded_by in auth.weilded_by:
                        print(Personhood.every[weilded_by].name, 'added to weilded_by')
                        auth.weilded_by.append(weilded_by)
                        added.append(weilded_by)
                    else:
                        print(Personhood.every[weilded_by].name, 'already has that auth')
                        return False
                if len(added) > 0:
                    return auth
        auth = Authority(self.id)
        auth.action = action
        auth.grantors = [self.id]
        auth.over_whom = [self.id]
        auth.requirement = requirement
        auth.weilded_by = []
        del auth.grantable_action
        if type(weilded_by) == list:
            for each in weilded_by:
                auth.weilded_by.append(each)
        elif type(weilded_by) == Personhood:
            auth.weilded_by.append(weilded_by.id)
        elif type(weilded_by) == str:
            auth.weilded_by.append(weilded_by)
        return auth
    def grant_meta_authority_over_self(self, action, weilded_by, over_whom, requirement):
        if not self.has_authority_grant_from_self(action):
            return False
        print("HAS AUTH TO GRANT META AUTH")
        for auth in Authority.every:
            if (auth.action == 'grant_authority_over_other'
               and auth.grantable_action == action
               and requirement.is_same(auth.requirement)
               and self.id == auth.original_grantor):
                new_weilded_by = False
                missing_weilded_by = False
                new_overs = False
                missing_overs = False
                if not type(weilded_by) == list:
                    if not type(weilded_by) == str:
                        if not type(weilded_by) == Personhood:
                            return False
                        weilded_by = weilded_by.id
                    weilded_by = [weilded_by]
                if not type(over_whom) == list:
                    if not type(over_whom) == str:
                        if not type(over_whom) == Personhood:
                            return False
                        over_whom = over_whom.id
                    over_whom = [over_whom]
                for each in weilded_by:
                    if type(each) == Personhood:
                        each = each.id
                    elif not type(each) == str:
                        return False
                for each in over_whom:
                    if type(each) == Personhood:
                        each = each.id
                    elif not type(each) == str:
                        return False
                for new in weilded_by:
                    if not new in auth.weilded_by:
                        new_weilded_by = True
                for existing in auth.weilded_by:
                    if not existing in weilded_by:
                        missing_weilded_by = True
                for new in over_whom:
                    if not new in auth.over_whom:
                        new_overs = True
                for existing in auth.over_whom:
                    if not existing in over_whom:
                        missing_overs = True
                if new_weilded_by and not new_overs and not missing_overs:
                    if type(weilded_by) == list:
                        for each in weilded_by:
                            if type(each) == Personhood:
                                if not each in auth.weilded_by:
                                    auth.weilded_by.append(each.id)
                                else:
                                    print(each.name, 'already has that auth')
                            if type(each) == str:
                                if not each in auth.weilded_by:
                                    auth.weilded_by.append(each)
                                else:
                                    print(Personhood.every[each].name, 'already has that auth')
                        return auth
                    elif type(weilded_by) == str:
                        auth.weilded_by.append(weilded_by)
                    elif type(weilded_by) == Personhood:
                        auth.weilded_by.append(weilded_by.id)
                elif new_overs and not new_weilded_by and not missing_weilded_by:
                    if type(over_whom) == list:
                        for each in over_whom:
                            if type(each) == str:
                                if not each in auth.over_whom:
                                    auth.over_whom.append(each)
                                else:
                                    print(Personhood.every[each].name, 'already has that auth')
                            if type(each) == Personhood:
                                auth.over_whom.append(each.id)
                    elif type(over_whom) == str:
                        auth.over_whom.append(over_whom)
                    elif type(over_whom) == Personhood:
                        auth.over_whom.append(over_whom.id)
                    return auth
                if not new_overs and not new_weilded_by:
                    return auth
        print(" CREATING NEW META AUTH")
        auth = Authority(self.id)
        auth.action = 'grant_authority_over_other'
        auth.grantable_action = action
        auth.grantors = [self.id]
        auth.requirement = requirement
        auth.over_whom = []
        if type(over_whom) == list:
            for each in over_whom:
                if type(each) == str:
                    auth.over_whom.append(each)
                elif type(each) == Personhood:
                    auth.over_whom.append(each.id)
                else:
                    print(each, 'is not neither a personhood not id')
        elif type(over_whom) == Personhood:
            auth.over_whom.append(over_whom.id)
        elif type(over_whom) == str:
            auth.over_whom.append
        auth.weilded_by = []
        if type(weilded_by) == list:
            for each in weilded_by:
                if type(each) == str:
                    auth.weilded_by.append(each)
                if type(each) == Personhood:
                    auth.weilded_by.append(each.id)
                else:
                    print(each, 'is not neither a personhood not id')
        elif type(weilded_by) == str:
            auth.weilded_by.append(weilded_by)
        elif type(weilded_by) == Personhood:
            auth.weilded_by.append(weilded_by.id)
        auth.print_self()
        return auth
    def has_authority_grant_over_other(self, action, weilded_by, over_whom, requirement):
        """ check if exists, check if req is valid, action == 'grant_authority_over_other',
            grantable authority == action """
        """ new edge case idea: if trying to add two groups to auth.overwhom so user2 can grant
            the auth to anyone in either t1 or t2, but someone is in both, then when revoking
            ability to grant auth to personhood of t2, you don't want to remove common personhood.
            So overwhom should be more than a simple list. It should be a dictionary of as many
            lists and ids as necessary. So it's like userid:userid, T1.id:T.personhoodhip """
        if type(over_whom) == Personhood:
            over_whom = over_whom.id
        for auth in Authority.every:
            p = {'action': action, 'weilded_by': weilded_by, 'over_whom': over_whom, 'requirement': requirement}
            if (auth.action == 'grant_authority_over_other'
               and auth.grantable_action == action
               and auth.original_grantor == over_whom
               and over_whom in auth.grantors
               and auth.requirement.validate(p)):
                if type(weilded_by) == list:
                    for each in weilded_by:
                        if type(each) == str:
                            # this isn't working. Gotta create a list of peeps to add in
                            # over_whom is not being checked?
                            if not Personhood.every[each].id in auth.over_whom:
                                return False
                        elif type(each) == Personhood:
                            if not each.id in auth.over_whom:
                                return False
                        else:
                            print('overwhom is formatted incorrectly')
                            return False
                elif type(weilded_by) == str:
                    if not weilded_by in auth.over_whom:
                        return False
                elif type(weilded_by) == Personhood:
                    if not weilded_by.id in auth.over_whom:
                        return False
                return True
        return False
    def grant_authority_over_other(self, action, weilded_by, over_whom, requirement):
        if type(over_whom) == Personhood:
            over_whom = over_whom.id
        if not self.has_authority_grant_over_other(action, weilded_by, over_whom, requirement):
            return False
        for auth in Authority.every:
            if (auth.original_grantor == over_whom
               and auth.action == action
               and auth.requirement.is_same(requirement)):
                added = []
                if type(weilded_by) == list:
                    for each in weilded_by:
                        if type(each) == str:
                            if each not in auth.weilded_by:
                                added.append(each)
                                auth.weilded_by.append(each)
                        elif type(each) == Personhood:
                            if each.id not in auth.weilded_by:
                                added.append(each)
                                auth.weilded_by.append(each.id)
                elif type(weilded_by) == str:
                    if weilded_by not in auth.weilded_by:
                        added.append(weilded_by)
                        auth.weilded_by.append(weilded_by)
                elif type(weilded_by) == Personhood:
                    if not weilded_by.id in auth.weilded_by:
                        added.append(weilded_by.id)
                        auth.weilded_by.append(weilded_by.id)
                if len(added) > 0:
                    auth.grantors.append(self.id)
                    return auth
        auth = Authority(over_whom)
        auth.action = action
        auth.grantors = [self.id]
        auth.requirement = requirement
        auth.over_whom = [over_whom]
        auth.weilded_by = []
        if type(weilded_by) == list:
            for each in weilded_by:
                if type(each) == str:
                    auth.weilded_by.append(each)
                if type(each) == Personhood:
                    auth.weilded_by.append(each.id)
        if type(weilded_by) == str:
            auth.weilded_by.append(weilded_by)
        if type(weilded_by) == Personhood:
            auth.weilded_by.append(weilded_by.id)
        return auth
    

class Team(Personhood):
    every = {}
    def __init__(self, name):
        super().__init__(name)
        Team.nonsharables = []
        Team.every[self.name] = self
        Team.every[self.id] = self
        self.membership = {}
        self.roles = {}
        auth = Authority(self.id)
        auth.action = 'request_join_team'
        auth.grantors = [self.id]
        auth.over_whom = [self.id]
        auth.weilded_by = ['*']
        r = Requirement()
        r.setup('and', ['True'])
        auth.requirement = r
        self.auths_over_members = {} # auths upon which membership is conditional
    def invite_member(self, member):
        if type(member) == str:
            try:
                member = Personhood.every[member]
            except KeyError:
                return False
        elif not isinstance(member, Personhood):
            return False
        print('one')
        # if member already requested to join, accept
        if member.id in self.invitations:
            print('invitation exists')
            # add member
            self.membership[member.id] = member
            # delete their previous request to join
            del self.invitations[member.id]
            added = []
            for auth in self.auths_over_members.values():
                # apply membership authorities to member
                print('Team authority to:', auth.action)
                if member.has_authority_grant_from_self(auth.action):
                    if not member.id == auth.over_whom and not member.id in auth.over_whom:
                        if type(auth.over_whom) == list:
                            auth.over_whom.append(member.id)
                        else:
                            auth.over_whom = [member.id]
                        auth.grantors.append(member.id)
                        added.append(auth)
                        print(member.name, 'added to weilded_by (hopefully)')
                else:
                    print('does not have auth')
                    for each in added:
                        for i in range(len(each.over_whom) - 1):
                            if each[i] == member.id:
                                del each[i]
                                return False
            for role in self.roles:
                for auth in role.auths_over_team_members:
                    print('Role authority to:', auth.action)
                    if not member.id == auth.over_whom and not member.id in auth.over_whom:
                        if type(auth.over_whom) == list:
                            auth.over_whom.append(member.id)
                        else:
                            auth.over_whom = [member.id]
                            auth.grantors.append(member.id)
                            added.append(auth)
                            print(member.name, 'added to weilded_by (hopefully)')
                    else:
                        for each in added:
                            for i in range(len(each.over_whom) - 1):
                                if each[i] == member.id:
                                    del each[i]
                                    return False
            member.teams[self.id] = self
            return True
        # otherwise, invite member to join
        print('two')
        member.invitations[self.id] = self
        print('invitation sent')
        return True
    def remove_member(self, member):
        del self.membership[member.id]


class Role(Team):
    def __init__(self, name):
        self.auths_over_team_members = []



"""
1. user excersises authority on self
2. user atempts excersise authority over another user
3. user grants authority to another user
4. user successfully excersises authority over another user
5. user grants authority to grant authority to a third user
6. user grants previously granted authority to a third user
7. that third user uses authority granted by proxy on first user
8. requirement for granted authority is changed, demonstrate
9. requirement for authority to grant is changed, demonstrate
10"""