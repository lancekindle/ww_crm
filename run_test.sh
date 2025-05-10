#!/bin/bash
failed_tests_reminders=$(cat << EOF
You have some failed tests. I would like to remind you that failed tests must be treated cautiously!
For each test, please use the think tool to think very hard about why the test is failing, what the purpose of the test
is, and how to make the test pass, maintaining the purpose of the test (e.g. verify a feature is working as desired)
EOF
)

set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
"${SCRIPT_DIR}/.venv/bin/python" -m pytest $@  || echo $failed_tests_reminders
