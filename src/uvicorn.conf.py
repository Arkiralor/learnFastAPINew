# uvicorn_conf.py

import uvicorn
from multiprocessing import cpu_count

def run():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        workers=int(cpu_count()//2) + 1,
        loop="asyncio",
        proxy_headers=True,
        use_colors=True,
        timeout_keep_alive=3600,
    )

if __name__ == "__main__":
    run()