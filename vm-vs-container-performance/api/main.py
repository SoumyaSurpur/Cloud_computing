from fastapi import FastAPI
import math
import time

app = FastAPI(
    title="Cloud Computing Microservice Benchmark",
    description="FastAPI service for evaluating VM vs Container application latency & throughput",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "service": "cloud-performance-benchmark",
        "runtime": "FastAPI with Uvicorn"
    }

@app.get("/compute/{iterations}")
def cpu_bound_endpoint(iterations: int = 100000):
    """Executes a compute-heavy mathematical loop to benchmark CPU scheduling overhead."""
    start_time = time.perf_counter()
    accum = 0.0
    for i in range(1, iterations + 1):
        accum += math.sqrt(i) * math.sin(i)
    elapsed = time.perf_counter() - start_time
    return {
        "iterations": iterations,
        "execution_time_seconds": elapsed,
        "accumulated_value": accum
    }
