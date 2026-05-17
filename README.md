# Crypto Graveyard 🪦

Database interaktif token crypto yang sudah mati — rug pull, exchange collapse, hack, abandoned, dan kasus terkenal lainnya. **Belajar dari yang sudah jatuh.**

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Flask](https://img.shields.io/badge/Flask-3.1-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Fitur

- 🪦 **30+ token mati** dengan info lengkap: nama, chain, tanggal mati, penyebab, kerugian
- 🔍 **Quick Check** — input symbol token, cek apakah ada di graveyard
- 📊 **Statistik & Visualisasi** — total loss, timeline kematian, penyebab utama
- 💸 **Top 5 kerugian terbesar** dalam sejarah crypto
- 🎯 **Filter & Search** — cari berdasarkan chain, penyebab, atau keyword

## 🎓 Edukatif

Setiap token punya konteks: founder, mekanisme kematian, kronologi, dan dampak finansial. Berguna buat:
- Belajar pola umum scam crypto
- Verifikasi sebelum invest token baru
- Riset historical crypto winter

## 🛠️ Instalasi

```bash
git clone https://github.com/moonzyr17/crypto-graveyard.git
cd crypto-graveyard

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 app.py
```

Buka `http://localhost:5000`

## 🔌 API Endpoints

| Endpoint | Method | Deskripsi |
|---|---|---|
| `/` | GET | Dashboard utama |
| `/api/tokens?q=&chain=&cause=` | GET | List/filter token |
| `/api/check/<symbol>` | GET | Cek apakah token mati |
| `/api/stats` | GET | Statistik agregat |

## 📚 Data Source

Data dikompilasi dari:
- CoinGecko (delisted tokens)
- DeFiLlama (dead protocols)
- Public investigation reports (FTX, Luna, Celsius, dll)
- News archives & SEC filings

## 🤝 Kontribusi

Mau menambah token mati? Edit `data/seed.json` dan PR. Format:

```json
{
  "name": "Token Name",
  "symbol": "TKN",
  "chain": "Ethereum",
  "death_date": "YYYY-MM-DD",
  "cause": "rug_pull|hack|fraud|collapse|abandoned|...",
  "loss_estimate_usd": 1000000,
  "description": "Cerita singkat tentang kematiannya...",
  "founder": "Nama founder",
  "type": "memecoin|defi|nft|exchange_token|...",
  "verdict": "rug|fraud|hack|collapse|..."
}
```

## 🤖 Tech Stack

- **Backend**: Flask + SQLite
- **Frontend**: Tailwind CSS + Chart.js
- **Deploy**: Railway

## ⚠️ Disclaimer

Data bersifat informasi historis. **Bukan jaminan token tidak ada di graveyard adalah token aman.** Always DYOR.

## Lisensi

MIT License
