#!/usr/bin/env bash

set -euo pipefail

SEARCH_DIR='./content/en/docs'

build_files_github_api() {
    if [[ -f ./temp_outdated ]]; then
        rm ./temp_outdated
    fi

    find $SEARCH_DIR -name '*.md' -not -name '_index.md' -exec git log --pretty="%H" -1 {} \; >> ./temp_outdated
}

query_old_files() {
    # find markdown files in content/en/docs excluding _index.md and glossary files
    SEARCH_FILES=($(find $SEARCH_DIR -name '*.md' -not -name '_index.md' -not -path '*/glossary/*'))
    MOD_FILES=($(git log --since '1 year ago' --name-only --pretty=format: content/en/docs | sort  | uniq | awk '{print "./"$1}' ))

    declare -a output=()
    for i in "${SEARCH_FILES[@]}"; do
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
}

query_old_files
build_files_github_api
