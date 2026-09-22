#!/bin/bash

mkdir -p output_mo

# Pretvori template-ove u portable object file-ove
for pot in *.pot; do
    msginit --no-translator -i "$pot" -o "${pot%.pot}.po" -l hr
done

# Kompajliraj sve .po datoteke u .mo
for po in *.po; do
    msgfmt -o "output_mo/${po%.po}.mo" "$po"
done

# Kopiraj sve kompajlirane datoteke u sistemski lokacijski direktorij
sudo cp output_mo/*.mo /usr/share/locale/hr/LC_MESSAGES/
