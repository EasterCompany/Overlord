from Overlord.Canopy.Core import Document
from Overlord.Canopy.Templates import header
from Overlord.Canopy.Elements import element, flex, block
from Overlord.Canopy.Image import youtube, instagram, img, svg

# Page Root
App = Document(template=header)
App.import_css('https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap')
App.import_css('https://fonts.googleapis.com/css2?family=Spartan:wght@700&display=swap')
App.set_font("Roboto")


def library_category(icon=str(), label=str()):
    return element(
        Class='library-category',
        Items=icon + "<h6>" + label + "</h6>"
    )


# Page Elements
App.add_elements(
    element(
        Class='library-category-section',
        Items=[
            library_category(icon=svg('spanner'), label='Engineering'),
            library_category(icon=svg('gamepad'), label='Entertainment'),
            library_category(icon=svg('badge'), label='Enterprise'),
        ]
    ),
    youtube(
        title="Machine Learning Pong (2017)",
        url="5U1AO0ZDhEM",
        text='''
            Dexter Mark 1 was actually named "Vi" at this point and was souly developed
            as a machine learning game project - in this video we demonstrate Vi (Dexter)
            playing Pong at a super human - almost perfect level. Later versions would
            grow to the same level with only 2 hours of training. The algorithm and methods 
            used were library-less although prior to this version I also developed the same 
            product in tensorflow which required much more training for similar results.
            One remarkable strategy I recognised was that Vi (Dexter) always returns to the 
            middle of the screen after returning the ball to save time on the next return.
        '''
    ),
    youtube(
        title="Extensive Dexter A.I. Demonstration (2018)",
        url="Ud8pgj1g-9s",
        text='''
            In this video we demonstrate News, Weather, Music, Search & Chat functionality
            from Dexter Mark 4 - one of the greatest versions of out unreleased A.I. project.
            Allow the video to speak for itself. 
        '''
    ),
    youtube(
        title="Chatting with Dexter (2017)",
        url="Fd6-4n4ePKk", 
        text='''
            Demonstration of a very early build of Dexter Mark 4 (2017 Alpha Build "Pluto") 
            playing around with his smart conversation functionality
            and a few other features such as media control on windows.
            This was one of the most entertaining and complex projects I've worked on
            involving over 50,000 lines of code written in under a year by Myself.
            Later versions of Dexter would re-shape the idea into a more traditional 
            virtual assitant similar to the likes of Alex, Google Assistant and Siri.
            Incorporating smart home functionality and more...
        '''
    ),
    youtube(
        title="Machine Learning Algebra (2017)",
        url="YnwVekrU5uY",
        text='''
            This is a simple and badly recorded example of Dexter Mark 4's indepth understanding
            of the English language and Mathematics, although a seemingly simple question;
            "if a=1 and b=2, what is a+b" this was a world first at the time of recording
            no virtual assistant; Alexa, Siri or Google Assistant could answer this question
            and yet Dexter with his unique approach handles this question easily and quickly.
        '''
    ),
    youtube(
        title='Hades One (2019)',
        url="3UHFJ4wbMPM",
        text='''
            Showing off the title screen designed for "Hades One" a game project;
            developed exclusively in Python without using a game engine. All assets
            and libraries used are from open source projects from Easter Companies previous
            ventures. Music Credit to Andrew McArthur (AndyRoo42 on Spotify).
        '''
    ),
    youtube(
        title='Untitled Project (2016)',
        url="2DKuwgHqtf8",
        text='''
            Another game demo using raw Python and no game engine from 2016, mostly used
            as an experimental project for developing an internal software framework.
            Music, Art & Programming by Owen Cameron Easter.
        '''
    ),
    youtube(
        title='Dexter Desktop Application (2018)',
        url="1bH0NYBe2jc",
        text='''
            Here we do a quick demonstration of the Dexter Desktop & Mobile interface application.
            It was created using Kivy (Python Framework) and was optimized to use less than 2MB of
            memory on all supported platforms (Linux, Windows & Android).
        '''
    ),
    youtube(
        title='Dexter Messenger & RDFS Demo (2018)',
        url="n_es-5XiOqk",
        text='''
            In this demo we ask Dexter via Facebook Messenger to open a file on our home desktop;
            which he does quickly and responsively. Allowing us to watch movies or tv shows on any
            device over WLAN or Internet by hosting our file on a Python Flask server.
        '''
    ),
    youtube(
        title='Smart Search Feature Demo (2018)',
        url='mtHmCCz2ji8',
        text='''
            Dexter's intelligence allows him to understand commands in a way other virutal assistants
            can not! - were open a programmed command he would be limited a scope of either files on 
            your PC or google search results; however due to his generalised machine learning strategy 
            he understands when you're speaking about programs on your PC; pictures on the cloud or 
            even a specific video on youtube. 
        '''
    )
)

# Page Render
App = App.render()
