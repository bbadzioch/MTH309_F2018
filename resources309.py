import requests
import os


def get_resources(*flist):

    url_root = "https://raw.githubusercontent.com/bbadzioch/MTH309_F2018/master/py309/"
    cwd = os.getcwd()
    py309 = cwd + "/py309/"

    if not os.path.isdir(py309):
        print("creating directory py309...", end="")
        os.makedirs(py309)
        print("done.")
        print("Downloading __init__.py...", end="")
        try:
            r = requests.get(url_root + "__init__.py")
        except:
            print("\n\nCONNECTION ERROR. Check your internet connection.")
            return None
            
        with open(py309 + "__init__.py", "w") as f:
            if r.status_code == requests.codes.ok:
                f.write(r.text)
                print("done.")
            else:
                f.write("#py309 package")
                print("done, status code: {}.".format(r.status_code))

       

    for fname in flist:
        if not os.path.isfile(py309 + fname):
            print("Downloading "+ fname + "...", end="")
            try:
                r = requests.get(url_root + fname)
            except requests.ConnectionError:
                print("\n\nCONNECTION ERROR. Check your internet connection.")
                return None
            if not r.status_code == requests.codes.ok:
                if r.status_code == 404:
                    print("FILE NOT FOUND 404")   
                else: 
                    print("Status code: {}.".format(r.status_code))
                continue
                          
            with open(py309 + fname, "wb") as f:
                f.write(r.content)
            print("done.")
    
    print("Resource check finished.")
    
    
    