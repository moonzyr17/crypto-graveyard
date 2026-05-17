#!/usr/bin/env python3
"""
Crypto Graveyard 🪦
Database interaktif token crypto yang sudah mati.
"""

import os
import json
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify, g

app = Flask(__name__)
DB_PATH = os.environ.get("DB_PATH", "graveyard.db")
SEED_PATH = "data/seed.json"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Initialize database and seed data if empty."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            symbol TEXT NOT NULL,
            chain TEXT,
            death_date TEXT,
            cause TEXT,
            loss_estimate_usd REAL,
            description TEXT,
            founder TEXT,
            type TEXT,
            verdict TEXT
        )
    """)
    conn.commit()

    # Seed if empty
    count = c.execute("SELECT COUNT(*) FROM tokens").fetchone()[0]
    if count == 0 and os.path.exists(SEED_PATH):
        with open(SEED_PATH, "r", encoding="utf-8") as f:
            seed = json.load(f)
        for t in seed:
            c.execute("""
                INSERT INTO tokens (name, symbol, chain, death_date, cause, loss_estimate_usd,
                                    description, founder, type, verdict)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                t.get("name"), t.get("symbol"), t.get("chain"), t.get("death_date"),
                t.get("cause"), t.get("loss_estimate_usd"), t.get("description"),
                t.get("founder"), t.get("type"), t.get("verdict")
            ))
        conn.commit()
        print(f"✓ Seeded {len(seed)} tokens to graveyard")
    conn.close()


@app.route("/")
def index():
    db = get_db()
    tokens = db.execute("SELECT * FROM tokens ORDER BY death_date DESC").fetchall()
    tokens = [dict(t) for t in tokens]

    # Stats
    total_loss = sum(t["loss_estimate_usd"] or 0 for t in tokens)
    chain_counts = {}
    cause_counts = {}
    type_counts = {}
    year_counts = {}
    for t in tokens:
        chain = t.get("chain") or "Unknown"
        cause = t.get("cause") or "unknown"
        type_ = t.get("type") or "other"
        year = (t.get("death_date") or "")[:4] or "Unknown"
        chain_counts[chain] = chain_counts.get(chain, 0) + 1
        cause_counts[cause] = cause_counts.get(cause, 0) + 1
        type_counts[type_] = type_counts.get(type_, 0) + 1
        year_counts[year] = year_counts.get(year, 0) + 1

    top_chains = sorted(chain_counts.items(), key=lambda x: x[1], reverse=True)[:8]
    top_causes = sorted(cause_counts.items(), key=lambda x: x[1], reverse=True)
    top_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
    timeline = sorted(year_counts.items())

    biggest = sorted(tokens, key=lambda t: t.get("loss_estimate_usd") or 0, reverse=True)[:5]

    return render_template("index.html",
        tokens=tokens,
        total_loss=total_loss,
        total_count=len(tokens),
        top_chains=top_chains,
        top_causes=top_causes,
        top_types=top_types,
        timeline=timeline,
        biggest=biggest,
    )


@app.route("/api/tokens")
def api_tokens():
    db = get_db()
    q = request.args.get("q", "").strip().lower()
    chain = request.args.get("chain", "").strip()
    cause = request.args.get("cause", "").strip()

    sql = "SELECT * FROM tokens WHERE 1=1"
    params = []
    if q:
        sql += " AND (LOWER(name) LIKE ? OR LOWER(symbol) LIKE ? OR LOWER(description) LIKE ?)"
        params.extend([f"%{q}%"] * 3)
    if chain:
        sql += " AND chain = ?"
        params.append(chain)
    if cause:
        sql += " AND cause = ?"
        params.append(cause)
    sql += " ORDER BY death_date DESC"

    tokens = [dict(t) for t in db.execute(sql, params).fetchall()]
    return jsonify({"count": len(tokens), "tokens": tokens})


@app.route("/api/check/<symbol>")
def api_check(symbol):
    """Check if a token is in the graveyard by symbol."""
    db = get_db()
    token = db.execute(
        "SELECT * FROM tokens WHERE LOWER(symbol) = ?",
        (symbol.lower(),)
    ).fetchone()
    if token:
        return jsonify({"dead": True, "token": dict(token)})
    return jsonify({"dead": False, "message": "Token tidak ditemukan di graveyard."})


@app.route("/api/stats")
def api_stats():
    db = get_db()
    tokens = [dict(t) for t in db.execute("SELECT * FROM tokens").fetchall()]
    total_loss = sum(t["loss_estimate_usd"] or 0 for t in tokens)
    return jsonify({
        "total_tokens": len(tokens),
        "total_loss_usd": total_loss,
    })


# Initialize DB on startup
init_db()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
