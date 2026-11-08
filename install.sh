#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$ROOT_DIR/output_mo"
LOCALE_DIR="${LOCALE_DIR:-/usr/share/locale/hr/LC_MESSAGES}"
DATA_DIR="${DATA_DIR:-/usr/local/share}"
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
DATA_FILES=()
DATA_TARGETS=()

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

desktop_manifest="$(mktemp)"
trap 'rm -f "$desktop_manifest"' EXIT
python3 "$ROOT_DIR/translate_desktop.py" "$ROOT_DIR" "$OUTPUT_DIR/translated" /usr/share > "$desktop_manifest"
while IFS= read -r -d '' relative_path; do
    DATA_FILES+=("$OUTPUT_DIR/translated/$relative_path")
    DATA_TARGETS+=("$DATA_DIR/$relative_path")
done < "$desktop_manifest"

printf 'Compiled %d translation catalogs into %s\n' "${#MO_FILES[@]}" "$OUTPUT_DIR"
printf 'Prepared %d localized desktop files\n' "${#DATA_FILES[@]}"
printf 'AppStream PO catalogs are compiled as MO files only; AppStream XML is not updated.\n' >&2

if [[ "$COMPILE_ONLY" == true ]]; then
    exit 0
fi

sudo install -d "$LOCALE_DIR"
sudo install -m 0644 "${MO_FILES[@]}" "$LOCALE_DIR/"
for index in "${!DATA_FILES[@]}"; do
    sudo install -D -m 0644 "${DATA_FILES[$index]}" "${DATA_TARGETS[$index]}"
done
printf 'Installed translations into %s\n' "$LOCALE_DIR"
if [[ ${#DATA_FILES[@]} -gt 0 ]]; then
    printf 'Installed localized desktop files under %s\n' "$DATA_DIR"
fi
