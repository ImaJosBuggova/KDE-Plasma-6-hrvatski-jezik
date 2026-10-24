#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$ROOT_DIR/output_mo"
LOCALE_DIR="${LOCALE_DIR:-/usr/share/locale/hr/LC_MESSAGES}"
COMPILE_ONLY=false

case "${1:-}" in
    "") ;;
    --compile-only) COMPILE_ONLY=true ;;
    --help)
        printf 'Usage: %s [--compile-only]\n' "${0##*/}"
        exit 0
        ;;
    *)
        printf 'Unknown option: %s\n' "$1" >&2
        exit 2
        ;;
esac

mkdir -p "$OUTPUT_DIR"

mapfile -d '' PO_FILES < <(
    find "$ROOT_DIR" \
        -type d \( -name .git -o -name output_mo \) -prune -o \
        -type f -name '*.po' ! -name '.*.po' -print0 | sort -z
)

if [[ ${#PO_FILES[@]} -eq 0 ]]; then
    printf 'No PO files found under %s\n' "$ROOT_DIR" >&2
    exit 1
fi

declare -A CATALOGS=()
MO_FILES=()

for po_file in "${PO_FILES[@]}"; do
    filename="${po_file##*/}"
    catalog="${filename%.po}"

    if [[ -n "${CATALOGS[$catalog]:-}" ]]; then
        printf 'Duplicate catalog name "%s":\n  %s\n  %s\n' \
            "$catalog" "${CATALOGS[$catalog]}" "$po_file" >&2
        exit 1
    fi

    CATALOGS[$catalog]="$po_file"
    mo_file="$OUTPUT_DIR/$catalog.mo"
    msgfmt --check --check-header -o "$mo_file" "$po_file"
    MO_FILES+=("$mo_file")
done

printf 'Compiled %d translation catalogs into %s\n' "${#MO_FILES[@]}" "$OUTPUT_DIR"

if [[ "$COMPILE_ONLY" == true ]]; then
    exit 0
fi

sudo install -d "$LOCALE_DIR"
sudo install -m 0644 "${MO_FILES[@]}" "$LOCALE_DIR/"
printf 'Installed translations into %s\n' "$LOCALE_DIR"
