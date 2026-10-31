# CROUS Housing Notifier

### Automated Monitoring and Real-Time Notification Engine for CROUS Student Accommodations

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Discord](https://img.shields.io/badge/Discord-Webhook-5865F2.svg)](https://discord.com/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-0088cc.svg)](https://telegram.org/)

🌐 **Language / Langue** : **English 🇬🇧** | [Français 🇫🇷](#-version-française)

---

An intelligent Python service that reverse-engineers the internal REST API of the French student housing portal ([trouverunlogement.lescrous.fr](https://trouverunlogement.lescrous.fr)) to monitor vacancies in real time and deliver instant alerts via **Discord Webhooks** or **Telegram**.

---

## 🎯 Features

* ⚡ **High Performance Direct API:** Directly queries the underlying internal SvelteKit endpoint (`POST /api/fr/search/47`) with lightweight JSON payloads — **no slow or brittle headless browsers** (Selenium / Playwright / Puppeteer).
* 🔐 **Dual Mode Support:**
  * **Public Mode:** Queries open nationwide housing inventory without authentication.
  * **Authenticated Mode:** Unlocks restricted quotas and priority allocations (scholarship holders, DSE status) using session cookies (`PHPSESSID`).
* 🔔 **Multi-Channel Instant Notifications:** Rich embeds formatted with residence address, monthly rent, floor area, transport connections, and direct reservation links sent to **Discord** or **Telegram**.
* 🛡️ **Zero Duplicate Alerts:** Maintains local transaction history cache (`seen_logements.json`) to prevent notification spam across restarts.
* 🌍 **Configurable Geographic Boundaries:** Target any city, metropolitan area, or query nationwide using geographic bounding boxes (`bounds`).
* 🔒 **Secure Credential Isolation:** All tokens and session cookies remain safely isolated inside `.env`.

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/delaubier/crous-housing-notifier.git
cd crous-housing-notifier
```

### 2. Set up virtual environment & install dependencies
```bash
# Using standard Python
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Or ultra-fast with uv
uv venv
uv pip install -r requirements.txt
```

### 3. Configure `.env`
Copy the template configuration:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
# Optional: your PHPSESSID from Chrome DevTools for authenticated/student quotas
CROUS_PHPSESSID=

# Bounding box coordinates (lon1_lat1_lon2_lat2). Default is Paris & inner suburbs
CROUS_BOUNDS=2.2402013113776147_48.934454116839824_2.4321187308112084_48.752114467903624

# Check interval in seconds (default: 60s)
CHECK_INTERVAL_SECONDS=60

# Optional notification channels
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

### 4. Run the Bot
```bash
# Continuous monitoring
python bot.py

# One-shot check
python bot.py --once
```

---

<br>

<a name="-version-française"></a>
## 🇫🇷 Version Française

### Pourquoi ce projet ?
Face à la saturation des logements étudiants en France (notamment en Île-de-France), les logements CROUS remis en ligne sont réservés en quelques minutes. Vérifier manuellement le site est fastidieux. 

Ce projet automatise cette veille en interrogeant directement l'API interne JSON du CROUS pour détecter immédiatement toute nouvelle vacance et envoyer une alerte instantanée.

---

### ⚙️ Options de Configuration (`.env`)

| Variable | Description | Exemple / Défaut |
| :--- | :--- | :--- |
| `CROUS_PHPSESSID` | Cookie de session récupéré dans Chrome DevTools pour voir les logements réservés aux boursiers / DSE. | `u4ta9kn...` (Optionnel) |
| `CROUS_BOUNDS` | Coordonnées de recherche rectangulaire (`lon1_lat1_lon2_lat2`). Laisser vide pour toute la France. | Paris et banlieue par défaut |
| `MAX_PRICE_EUROS` | Plafond de loyer maximum en euros. | `500` (Optionnel) |
| `CHECK_INTERVAL_SECONDS` | Intervalle entre chaque vérification en secondes. | `60` |
| `DISCORD_WEBHOOK_URL` | URL de Webhook pour recevoir les alertes sur un salon Discord. | `https://discord.com/...` |
| `TELEGRAM_BOT_TOKEN` | Token du bot Telegram. | `123456:ABC...` |
| `TELEGRAM_CHAT_ID` | Identifiant de la conversation Telegram où envoyer les alertes. | `987654321` |

---

### 🔎 Comment récupérer son `PHPSESSID` ?
1. Connectez-vous sur [trouverunlogement.lescrous.fr](https://trouverunlogement.lescrous.fr) avec votre compte étudiant.
2. Ouvrez les outils de développement (**F12**).
3. Allez dans l'onglet **Application** (ou *Stockage*) > **Cookies** > `https://trouverunlogement.lescrous.fr`.
4. Copiez la valeur du cookie **`PHPSESSID`** et collez-la dans votre `.env`.

---

## ⚖️ Avertissement & Éthique (Disclaimer)

Cet outil est un projet éducatif open-source conçu pour la veille personnelle d'informations publiques. 
* Il respecte l'infrastructure en imposant un intervalle d'interrogation modéré (60s+ par défaut).
* Il n'automatise **pas** la signature ni la réservation illégitime d'un logement (qui doit être effectuée manuellement par l'étudiant).

---

## 📜 Licence

Distribué sous licence **MIT**. Voir [LICENSE](LICENSE) pour plus de détails.

