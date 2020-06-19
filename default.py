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
    def setup(self, operator: str, conditions: List) -> bool:
        """
        Instantiate the operator (str) and conditions (list).
        """
        if not type(operator) == str or not conditions == list:
            return False
        allowed_operators = ['and', 'or']
        allowed_conditions = ['1 == 1', '1 == 2']
        if not operator in allowed_operators:
            return False
        for each in conditions:
            if not type(each) == str and not type(each) == Requirement:
                return False
            if each not in allowed_conditions:
                return False
        self.__operator = operator
        self.__conditions = conditions
        return True
    def validate(self, current_parameters: dict) -> bool:
        """
        Determine if the requirement is valid.
        """
        return eval(self.operator + '_operator(current_parameters')
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
        parameters = p('parameters')
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
        parameters = p('parameters')
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
        self.id = uuid4()
        self.weilded_by = []
        self.over_whom = []
        self.grantors = []
        self.__original_grantor = original_grantor
        self.action = ''
        self.granted_action = ''
        self.requirement = Requirement()
    @property
    def original_grantor(self):
        return self.__original_grantor
    

Authorities = [Authority()]


class Member():
    """
    Member Class
    """
    def __init__(self, name):
        self.name = name
        self.id = uuid4()
    def grant_authority_over_self(self, action, weilded_by, requirement):
        if not self.has_authority_grant_from_self(action):
            return False
        for auth in Authorities:
            if (auth.action == action and self in auth.over_whom
               and requirement.is_same(auth.requirement)):
                for each in weilded_by:
                   auth.weilded_by.append(each)
                return True
        auth = Authority(self.id)
        auth.action = action
        auth.grantors = [self.id]
        auth.over_whom = self.id
        auth.requirement = requirement
        auth.weilded_by = []
        del auth.granted_action
        for each in weilded_by:
            auth.weilded_by.append(each)
    def same_weilded_by_and_over_whom(self, auth, weilded_by, over_whom):
        
    def grant_meta_authority_to_others(self, action, weilded_by, over_whom, requirement):
        if not self.has_authority_grant_from_self(action):
            return False
        for auth in Authorities:
            if (auth.action == 'grant_authority'
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
        auth.action = 'grant_authority'
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
    def has_authority_grant_from_self(self, action):
        """
        Verify action is a method of class self.
        """
        return True if action in self.__class__.__dict__ else False
    def has_authority_grant_other(self, action, weilded_by, requirement):
        """
        Verify self has a matching authority.
        """
        p = {'action': action, 'weilded_by': weilded_by,
             'requirement': requirement, 'over_whom': over_whom}
        for auth in Authorities:
            if (self in auth.weilded_by and over_whom == auth.over_whom
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