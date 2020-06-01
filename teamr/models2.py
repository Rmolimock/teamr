#!/usr/bin/env python3

class User():
    def __init__(self, name, teams=None, roles=None, subject_to=None, authority_over=None):
        self.name = name
        self.teams = teams
        self.roles = roles
        self.subject_to = subject_to
        self.authority_over = authority_over


class Team():
    def __init__(self, name, members, teams=None, roles=None, subject_to=None, authority_over=None):
        super().__init__()
        self.members = members
        self.subject_to = members.authority_over[self.name]
        


class Role():
    def __init__(self, members=None, teams=None, roles=None, subject_to=None, authority_over=None):
        super().__init__()


class Auth():
    def __init__(self, subject, action, requirement):
        self.all = {subject: 
                            {action: 
                                    {requirement: requirement}
                                    }
                            }
    def remove(self, subject, action=None, requirements=None, req=None):
        """
        Remove auth(s) from Auth object.
        If 'req' is not None, that specific requirement is removed
        If 'req' IS None, all requirements are replaced with None.
        If 'requirements' is None, 'action' is deleted.
        If 'action' is None, 'subject' is deleted.
        """
        if not subject in self.all.items():
            print('no authority over ' + subject.name)
            return
        elif not action in self.all[subject]:
            # If 'action' is None, 'subject' is deleted.
            if not action:
                del self.all[subject]
                return
            else:
                print('action does not exist over')
                return
        elif not requirements in self.all[subject][action]:
            if not requirements:
                # If 'requirements' is None, 'action' is deleted.
                del self.all[subject][action]
                return
            else:
                print('requirement does not exist')
                return
        elif not req:
            # If 'req' IS None, all requirements are replaced with None.
            del self.all[subject][action][requirements]
            return
        # If 'req' is not None, that specific requirement is removed
        del self.all[subject][action][requirements][req]
        # add an unless to the parameters
        # 
    def add_or_modify(self, subject, action, requirements, req=None):
        """
        Add or modify an authority to Auth object.
        If 'req' is None, all requirements are replaced.
        """
        if not type(subject) == dict:
            print('must be dict')
            return
        if not type(action) == dict:
            print('must be dict')
            return
        if not type(requirements) == dict:
            print('must be dict')
            return
        # add a new subject, along with an action and requirements
        if not subject in self.all.items():
            self.all[subject] = subject
            self.all[subject][action] = action
            self.all[subject][action][requirements] = requirements
            if req:
                self.all[subject][action][requirements][req] = req
            return
        # add an action to an existing subject
        if not action in self.all[subject]:
            self.all[subject][action] = action
            self.all[subject][action][requirements] = requirements
            if req:
                self.all[subject][action][requirements][req] = req
            return
        # If 'req' is None, all requirements are replaced.
        if not req:
            self.all[subject][action][requirements] = requirements
            return
        # modify one specific requirement of existing action
        self.all[subject][action][requirements][req] = req
        return


auth = Auth('s_1', 'a_1', 'r_1')
auth.all['s_1']['a_1']['r_1']
auth.add_or_modify('s_1', 'a_1', 'r_1')
        

parties = {'team_1': 
           {'a_1':
            {'requirement_1': 0.5,
             'requirement_2': user_2.authority_over.parties['Team_2']
            }
        }

}
actions = {'a_1':
           {'team_1':
            {'requirement_1': 0.5,
             'requirement_2': user_2.authority_over.parties['Team_2']
            }
        }
}


users = [User('user_' + str(u)) for u in range(100)]
team = Team('Team_1', members=users)



class SubjTo():
    def __init__(self):
        self.
        self.