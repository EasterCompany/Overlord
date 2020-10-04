from .Core import var, script
from .Image import svg
from .Elements import *


def default_navbar():
    return navbar(
        elements=[
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
                ),
                button(
                    Icon=svg('check'),
                    OnClick=
                        script('hide', 'user-menu') +
                        script('hide', 'chat-menu') +
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
        svg('logo'),
    """
    </div>
    <div style='display:block;'>
    <h1 style='margin-top:16px;font-family:Caesar Dressing;'> EASTER COMPANY </h1>
    <br/>
    <h4> Business Contact </h4>
    <br/>
    <h5> owen@easter.company </h5> 
    <h5> +441382527319 </h5>
    <div style='display:flex;margin:32px 0 0 0;justify-content: center;'>
        <iframe scrolling="no" frameborder="0" style="border:none; overflow:hidden; height:80px; width:80px;" allowTransparency="true" src="https://www.facebook.com/plugins/like.php?locale=en_GB&href=https://www.facebook.com/eastercompany&layout=button&action=like&show_faces=false&share=false&"><div><small><a href="www.fbaddlikebutton.com">http://www.fbaddlikebutton.com</a></small></div><div><small><a href=""></a></small></div></iframe>
        <a href="https://twitter.com/eastercompany?ref_src=twsrc%5Etfw" class="twitter-follow-button" data-show-count="false">Follow @eastercompany</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    </div></div></div>
    """
]
