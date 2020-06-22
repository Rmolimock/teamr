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
        weilded_by = p.get('weilded_by')
        over_whom = p.get('over_whom')
        grantors = p.get('grantors')
        original_grantor = p.get('original_grantor')
        action = p.get('action')
        requirement = self
        parameters = p.get('parameters')
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
        weilded_by = p.get('weilded_by')
        over_whom = p.get('over_whom')
        grantors = p.get('grantors')
        original_grantor = p.get('original_grantor')
        action = p.get('action')
        requirement = self
        parameters = p.get('parameters')
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
        self.granted_action = ''
        self.requirement = Requirement()
    @property
    def original_grantor(self):
        return self.__original_grantor
    

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
        self.nonsharables = ['grant_authority_over_self', 'grant_meta_authority_to_others']
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
                print('Authority already exists: ', auth.id)
                if type(weilded_by) == list:
                    for each in weilded_by:
                        if not each.id in auth.weilded_by:
                            auth.weilded_by.append(each.id)
                            print(Member.members[each].name, 'added to weilded_by')
                            return True
                        else:
                            print(Member.members[each].name, 'already has that auth')
                            return False
                elif type(weilded_by) == Member:
                    if not weilded_by.id in auth.weilded_by:
                        auth.weilded_by.append(weilded_by.id)
                        print(weilded_by.name, 'added to weilded_by')
                        return True
                    else:
                        print(weilded_by.name, 'already has that auth')
                        return False
                elif type(weilded_by) == str:
                    if not weilded_by in auth.weilded_by:
                        print(Member.members[weilded_by].name, 'added to weilded_by')
                        auth.weilded_by.append(weilded_by)
                        return True
                    else:
                        print(Member.members[weilded_by].name, 'already has that auth')
                        return False
        auth = Authority(self.id)
        auth.action = action
        auth.grantors = [self.id]
        auth.over_whom = self.id
        auth.requirement = requirement
        auth.weilded_by = []
        del auth.granted_action
        if type(weilded_by) == list:
            for each in weilded_by:
                auth.weilded_by.append(each)
        elif type(weilded_by) == Member:
            auth.weilded_by.append(weilded_by.id)
        elif type(weilded_by) == str:
            auth.weilded_by.append(weilded_by)
        Authorities.append(auth)
        return auth
    def grant_meta_authority_to_others(self, action, weilded_by, over_whom, requirement):
        if not self.has_authority_grant_from_self(action):
            return False
        for auth in Authorities:
            if (auth.action == 'grant_authority_over_other'
               and auth.granted_action == action
               and requirement.is_same(auth.requirement)):
                new_weilded_by = False
                missing_weilded_by = False
                new_overs = False
                missing_overs = False
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
                    for each in weilded_by:
                        auth.weilded_by.append(each)
                    return auth
                elif new_overs and not new_weilded_by and not missing_weilded_by:
                    for each in over_whom:
                        auth.over_whom.append(each)
                    return auth
        auth = Authority(self.id)
        auth.action = 'grant_authority_over_other'
        auth.granted_action = action
        auth.grantors = [self.id]
        auth.requirement = requirement
        auth.over_whom = []
        for each in over_whom:
            auth.over_whom.append(each)
        auth.weilded_by = []
        for each in weilded_by:
            auth.weilded_by.append(each)
        Authorities.append(auth)
        return auth
    def grant_authority_over_other(self, action, weilded_by, over_whom, requirement):
        if not self.has_authority_grant_other(action, weilded_by, over_whom):
            return False
        for auth in Authorities:
            if (auth.action == action
               and requirement.is_same(auth.requirement)
               and over_whom == auth.original_grantor):
                for each in weilded_by:
                    if not each in auth.weilded_by:
                        auth.weilded_by.append(each)
                    return auth
        auth = Authority(self.id)
        auth.action = action
        auth.grantors = [over_whom, self.id]
        auth.original_grantor = over_whom
        auth.requirement = requirement
        auth.over_whom = over_whom
        auth.weilded_by = []
        for each in weilded_by:
            auth.weilded_by.append(each)
        Authorities.append(auth)
        return auth
    


                   
    def grant_authority_over_other(self, granted_action, weilded_by, requirement):
        if not self.has_authority_grant_from_other():
            return False

    def has_authority_grant_other(self, action, weilded_by, requirement):
        """
        Verify self has a matching authority.
        """
        p = {'action': action, 'weilded_by': weilded_by,
             'requirement': requirement, 'over_whom': over_whom}
        for auth in Authorities:
            if (self.id in auth.weilded_by and over_whom == auth.over_whom
               and 'grant_authority' == auth.action
               and action == auth.granted_action):
                if auth.requirement.validate(p):
                    return True
        return False





"""
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