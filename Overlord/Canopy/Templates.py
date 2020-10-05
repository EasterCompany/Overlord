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
        Style='color:grey;text-align:center;',
        Items='By Easter Company&trade; from the United Kingdom'
    )


def user_menu():
    return dropmenu(
        [
            "<hr>",
            button(
                Text='Log out',
                Border=True
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


def media_menu():
    return element(
        ID='media-menu',
        Style='display:none;'
    )


default = [
    default_navbar(),
    appbar(
        block(
            user_menu(),
            chat_menu(),
            media_menu(),
            element(Items=[
                button(
                    Icon=svg('menu'),
                    OnClick=
                        script('toggleBox', 'user-menu') +
                        script('hide', 'chat-menu') +
                        script('hide', 'media-menu')
                ),
                button(
                    Icon=svg('chat'),
                    OnClick=
                        script('toggleBox', 'chat-menu') +
                        script('hide', 'user-menu') +
                        script('hide', 'media-menu')
                )
            ], Style='padding:8px 8px 8px 8px;display:flex;'
            ),
        )
    ),
    content(
        elements='''
            <h1> Loading... </h1>
        ''',
        source='/dist?app=library'
    ),
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
                `“Spartans are equal too any man as <br/> individuals; but together as a collective,<br/> they surpass all men.” - Damaratus to Xerxes. <br/><br/>`,
                ` “Quality before Quanity. <br/> Pruned before Perfect.” <br/> - Ethos. <br/><br/>`,
                ` “silence over empty words, <br/> simplicity over decoration, <br/> and precision over expansiveness.” <br/> - Ethos `,
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
    """
]
