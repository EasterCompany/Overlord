from Overlord.Canopy.Core import Document, script
from Overlord.Canopy.Image import svg
from Overlord.Canopy.Elements import flex, button, shader, story

# Page Root
App = Document()
App.import_css('https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap')
App.import_css('https://fonts.googleapis.com/css2?family=Spartan:wght@700&display=swap')
App.set_font("Roboto")


def social_links():
    return flex(
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
    )


# Page Elements
App.add_elements(
        "<div class='site-header'>",
        "<div class='site-header-logo'>",
            svg('logo2'),
        """
        </div>
        <div>
            <h1 style='margin-top:16px;font-family:Spartan;font-size:36px;'> EASTER COMPANY </h1>
            <h4 id='site-header-quote' style='color:#fe8605;margin:32px 0 16px 0;font-family:Roboto;'></h4>
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
        social_links(),
    """
        </div>
    </div>
    """,
    shader(),
    story(
        align="left",
        header='Forensic Financial Software',
        text="""
            Our suite of Forensic Financial tools allows individuals to industrial size organisations to
            track and manage their budgets with built intelligent automation APIs which give real time
            feedback and helpful statistics in a pragmatic manner when you need it most.
            <br>
            <br>
            <a href='/'>read more...</a>
            <br>
        """,
        image="/Image/budgetGraph.png"
    ),
    shader(),
    story(
        align="right",
        header='The Entropy Enviroment',
        text="""
            Entropy is a collection of web based applications for productivity which provides services for
            Entertainment, Education and Enterprise clients - including but not exclusive too eChat & eDocs.
            We compete with other common cloud based productivity suites with a focus on efficieny and
            all-in-one methodology.
            <br>
            <br>
            <a href='/'>read more...</a>
            <br>
        """,
        image="/Image/entropyLogo.png"
    ),
    shader(),
    story(
        align="left",
        header='Dexter Digital Intelligence',
        text="""
            The Dexter digital intelligence program incorporates a wide scope of machine learning and non-ml features
            to bring together a variety of APIs, Desktop & Mobile applications which may be stand alone or with other
            applications to enhance your daily life with the power of artificial intelligence. From smart homes to
            digital intefacing - we plan on making the most varied piece of software on the market.
            <br>
            <br>
            <a href='/'>read more...</a>
            <br>
        """,
        image="/Image/dexterLogo.png"
    ),
    shader(),
        story(
        align="right",
        header='Canopy Creative Library',
        text="""
            Our canopy frontend library built into our Overlord framework provides developers with a pure-python
            focused frontend development kit which combines server side rendering with client side pre-written
            javascript modules with a flexible design methodology to achieve the best of both worlds and ease of
            mind knowing your tech stack stays minimal.
            <br>
            <br>
            <a href='/'>read more...</a>
            <br>
        """,
        image="/Image/canopyLogo.png"
    ),
    shader(),
        story(
        align="left",
        header='Bionic Backend Library',
        text="""
            Our bionic backend library built into our Overlord framework provides robust server side systems
            with high performance functionality and low operating costs which allows for scalable standards
            from an individuals blog to industry leading web applications.
            <br>
            <br>
            <a href='/'>read more...</a>
            <br>
        """,
        image="/Image/bionicLogo.png"
    ),
    shader(),
    story(
        align="right",
        header='Atlas Automated Testing',
        text="""
            The atlas automated test library built into our Overlord framework allows bring the 'reliable' to
            Overlords rapid & reliable deployment methodology by allowing developers to quickly deploy new
            software with accurate and automated testing procedures designed by digital intelligence.
            <br>
            <br>
            <a href='/'>read more...</a>
            <br>
        """,
        image="/Image/atlasLogo.png"
    ),
    shader(),
    """<div style='min-height:24px;'>&nbsp;</div>
    <div style='max-width:500px;margin:16px auto;justify-content:center;text-align:center;'>
        <h3>follow us on social media</h3>
        <h4>stay up-to-date and keep us on your news feed!</h4><br>""",
        social_links(),
    "<br><br>EASTER COMPANY™ COPYRIGHT 2020<br><br><div style='min-height:24px;'>&nbsp;</div></div>"
)

# Page Render
App = App.render()
