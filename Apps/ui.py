# Root Document Import
from ..Overlord.Canopy.Core import Document
from ..Overlord.Canopy.Templates import default

# Create Document Template
App = Document(template=default)

# Personalise Document
App.import_css('https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap')
App.set_font("Roboto")

# Build & Render Document
App = App.render()
