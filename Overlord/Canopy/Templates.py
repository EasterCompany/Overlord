from .Core import var, script
from .Image import svg
from .Elements import *


def default_navbar():
    return navbar(
        elements=[
            button(
                Icon=svg('home'),
                OnClick=var(
                    'window.location.href',
                    '/'
                )
            ),
            button(
                Icon=svg('user')
            )
        ]
    )


def footer():
    return element(
        Tag='p',
        Style='color:grey;text-align:center;font-size:.7rem;',
        Items='EASTER COMPANY&trade; COPYRIGHT 2020.'
    )


def user_menu():
    return dropmenu(
        [
            "<hr>",
            button(
                Text='Log out',
                Border=True,
                OnClick='__logout__();'
            ),
            button(
                Text='Settings',
                Border=True
            ),
            button(
                Text='Terms of Service',
                Border=True
            ),
            footer()
        ],
        ID='user-menu'
    )


def no_user_menu():
    return dropmenu(
        [
            "<hr>",
            button(
                Text='Login',
                Border=True,
                OnClick='document.getElementById(`content`).src = `/dist?app=login`;'
            ),
            button(
                Text='New Account',
                Border=True,
                OnClick='document.getElementById(`content`).src = `/dist?app=register`;'
            ),
            footer()
        ],
        ID='no-user-menu'
    )


def chat_menu():

    def chat_user(user='John Doe'):
        return element(
            Class='button',
            Items=[
                flex(
                element(
                    Items=svg('user'),
                    Style='''
                    width:26px;
                    height:26px;
                    margin:8px 8px 8px 8px;
                    '''
                ),
                "<h4 style='margin:8px 4px 8px 4px;text-align:left;'> {username} </h4>".\
                    format(username=user),
                "<h6 style='margin:12px 4px 8px 4px;color:grey;text-align:left;'> preview message.. </h6>"
            )
            ]
        )

    return element(
        Items=[
            element(
                Items=[
                    chat_user(),
                    chat_user(),
                    chat_user(),
                    chat_user(),
                    chat_user(),
                    chat_user(),
                    chat_user(),
                    chat_user(),
                ],
                ID='chat-inbox',
                Class='menu',
                Style='margin:3% 0 3% 0;display:block;'
            ),
            "<input placeholder='search for users...'/>",
        ],
        ID='chat-menu',
        Style='display:none;'
    )


default = [
    default_navbar(),
    appbar(
        block(
            no_user_menu(),
            user_menu(),
            chat_menu(),
            element(Items=[
                button(
                    Icon=svg('menu'),
                    OnClick=
                        script('userMenu') +
                        script('hide', 'chat-menu')
                ),
                button(
                    ID='chat-btn',
                    Icon=svg('chat'),
                    OnClick=
                        script('toggleBox', 'chat-menu') +
                        script('hide', 'no-user-menu') +
                        script('hide', 'user-menu')
                )
            ], Style='padding:8px 8px 8px 8px;display:flex;'
            ),
        )
    ),
    content(
        elements='''
            <h1> Loading... </h1>
        ''',
        source='/dist?app=home'
    )
]

header = [
    "<div class='site-header'>",
        "<div class='site-header-logo'>",
            svg('logo2'),
        """
        </div>
        <div style='display:block;'>
            <h1 style='margin-top:16px;font-family:Spartan;font-size:36px;'> EASTER COMPANY </h1>
            <h4 id='site-header-quote' style='color:#fe8605;margin:32px 0 16px 0;font-family:Roboto;'></h4>
            <h5> contact@easter.company </h5>
            <hr/>
        """,
        script(
            function='random',
            parameters='''`site-header-quote`, [
                `“Spartans are equal too any man as <br/> individuals; but together as a collective,<br/> they surpass all other men.” <br/> - Damaratus to Xerxes. <br/>`,
                ` “Quality before Quanity. <br/> Pruned before Perfect.” <br/> - Ethos. <br/><br/>`,
                ` “silence over empty words, <br/> simplicity over decoration and <br/> precision over expansiveness.” <br/> - Ethos `,
                ` “Liberty, Equality <br/> and Fraternity.” <br/> - Ethos <br/><br/> `,
                ` “Gradatim Ferociter.” <br/> - Step by Step Ferociously <br/><br/> `,
            ]
            ''',
            addon=True
        ),
        flex(
            button(
                Icon=svg('facebook'),
                OnClick=script(
                    'window.open',
                    'https://www.facebook.com/eastercompany'
                )
            ),
            button(
                Icon=svg('twitter'),
                OnClick=script(
                    'window.open',
                    'https://www.twitter.com/eastercompany'
                )
            ),
            button(
                Icon=svg('github'),
                OnClick=script(
                    'window.open',
                    'https://github.com/EasterCompany'
                )
            )
        ),
    """
        </div>
    </div>
    """,
    shader()
]
