"""Shared pytest configuration.

Hypothesis profiles:
    * ``dev`` (default): fast feedback while coding.
    * ``ci``: more examples, derandomized so CI failures are reproducible.

Select with the ``HYPOTHESIS_PROFILE`` environment variable.
"""

import os

from hypothesis import HealthCheck, settings

settings.register_profile("dev", max_examples=50)
settings.register_profile(
    "ci",
    max_examples=300,
    derandomize=True,
    deadline=None,  # shared CI runners have noisy timings
    suppress_health_check=[HealthCheck.too_slow],
)
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "dev"))
