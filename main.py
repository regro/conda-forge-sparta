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
    print("************* RELOADING LINKS *************")
    global LINKS
    new_links = requests.get(
        "https://github.com/regro/repodata/releases/latest/download/links.json"
    ).json()
    LINKS = new_links


_stop_update_links = _update_links()

app = FastAPI()


################################################################################
# labels
################################################################################

@app.get("/label/{label}")
async def root_label(label):
    return {"message": "this is the index!"}
    # return RedirectResponse(
    #     f"https://regro.github.io/repodata/label/{label}/index.html"
    # )


@app.get("/label/{label}/channeldata.json")
async def channeldata_label(label):
    return RedirectResponse(
        "https://github.com/regro/repodata/releases/latest/download/"
        f"channeldata_{label}.json"
    )


@app.get("/label/{label}/{subdir}/")
async def subdir_root_label(label, subdir):
    return {"message": "this is the index!"}
    # return RedirectResponse(
    #     f"https://regro.github.io/repodata/label/{label}/{subdir}/index.html"
    # )


@app.get("/label/{label}/{subdir}/repodata.json")
async def subdir_repodatadata_label(label, subdir):
    return RedirectResponse(
        "https://github.com/regro/repodata/releases/latest/download/"
        f"repodata_{subdir}_{label}.json"
    )


@app.get("/label/{label}/{subdir}/repodata.json.bz2")
async def subdir_repodatadatabz2_label(label, subdir):
    return RedirectResponse(
        "https://github.com/regro/repodata/releases/latest/download/"
        f"repodata_{subdir}_{label}.json.bz2"
    )


@app.get("/label/{label}/{subdir}/repodata_from_packages.json")
async def subdir_repodatadata_pkgs_label(label, subdir):
    return RedirectResponse(
        "https://github.com/regro/repodata/releases/latest/download/"
        f"repodata_{subdir}_{label}.json"
    )


@app.get("/label/{label}/{subdir}/repodata_from_packages.json.bz2")
async def subdir_repodatadatabz2_pkgs_label(label, subdir):
    return RedirectResponse(
        "https://github.com/regro/repodata/releases/latest/download/"
        f"repodata_{subdir}_{label}.json.bz2"
    )


@app.get("/label/{label}/{subdir}/current_repodata.json")
async def subdir_repodatadata_curr_label(label, subdir):
    return RedirectResponse(
        "https://github.com/regro/repodata/releases/latest/download/"
        f"repodata_{subdir}_{label}.json"
    )


@app.get("/label/{label}/{subdir}/current_repodata.json.bz2")
async def subdir_repodatadatabz2_curr_label(label, subdir):
    return RedirectResponse(
        "https://github.com/regro/repodata/releases/latest/download/"
        f"repodata_{subdir}_{label}.json.bz2"
    )


@app.get("/label/{label}/{subdir}/{pkg}")
async def subdir_pkg_label(label, subdir, pkg):
    subdir_pkg = os.path.join(subdir, pkg)
    url = LINKS[label].get(subdir_pkg, None)
    if url is None:
        raise HTTPException(
            status_code=404, detail=f"label/{label}/{subdir_pkg} not found!"
        )
    return RedirectResponse(url)


################################################################################
# main
################################################################################


@app.get("/")
async def root():
    return {"message": "this is the index!"}
    # return RedirectResponse("https://regro.github.io/repodata/label/main/index.html")


@app.get("/channeldata.json")
async def channeldata():
    return RedirectResponse(
        "https://github.com/regro/repodata/releases/latest/download/"
        "channeldata_main.json"
    )


@app.get("/{subdir}/")
async def subdir_root(subdir):
    return {"message": "this is the index!"}
    # return RedirectResponse(
    #     f"https://regro.github.io/repodata/label/main/{subdir}/index.html"
    # )


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
