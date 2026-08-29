#!/bin/bash
set -e
cd /workspace
exec python3 /tests/test_csq-12_lru_cache.py
