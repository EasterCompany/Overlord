# Overlord library
from .api import domain, fetch_api
from core.library import console


def request():
    console.out(f"\n> Reload Server @ {domain}")

    console.out(f"  {console.wait} Reloading ... ", end="\r")

    data = fetch_api('webapps', args=(domain, 'reload'), method='POST')
    console.out(
        "  ✅ Successfully Reloaded  ", "success"
    ) if data['status'] == "OK" else console.out(
        "  ⚠️ Unknown Error       ", "yellow"
    )

    if 'data' in data and data['data'] == "[500] Internal server error.":
        print('REASON:', console.out(data['data'], 'red'))
        print('\nAre you using the correct authentication method?')

    return data
