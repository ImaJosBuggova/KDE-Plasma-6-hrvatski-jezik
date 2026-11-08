#!/bin/bash

tot_trans=0
tot_fuzzy=0
tot_untrans=0

while IFS= read -r -d '' file; do
    # msgfmt vraća statistiku na stderr, pa ga hvatamo s 2>&1
    stats=$(msgfmt -o /dev/null --statistics "$file" 2>&1)
    
    # Čitamo liniju po liniju iz outputa msgfmt-a
    while IFS= read -r line; do
        # Uzimamo prvi broj u liniji
        num=$(echo "$line" | awk '{print $1}')
        [[ -z "$num" ]] && continue
        
        # Provjeravamo o kojoj se vrsti poruke radi
        if echo "$line" | grep -q "prevedenih" && ! echo "$line" | grep -q "netočnih" && ! echo "$line" | grep -q "neprevedenih"; then
            tot_trans=$((tot_trans + num))
        elif echo "$line" | grep -q "netočnih"; then
            tot_fuzzy=$((tot_fuzzy + num))
        elif echo "$line" | grep -q "neprevedenih"; then
            tot_untrans=$((tot_untrans + num))
        fi
    done <<< "$stats"
done < <(find . -name "*.po" -print0)

echo "Ukupno -> Prevedeno: $tot_trans, Netočno: $tot_fuzzy, Neprevedeno: $tot_untrans"