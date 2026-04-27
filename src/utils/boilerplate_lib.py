from __future__ import annotations
import importlib
import re
import inspect
import subprocess

"""
BOILERPLATE DE BANDIDO PARA INSPECIONAR LIBRARYS 
WARNING - LIBRARYS AMPLAS PODE NÃO FUNCIONAR TÃO BEM.

"""

def inspection(lib_str="streamlit", which="All", doc="link"):
    functs, builtins, methods = [], [], []
    lib = resolve_lib(lib_str)
    iterlib = dir(lib) or inspect.getmembers(lib)
    for item in iterlib:
        try:
            value = getattr(lib, item)
        except Exception as e:
            print(f"""\n{'=='*55}\n[CRITICAL] {e}\n
            Output Item:\n{item[:500]}\n
            MUDE 'iterlib' PARA FUNÇÃO 'dir()'\n{'=='*55}""")
        function = inspect.isfunction(value)
        builtin = inspect.isbuiltin(value)
        method = inspect.ismethod(value)
        if item == "Page" or item.startswith("_"):
            continue
        if which != "All":
            try:
                m = re.match(rf"{re.escape(which)}", item)
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
    print(f"\nFunctions:\n {functs}")
    print(f"Builtins:\n {builtins}")
    print(f"Methods:\n {methods}")

    if doc == "link":    # Se é a primeira vez, RODE ISSO AQUI PARA PEGAR O LINK!
        doc_text = inspect.getdoc(lib) or ""
        links = re.findall(r"https://[^\s)<>\]]+", doc_text) 
        if links:
            for link in links:
                print("Docs:\n", link)
        else: 
            print("Nada foi encontrado")
    elif doc == "html":    # Insira no corpo do 'res' o link que veio no Docs do If acima.  
        res = subprocess.run(["curl", "-s", "https://docs.streamlit.io"], capture_output=True)
        html = res.stdout.decode("utf-8", errors="replace")
        print(html[:500]) # Cuidado! Essa opção é mais experimental do que para Research de Doc.
    else: 
        raise ValueError("Valor não aceito para 'doc'.")

def resolve_lib(lib_str):
    if isinstance(lib_str, str):
        return importlib.import_module(lib_str)
    else:
        raise TypeError("Não aceitamos outros valores fora 'String'.")

if __name__ == "__main__":
    inspection(which="c", doc="link")

    """
    lib_str: Colocar a Library desejada.
    which: A string colocada vai ser procurada na Library. LEMBRE-SE NÃO É IGUAL CTRL+F, BUSCA FIELMENTE AO PRIMEIRO CARACTERE!
    doc: Permite você obter o link da Documentação Oficial da Library, ou obter o HTML (NÃO RECOMENDADO).
    
    """