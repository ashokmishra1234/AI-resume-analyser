import hashlib
import json
import os

import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL       = os.getenv("REDIS_URL", "redis://localhost:6379")
CACHE_TTL       = 3600   # cache analysis result for 1 hour
RATE_LIMIT_MAX  = 10     # max analyses per user per hour
RATE_LIMIT_WINDOW = 3600

# Try to connect once at module load. If Redis is down the app still works.
try:
    _client = redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=2)
    _client.ping()
    REDIS_AVAILABLE = True
except Exception:
    _client = None
    REDIS_AVAILABLE = False


# ── key builders ──────────────────────────────────────────────────────────────

def _analysis_key(resume_text: str, job_description: str) -> str:
    content = resume_text.strip() + "|||" + job_description.strip()
    return "analysis:" + hashlib.sha256(content.encode()).hexdigest()


def _rate_key(user_id: int) -> str:
    return f"rate:{user_id}"


def _blacklist_key(token: str) -> str:
    return "blacklist:" + hashlib.sha256(token.encode()).hexdigest()


# ── analysis cache ────────────────────────────────────────────────────────────

def get_cached_result(resume_text: str, job_description: str):
    """Return cached result dict or None if not found / Redis unavailable."""
    if not REDIS_AVAILABLE:
        return None
    try:
        raw = _client.get(_analysis_key(resume_text, job_description))
        return json.loads(raw) if raw else None
    except Exception:
        return None


def set_cached_result(resume_text: str, job_description: str, result: dict):
    """Cache the analysis result for CACHE_TTL seconds."""
    if not REDIS_AVAILABLE:
        return
    try:
        _client.setex(
            _analysis_key(resume_text, job_description),
            CACHE_TTL,
            json.dumps(result)
        )
    except Exception:
        pass


# ── rate limiting ─────────────────────────────────────────────────────────────

def check_rate_limit(user_id: int) -> tuple:
    """
    Returns (is_allowed: bool, remaining: int).
    Falls back to (True, RATE_LIMIT_MAX) when Redis is unavailable.
    """
    if not REDIS_AVAILABLE:
        return True, RATE_LIMIT_MAX
    try:
        key = _rate_key(user_id)
        count = _client.get(key)

        if count is None:
            # First call this window — create key with TTL
            _client.setex(key, RATE_LIMIT_WINDOW, 1)
            return True, RATE_LIMIT_MAX - 1

        count = int(count)
        if count >= RATE_LIMIT_MAX:
            return False, 0

        _client.incr(key)
        return True, RATE_LIMIT_MAX - count - 1
    except Exception:
        return True, RATE_LIMIT_MAX


# ── token blacklist (for logout) ──────────────────────────────────────────────

def blacklist_token(token: str, expires_in: int = 86400):
    """Store token hash in Redis so it is rejected even before JWT expiry."""
    if not REDIS_AVAILABLE:
        return
    try:
        _client.setex(_blacklist_key(token), expires_in, "1")
    except Exception:
        pass


def is_token_blacklisted(token: str) -> bool:
    """Return True if the token was explicitly revoked via logout."""
    if not REDIS_AVAILABLE:
        return False
    try:
        return _client.exists(_blacklist_key(token)) == 1
    except Exception:
        return False