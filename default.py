#!/usr/bin/env python3
class Requirement():
    """ Requirement class """
    def __init__(self):
        self.__conditions = []
        self.__operator = ''
    @property
    def operator(self):
        return self.__operator
    @property
    def conditions(self):
        return self.__conditions
    @conditions.setter
    def conditions(self, value):
        if not type(value) == str or type(value) == list:
            return False
        self.__conditions = value
    @operator.setter
    def operator(self, value):
        if not type(value) == str:
            return False
        self.__operator = value
    def create(self, operator, conditions):
        """ create a single rule """
        if not type(operator) == str:
            print('operator must be a string')
            return False
        if not type(conditions) == list:
            if not type(conditions) == Requirement:
                if not type(conditions) == str:
                    print('conditions must be strings or Requirement objects')
                    return False
            self.__conditions = [conditions]
            self.__operator = operator
            return True
        for c in conditions:
            if not type(c) == str and not type(c) == Requirement:
                print('conditions must be strings or Requirement objects')
                return False
        self.__conditions = conditions
        self.__operator = operator
    def validate(self, auth):
        """ validate all requirements for action """
        if self.operator == 'and':
            return self.and_operator(auth)
        if self.operator == 'or':
            return self.or_operator(auth)
    def and_operator(self, auth):
        member = auth['member']
        subject = auth['subject']
        action = auth['action']
        parameters = auth['parameters']
        for condition in self.conditions:
            if type(condition) == str:
                    # something like:
                    #   'member.uid == 123'
                    # or:
                    #   '"arg" in parameters'
                    #   'parameters[arg] == 987
                if not eval(condition):
                    return False
            elif type(condition) == Requirement:
                if not condition.validate(auth):
                    return False
        return True
    def or_operator(self, auth):
        member = auth['member']
        subject = auth['subject']
        action = auth['action']
        parameters = auth['parameters']
        for condition in self.conditions:
            if type(condition) == str:
                if eval(condition):
                    return True
            elif type(condition) == Requirement:
                if condition.validate(auth):
                    return True
            return False






class Member():
    def __init__(self, name):
        from uuid import uuid4
        self.uid = str(uuid4())
        self.name = name
        self.teams = {}
        self.roles = {}
        self.subject_to = {True: {'example_action': {False: False}}}
        self.authority_over = {self.uid: {'example_action': {True: True, '__transferable__': False}},
                               None: {'example_action': {False: False}}
                               }
    # simple get/print/format helper methods
    def example_action(self):
        """ empty method """
        return
    def get_auth_by_uid(self, uid):
        """
        return the actions and their requirements by given uid
        """
        if uid not in self.authority_over:
            return {}
        return self.authority_over[uid]
    def get_auth_by_action(self, action):
        """
        return uids the member has authority to perform a given action on
        """
        uids = {}
        for key, action_dict in self.authority_over.items():
            if action in action_dict:
                uids[key] = {action: {}}
                for r in action_dict[action]:
                    uids[key][action][r] = r
        return uids
    def print_authorities(self):
        """
        print a representation of the member's authorities
        """
        for s in self.authority_over:
            print('uid:')
            print("    {}".format(s))
            print()
            for a in self.authority_over[s]:
                print('    ACTION:')
                print("        {}".format(a))
                print()
                for r in self.authority_over[s][a]:
                    print('        REQUIREMENT:')
                    print("            {}".format(r))
        return True
    def format_action(self, action):
        """
        format action from obj.method() to obj and method
        """
        # action
        if '.' in action:
            action = action.split('.')[1]
        while action.endswith('()') or action.endswith('(') or action.endswith(')'):
            while action.endswith('()'):
                action = action[:-2]
            while action.endswith('(') or action.endswith(')'):
                action = action[:-1]
        return action
    # methods that handle Member authorities
    def has_authority(self, action, uid, parameters=None):
        """
        check if member has the authority to perform an action on the given
        uid, and if all requirements are met.
        uid: entity on which member is peforming the action
        action: the action being performed on uid
        """
        if not type(action) == str:
            raise TypeError('action must be a string, ex: "user.method" ')
        action = self.format_action(action)
        try:
            # check if action is a valuid function for member
            # eval should be safe here because format_action removes any () 
            eval('self.' + action)
        except AttributeError:
            print(self.name + ' does not have that method')
            return False
        except Exception as e:
            raise e
        if uid == self:
            return action
        if uid not in self.authority_over:
            return False
        if action not in self.authority_over[uid]:
            return False
        requirement = self.authority_over[uid][action]
        auth = {'member': self, 
                 'subject': uid,
                 'action': action,
                 'parameters': parameters}
        if not requirement.validate(auth):
            return False
        return action
    def grant_authority(self, action, subject, requirements=False):
        """
        member yields an authority over themselves to another entity
        """
        # HEY create optional giver parameter for being more explicit about
        # over whom the authority is that's transfering from giver->reciever.
        # WHAT ABOU PARAMETERS*************
        # FIX uid so it's the uid you're giving the auth to!
        # one possibility for dealing with transferable authorities is
        # to have a special __transferable__ key in self.authority_over[uid]
        # where uid is not self. This would have it's own requirements just
        # like an action key would, meaning the authority is tranferable so long
        # as given requirements evaluate true
        # rework this so you create the dict (or sub dict) first then enter it into
        # subject.auth_over at the end, same time enter uuid into self.subject_to
        # change uid in THIS METHOD ONLY to subject
        # verify member has the authority they're trying to grant to other
        # member, and that it's transferable
        # you'll have to rework has authority to handle transfering auths from other members
        action = self.has_authority(action, self)
        if not action:
            return False
        uid_auth = subject.get_auth_by_uid(self)
        if not uid_auth:
            subject.authority_over[self.uid] = {action: {}}
        elif not action in uid_auth:
            subject.authority_over[self.uid][action] = {}
        if requirements:
            for r in requirements:
                subject.authority_over[self.uid][action][r] = r
        else:
            subject.authority_over[self.uid][action][True] = True
        if not subject.uid in self.subject_to:
            self.subject_to[subject.uid] = {action: {}}
        else:
            self.subject_to[subject.uid][action] = {}
        if requirements:
            for r in requirements:
                self.subject_to[subject.uid][action][r] = r
        else:
            self.subject_to[subject.uid][action][True] = True
        return True
    def relinquish_authority(self, action, uid):
        """
        relinquish an authority that Member already has where action is entity.action
        """
        action = self.has_authority(action, uid)
        if not action:
            return False
        uid, action = self.format_action(action)
        if uid == self:
            raise('self ownership is immutable')
        if not uid in self.authority_over:
            return False
        if action and action not in self.authority_over[uid]:
            return False
        if not action:
            del self.authority_over[uid]
            return True
        del self.authority_over[uid][action]
        """ next up is revoke_authority(): """
        return True





