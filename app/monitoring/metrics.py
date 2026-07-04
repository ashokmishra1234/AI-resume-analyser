from prometheus_client import Counter, Histogram, Gauge

# ── Resume analysis ───────────────────────────────────────────────────────────

analyses_total = Counter(
    "resume_analyses_total",
    "Total resume analyses requested",
    ["status"],   # success | cache_hit | rate_limited | error
)

pipeline_duration_seconds = Histogram(
    "pipeline_duration_seconds",
    "Time taken to run the full 11-step analysis pipeline",
    buckets=[0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0],
)

# ── LLM calls ─────────────────────────────────────────────────────────────────

llm_calls_total = Counter(
    "llm_calls_total",
    "Total calls made to the Groq LLM API",
    ["status"],   # success | fallback_text | fallback_rule | error
)

# ── Redis cache ───────────────────────────────────────────────────────────────

cache_hits_total   = Counter("cache_hits_total",   "Redis cache hits for analysis results")
cache_misses_total = Counter("cache_misses_total",  "Redis cache misses for analysis results")

# ── Authentication ────────────────────────────────────────────────────────────

auth_events_total = Counter(
    "auth_events_total",
    "Auth events (register, login, logout, token_rejected)",
    ["event"],
)

# ── Comparisons ───────────────────────────────────────────────────────────────

comparisons_total = Counter(
    "comparisons_total",
    "Total resume comparisons requested",
)