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
        p['requirement'] = self
        for condition in self.conditions:
            if type(condition) == str:
                if not eval(condition):
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
        requirement = self
        p['requirement'] = self
        for condition in self.conditions:
            if type(condition) == str:
                if eval(condition):
                    return True
            elif type(condition) == Requirement:
                if condition.validate(p):
                    return True
        return False
        

class Authority():
    """
    Authority Class
    """
    def __init__(self, original_grantor):
        self.id = str(uuid4())
        self.weilded_by = []
        self.over_whom = ''
        self.grantors = []
        self.__original_grantor = original_grantor
        self.action = ''
        self.grantable_action = ''
        self.requirement = Requirement()
        Authorities.append(self)
    @property
    def original_grantor(self):
        return self.__original_grantor
    def print_self(self):
        print(self.action)
        print("OG")
        print(Member.members[self.original_grantor].name)
        print(self.requirement.conditions)
        print("WB")
        print(self.weilded_by)
        print("OV WHOM")
        print(self.over_whom)
    @classmethod
    def print_authorities(cls):
        print("\nAUTHORITIES:\n")
        for auth in Authorities:
            print('action:')
            print('   ', auth.action)
            print('over whom:')
            if type(auth.over_whom) == list:
                for u_id in auth.over_whom:
                    print('   ', Member.members[u_id].name)
            else:
                print('   ', Member.members[auth.over_whom].name)
            print('weilded by:')
            if type(auth.weilded_by) == list:
                for u_id in auth.weilded_by:
                    print('   ', Member.members[u_id].name)
            else:
                print(Member.members[auth.weilded_by].name)
            print('original grantor')
            print('   ', auth.original_grantor)
            print('grantable action')
            print('   ', auth.grantable_action if hasattr(auth, 'grantable_action') else 'no grantable action')
            print()
        for k, mem in Member.members.items():
            print(mem.name, '\n', mem.id)
    

Authorities = []


class Member():
    """
    Member Class
    """
    members = {}
    def __init__(self, name):
        self.name = name
        self.id = str(uuid4())
        Member.members[self.id] = self
        self.nonsharables = ['grant_authority_over_self', 'grant_meta_authority_over_self']
    def has_authority(self, parameters):
        """ verify user has the authority to perform an action """
        p = parameters
        if type(p['over_whom']) == str and p['over_whom'] == self.id:
            return True
        if type(p['over_whom']) == list and len(p['over_whom']) == 0 and p['over_whom'] == self.id:
            return True
        for auth in Authorities:
            if (auth.action == p['action'] and self.id in auth.weilded_by and
               p['over_whom'] in auth.over_whom and auth.requirement.validate(p)):
                return True
        return False
    def f(self, over_whom, x):
        p = {'action': 'f', 'over_whom': over_whom, 'x': x}
        if not self.has_authority(p):
            print('no auth!')
            return
        else:
            print(self.name, 'performed the action over', Member.members[over_whom].name)
            return True
    def has_authority_grant_from_self(self, action):
        """
        Verify action is a method of self.__class__
        """
        return True if (action in self.__class__.__dict__
                       and action not in self.nonsharables
                       and callable(eval('self.' + action))) else False
    def grant_authority_over_self(self, action, weilded_by, requirement):
        if not self.has_authority_grant_from_self(action):
            return False
        for auth in Authorities:
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
                                print(Member.members[each].name, 'added to weilded_by')
                            else:
                                print(Member.members[each].name, 'already has that auth')
                        elif type(each) == Member:
                            if not each.id in auth.weilded_by:
                                auth.weilded_by.append(each.id)
                                added.append(each.id)
                                print(each.name, 'added to weilded_by')
                elif type(weilded_by) == Member:
                    if not weilded_by.id in auth.weilded_by:
                        auth.weilded_by.append(weilded_by.id)
                        added.append(weilded_by.id)
                        print(weilded_by.name, 'added to weilded_by')
                    else:
                        print(weilded_by.name, 'already has that auth')
                        return False
                elif type(weilded_by) == str:
                    if not weilded_by in auth.weilded_by:
                        print(Member.members[weilded_by].name, 'added to weilded_by')
                        auth.weilded_by.append(weilded_by)
                        added.append(weilded_by)
                    else:
                        print(Member.members[weilded_by].name, 'already has that auth')
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
        elif type(weilded_by) == Member:
            auth.weilded_by.append(weilded_by.id)
        elif type(weilded_by) == str:
            auth.weilded_by.append(weilded_by)
        return auth
    def grant_meta_authority_over_self(self, action, weilded_by, over_whom, requirement):
        if not self.has_authority_grant_from_self(action):
            return False
        print("HAS AUTH TO GRANT META AUTH")
        for auth in Authorities:
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
                        if not type(weilded_by) == Member:
                            return False
                        weilded_by = weilded_by.id
                    weilded_by = [weilded_by]
                if not type(over_whom) == list:
                    if not type(over_whom) == str:
                        if not type(over_whom) == Member:
                            return False
                        over_whom = over_whom.id
                    over_whom = [over_whom]
                for each in weilded_by:
                    if type(each) == Member:
                        each = each.id
                    elif not type(each) == str:
                        return False
                for each in over_whom:
                    if type(each) == Member:
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
                            if type(each) == Member:
                                if not each in auth.weilded_by:
                                    auth.weilded_by.append(each.id)
                                else:
                                    print(each.name, 'already has that auth')
                            if type(each) == str:
                                if not each in auth.weilded_by:
                                    auth.weilded_by.append(each)
                                else:
                                    print(Member.members[each].name, 'already has that auth')
                        return auth
                    elif type(weilded_by) == str:
                        auth.weilded_by.append(weilded_by)
                    elif type(weilded_by) == Member:
                        auth.weilded_by.append(weilded_by.id)
                elif new_overs and not new_weilded_by and not missing_weilded_by:
                    if type(over_whom) == list:
                        for each in over_whom:
                            if type(each) == str:
                                if not each in auth.over_whom:
                                    auth.over_whom.append(each)
                                else:
                                    print(Member.members[each].name, 'already has that auth')
                            if type(each) == Member:
                                auth.over_whom.append(each.id)
                    elif type(over_whom) == str:
                        auth.over_whom.append(over_whom)
                    elif type(over_whom) == Member:
                        auth.over_whom.append(over_whom.id)
                    return auth
                if not new_overs and not new_weilded_by:
                    return auth
        print(" CREATING NEW META AUTH")
        print(self.name, 'grants grant of f to', weilded_by.name, 'to give to others')
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
                elif type(each) == Member:
                    auth.over_whom.append(each.id)
                else:
                    print(each, 'is not neither a member not id')
        elif type(over_whom) == Member:
            auth.over_whom.append(over_whom.id)
        elif type(over_whom) == str:
            auth.over_whom.append
        auth.weilded_by = []
        if type(weilded_by) == list:
            for each in weilded_by:
                if type(each) == str:
                    auth.weilded_by.append(each)
                if type(each) == Member:
                    auth.weilded_by.append(each.id)
                else:
                    print(each, 'is not neither a member not id')
        elif type(weilded_by) == str:
            auth.weilded_by.append(weilded_by)
        elif type(weilded_by) == Member:
            auth.weilded_by.append(weilded_by.id)
        auth.print_self()
        return auth
    def has_authority_grant_over_other(self, action, weilded_by, over_whom, requirement):
        """ check if exists, check if req is valid, action == 'grant_authority_over_other',
            grantable authority == action """
        """ new edge case idea: if trying to add two groups to auth.overwhom so user2 can grant
            the auth to anyone in either t1 or t2, but someone is in both, then when revoking
            ability to grant auth to members of t2, you don't want to remove common members.
            So overwhom should be more than a simple list. It should be a dictionary of as many
            lists and ids as necessary. So it's like userid:userid, T1.id:T.membership """
        for auth in Authorities:
            p = {'action': action, 'weilded_by': weilded_by, 'over_whom': over_whom, 'requirement': requirement}
            if (auth.action == 'grant_authority_over_other'
               and auth.grantable_action == action
               and auth.original_grantor == over_whom
               and over_whom in auth.grantors
               and auth.requirement.validate(p)):
                if type(weilded_by) == list:
                    for each in weilded_by:
                        if type(each) == str:
                            if not Member.members[each].id in auth.over_whom:
                                return False
                        elif type(each) == Member:
                            if not each.id in auth.over_whom:
                                return False
                        else:
                            print('overwhom is formatted incorrectly')
                            return False
                elif type(weilded_by) == str:
                    if not weilded_by in auth.over_whom:
                        return False
                elif type(weilded_by) == Member:
                    if not weilded_by.id in auth.over_whom:
                        return False
                return True
        return False
    def grant_authority_over_other(self, action, weilded_by, over_whom, requirement):
        if type(over_whom) == Member:
            over_whom = over_whom.id
        if not self.has_authority_grant_over_other(action, weilded_by, over_whom, requirement):
            return False
        for auth in Authorities:
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
                        elif type(each) == Member:
                            if each.id not in auth.weilded_by:
                                added.append(each)
                                auth.weilded_by.append(each.id)
                elif type(weilded_by) == str:
                    if weilded_by not in auth.weilded_by:
                        added.append(weilded_by)
                        auth.weilded_by.append(weilded_by)
                elif type(weilded_by) == Member:
                    if not weilded_by.id in auth.weilded_by:
                        added.append(weilded_by.id)
                        auth.weilded_by.append(weilded_by.id)
                if len(added) > 0:
                    auth.grantors.append(self.id)
                    return auth
        auth = Authority(over_whom)
        auth.action = action
        auth.grantors = [over_whom, self.id]
        auth.requirement = requirement
        auth.over_whom = [over_whom]
        auth.weilded_by = []
        if type(weilded_by) == list:
            for each in weilded_by:
                if type(each) == str:
                    auth.weilded_by.append(each)
                if type(each) == Member:
                    auth.weilded_by.append(each.id)
        if type(weilded_by) == str:
            auth.weilded_by.append(weilded_by)
        if type(weilded_by) == Member:
            auth.weilded_by.append(weilded_by.id)
        return auth
    

"""
                   
    def grant_authority_over_other(self, grantable_action, weilded_by, requirement):
        if not self.has_authority_grant_from_other():
            return False

    def has_authority_grant_other(self, action, weilded_by, requirement):
        Verify self has a matching authority.
        p = {'action': action, 'weilded_by': weilded_by,
             'requirement': requirement, 'over_whom': over_whom}
        for auth in Authorities:
            if (self.id in auth.weilded_by and over_whom == auth.over_whom
               and 'grant_authority' == auth.action
               and action == auth.grantable_action):
                if auth.requirement.validate(p):
                    return True
        return False





        Grant a currently held authority to another Member, Team, or Role.
        1. If over_whom != self:
            MEMBER B TRANSFERS AUTH TO DO X OVER MEMBER A TO MEMBER C
            a. create current_parameters dictionary from above parameters.
            b. if action == 'grant_authority':
                Confirm there is an authority where:
                    * auth.action == 'grant_authority'
                    * self is in auth.weilded_by
                    * auth.original_grantor == c
                    * over_whom is in auth.over_whom
                    * auth.requirement.validate(p) == True
            c. if action != 'grant_authority':
                Confirm there is an authority where:
                    * auth.action == action
                    * self in auth.weilded_by
                    * over_whom in auth.over_whom
                    * over_whom in auth.original_grantor
                    * auth.requirement.validate(p) == True
        2. If over_whom == self:
            MEMBER A GRANTS B THE AUTH TO DO X ON A
            Check if A has authority to do X.
                If over_whom == self:
                    Confirm eval(action) is a method of self.class.dict
                    Member A has authority
                If auth.over_whom != self:
                    check_authority()
"""