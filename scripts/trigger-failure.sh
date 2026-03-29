#!/bin/bash
# Trigger simulated PostgreSQL failure for observability demo
# Call this before asking "What went wrong?"

echo "🔴 Simulating PostgreSQL failure..."
curl -s -X POST http://localhost:18790/__debug__/trigger-error 2>/dev/null || true
echo "✅ Failure triggered. Now ask agent: 'What went wrong?'"
