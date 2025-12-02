#!/bin/sh

set -e

TEMP_PATH="./template/template.go"

while [[ $# -gt 0 ]]; do
  case $1 in
    -y|--year)
      p_y="$2"
      shift
      shift
      ;;
    -d|--day)
      p_d="$2"
      shift
      shift
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
  esac
done

if [[ -n "$p_d" ]] && [[ -n "$p_y" ]]; then
  p_t=".\\$p_y\\d$p_d"
  mkdir -p "$p_t"
  cat "$TEMP_PATH" > "$p_t\\p1.go"
  echo "creating new files $p_t\\p1.go"
  cat "$TEMP_PATH" > "$p_t\\p2.go"
  echo "creating new files $p_t\\p2.go"
  touch "$p_t\\data.txt"
  echo "creating new files $p_t\\data.txt"
  touch "$p_t\\test_data.txt"
  echo "creating new files $p_t\\test_data.txt"
fi

read -p "Press any key to resume ..."