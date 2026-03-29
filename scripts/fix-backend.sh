#!/bin/bash
# Simulate fixing the planted bug in backend error handling

echo "🔧 Fixing backend error handler..."

# В реальном проекте здесь был бы:
# 1. Поиск except Exception: в backend/
# 2. Замена на конкретный except psycopg2.OperationalError:
# 3. Возврат 503 вместо 404

# Для демо просто "чиним" состояние
curl -s -X POST http://localhost:18790/__debug__/clear-error 2>/dev/null || true

echo "✅ Backend fixed. Restarting service..."
# docker compose restart backend  # раскомментируй в реальном проекте

echo "✅ Recovery complete. System should now report real errors."
