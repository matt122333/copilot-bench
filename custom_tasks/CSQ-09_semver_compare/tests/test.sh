#!/bin/bash
set -e
cd /workspace
exec python3 /tests/test_csq-09_semver_compare.py
