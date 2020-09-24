import os
from anytree import Node, RenderTree

root = Node(".")

def help():
    print("""
        Ingrese 'create <path/to/file>' para crear un árbol a partir de la lista de dominios del archivo ingresado
        Ingrese 'add <domain>' para agregar un nuevo dominio
        Ingrese 'query <domain>' para consultar si existe el dominio en el árbol
        Ingrese 'print' para imprimr el árbol
        Ingrese 'export <path/to/file>' para crear una imagen png del árbol en el path ingresado
        Ingrese 'exit' para finalizar
    """)


def find_node(node, subdom):
    """Busca si un subdominio está en el árbol.
    
    Parameters:
        node (Node): Nodo actual
        subdom (str): Subdominio

    Returns:
        Node: Si encuentra el nodo en el que está el subdominio.
        None: No encuentra el subdominio.
    """
    for c in node.children:
        if c.name == subdom:
            return c
    return None


def create(path):
    """Crea un árbol de dominios a partir de un archivo y lo imprime.
    Permite al usuario decidir sobre el proceso de creación.
    
    Parameters:
        path (str): Path al archivo que contiene los dominios.
    """
    global root
    if not root.is_leaf:
        opt = input("Ya existe un árbol. Desea sobreescribirlo? Y/N ")
        if opt == "N":
            return
    root = Node(".")
    if not os.path.isfile(path):
        print(f"El path {path} no es un archivo válido")
        return
    file = open(path, 'r')
    lines = file.readlines()
    for line in lines:
        add(line.rstrip())
    print_tree()

    
def add(st):
    """Agrega un dominio al árbol existe.
    
    Parametros:
        st (str): Dominio a agregar
    """
    domain = st.split('.')
    domain.reverse()
    add_tree(domain)


def query(st):
    """"Busca un dominio en el árbol.
    
    Parameters:
        st (str): Dominio a buscar.
    """
    domain = st.split('.')
    domain.reverse()
    ok = query_tree(domain)
    if ok:
        print(f"El dominio {st} esta en el árbol")
    else:
        print(f"El dominio {st} no está en el árbol")


def add_tree(domain):
    """Agrega un dominio al árbol existente.
    
    Parameters:
        domain (list<str>): Representación del dominio en formato de lista.
    """
    act = root
    for subdom in domain:
        act1 = find_node(act, f".{subdom}")
        if act1 is None:
            act = Node(f".{subdom}", parent=act)
        else:
            act = act1


def query_tree(domain):
    """Busca un dominio en el árbol
    
    Parameters:
        domain (list<str>): Representación del dominio en formato de lista.
    
    Returns:
        False: El dominio no está en el árbol.
        True: El dominio está en el árbol.
    """
    act = root
    for subdom in domain:
        act = find_node(act, f".{subdom}")
        if act is None:
            return False
    return True


def print_tree():
    """Imprime el árbol de dominios
    """
    for pre, _, node in RenderTree(root):
        print("%s%s" % (pre, node.name))


def export(path):
    """Crea una imagen png del árbol de dominios
    Parameters:
        path (str): Path donde se almacenará la imagen
    """
    from anytree.exporter import UniqueDotExporter
    UniqueDotExporter(root).to_picture(path)
    print("Se exportó una imagen png")
 

switcher = {
    "help": help,
    "create": create,
    "add": add,
    "query": query,
    "print": print_tree,
    "export": export,
    "exit": exit
}

while True:
    print("Ingrese help para ver las opciones")
    line = input("Ingrese una opción: ")
    op = line.split(' ')
    fun = switcher.get(op[0], lambda: "Opción inválida")
    if len(op) == 2 and op[0] in ["create", "add", "query", "export"]:
        fun(op[1])
    elif len(op) == 1 and op[0] in ["help", "print", "exit"]: 
        fun()
    else:
        print("Opción inválida.")
