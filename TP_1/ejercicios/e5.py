import os,sys

def main():
    parent_to_child_r,parent_to_child_w=os.pipe()
    pid = os.fork()
    if pid > 0:
        os.close(parent_to_child_r)
        os.write(parent_to_child_w,b"hola")
        os.close(parent_to_child_w)

    else:
        print("hijo", os.getpid())
        print(os.read(parent_to_child_r,10))
        


if __name__ == "__main__":
    main()