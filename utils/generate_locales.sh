#!/bin/bash

PROJECT_ROOT="$(pwd)/bot"
POT_FILE="messages.pot"

function update_po_files {
    for lang_dir in "$PROJECT_ROOT"/locales/*/LC_MESSAGES; do
        echo "Updating locale in $(basename "$(dirname "$lang_dir")")..."
        for po_file in "$lang_dir"/*.po; do
            echo "Merging $po_file..."
            msgmerge --update --backup=none "$po_file" "$POT_FILE"
        done
    done
}

function compile_locales() {
    for lang in bot/locales/*/LC_MESSAGES; do
        msgfmt "$lang"/*.po -o "$lang"/epictales.mo
    done
}

# Use find to list all .py files and pass them to xgettext through xargs
find "$PROJECT_ROOT" -iname '*.py' -not -path "*/__pycache__/*" -print | xargs xgettext --from-code=UTF-8 -o "$POT_FILE" -L Python

update_po_files
compile_locales

echo "POT file generated at $POT_FILE."
