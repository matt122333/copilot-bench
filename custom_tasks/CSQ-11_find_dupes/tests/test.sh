#!/bin/bash
set -e
cd /workspace
exec python3 /tests/test_csq-11_find_dupes.py
