import numpy as np
from numba import cuda, uint8

@cuda.jit
def compute_direction(max_depth, i_bolita, camino):

    # Get the depth index of the element
    depth = cuda.grid(1)
    depth = depth+1

    if depth <= max_depth:
        max = 1 << depth    # 2**depth
        index_in_depth = (i_bolita-1) % max
            
        mid = 1 << (depth-1)    # 2**(depth-1)
        if index_in_depth < mid:
            camino[depth-1] = 0
        else:
            camino[depth-1] = 1


def donde_esta_la_bolita_gpu(profundidad, i_bolita):

    # Configure the GPU
    threads_per_block = 1024
    blocks = int(np.ceil(profundidad / threads_per_block))

    # Allocate memory on the GPU
    gpu_camino = cuda.device_array(profundidad, dtype=np.uint8)

    compute_direction[blocks, threads_per_block](profundidad, i_bolita, gpu_camino)

    return gpu_camino.copy_to_host()
