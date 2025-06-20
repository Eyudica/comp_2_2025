# import multiprocessing

# def aumentar_contador(contador):
#     contador.value+=1
#     print(contador.value)

# if __name__ == "__main__":
#     contador=multiprocessing.Value('i',0)
#     for _ in range(4):
#         p=multiprocessing.Process(target=aumentar_contador,args=(contador,))
#         p.start()

import multiprocessing

def aumentar_contador(contador):
    with lock:
        contador.value+=1
        print(contador.value)

if __name__ == "__main__":
    lock=multiprocessing.Lock()
    contador=multiprocessing.Value('i',0)
    for _ in range(100):
        p=multiprocessing.Process(target=aumentar_contador,args=(contador,))
        p.start()
        p.join() # el join no garantiza exclusion , solo sirve para esperar al proceso anterior que termine
