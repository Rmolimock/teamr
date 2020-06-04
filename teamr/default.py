#!/usr/bin/env python3
class Member():
    def __init__(self, name):
        self.name = name
        self.teams = {}
        self.roles = {}
        self.subject_to = {}
        self.authority_over = {self: {'*': {True: True}},
                               None: {'example_action': {False: False}}
                               }
    def get_auth_by_subject(self, subject):
        """
        return the actions and their requirements by given subject
        """
        if subject not in self.authority_over:
            return {}
        return self.authority_over[subject]
    def get_auth_by_action(self, action):
        """
        return subjects the member has authority to perform a given action on
        """
        subjects = {}
        for subject in self.authority_over:
            if action in self.authority_over[subject]:
                subjects[subject] = subject
        return subjects
    def grant_authority(self, subject, action, requirements=False):
        """ member yields an authority over themselves to another entity """
        if not self.has_authority(action):
            return False
        subject_auth = subject.get_auth_by_subject(self)
        if not subject_auth:
            subject.authority_over[self] = {action: {}}
        elif not action in subject_auth:
            subject.authority_over[self][action] = {}
        if requirements:
            for r in requirements:
                subject.authority_over[self][action][r] = r
        else:
            subject.authority_over[self][action][True] = True
    def format_action(self, action):
        """ format action from obj.method() to obj and method """
        subject, action = action.split('.')
        subject = eval(subject)
        if not isinstance(subject, Member):
            raise('subject must be an instance of class Member')
        if action.endswith('()'):
            action = action[:-2]
        if action.endswith('('):
            action = action[:-1]
        return subject, action
    def relinquish_authority(self, action):
        """ relinquish an authority where action is entity.action """
        if not self.has_authority(action):
            return False
        subject, action = self.format_action(action)
        if subject == self:
            raise('self ownership is immutable')
        if not subject in self.authority_over:
            return False
        if action and action not in self.authority_over[subject]:
            return False
        if not action:
            del self.authority_over[subject]
            return True
        del self.authority_over[subject][action]
        return True
    def has_authority(self, action):
        """
        check if member has the authority to perform an action on the given
        subject, and if all requirements are met.
        subject: entity on which member is peforming the action
        action: the action being performed on subject
        """
        if not type(action) == str:
            raise TypeError('action must be a string, ex: "user.method" ')
        subject, action = self.format_action(action)
        try:
            # check if action is a valid function for member
            eval('self.' + action)
        except AttributeError:
            print('member does not have that method')
            return False
        except Exception as e:
            raise e
        if subject == self:
            return True
        if subject not in self.authority_over:
            return False
        if action not in self.authority_over[subject]:
            return False
        for requirement in self.authority_over[subject][action]:
            if not requirement:
                return False
        return True
    def print_authorities(self):
        for s in self.authority_over:
            print('SUBJECT:')
            print("    {}".format(s))
            print()
            for a in self.authority_over[s]:
                print('    ACTION:')
                print("        {}".format(a))
                print()
                for r in self.authority_over[s][a]:
                    print('        REQUIREMENT:')
                    print("            {}".format(r))




if __name__ == "__main__":
    a, b = Member(''), Member('')
    a.grant_authority(b, 'a.get_auth_by_subject')