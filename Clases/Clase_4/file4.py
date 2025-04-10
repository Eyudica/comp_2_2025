import os

def main(command):
    p1_r, p1_w = os.pipe()
    pid = os.fork()
    if pid > 0:
        os.close(p1_r)
        os.write(p1_w, command.encode())
        os.close(p1_w)
    else:
        os.close(p1_w)
        response = os.read(p1_r, 100).decode()
        os.close(p1_r)
        os.system(response)
        os._exit(0)
if __name__ == "__main__":
    while True:
        command = input("> ")
        if command == "exit":
            break
        else:
            main(command)