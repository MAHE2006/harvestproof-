"""Small in-memory rate limiter (per client address). Behind a proxy, start uvicorn with --proxy-headers so the real address is used.
For several server processes use a shared limiter at the proxy instead. Disable with HP_RATE_LIMIT=0."""
import collections, os, threading, time
from fastapi import Depends, HTTPException, Request


class Limiter:
    def __init__(self):
        self.hits, self.lock = collections.defaultdict(collections.deque), threading.Lock()

    def reset(self):
        with self.lock:
            self.hits.clear()

    def allow(self, key, n, per):
        if os.getenv("HP_RATE_LIMIT", "1") == "0":
            return True
        now = time.monotonic()
        with self.lock:
            q = self.hits[key]
            while q and q[0] <= now - per:
                q.popleft()
            if len(q) >= n:
                return False
            q.append(now)
            if len(self.hits) > 20000:                       # forget idle clients
                for k in [k for k, d in self.hits.items() if not d or d[-1] <= now - per]:
                    del self.hits[k]
            return True


limiter = Limiter()


def rate(name, n, per=60):
    def check(request: Request):
        ip = request.client.host if request.client else "?"
        if not limiter.allow(f"{name}:{ip}", n, per):
            raise HTTPException(429, "Too many requests. Please wait a minute and try again.")
    return Depends(check)
