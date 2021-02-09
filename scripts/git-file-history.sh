#!/usr/bin/env bash
set -euo pipefail

ALL_FILES=($(find ./content/en/docs -name '*.md' -not -name '_index.md'))
MOD_FILES=($(git log --since '1 year ago' --name-only --pretty=format: content/en/docs | sort  | uniq | awk '{print "./"$1}' ))

declare -a output=()
for i in "${ALL_FILES[@]}"; do
    if [[ ! " ${MOD_FILES[@]} " =~ " $i " ]]; then
        timestamp=$(git log -1 --pretty='format:%as' $i)
        output+=("$timestamp $i")
    fi
done

IFS=$'\n'
sorted=($(sort <<<"${output[*]}"))
unset IFS

for row in "${sorted[@]}"; do
    echo "$row"
done
