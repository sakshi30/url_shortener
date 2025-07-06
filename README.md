# 🔗 URL Shortener

A minimal, fast, and analytics-enabled URL shortener built with **FastAPI** and **MongoDB**.

---

## 🚀 Features

- Shorten long URLs into clean, shareable links
- Redirect to original destination
- Track click analytics (IP, user-agent, referrer, timestamp)
- Base62 encoding for compact short URLs

---

## 🛠 Tech Stack

- **Backend**: FastAPI
- **Database**: MongoDB
- **Encoding**: Base62
- **Deployment**: GitHub Pages / Local / Cloud

---

## ⚙️ Installation (Local Development)

```bash
git clone https://github.com/sakshi30/url_shortener.git
cd url_shortener
python3 -m venv .venv1
source .venv1/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
