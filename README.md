# KDE Plasma 6 - Hrvatski prijevod (Lokalizacija)

Ovaj repozitorij sadrži neslužbene prijevode i lokalizacijske datoteke za **KDE Plasma 6** radno okruženje na hrvatski jezik.

Cilj projekta je pružiti potpuni i točan prijevod korisničkog sučelja KDE Plasma 6 okruženja, uključujući sistemske postavke (`System Settings`), KCM module, prateće aplikacije te opise stavki u izbornicima i bočnim trakama.

---

## 📌 Status prijevoda

| Komponenta / Modul | Status | Napomena / Prevoditelj |
| :--- | :---: | :--- |
| **plasma-workspace** | ✅ | Pregledao Roko Tomović |
| **systemsettings** | ✅ | Pregledao Roko Tomović |
| **plasma-desktop** | ❌ | Prevedeno s AI-jem, čeka provjeru |

❌ Nije prevedeno
⚠️ Prevedeno s AI-jem, čeka provjeru
✅ Ručno provjereno

## 🛠️ Kako instalirati i testirati prijevode

Ako želite isprobati ove prijevode na svom Arch Linux (ili drugom) sustavu s KDE Plasma 6 okruženjem, slijedite ove korake:

### 1. Klonirajte repozitorij
```bash
git clone https://github.com/VAŠ_USERNAME/KDE-Plasma-6-Hrvatski-jezik.git
cd KDE-Plasma-6-Hrvatski-jezik
```

### 2. Kompajliranje i instalacija `.po` datoteka
Prijevod se mora pretvoriti u `.mo` binarni format i postaviti u sistemski direktorij za hrvatski jezik (`hr`):

```bash
# Primjer za prevođenje i kopiranje systemsettings.po
msgfmt systemsettings.po -o systemsettings.mo
sudo cp systemsettings.mo /usr/share/locale/hr/LC_MESSAGES/

# Primjer za desktop nazive u lijevoj traci
msgfmt desktop_plasma-desktop.po -o desktop_plasma-desktop.mo
sudo cp desktop_plasma-desktop.mo /usr/share/locale/hr/LC_MESSAGES/
```

### 3. Osvježavanje KDE predmemorije (Cache)
Da bi KDE Plasma prepoznala nove prijevode, potrebno je osvježiti sistemsku predmemoriju:

```bash
kbuildsycoca6 --noincremental
```

Nakon ovoga ponovno pokrenite aplikaciju ili se odjavite i ponovno prijavite u sustav.

---

## 🤝 Kako doprinijeti (Contribution)

Svaka pomoć u obliku provjere AI prijevoda, ispravljanja tipfelera ili prevođenja novih modulā je i više nego dobrodošla!

1. **Forkajte** ovaj repozitorij.
2. Kreirajte novu granu (`git checkout -b prijevod-modula`).
3. Napravite izmjene u `.po` datotekama koristeći alate kao što su [Poedit](https://poedit.net/) ili obični uređivač teksta.
4. Otvorite **Pull Request** s opisom izmjena.

---

## 👤 Autor i održavatelj

* **Roko Tomović** – *Inicijator projekta, provjera i korektura AI prijevoda*