#!/bin/sh
# Opt-in trace of which instruction files Claude Code loads, and why.
# Inert unless NORTHWIND_TRACE=1. Log: $NORTHWIND_TRACE_LOG (default /tmp/northwind-instructions-trace.log)
#
#   NORTHWIND_TRACE=1 claude          # then, in another terminal:
#   tail -f /tmp/northwind-instructions-trace.log
if [ "$NORTHWIND_TRACE" != "1" ]; then
  cat > /dev/null
  exit 0
fi
LOG="${NORTHWIND_TRACE_LOG:-/tmp/northwind-instructions-trace.log}"
python3 -c '
import datetime, json, sys
d = json.load(sys.stdin)
line = [datetime.datetime.now().strftime("%H:%M:%S"), d.get("memory_type", "?"), d.get("load_reason", "?"), d.get("file_path", "?")]
if d.get("trigger_file_path"):
    line.append("<- read " + d["trigger_file_path"])
print("  ".join(line))
' >> "$LOG"
