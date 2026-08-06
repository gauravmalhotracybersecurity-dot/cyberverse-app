from slowapi import Limiter
from slowapi.util import get_remote_address

# Keyed by client IP. Good enough to stop runaway costs on AI-backed
# endpoints and brute-force attempts on auth endpoints for a single-instance
# deployment. If you scale to multiple backend instances behind a load
# balancer, back this with Redis (slowapi supports it via storage_uri).
limiter = Limiter(key_func=get_remote_address)
