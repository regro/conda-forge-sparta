import os
import requests
import threading

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse


# https://stackoverflow.com/questions/12435211/python-threading-timer-repeat-function-every-n-seconds
def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop():  # executed in another thread
                while not stopped.wait(interval):  # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True  # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator


LINKS = requests.get(
    "https://github.com/regro/repodata/releases/latest/download/links.json"
).json()


@setInterval(300)  # every 5 minutes
def _update_links():
    print("RELOADING LINKS")
    global LINKS
    new_links = requests.get(
        "https://github.com/regro/repodata/releases/latest/download/links.json"
    ).json()
    LINKS = new_links


_stop_update_links = _update_links()

app = FastAPI()


@app.get("/")
async def root():
    return RedirectResponse("https://regro.github.io/repodata/index.html")


@app.get("/channeldata.json")
async def channeldata():
    return RedirectResponse(
        "https://github.com/regro/repodata/releases/latest/download/"
        "channeldata_main.json"
    )


@app.get("/{subdir}/")
async def subdir_root(subdir):
    return RedirectResponse(f"https://regro.github.io/repodata/{subdir}/index.html")


@app.get("/{subdir}/repodata.json")
async def subdir_repodatadata(subdir):
    return RedirectResponse(
        "https://github.com/regro/repodata/releases/latest/download/"
        f"repodata_{subdir}_main.json"
    )


@app.get("/{subdir}/repodata.json.bz2")
async def subdir_repodatadatabz2(subdir):
    return RedirectResponse(
        "https://github.com/regro/repodata/releases/latest/download/"
        f"repodata_{subdir}_main.json.bz2"
    )


@app.get("/{subdir}/repodata_from_packages.json")
async def subdir_repodatadata_pkgs(subdir):
    return RedirectResponse(
        "https://github.com/regro/repodata/releases/latest/download/"
        f"repodata_{subdir}_main.json"
    )


@app.get("/{subdir}/repodata_from_packages.json.bz2")
async def subdir_repodatadatabz2_pkgs(subdir):
    return RedirectResponse(
        "https://github.com/regro/repodata/releases/latest/download/"
        f"repodata_{subdir}_main.json.bz2"
    )


@app.get("/{subdir}/current_repodata.json")
async def subdir_repodatadata_curr(subdir):
    return RedirectResponse(
        "https://github.com/regro/repodata/releases/latest/download/"
        f"repodata_{subdir}_main.json"
    )


@app.get("/{subdir}/current_repodata.json.bz2")
async def subdir_repodatadatabz2_curr(subdir):
    return RedirectResponse(
        "https://github.com/regro/repodata/releases/latest/download/"
        f"repodata_{subdir}_main.json.bz2"
    )


@app.get("/{subdir}/{pkg}")
async def subdir_pkg(subdir, pkg):
    subdir_pkg = os.path.join(subdir, pkg)
    url = LINKS["main"].get(subdir_pkg, None)
    if url is None:
        raise HTTPException(status_code=404, detail=f"{subdir_pkg} not found!")
    return RedirectResponse(url)
