# KDE Plasma 6 - Hrvatski prijevod

Ovaj repozitorij sadrži neslužbene prijevode **KDE Plasma 6** radnog okruženja na hrvatski jezik.

Cilj projekta je pružiti potpuni i točan prijevod korisničkog sučelja KDE Plasma 6 okruženja.

---

## 📌 Status prijevoda

| Komponenta / Modul | Status | Napomena |
| :--- | :---: | :--- |
| **plasma-workspace** | ✅ | Pregledao Roko Tomović |
| **systemsettings** | ✅ | Pregledao Roko Tomović |
| **plasma-desktop** | ⚠️ | Čeka provjeru |
| **ark** | ⚠️ | Čeka provjeru |
| **bluedevil** | ⚠️ | Čeka provjeru |
| **breeze** | ⚠️ | Čeka provjeru |
| **breeze-icons** | ⚠️ | Čeka provjeru |
| **dolphin** | ⚠️ | Čeka provjeru |
| **kdeconnect-kde** | ⚠️ | Čeka provjeru |
| **kdecoration** | ⚠️ | Čeka provjeru |
| **kinfocenter** | ⚠️ | Čeka provjeru |
| **kio** | ⚠️ | Čeka provjeru |
| **kio-extras** | ⚠️ | Čeka provjeru |
| **knotifications** | ⚠️ | Čeka provjeru |
| **knotifyconfig** | ⚠️ | Čeka provjeru |
| **konzole** | ⚠️ | Čeka provjeru |
| **kscreenlocker** | ⚠️ | Čeka provjeru |
| **kwin** | ⚠️ | Čeka provjeru |
| **kwindowsystem** | ✅ | Pregledao Roko Tomović |
| **oxygen-sounds** | ✅ | Pregledao Roko Tomović |
| **plasma-integration** | ⚠️ | Čeka provjeru |
| **plasma-nm** | ⚠️ | Čeka provjeru |
| **plasma-pa** | ⚠️ | Čeka provjeru |
| **plasma-settings** | ✅ | Pregledao Roko Tomović |
| **plasma-systemmonitor** | ⚠️ | Čeka provjeru |
| **sddm-kcm** | ⚠️ | Čeka provjeru |
| **kdeplasma-addons** | ⚠️ | Čeka provjeru |
| **libplasma** | ⚠️ | Čeka provjeru |
| **plasma-browser-integration** | ⚠️ | Čeka provjeru |
| **plasma-login-manager** | ⚠️ | Čeka provjeru |
| **kio-admin** | ⚠️ | Čeka provjeru |
| **powerdevil** | ✅ | Pregledao Roko Tomović |
| **frameworkintegration** | ❌ | Nije prevedeno |
| **kactivitymanagerd** | ❌ | Nije prevedeno |
| **kcmutils** | ❌ | Nije prevedeno |
| **kconfig** | ❌ | Nije prevedeno |
| **kconfigwidgets** | ❌ | Nije prevedeno |
| **kcoreaddons** | ❌ | Nije prevedeno |
| **kcrash** | ❌ | Nije prevedeno |
| **kdbusaddons** | ❌ | Nije prevedeno |
| **kdeclerative** | ❌ | Nije prevedeno |
| **kglobalaccel** | ❌ | Nije prevedeno |
| **kguiaddons** | ❌ | Nije prevedeno |
| **ki18n** | ❌ | Nije prevedeno |
| **kiconthemes** | ❌ | Nije prevedeno |
| **kjobwidgets** | ❌ | Nije prevedeno |
| **knewstuff** | ❌ | Nije prevedeno |
| **kpackage** | ❌ | Nije prevedeno |
| **kparts** | ❌ | Nije prevedeno |
| **kpeople** | ❌ | Nije prevedeno |
| **krunner** | ❌ | Nije prevedeno |
| **kservice** | ❌ | Nije prevedeno |
| **kstatusnotifieritem** | ❌ | Nije prevedeno |
| **ksvg** | ❌ | Nije prevedeno |
| **ktextwidgets** | ❌ | Nije prevedeno |
| **kwidgetsaddons** | ❌ | Nije prevedeno |
| **kxmlgui** | ❌ | Nije prevedeno |
| **libksysguard** | ❌ | Nije prevedeno |

❌ Nije prevedeno
⚠️ Prevedeno s AI-jem, čeka provjeru
✅ Ručno provjereno

## 🛠️ Kako instalirati i testirati prijevode

Ako želite isprobati ove prijevode na svom sustavu s KDE Plasma 6 okruženjem, u svom omiljenom terminalu pokrenite komandu u datoteci gdje ste kopirali repozitorij:

```bash
./install.sh
```

> Nekad je potrebno osvježiti KDE predmemoriju

### 3. Osvježavanje KDE predmemorije (Cache)
Da bi KDE Plasma prepoznala nove prijevode, potrebno je osvježiti sistemsku predmemoriju:

```bash
kbuildsycoca6 --noincremental
```

Nakon ovoga ponovno pokrenite aplikaciju ili se odjavite i ponovno prijavite u sustav ili ponovo pokrenite cijeli linux sustav (moja omiljena metoda).

---

## 🤝 Kako doprinijeti (Contribution)

Svaka pomoć u obliku provjere AI prijevoda, ispravljanja tipfelera ili prevođenja novih modulā je i više nego dobrodošla!

1. **Napantarulajte** ovaj repozitorij.
2. Stvorite novu granu (`git checkout -b prijevod-modula`).
3. Napravite izmjene.
4. Otvorite **Pull Request** s opisom izmjena.

---

## 👤 Autor i održavatelj

* **Roko Tomović** – *Inicijator projekta, provjera i korektura AI prijevoda*

## Za gledat statove

find . -name "*.po" -exec sh -c 'echo -n "$1: "; msgfmt --statistics -o /dev/null "$1"' _ {} \; 2>&1