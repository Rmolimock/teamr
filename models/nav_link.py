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


# same-page navigation links for home page

#logged out
mission = NavLink('Our Mission', '#mission')
about = NavLink('About Us', '#about')
team = NavLink('Meet the Team', '#team')
# logged in
my_teams = NavLink('My Teams', '#myteams')
all_teams = NavLink('All Teams', '#allteams')



# button links for home page

# logged out
register = NavLink('REGISTER', '/register', ['strong_nav_button'])
login = NavLink('log in', '/login')
# logged in
profile = NavLink('Profile', '#', ['strong_nav_button'])
logout = NavLink('log out', '/logout')

