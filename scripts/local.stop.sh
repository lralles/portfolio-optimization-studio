#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_DIR="$PROJECT_ROOT/.local"
BACKEND_PID_FILE="$STATE_DIR/backend.pid"
FRONTEND_PID_FILE="$STATE_DIR/frontend.pid"

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

stop_process() {
  local name="$1"
  local pid_file="$2"

  if [[ ! -f "$pid_file" ]]; then
    echo "$name is not running"
    return 0
  fi

  local pid
  pid="$(<"$pid_file")"
  rm -f "$pid_file"

  if [[ ! "$pid" =~ ^[0-9]+$ ]] || ! kill -0 "$pid" 2>/dev/null; then
    echo "$name was not running"
    return 0
  fi

  if ! matches_process "$name" "$pid"; then
    echo "$name PID file was stale; no matching process was stopped"
    return 0
  fi

  echo "Stopping $name (PID $pid)..."
  kill "$pid" 2>/dev/null || true

  for _ in {1..20}; do
    if ! kill -0 "$pid" 2>/dev/null; then
      echo "$name stopped"
      return 0
    fi
    sleep 0.25
  done

  echo "$name did not stop gracefully; sending SIGKILL"
  kill -KILL "$pid" 2>/dev/null || true
}

stop_process "frontend" "$FRONTEND_PID_FILE"
stop_process "backend" "$BACKEND_PID_FILE"
