from multiprocessing import Process,current_process

def hijo():
    print(f"Hola desde el {current_process().name}")

if __name__ == "__main__":
    process=[Process(target=hijo) for _ in range(2)]
    for p in process:
        p.start()
    for p in process:
        p.join()
    print("padre finalizo ",current_process().name)