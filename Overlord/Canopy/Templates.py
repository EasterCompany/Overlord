from .Core import var, script
from .Image import svg
from .Elements import *


def default_navbar():
    return navbar(
        elements=[
            button(
                Icon=svg('home'),
                OnClick=var(
                    variable='window.location.href', 
                    value='/'
                )
            ),
            button( 
                Icon=svg('user')
            )
        ]
    )


def footer():
    return """<p style='color:grey;text-align:center;'>
    By Easter Company&trade; from the United Kingdom</p>"""


def new_user_menu_options():
    return dropmenu(
        [
            button(
                Text='Log in',
                Border=True
            ),
            button(
                Text='New Account',
                Border=True
            ),
            footer()
        ],
        ID='app-menu'
    )


def user_menu_options():
    return dropmenu(
        [
            button(
                Text='Log out',
                Border=True
            ),
            button(
                Text='Settings',
                Border=True
            ),
            footer()
        ],
        ID='app-menu'
    )


default = [
    appbar(
        block(
            user_menu_options(),
            flex(
                button(
                    ID='menu-button',
                    Icon=svg('menu'),
                    OnClick=script('toggleBox', 'app-menu')
                ),
                button(
                    ID='notification-button',
                    Icon=svg('bell')
                ),
                button(
                    ID='message-button',
                    Icon=svg('chat')
                ),
                button(
                    ID='dexter-button',
                    Icon=svg('dexter')
                )
            ),
        )
    ),
    default_navbar(),
    content(source=''),
]
