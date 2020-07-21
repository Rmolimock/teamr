#!/usr/bin/env python3
""" NavLink class """

class NavLink():
    """ Information for jinja to dynamically render navigation links """
    def __init__(self, text, url=None, classes=None, ids=None, styles=None):
        self.text = text
        self.url = url
        self.classes = classes
        self.ids = ids
        self.styles = styles



"""
HOME PAGE LINKS AND BUTTONS
"""
# home page links
#logged out
mission = NavLink('Our Mission', '#mission')
about = NavLink('About Us', '#about')
team = NavLink('Meet the Team', '#team')
home_pub_links = [mission, about, team]
# logged in
my_teams = NavLink('My Teams', '#myteams')
all_teams = NavLink('All Teams', '#allteams')
home_private_links = [my_teams, all_teams]

# home page buttons
# logged out
register = NavLink('REGISTER', '/register', ['strong_nav_button'])
login = NavLink('login', '/login')
home_pub_buttons = [register, login]
# logged in
profile = NavLink('Profile', '#', ['strong_nav_button'])
logout = NavLink('logout', '/logout')
home_private_buttons = [profile, logout]


"""
REGISTER LINKS AND BUTTONS
"""
# register links
back = NavLink('back', 'https://thepointistochangeit.com')
# register buttons
login = NavLink('login', 'https://thepointistochangeit.com/login')
# ---------
register_links = [back]
register_buttons = [login]



"""
LOGIN LINKS AND BUTTONS
"""
# login links
back = NavLink('back', 'https://thepointistochangeit.com')
# login buttons
register = NavLink('register', 'https://thepointistochangeit.com/register', ['strong_nav_button'])
# ---------
login_links = [back]
login_buttons = [register]



"""
PROFILE LINKS AND BUTTONS
"""
# logged in
# links
home = NavLink('Home', 'https://thepointistochangeit.com')
account = NavLink('Account', '#account')
my_teams = NavLink('My Teams', '#myteams')
# buttons
logout = NavLink('logout', 'https://thepointistochangeit.com/logout')
# ---------
profile_private_links = [home, account, my_teams]
profile_private_buttons = [logout]

# logged out
home = NavLink('Home', 'https://thepointistochangeit.com')
register = NavLink('REGISTER', 'https://thepointistochangeit.com/register', ['strong_nav_button'])
login = NavLink('login', 'https://thepointistochangeit.com/login')
public_profile_links = [home]
public_profile_butons = [login]
