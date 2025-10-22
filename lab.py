import numpy as np

import time
import tracemalloc

class NodArbore:
    def __init__(self, _informatie, _parinte=None, _g=0):
        self.informatie = _informatie
        self.parinte = _parinte
        self.g = _g

    def drumRadacina(self):
        nod = self
        l = []
        while nod:
            l.append(nod)
            nod = nod.parinte
        return l[::-1]

    def inDrum(self, infoNod):
        nod = self
        while nod:
            if nod.informatie == infoNod:
                return True
            nod = nod.parinte
        return False

    def __str__(self):
        return str(self.informatie)

    def __repr__(self):
        sirDrum = "->".join([str(nod) for nod in self.drumRadacina()])
        return f"{self.informatie}, ({sirDrum}), cost={self.g}"

class Graf:
    def __init__(self, _matr, _start, _scopuri):
        self.matr = _matr
        self.start = _start
        self.scopuri = _scopuri

    def scop(self, informatieNod):
        return informatieNod in self.scopuri

    def succesori(self, nod):
        lSuccesori = []
        for infoSuccesor in range(len(self.matr)):
            cost = self.matr[nod.informatie][infoSuccesor]
            # considerăm muchie validă dacă cost != 0 și nu e sentinel 100
            conditieMuchie = (cost != 0 and cost != 100)
            conditieNotInDrum = not nod.inDrum(infoSuccesor)
            if conditieMuchie and conditieNotInDrum:
                nodNou = NodArbore(infoSuccesor, _parinte=nod, _g=nod.g + cost)
                lSuccesori.append(nodNou)
        return lSuccesori

def breadth_first(gr, nsol):
    coada = [NodArbore(gr.start, _parinte=None, _g=0)]
    while coada:
        nodCurent = coada.pop(0)
        if gr.scop(nodCurent.informatie):
            print("Solutie: ", end="")
            print(repr(nodCurent))
            nsol -= 1
            if nsol == 0:
                return
        coada += gr.succesori(nodCurent)

def depth_first(gr, nsol=1):
    DF(gr, NodArbore(gr.start, _parinte=None, _g=0), nsol)

def DF(gr, nodCurent, nsol):
    if nsol <= 0:
        return nsol
    if gr.scop(nodCurent.informatie):
        print("Solutie: ", end="")
        print(repr(nodCurent))
        nsol -= 1
        if nsol == 0:
            return 0
    lSuccesori = gr.succesori(nodCurent)
    for sc in lSuccesori:
        if nsol != 0:
            nsol = DF(gr, sc, nsol)
    return nsol

def depth_first_nerecursiv(gr, nsol):
    stiva = [NodArbore(gr.start, _parinte=None, _g=0)]
    while stiva:
        nodCurent = stiva.pop(-1)
        if gr.scop(nodCurent.informatie):
            print("Solutie: ", end="")
            print(repr(nodCurent))
            nsol -= 1
            if nsol == 0:
                return
        stiva += gr.succesori(nodCurent)[::-1]

#################################################

m = np.array([
    [0, 3, 5, 10, 0, 0, 100],
    [0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 4, 9, 3, 0],
    [0, 3, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 5],
    [0, 0, 3, 0, 0, 0, 0]
])
start = 0
scopuri = [4]
#################################################
gr = Graf(m, start, scopuri)


print("Solutii breadth-first:")
tracemalloc.start()
start_time = time.time()

breadth_first(gr, 4)

end_time = time.time()
current_mem, peak_mem = tracemalloc.get_traced_memory()
tracemalloc.stop()

print("\n")
print(f"Timp executie: {end_time - start_time} secunde")
print(f"Memorie folosita: {peak_mem / 1024:.2f} KB")



print("\n----------------\n")
print("Solutii depth-first (recursiv):")
print("\n")
tracemalloc.start()
start_time = time.time()

# breadth_first(gr, 4)
depth_first(gr, 4)

end_time = time.time()
current_mem, peak_mem = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(f"Timp executie: {end_time - start_time} secunde")
print(f"Memorie folosita: {peak_mem / 1024:.2f} KB")

print("\n----------------\n")
print("Solutii depth-first (nerecursiv):")

tracemalloc.start()
start_time = time.time()

depth_first_nerecursiv(gr, 4)

end_time = time.time()
current_mem, peak_mem = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(f"Timp executie: {end_time - start_time} secunde")
print(f"Memorie folosita: {peak_mem / 1024:.2f} KB")