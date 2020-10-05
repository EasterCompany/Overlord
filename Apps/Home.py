from Overlord.Canopy.Core import Document, script
from Overlord.Canopy.Templates import header

# Page Root
App = Document(template=header)
App.import_css('https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap')
App.import_css('https://fonts.googleapis.com/css2?family=Spartan:wght@700&display=swap')
App.set_font("Roboto")

# Page Render
App = App.render()
