from os import system as s, getcwd as _cwd
from sys import argv as a, executable as E
cwd,n=_cwd(),a[1]
s(f"git clone git@github.com:EasterCompany/Overlord.git {n}")
s(f"cd {n}")
s(f"{E} core.py install {cwd}/{n}")

#from json import loads as l
#from requests import get as g
#m=lambda fp: f"https://eastercompany.pythonanywhere.com/api/download?RDFS=true&file={fp}"
#d=lambda fp: g(m(fp))
#j=lambda fp: l(d(fp))

# j -> {
#  'name': str( name of the file )
#  'type': str( file type such as 'txt' for '.txt' files )
#  'create': str( optional bash command to run before downloading the file )
#  'content': str or bytes to write to file
#  'post': str( optional bash command to run after downloading the file )
# }
