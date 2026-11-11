"""G-code dialect profiles.

A dialect profile is a YAML file shipped inside the package (``profiles/``) that
holds everything machine- or controller-specific: G0 rapid feed, default bead
width, which M-codes switch the laser and the wire feeder, and so on. Keeping
these values out of the parser code is what allows supporting several machines
without hardcoding any of them.

The profile schema (validated with Pydantic v2) is defined in Phase 1.
"""
