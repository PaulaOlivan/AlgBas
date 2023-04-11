import numpy as np
from numba import cuda, float32

@cuda.jit
def matmul(A, B, C):
    """Matrix multiplication on GPU"""
    # Get the row and column indices of the element
    row, col = cuda.grid(2)
    # Calculate the product of corresponding row and column elements
    if row < C.shape[0] and col < C.shape[1]:
        C[row, col] = 0.0
        for k in range(A.shape[1]):
            C[row, col] += A[row, k] * B[k, col]

def main():
    # Define matrix dimensions
    N = 1024
    M = 2048
    K = 1536
    
    # Initialize random matrices
    A = np.random.rand(N, M).astype(np.float32)
    B = np.random.rand(M, K).astype(np.float32)
    C = np.zeros((N, K)).astype(np.float32)

    # Configure the GPU
    threads_per_block = (16, 16)
    blocks_per_grid_x = int(np.ceil(N / threads_per_block[0]))
    blocks_per_grid_y = int(np.ceil(K / threads_per_block[1]))
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

    # Allocate memory on the GPU
    d_A = cuda.to_device(A)
    d_B = cuda.to_device(B)
    d_C = cuda.to_device(C)

    # Perform matrix multiplication on the GPU
    matmul[blocks_per_grid, threads_per_block](d_A, d_B, d_C)

    # Copy the result back to the CPU
    C = d_C.copy_to_host()

    # Print the result
    print(C)

if __name__ == '__main__':
    main()
