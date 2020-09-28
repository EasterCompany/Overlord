from Overlord.Bionic.Basics import platform_version
from urllib import request as req

sources = {
        'internal': {
            'url': "https://easter.company/b/update?file=vers.ctrl",
            'status': -1,
            'version': -1,
            'response': ''
        },
        'github': {
            'url': "https://raw.githubusercontent.com/EasterCompany/Overlord/master/vers.ctrl",
            'status': -1,
            'version': -1,
            'response': ''
        }
    }


def fetch_source():
    latest_version = 0.0
    latest_source = None

    for src in sources:
        try:
            response = req.urlopen(sources[src]['url'])
            sources[src]['status'] = 1
            sources[src]['response'] = response.read().decode('utf-8')
            sources[src]['version'] = sources[src]['response']
        except Exception as src_error:
            sources[src]['status'] = 0
            sources[src]['response'] = str(src_error)
            sources[src]['version'] = -1.0
        
    if float(sources[src]['version']) > float(latest_version):
        latest_version = sources[src]['version']
        latest_source = sources[src]
    
    return latest_source


def approve_certificate(source):
    cv = float(platform_version())
    nv = float(source['version'])
    if nv > cv:
        return 1
    elif nv == cv:
        return 0
    else:
        return -1

