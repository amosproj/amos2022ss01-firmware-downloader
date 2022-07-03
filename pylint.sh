#!/bin/bash
export PYTHONPATH="$PYTHONPATH: ${PWD}/"
export PIPENV_VENV_IN_PROJECT="True"

cd "$(dirname "$0")" || exit 1
cd .. || exit 1

RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BOLD='\033[1m'
NC='\033[0m' # no color

if [[ $EUID -eq 0 ]]; then
  echo -e "\\n$RED""Running this script as root is not supported""$NC\\n"
fi

pylinter(){
  cd ./ || exit 1
  echo -e "\\n""$ORANGE""$BOLD"" pylint check""$NC""\\n""$BOLD""=================================================================""$NC"
  mapfile -t PY_SCRIPTS < <(find . -type d -name migrations -prune -false -o -iname "*.py")
  for PY_SCRIPT in "${PY_SCRIPTS[@]}"; do
    echo -e "\\n""$GREEN""Run pylint on $PY_SCRIPT:""$NC""\\n"
    pwd
    mapfile -t PY_RESULT < <(pipenv run pylint --rcfile=./amos2022ss01-firmware-downloader/.pylintrc "$PY_SCRIPT" 2> >(grep -v "Courtesy Notice\|Loading .env" >&2) )
    local RATING_10=0
    if [[ "${#PY_RESULT[@]}" -gt 0 ]]; then
      if ! printf '%s\n' "${PY_RESULT[@]}" | grep -q -P '^Your code has been rated at 10'; then
        for LINE in "${PY_RESULT[@]}"; do
          echo "$LINE"
        done
      else
        RATING_10=1
      fi
        if [[ "$RATING_10" -ne 1 ]]; then
        echo -e "\\n""$ORANGE$BOLD==> FIX ERRORS""$NC""\\n"
        ((MODULES_TO_CHECK=MODULES_TO_CHECK+1))
        MODULES_TO_CHECK_ARR+=( "$PY_SCRIPT" )
      else
        echo -e "$GREEN""$BOLD""==> SUCCESS""$NC""\\n"
      fi
    else
      echo -e "$GREEN""$BOLD""==> SUCCESS""$NC""\\n"
    fi
  done

  echo -e "\\n""$GREEN""Run pylint on all scripts:""$NC""\\n"
  pipenv run pylint --rcfile=./amos2022ss01-firmware-downloader/.pylintrc ./*  2> >(grep -v "Courtesy Notice\|Loading .env" >&2) | grep "Your code has been rated"
  cd .. || exit 1
}

# main
pylinter

if [[ "${#MODULES_TO_CHECK_ARR[@]}" -gt 0 ]]; then
  echo -e "\\n\\n""$GREEN$BOLD""SUMMARY:$NC\\n"
  echo -e "Modules to check: $MODULES_TO_CHECK\\n"
  for MODULE in "${MODULES_TO_CHECK_ARR[@]}"; do
    echo -e "$RED$BOLD==> FIX MODULE: ""$MODULE""$NC"
  done
  exit 1
fi
echo -e "$GREEN$BOLD===> ALL CHECKS SUCCESSFUL""$NC"
exit 0