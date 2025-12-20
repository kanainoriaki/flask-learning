from __future__ imoort annotations
import sqlite3
from pathlib import pathlib
from datetime import datetime
from flask import Flask, request, redirect, url_for. render_template, abort

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "app.db"

def get_conn():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  return conn

def init_db():
  with get_conn() as conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS estimates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        facility_type TEXT NOT NULL,
        title TEXT NOT NULL,
        work_hours REAL DEFAULT 0,
        cost INTEGER DEFAULT 0,
        note TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)
    conn.commit()

init_db()
    
def now():
  return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route("/")
def root():
    return redirect(url_for("list_estimates"))

@app.route("/estimates")
def list_estimates():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM estimates ORDER BY id DESC"
        ).fetchall()
    return render_template("estimates_list.html", estimates=rows)


@app.route("/estimates/new", methods=["GET", "POST"])
def new_estimate():
    if request.method == "POST":
        ts = now()
        with get_conn() as conn:
            conn.execute("""
            INSERT INTO estimates
            (customer_name, facility_type, title, work_hours, cost, note, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                request.form["customer_name"],
                request.form["facility_type"],
                request.form["title"],
                request.form.get("work_hours", 0),
                request.form.get("cost", 0),
                request.form.get("note", ""),
                ts, ts
            ))
            conn.commit()
        return redirect(url_for("list_estimates"))

    return render_template("estimates_form.html", estimate=None)


@app.route("/estimates/<int:estimate_id>")
def show_estimate(estimate_id):
    with get_conn() as conn:
        e = conn.execute(
            "SELECT * FROM estimates WHERE id=?", (estimate_id,)
        ).fetchone()
    if not e:
        abort(404)
    return render_template("estimates_show.html", e=e)

@app.route("/estimates/<int:estimate_id>/edit", methods=["GET", "POST"])
def edit_estimate(estimate_id):
    with get_conn() as conn:
        e = conn.execute(
            "SELECT * FROM estimates WHERE id=?", (estimate_id,)
        ).fetchone()
    if not e:
        abort(404)

    if request.method == "POST":
        with get_conn() as conn:
            conn.execute("""
            UPDATE estimates
            SET customer_name=?, facility_type=?, title=?, work_hours=?, cost=?, note=?, updated_at=?
            WHERE id=?
            """, (
                request.form["customer_name"],
                request.form["facility_type"],
                request.form["title"],
                request.form.get("work_hours", 0),
                request.form.get("cost", 0),
                request.form.get("note", ""),
                now(), estimate_id
            ))
            conn.commit()
        return redirect(url_for("show_estimate", estimate_id=estimate_id))

    return render_template("estimates_form.html", estimate=e)