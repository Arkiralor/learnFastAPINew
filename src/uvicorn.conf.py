# uvicorn_conf.py

import uvicorn
from multiprocessing import cpu_count

def run():
    workers:int = int(cpu_count() // 2) + 1
    print(f"Starting server with {workers} workers")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        workers=workers,
        loop="asyncio",
        proxy_headers=True,
        use_colors=True,
        timeout_keep_alive=3600,
    )

if __name__ == "__main__":
    run()