# Overlord library
from .api import domain, server
from core.library import console


def request():
    print(f'\n> Upgrade Server @ {domain}')
    console.out(f"  {console.wait} Upgrading ...", end="\r")

    data = server('upgrade')
    console.out(
        "  ✅ Server Upgraded  ", "success"
    ) if data['status'] == "OK" else console.out(
        "  ⚠️ Unexpected Error ",
    )

    if 'data' in data and data['data'] == "[500] Internal server error.":
        console.out(data['data'], 'red')

    return data
