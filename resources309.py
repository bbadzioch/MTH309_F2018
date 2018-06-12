import requests
import os

url_root = "https://raw.githubusercontent.com/bbadzioch/MTH309_F2018/master/"


def get_resources(*flist):

    global url_root

    url_root309 = url_root + "py309/"
    cwd = os.getcwd()
    py309 = os.path.join(cwd,  "py309")

    if not os.path.isdir(py309):
        print("creating directory py309...", end="")
        os.makedirs(py309)
        print("done.")
        print("Downloading __init__.py...", end="")
        try:
            r = requests.get(url_root309 + "__init__.py")
        except:
            print("\n\nCONNECTION ERROR. Check your internet connection.")
            return None

        with open(os.path.join(py309 , "__init__.py"), "w") as f:
            if r.status_code == requests.codes.ok:
                f.write(r.text)
                print("done.")
            else:
                f.write("#py309 package")
                print("done, status code: {}.".format(r.status_code))


    for fname in flist:
        if not os.path.isfile(os.path.join(py309, fname)):
            print("Downloading "+ fname + "...", end="")
            try:
                r = requests.get(url_root309 + fname)
            except requests.ConnectionError:
                print("\n\nCONNECTION ERROR. Check your internet connection.")
                return None
            if not r.status_code == requests.codes.ok:
                if r.status_code == 404:
                    print("FILE NOT FOUND 404")
                else:
                    print("Status code: {}.".format(r.status_code))
                continue

            with open(os.path.join(py309 , fname) , "wb") as f:
                f.write(r.content)
            print("done.")

    print("Resource check finished.")




def get_notebooks():

    notebook_list = "notebook_list.txt"
    cwd = os.getcwd()

    try:
        r = requests.get(url_root + notebook_list)
    except:
        print("\n\nCONNECTION ERROR. Check your internet connection.")
        return None
    for nname in r.text.split('\n'):
        nname = nname.strip()
        if nname == "":
            continue
        nname = nname + ".ipynb"
        if not os.path.isfile(os.path.join(cwd, nname)):
            print("Downloading "+ nname + "...", end="")
            try:
                nr = requests.get(url_root + nname)
            except requests.ConnectionError:
                print("\n\nCONNECTION ERROR. Check your internet connection.")
                return None
            if not nr.status_code == requests.codes.ok:
                if nr.status_code == 404:
                    print("FILE NOT FOUND 404")
                else:
                    print("Status code: {}.".format(nr.status_code))
                continue

            with open(os.path.join(cwd , nname) , "wb") as f:
                f.write(nr.content)
            print("done.")

    print("Download finished.")
