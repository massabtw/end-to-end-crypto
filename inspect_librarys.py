from __future__ import annotations
import importlib
import re
import inspect
import subprocess

"""
BOILERPLATE PARA INSPECIONAR LIBRARYS, APROVEITE! 
ASS: MANO SENS 

"""

def inspection(lib_str="streamlit", which="All", doc=False):
    functs, builtins, methods = [], [], []
    lib = resolve_lib(lib_str)
    for item in dir(lib):
        value = getattr(lib, item)
        function = inspect.isfunction(value)
        builtin = inspect.isbuiltin(value)
        method = inspect.ismethod(value)
        if item == "Page" or item.startswith("_"):
            continue
        if which != "All":
            try:
                m = re.match(rf"{which}", item)
                if not m:
                    continue
                if function:
                    print(f"Function: {item}")
                    functs.append(item)
                elif builtin:
                    print(f"Builtin: {item}")
                    builtins.append(item)
                elif method:
                    print(f"Method: {item}")
                    methods.append(item)
                else:
                    print(f"Type of {item}: {type(value).__name__}")
            except AttributeError as e:
                print(f"Não foi reconhecido. [ERROR] : {e}")
                continue
        else:
            try:
                if function:
                    print(f"Function: {item}")
                    functs.append(item)
                elif builtin:
                    print(f"Builtin: {item}")
                    builtins.append(item)
                elif method:
                    print(f"Method: {item}")
                    methods.append(item)
                else:
                    print(f"Type of {item}: {type(value).__name__}")
            except AttributeError as e:
                print(f"Não foi reconhecido. [ERROR] : {e}")
                continue
    print(f"Functions:\n {functs}")
    print(f"Builtins:\n {builtins}")
    print(f"Methods:\n {methods}")

    if doc == "html":
        res = subprocess.run(["curl", "-s", "https://docs.streamlit.io"], capture_output=True)
        html = res.stdout.decode("utf-8", errors="replace")
        print(html[:500])
    
    elif doc == "link":
        links = re.findall(r"https://[^\s)<>\]]+", inspect.getdoc(lib))
        if links:
            for link in links:
                print("Docs:\n", link)
        else: 
            print("Nada foi encontrado")

def resolve_lib(lib_str):
    if isinstance(lib_str, str):
        return importlib.import_module(lib_str)
    else:
        raise TypeError("Não aceitamos outros valores fora 'String'.")

if __name__ == "__main__":
    inspection(which="selectbox", doc="link")