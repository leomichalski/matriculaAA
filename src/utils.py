import threading
import os


def run_in_parallel(command):
    def target():
        os.system(command)
    threading.Thread(target=target).start()
    # nao to dando stop(), mas nao me importo
    # ate pq as threads q eu to usando vao parar. confia
