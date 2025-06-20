import multiprocessing,time
def main():
    with sem:
        print("Entrando!!!")
        time.sleep(1)
        print("Saliendo!!!")
    

if __name__ == "__main__":
    concurrency=3
    sem=multiprocessing.Semaphore(concurrency)
    for _ in range(10):
        p=multiprocessing.Process(target=main)
        p.start()