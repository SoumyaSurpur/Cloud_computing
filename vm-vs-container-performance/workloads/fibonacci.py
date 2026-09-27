import sys
import time

def fibonacci(n: int) -> int:
    """Recursive Fibonacci implementation representing CPU-intensive algorithmic compute."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 35
    print(f"Executing recursive Fibonacci computation for n = {n}...")
    t0 = time.time()
    result = fibonacci(n)
    t1 = time.time()
    elapsed = t1 - t0
    print(f"Result: Fibonacci({n}) = {result}")
    print(f"Execution Time: {elapsed:.4f} seconds")
