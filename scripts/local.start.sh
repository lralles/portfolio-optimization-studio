#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_DIR="$PROJECT_ROOT/.local"
BACKEND_PID_FILE="$STATE_DIR/backend.pid"
FRONTEND_PID_FILE="$STATE_DIR/frontend.pid"
BACKEND_LOG="$STATE_DIR/backend.log"
FRONTEND_LOG="$STATE_DIR/frontend.log"

mkdir -p "$STATE_DIR"

matches_process() {
  local name="$1"
  local pid="$2"
  local command
  command="$(ps -p "$pid" -o command= 2>/dev/null || true)"

  case "$name" in
    backend)
      [[ "$command" == *"uvicorn src.webapi.main:app"* ]]
      ;;
    frontend)
      [[ "$command" == *"npm run dev"* || "$command" == *"vite"* ]]
      ;;
    *)
      return 1
      ;;
  esac
}

if [[ ! -x "$PROJECT_ROOT/.venv/bin/python" ]]; then
  echo "Backend virtual environment not found at $PROJECT_ROOT/.venv" >&2
  echo "Create it and install requirements.txt first." >&2
  exit 1
fi

if [[ ! -x "$PROJECT_ROOT/frontend/node_modules/.bin/vite" ]]; then
  echo "Frontend dependencies not found." >&2
  echo "Run: cd frontend && npm install" >&2
  exit 1
fi

start_process() {
  local name="$1"
  local pid_file="$2"
  local log_file="$3"
  shift 3

  if [[ -f "$pid_file" ]]; then
    local existing_pid
    existing_pid="$(<"$pid_file")"
    if [[ "$existing_pid" =~ ^[0-9]+$ ]] && kill -0 "$existing_pid" 2>/dev/null && matches_process "$name" "$existing_pid"; then
      echo "$name is already running (PID $existing_pid)"
      return 0
    fi
    rm -f "$pid_file"
  fi

  echo "Starting $name..."
  "$@" >"$log_file" 2>&1 &
  local pid=$!
  echo "$pid" >"$pid_file"

  sleep 1
  if ! kill -0 "$pid" 2>/dev/null; then
    echo "$name failed to start. See $log_file" >&2
    rm -f "$pid_file"
    return 1
  fi

  echo "$name started (PID $pid)"
}

start_process \
  "backend" \
  "$BACKEND_PID_FILE" \
  "$BACKEND_LOG" \
  bash -c "cd \"$PROJECT_ROOT\" && exec \"$PROJECT_ROOT/.venv/bin/python\" -m uvicorn src.webapi.main:app --host 127.0.0.1 --port 8000"

if ! start_process \
  "frontend" \
  "$FRONTEND_PID_FILE" \
  "$FRONTEND_LOG" \
  bash -c "cd \"$PROJECT_ROOT/frontend\" && exec npm run dev -- --host 127.0.0.1 --port 5173"; then
  if [[ -f "$BACKEND_PID_FILE" ]]; then
    backend_pid="$(<"$BACKEND_PID_FILE")"
    if [[ "$backend_pid" =~ ^[0-9]+$ ]]; then
      kill "$backend_pid" 2>/dev/null || true
    fi
    rm -f "$BACKEND_PID_FILE"
  fi
  exit 1
fi

cat <<EOF

Local services are running:
  Frontend: http://127.0.0.1:5173
  Backend:  http://127.0.0.1:8000
  API docs: http://127.0.0.1:8000/docs

Logs:
  $FRONTEND_LOG
  $BACKEND_LOG

Stop both with: scripts/local.stop.sh
EOF
