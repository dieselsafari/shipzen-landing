#!/usr/bin/env python3
"""
ShipZen Public Landing Page
------------------------------
Standalone Flask app for the public-facing landing page with lead capture.
Run with: python3 landing.py
Then open: http://localhost:5000
"""

import sqlite3
import os
import re
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "shipzen-landing-2026")

DB_PATH = Path(__file__).resolve().parent / "landing_leads.db"


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS landing_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            phone TEXT,
            website TEXT,
            monthly_shipments TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


init_db()


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_lead(data):
    errors = []
    email = data.get("email", "").strip()
    if not email:
        errors.append("Email is required.")
    elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        errors.append("Please enter a valid email address.")
    return errors


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def landing():
    return render_template_string(LANDING_HTML)


@app.route("/api/lead", methods=["POST"])
def submit_lead():
    data = request.get_json(silent=True) or {}
    errors = validate_lead(data)
    if errors:
        return jsonify({"ok": False, "errors": errors}), 400

    conn = get_db()
    conn.execute(
        """INSERT INTO landing_leads (email, phone, website, monthly_shipments)
           VALUES (?, ?, ?, ?)""",
        (
            data["email"].strip(),
            data.get("phone", "").strip(),
            data.get("website", "").strip(),
            data.get("monthly_shipments", "").strip(),
        ),
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "message": "Thanks! We'll send your savings quote within 24 hours."})


# ---------------------------------------------------------------------------
# Landing Page HTML
# ---------------------------------------------------------------------------

LANDING_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ShipZen  - Enterprise UPS Ground Rates | Flat-Rate Shipping Labels</title>
<meta name="description" content="Enterprise UPS Ground rates powered by lane optimization. Save $1-$2 on average per shipping label vs Pirate Ship, ShipStation, EasyShip.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
--bg:#fff;--bg-alt:#f7f8fa;--bg-card:#fff;
--border:#e2e5ea;--border-light:#eef0f3;
--text:#0f1419;--text-sec:#536471;--text-muted:#8899a6;
--accent:#3b82f6;--accent-dark:#2563eb;--accent-darker:#1e40af;
--green:#10b981;--green-lt:#ecfdf5;
--red:#dc2626;--red-lt:#fef2f2;
--shadow:0 4px 12px rgba(0,0,0,.06);--shadow-lg:0 12px 32px rgba(0,0,0,.08);
--radius:12px;--radius-lg:16px;--radius-xl:20px;
--max-w:1140px;--tr:.2s ease;
}
html{font-size:16px;scroll-behavior:smooth;-webkit-font-smoothing:antialiased}
body{font-family:'Inter',system-ui,sans-serif;color:var(--text);background:var(--bg);line-height:1.6}
a{color:var(--accent-dark);text-decoration:none}
.container{max-width:var(--max-w);margin:0 auto;padding:0 1.5rem}
.ck{width:16px;height:16px;flex-shrink:0}

/* ===== NAV ===== */
.nav{position:fixed;top:0;left:0;right:0;z-index:100;background:rgba(255,255,255,0.08);border-bottom:1px solid rgba(255,255,255,0.12);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);transition:background .3s,border-color .3s,box-shadow .3s}
.nav.nav-scrolled{background:rgba(255,255,255,0.92);border-bottom:1px solid var(--border);box-shadow:0 1px 8px rgba(0,0,0,0.06)}
.nav.nav-scrolled .nav-brand{color:var(--text)}
.nav.nav-scrolled .btn-gs{background:var(--accent);color:#fff!important}
.nav-in{max-width:var(--max-w);margin:0 auto;padding:0 1.5rem;height:56px;display:flex;align-items:center;justify-content:space-between}
.nav-brand{font-weight:800;font-size:1.15rem;color:#111;text-decoration:none;display:flex;align-items:center;gap:.45rem;transition:color .3s}
.nav-brand svg{flex-shrink:0}
.btn-gs{background:rgba(255,255,255,0.18);color:#fff!important;padding:.45rem 1.15rem;border-radius:8px;font-weight:700;font-size:.82rem;transition:all .3s;text-decoration:none;border:1px solid rgba(255,255,255,0.25)}
.btn-gs:hover{background:rgba(255,255,255,0.3);color:#fff!important;border-color:rgba(255,255,255,0.4)}
.nav.nav-scrolled .btn-gs{background:var(--accent);color:#fff!important;border:1px solid transparent}
.nav.nav-scrolled .btn-gs:hover{background:#60a5fa;color:#fff!important}

/* ===== HERO BG ===== */
.hero-bg{position:absolute;top:-56px;left:0;width:100%;height:calc(100% + 56px);overflow:hidden;pointer-events:none;z-index:0}
.hero-bg canvas{position:absolute;top:0;left:0;width:100%;height:100%}
.hero-bg::after{content:'';position:absolute;top:0;left:0;width:100%;height:100%;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.04'/%3E%3C/svg%3E");opacity:.5;mix-blend-mode:overlay;pointer-events:none}

/* ===== HERO ===== */
.hero{padding:calc(56px + 4rem) 0 3rem;overflow:hidden;position:relative}
.hero-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:2.5rem;align-items:start}
@media(max-width:920px){.hero-grid{grid-template-columns:1fr}}
.hero-left{text-align:left}
@media(max-width:920px){.hero-left{text-align:center}}
.hero-tagline{font-size:.8rem;font-weight:600;color:#111;margin-bottom:.75rem}
.hero h1{font-size:clamp(1.8rem,4vw,2.75rem);font-weight:900;line-height:1.15;letter-spacing:-.03em;margin-bottom:.75rem}
.hero-sub{font-size:1rem;color:var(--text-sec);margin-bottom:1.5rem;line-height:1.65}

/* ===== CHECKLIST ===== */
.hero-checks{display:flex;flex-direction:column;gap:.55rem;margin-bottom:0}
.hero-chk{display:flex;align-items:center;gap:.45rem;font-size:.85rem;font-weight:500;color:var(--text-sec)}
.hero-chk svg{color:var(--green)}

/* ===== HERO PRICING TABLE ===== */
.hero-ptable{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.08),0 1px 3px rgba(0,0,0,.04);max-width:480px}
@media(max-width:920px){.hero-ptable{margin:0 auto}}
.hero-ptable table{width:100%;border-collapse:collapse}
.hero-ptable th{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--text-muted);padding:.85rem 1.25rem;text-align:left;background:var(--bg-alt);border-bottom:1px solid var(--border)}
.hero-ptable th:not(:first-child){text-align:center}
.hero-ptable th.hl{background:var(--accent);color:#fff;border-bottom:1px solid rgba(255,255,255,0.2)}
.hero-ptable td{padding:1.1rem 1.25rem;font-size:.88rem;color:var(--text-sec);border-bottom:1px solid var(--border-light)}
.hero-ptable tr:last-child td{border-bottom:none}
.hero-ptable td.hp-ours{text-align:center;font-weight:800;font-size:1.6rem;color:#fff;background:var(--accent);border-bottom:1px solid rgba(255,255,255,0.15)}
.hero-ptable tr:last-child td.hp-ours{border-bottom:none}
.hero-ptable td.hp-theirs{text-align:center;font-weight:800;font-size:1.6rem;color:#111}
.hp-aname{font-weight:600;color:var(--text);font-size:.9rem}

/* ===== ANIMATIONS ===== */
@keyframes levitate{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
@keyframes levitate2{0%,100%{transform:translateY(0)}50%{transform:translateY(-16px)}}
@keyframes levitate3{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
@keyframes fadeSlideUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulseGlow{0%,100%{opacity:.4}50%{opacity:.7}}
@keyframes countUp{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
@keyframes shimmer{0%{background-position:-200% 0}100%{background-position:200% 0}}

.dash-wrap{position:relative;max-width:820px;margin:0 auto;padding:0 1rem 3rem;animation:fadeSlideUp .8s ease-out both;animation-delay:.3s}
.dash-glow{position:absolute;top:50%;left:50%;width:500px;height:300px;transform:translate(-50%,-55%);background:radial-gradient(ellipse,rgba(59,130,246,.18) 0%,rgba(37,99,235,.08) 40%,transparent 70%);border-radius:50%;pointer-events:none;animation:pulseGlow 4s ease-in-out infinite;z-index:0}
.dash-card{position:relative;z-index:1;background:#fff;border:1px solid var(--border);border-radius:var(--radius-xl);box-shadow:0 20px 60px rgba(0,0,0,.08),0 1px 3px rgba(0,0,0,.04);overflow:hidden}
.dash-topbar{display:flex;align-items:center;justify-content:space-between;padding:.65rem 1.25rem;background:#f8fafb;border-bottom:1px solid var(--border-light)}
.dash-topbar-brand{display:flex;align-items:center;gap:.35rem;font-size:.72rem;font-weight:700;color:var(--text)}
.dash-topbar-brand svg{flex-shrink:0}
.dash-dots{display:flex;gap:4px}
.dash-dots span{width:8px;height:8px;border-radius:50%;background:var(--border)}
.dash-dots span:nth-child(1){background:#ff5f57}
.dash-dots span:nth-child(2){background:#febc2e}
.dash-dots span:nth-child(3){background:#28c840}
.dash-body{padding:1.25rem}
.dash-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem;margin-bottom:1rem}
@media(max-width:600px){.dash-stats{grid-template-columns:repeat(2,1fr)}}
.dash-stat{background:var(--bg-alt);border:1px solid var(--border-light);border-radius:10px;padding:.75rem .85rem;text-align:left}
.dash-stat-label{font-size:.62rem;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:var(--text-muted);margin-bottom:.25rem}
.dash-stat-val{font-size:1.15rem;font-weight:800;color:var(--text);letter-spacing:-.02em}
.dash-stat-val.blue{color:var(--accent-dark)}
.dash-stat-val.green{color:var(--green)}
.dash-stat-change{font-size:.6rem;font-weight:600;color:var(--green);margin-top:.15rem}
.dash-chart{background:var(--bg-alt);border:1px solid var(--border-light);border-radius:10px;padding:.85rem 1rem;position:relative;overflow:hidden}
.dash-chart-title{font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--text-muted);margin-bottom:.6rem}
.dash-bars{display:flex;align-items:flex-end;gap:5px;height:60px}
.dash-bar{flex:1;border-radius:3px 3px 0 0;transition:height .6s ease}
.dash-bar.blue{background:var(--accent)}
.dash-bar.blue-lt{background:rgba(59,130,246,.3)}
.dash-table{margin-top:.75rem}
.dash-table table{width:100%;border-collapse:collapse;font-size:.68rem}
.dash-table th{font-weight:700;text-transform:uppercase;letter-spacing:.04em;color:var(--text-muted);padding:.4rem .5rem;text-align:left;border-bottom:1px solid var(--border-light);font-size:.6rem}
.dash-table td{padding:.4rem .5rem;color:var(--text-sec);border-bottom:1px solid var(--border-light)}
.dash-table .status{display:inline-flex;align-items:center;gap:3px;font-weight:600;font-size:.6rem}
.dash-table .status.delivered{color:var(--green)}
.dash-table .status.transit{color:var(--accent)}
.dash-table .status-dot{width:5px;height:5px;border-radius:50%;flex-shrink:0}
.dash-table .delivered .status-dot{background:var(--green)}
.dash-table .transit .status-dot{background:var(--accent)}

/* Floating stat badges */
.float-badge{position:absolute;z-index:5;background:rgba(255,255,255,.92);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid rgba(226,229,234,.6);border-radius:12px;padding:.6rem .85rem;box-shadow:0 8px 32px rgba(0,0,0,.08),0 1px 2px rgba(0,0,0,.04);pointer-events:none}
.float-badge-label{font-size:.58rem;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:var(--text-muted);margin-bottom:.15rem}
.float-badge-val{font-size:1.05rem;font-weight:800;letter-spacing:-.02em}
.float-badge-val.blue{color:var(--accent-dark)}
.float-badge-val.green{color:var(--green)}
.float-badge-sub{font-size:.55rem;color:var(--green);font-weight:600;margin-top:.1rem}
.fb-1{top:12%;left:-40px;animation:levitate 3s ease-in-out infinite}
.fb-2{top:25%;right:-44px;animation:levitate2 3.5s ease-in-out infinite;animation-delay:.5s}
.fb-3{bottom:18%;left:-36px;animation:levitate3 2.8s ease-in-out infinite;animation-delay:1s}
.fb-4{bottom:8%;right:-40px;animation:levitate 3.2s ease-in-out infinite;animation-delay:1.5s}
@media(max-width:860px){
.fb-1{left:-10px;top:5%}
.fb-2{right:-10px;top:20%}
.fb-3{left:-10px;bottom:22%}
.fb-4{right:-10px;bottom:5%}
.float-badge{transform:scale(.85)}
}

/* ===== PRICING TABLE (standalone centered) ===== */
.ptable-section{padding:0 0 3rem}
.ptable{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);max-width:560px;margin:0 auto}
.ptable table{width:100%;border-collapse:collapse}
.ptable th{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--text-muted);padding:.7rem 1rem;text-align:left;background:var(--bg-alt);border-bottom:1px solid var(--border)}
.ptable th:not(:first-child){text-align:center}
.ptable th.hl{color:var(--accent-dark)}
.ptable td{padding:.75rem 1rem;font-size:.85rem;color:var(--text-sec);border-bottom:1px solid var(--border-light)}
.ptable tr:last-child td{border-bottom:none}
.p-ours{text-align:center;font-weight:800;font-size:1.3rem;color:var(--accent-dark)}
.p-theirs{text-align:center;font-weight:600;font-size:1rem;color:var(--text-muted);text-decoration:line-through}
.p-save{text-align:center;font-weight:700;font-size:.85rem;color:var(--green)}
.aname{font-weight:600;color:var(--text)}

/* ===== FORM CARD ===== */
.hero-form-card{background:#fff;border:1px solid var(--border);border-radius:var(--radius-xl);padding:2.25rem;box-shadow:0 20px 60px rgba(0,0,0,.08),0 1px 3px rgba(0,0,0,.04)}
.form-card-title{font-size:1.45rem;font-weight:800;letter-spacing:-.03em;margin-bottom:.25rem;color:var(--heading)}
.form-card-sub{font-size:.88rem;color:var(--text-sec);margin-bottom:1.5rem}
.fg{display:grid;grid-template-columns:1fr;gap:.85rem}
.fi{display:flex;flex-direction:column;gap:.3rem}
.fi label{font-size:.68rem;font-weight:700;color:var(--text-sec);text-transform:uppercase;letter-spacing:.06em}
.fi input,.fi select{padding:.7rem .85rem;border:1px solid var(--border);border-radius:9px;font-size:.88rem;font-family:inherit;color:var(--text);background:var(--bg-alt);outline:none;transition:all var(--tr);-webkit-appearance:none;appearance:none}
.fi input::placeholder{color:var(--text-muted)}
.fi input:focus,.fi select:focus{border-color:var(--accent-dark);box-shadow:0 0 0 3px rgba(37,99,235,.12);background:#fff}
.fi input.err,.fi select.err{border-color:var(--red)}
.fi select{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath d='M3 5l3 3 3-3' fill='none' stroke='%2394a3b8' stroke-width='1.5' stroke-linecap='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right .85rem center;padding-right:2.2rem}
.f-btns{grid-column:1/-1;display:flex;flex-direction:column;gap:.55rem;margin-top:.15rem}
.btn-book{width:100%;background:var(--accent);color:#fff;border:none;border-radius:10px;padding:.8rem;font-size:.95rem;font-weight:700;font-family:inherit;cursor:pointer;transition:all var(--tr);letter-spacing:-.01em}
.btn-book:hover{background:#1d4ed8}
.btn-book:disabled{opacity:.6;cursor:not-allowed}
.form-trust{display:flex;justify-content:center;gap:1.25rem;margin-top:.35rem;flex-wrap:wrap}
.form-trust span{font-size:.72rem;color:var(--text-muted);font-weight:500;display:flex;align-items:center;gap:.3rem}
.form-msg{grid-column:1/-1;padding:.65rem .85rem;border-radius:7px;font-size:.82rem;font-weight:500;display:none}
.form-msg.ok{display:block;background:var(--green-lt);color:#059669}
.form-msg.err{display:block;background:var(--red-lt);color:var(--red)}

/* ===== PRICING DETAIL ===== */
.pd-section{padding:5rem 0}
.sl{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--accent-dark);margin-bottom:.5rem}
.st{font-size:clamp(1.5rem,3vw,2.1rem);font-weight:800;letter-spacing:-.03em;margin-bottom:.5rem}
.sd{color:var(--text-sec);max-width:560px;font-size:.95rem;margin-bottom:2rem}
.sl,.st,.sd{text-align:left}
.sl.c,.st.c,.sd.c{text-align:center;margin-left:auto;margin-right:auto}

.pd-wrap{display:grid;grid-template-columns:1fr 320px;gap:2rem;align-items:start}
@media(max-width:860px){.pd-wrap{grid-template-columns:1fr}}
.pd-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-xl);box-shadow:var(--shadow-lg);padding:2.5rem 2.75rem}
.pd-right{display:flex;flex-direction:column;gap:1rem;padding-top:.25rem}
.pd-head{display:flex;align-items:center;gap:.65rem;margin-bottom:.35rem}
.pd-head h3{font-size:1.55rem;font-weight:800;letter-spacing:-.02em}
.pd-badge{background:#dbeafe;color:#1e40af;font-size:.62rem;font-weight:700;padding:.25rem .6rem;border-radius:6px;text-transform:uppercase;white-space:nowrap;border:1px solid rgba(30,64,175,.1)}
.pd-sub{font-size:.88rem;color:var(--text-sec);margin-bottom:1.75rem;line-height:1.5}
.pd-prices{display:flex;gap:3rem;margin-bottom:2rem;flex-wrap:wrap}
.pd-price{display:flex;align-items:baseline;gap:.15rem}
.pd-price .sym{font-size:1.6rem;font-weight:800;color:var(--accent-dark);align-self:flex-start;margin-top:.5rem}
.pd-price .big{font-size:3.8rem;font-weight:900;color:var(--accent-dark);line-height:1}
.pd-price .lbl{font-size:.82rem;color:var(--text-muted);font-weight:500;margin-left:.2rem}
.pd-divider{border:none;border-top:1px dashed var(--border);margin:0 0 1.5rem}
.pd-list-title{font-size:.92rem;font-weight:700;margin-bottom:.85rem}
.pd-list{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:.7rem 1rem}
@media(max-width:600px){.pd-list{grid-template-columns:1fr}}
.pd-list li{display:flex;align-items:flex-start;gap:.45rem;font-size:.88rem;color:var(--text);font-weight:500}
.pd-list li svg{color:var(--green);flex-shrink:0;margin-top:3px}
.pd-callout{display:flex;gap:.85rem;align-items:flex-start;background:var(--bg-alt);border:1px solid var(--border-light);border-radius:var(--radius-lg);padding:1.1rem 1rem}
.pd-callout-icon{width:36px;height:36px;border-radius:50%;background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.15);display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px}
.pd-callout-icon svg{width:17px;height:17px;color:var(--accent-dark)}
.pd-callout h4{font-size:1rem;font-weight:800;margin-bottom:.3rem;line-height:1.3;letter-spacing:-.01em}
.pd-callout p{font-size:.82rem;color:var(--text-sec);line-height:1.55}
.net-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:.5rem;margin-top:.15rem}
.net-grid span{display:flex;align-items:center;justify-content:center;background:#fff;border:none;border-radius:8px;overflow:hidden}
.net-grid span svg{width:100%;height:auto;display:block}

/* ===== ENTERPRISE ===== */
.ent-section{padding:5rem 0;background:var(--bg-alt)}
.ent-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem}
@media(max-width:768px){.ent-grid{grid-template-columns:1fr}}
.ent-card{background:#fff;border:1px solid var(--border-light);border-radius:var(--radius-xl);overflow:hidden;display:flex;flex-direction:column;transition:box-shadow .35s ease,transform .35s ease}
.ent-card:hover{box-shadow:0 12px 40px rgba(0,0,0,.08);transform:translateY(-3px)}
.ent-head{display:flex;justify-content:space-between;align-items:flex-start;padding:1.5rem 1.5rem 0}
.ent-head h3{font-size:1.05rem;font-weight:700;line-height:1.35;color:var(--text);margin:0;max-width:85%}
.ent-head .ent-ico{width:32px;height:32px;border-radius:8px;background:var(--bg-alt);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.ent-head .ent-ico svg{width:16px;height:16px;color:var(--text-muted)}
.ent-visual{position:relative;flex:1;min-height:220px;overflow:hidden}
.ent-visual canvas{position:absolute;inset:0;width:100%;height:100%}
.ent-visual::before{content:'';position:absolute;top:0;left:0;right:0;height:45%;background:linear-gradient(to bottom,#fff 0%,#fff 10%,rgba(255,255,255,0) 100%);z-index:1;pointer-events:none}

/* ===== FAQ ===== */
.faq-s{padding:4rem 0}
.faq-s.alt{background:var(--bg-alt)}
.faq-wrap{max-width:720px;margin:0 auto}
.faq-i{border-bottom:1px solid var(--border)}
.faq-q{width:100%;background:none;border:none;padding:1rem 0;display:flex;align-items:center;justify-content:space-between;cursor:pointer;font-family:inherit;font-size:.9rem;font-weight:600;color:var(--text);text-align:left;gap:.75rem;transition:color var(--tr)}
.faq-q:hover{color:var(--accent-dark)}
.faq-ch{width:16px;height:16px;flex-shrink:0;transition:transform .3s;color:var(--text-muted)}
.faq-i.open .faq-ch{transform:rotate(180deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s}
.faq-i.open .faq-a{max-height:600px}
.faq-ai{padding:0 0 1rem;font-size:.85rem;color:var(--text-sec);line-height:1.7}

/* ===== ONBOARDING ===== */
.ob-section{padding:4rem 0}
.ob-title{font-size:clamp(1.5rem,3vw,2.1rem);font-weight:800;letter-spacing:-.03em;margin-bottom:.5rem}
.ob-sub{color:var(--text-sec);font-size:.95rem;margin-bottom:2.5rem;max-width:600px}
.ob-steps{display:flex;flex-direction:column;gap:.75rem;max-width:720px}
.ob-step h4{font-size:.95rem;font-weight:700;margin-bottom:.5rem}
.ob-step ul{list-style:disc;padding-left:1.25rem;display:flex;flex-direction:column;gap:.3rem}
.ob-step ul li{font-size:.82rem;color:var(--text-sec);line-height:1.5}

/* ===== HOW IT WORKS MODULES ===== */
.hiw-mod{background:#fff;border:1px solid var(--border-light);border-radius:var(--radius-xl);padding:1.75rem;position:relative;text-align:left;transition:box-shadow .3s,transform .3s}
.hiw-mod:hover{box-shadow:0 8px 30px rgba(59,130,246,.1);transform:translateY(-4px)}
.hiw-header{display:flex;align-items:center;gap:.75rem;margin-bottom:.75rem}
.hiw-icon{width:38px;height:38px;border-radius:10px;background:rgba(59,130,246,.06);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.hiw-icon svg{width:20px;height:20px}
.hiw-title{font-size:1.05rem;font-weight:700;color:var(--text);margin:0}
.hiw-desc{font-size:.875rem;color:var(--text-sec);line-height:1.65;margin-bottom:1rem}
.hiw-result{display:flex;align-items:center;gap:.4rem;font-size:.8rem;font-weight:600;color:#10b981;padding-top:.75rem;border-top:1px solid var(--border-light)}
@media(max-width:768px){[style*="grid-template-columns:repeat(3"]{grid-template-columns:1fr !important}}

/* ===== CTA ===== */
.cta-section{padding:0;position:relative;overflow:hidden;background:var(--accent-dark)}
.cta-section .container{position:relative;z-index:1;padding-top:4.5rem;padding-bottom:4.5rem}
.cta-section canvas{position:absolute;inset:0;width:100%;height:100%;z-index:0}
.cta-card{background:transparent;border-radius:0;padding:0;text-align:center;color:#fff;position:relative}
.cta-card h2,.cta-card p,.cta-card .btn-cta{position:relative;z-index:1}
.cta-card h2{font-size:clamp(1.5rem,3.5vw,2.25rem);font-weight:900;letter-spacing:-.03em;margin-bottom:.5rem}
.cta-card p{font-size:.95rem;opacity:.8;max-width:420px;margin:0 auto 1.5rem}
.btn-cta{display:inline-flex;background:#fff;color:var(--accent-darker);font-weight:700;font-size:.9rem;font-family:inherit;padding:.7rem 1.75rem;border-radius:9px;border:none;cursor:pointer;transition:all var(--tr);text-decoration:none}
.btn-cta:hover{transform:translateY(-2px);box-shadow:var(--shadow-lg);color:var(--accent-darker)}

/* ===== FOOTER ===== */
.footer{padding:1.5rem 0;border-top:1px solid var(--border)}
.footer-in{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:.75rem}
.footer-brand{font-weight:700;font-size:.95rem;color:var(--text);text-decoration:none;display:flex;align-items:center;gap:.35rem}
.footer-brand svg{flex-shrink:0}
.footer-links{display:flex;gap:1.25rem;list-style:none}
.footer-links a{font-size:.78rem;color:var(--text-muted);transition:color var(--tr)}
.footer-links a:hover{color:var(--text)}

.fade-in{opacity:0;transform:translateY(14px);transition:opacity .5s,transform .5s}
.fade-in.visible{opacity:1;transform:translateY(0)}
@media(max-width:768px){[style*="grid-template-columns:repeat(3"]{grid-template-columns:1fr !important}}
</style>
</head>
<body>

<!-- NAV -->
<nav class="nav">
<div class="nav-in">
<a href="#" class="nav-brand">
<svg width="26" height="26" viewBox="0 0 40 40" fill="none"><path d="M4,2L36,2Q39,2 39,5L39,14L7,29L1,14L1,5Q1,2 4,2Z" fill="#1e3a8a"/><path d="M33,11L39,26L39,35Q39,38 36,38L4,38Q1,38 1,35L1,26Z" fill="#00b4d8" opacity=".80"/></svg>
ShipZen
</a>
<a href="#contact" class="btn-gs">Get Started</a>
</div>
</nav>

<!-- HERO -->
<section class="hero" id="top">

<div class="hero-bg">
<canvas id="gradient-canvas"></canvas>
</div>

<div class="container" style="position:relative;z-index:1">
<div class="hero-grid">

<!-- LEFT: text + checklist + pricing table -->
<div class="hero-left">
<p class="hero-tagline">Enterprise UPS rates without the enterprise contract.</p>
<h1>Stop overpaying for shipping labels.</h1>
<p class="hero-sub">Flat-rate UPS Ground labels across the lower 48 states.<br><strong>Save $1-$2 on average per shipping label.</strong></p>
<div class="hero-checks">
<div class="hero-chk"><svg class="ck" viewBox="0 0 16 16" fill="none"><path d="M13 4L6 11 3 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Direct enterprise UPS partnership -not an aggregator discount</div>
<div class="hero-chk"><svg class="ck" viewBox="0 0 16 16" fill="none"><path d="M13 4L6 11 3 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Lane-optimized routes for the lowest per-package cost</div>
<div class="hero-chk"><svg class="ck" viewBox="0 0 16 16" fill="none"><path d="M13 4L6 11 3 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Works with Shopify, WooCommerce, and all major platforms</div>
</div>
</div>

<!-- RIGHT: lead capture form -->
<div class="hero-form-card" id="contact">
<div class="form-card-title">See how much you'd save</div>
<div class="form-card-sub">Get a custom savings quote in under 24 hours</div>
<form id="lead-form" class="fg" novalidate>
<div class="fi"><label>Email Address</label><input type="email" id="email" placeholder="you@yourstore.com" required></div>
<div class="fi"><label>Phone Number</label><input type="tel" id="phone" placeholder="(555) 123-4567"></div>
<div class="fi"><label>Store URL</label><input type="url" id="website" placeholder="yourstore.com"></div>
<div class="fi"><label>Monthly Shipments</label><select id="monthly_shipments"><option value="" disabled selected>Select estimate...</option><option value="1-100">1 - 100</option><option value="101-500">101 - 500</option><option value="501-1000">501 - 1,000</option><option value="1001-2500">1,001 - 2,500</option><option value="2500+">2,500+</option></select></div>
<div class="f-btns">
<button type="submit" class="btn-book" id="submit-btn">&#128230; Get Your Savings Quote</button>
</div>
<div class="form-trust">
<span>&#128274; No setup fees</span>
<span>&#10005; No contracts</span>
<span>&#8617; Cancel anytime</span>
</div>
<div class="form-msg" id="form-msg"></div>
</form>
</div>

</div>
</div>
</section>


<!-- FEATURES DETAIL CARD -->
<section class="pd-section" id="features">
<div class="container">
<p class="sl">Why ShipZen</p>
<h2 class="st">Guaranteed lowest UPS Ground rates for e-commerce sellers</h2>
<p class="sd">Keep more profit with enterprise contract rates -no minimums, no hidden fees.</p>

<div class="pd-wrap fade-in">
<div class="pd-card">
<div class="pd-head">
<h3>Flat-Rate Shipping Labels</h3>
<span class="pd-badge">Enterprise Rates</span>
</div>
<p class="pd-sub">No monthly fees. Pay per label. Cancel anytime.</p>

<div class="pd-list-title" style="margin-top:.5rem">What you get</div>
<ul class="pd-list">
<li><svg class="ck" viewBox="0 0 16 16" fill="none"><path d="M13 4L6 11 3 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Enterprise UPS Ground contract rates</li>
<li><svg class="ck" viewBox="0 0 16 16" fill="none"><path d="M13 4L6 11 3 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> No volume commitments or minimums</li>
<li><svg class="ck" viewBox="0 0 16 16" fill="none"><path d="M13 4L6 11 3 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Flat-rate pricing across lower 48 states</li>
<li><svg class="ck" viewBox="0 0 16 16" fill="none"><path d="M13 4L6 11 3 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Instant label generation &amp; tracking</li>
<li><svg class="ck" viewBox="0 0 16 16" fill="none"><path d="M13 4L6 11 3 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Works with Shopify, WooCommerce, custom stores</li>
<li><svg class="ck" viewBox="0 0 16 16" fill="none"><path d="M13 4L6 11 3 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> No hidden zone fees or surcharges</li>
</ul>
</div>
<div class="pd-right">
<div class="pd-callout">
<div class="pd-callout-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="22" height="18" rx="2"/><path d="M1 9h22"/></svg></div>
<div><h4>No zone calculations -flat rates</h4><p>Pay per label. No monthly fees, no contracts, no surprises.</p></div>
</div>
<div class="pd-callout">
<div class="pd-callout-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg></div>
<div><h4>Works with any e-commerce platform</h4><p>Shopify, WooCommerce, BigCommerce, Etsy, Amazon, eBay, and custom integrations via API.</p></div>
</div>
<div class="net-grid">
<span><svg viewBox="0 0 60 40" aria-label="UPS"><g transform="translate(10,0) scale(0.625)"><path d="M32 64c-1.7-.76-15.306-6.617-19.698-10.27a20.06 20.06 0 0 1-7.237-16.102V5.973C12.536 2.003 21.577 0 32 0s19.417 2.014 26.935 5.973v31.62c.21 6.2-2.457 12.148-7.226 16.114-4.32 3.513-18.082 9.58-19.663 10.27z" fill="#ffb500"/><path d="M42.364 26.654a6.21 6.21 0 0 1 6.277-6.101 8 8 0 0 1 5.129 1.522v4.064c-1.107-1.148-2.61-1.83-4.204-1.91-1.323 0-2.705.574-2.752 2.237s1.335 2.342 3.08 3.396c3.91 2.342 4.684 4.356 4.58 7.085-.015 1.747-.752 3.4-2.036 4.595s-3.002 1.785-4.744 1.66c-1.815-.015-3.593-.512-5.153-1.44v-4.286a7.46 7.46 0 0 0 4.474 1.909c.734.096 1.473-.14 2.014-.647s.83-1.226.784-1.965c0-1.464-.867-2.272-2.916-3.513-3.853-2.26-4.556-4.122-4.556-6.617zm-11.336-1.99a4.05 4.05 0 0 1 1.651-.34c2.717 0 3.84 2.167 3.84 7.413s-1.288 7.59-3.982 7.59c-.52-.004-1.035-.1-1.522-.28v-14.38zm0 28.048h-4.684V22.25c1.892-1.16 4.083-1.74 6.3-1.663 5.586 0 8.654 4.24 8.654 11.055S38.312 43.155 33.1 43.155c-.712.013-1.422-.078-2.108-.27V52.7zm-21.08-16.97V21.08h4.684v14.873c0 1.323.316 3.29 2.47 3.29a3.91 3.91 0 0 0 2.178-.597V21.08h4.684v20.248c-2.103 1.31-4.55 1.964-7.027 1.874-4.684 0-7.027-2.506-7.027-7.472zm-2.342 1.885c-.208 5.46 2.128 10.706 6.324 14.205 3.654 2.986 14.92 8.08 18.093 9.474 3.127-1.382 14.37-6.418 18.082-9.474 4.2-3.49 6.537-8.737 6.324-14.194v-31C40.77 5.188 22.256 6.078 7.594 19.522v18.105z" fill="#351c15"/></g></svg></span>
<span><svg viewBox="0 0 60 40" aria-label="Shopify"><g transform="translate(12.5,0) scale(0.137)"><path d="M223.774 57.34c-.201-1.46-1.48-2.268-2.537-2.357-1.055-.088-23.383-1.743-23.383-1.743s-15.507-15.395-17.209-17.099c-1.703-1.703-5.029-1.185-6.32-.805-.19.056-3.388 1.043-8.678 2.68-5.18-14.906-14.322-28.604-30.405-28.604-.444 0-.901.018-1.358.044C129.31 3.407 123.644.779 118.75.779c-37.465 0-55.364 46.835-60.976 70.635-14.558 4.511-24.9 7.718-26.221 8.133-8.126 2.549-8.383 2.805-9.45 10.462C21.3 95.806.038 260.235.038 260.235l165.678 31.042 89.77-19.42S223.973 58.8 223.775 57.34z" fill="#95BF46"/><path d="M156.49 40.848l-14.019 4.339c.005-.988.01-1.96.01-3.023 0-9.264-1.286-16.723-3.349-22.636 8.287 1.04 13.806 10.469 17.358 21.32zm-27.638-19.483c2.304 5.773 3.802 14.058 3.802 25.238 0 .572-.005 1.095-.01 1.624-9.117 2.824-19.024 5.89-28.953 8.966 5.575-21.516 16.025-31.908 25.161-35.828zm-11.131-10.537c1.617 0 3.246.549 4.805 1.622-12.007 5.65-24.877 19.88-30.312 48.297l-22.886 7.088C75.694 46.16 90.81 10.828 117.72 10.828z" fill="#95BF46"/><path d="M221.237 54.983c-1.055-.088-23.383-1.743-23.383-1.743s-15.507-15.395-17.209-17.099c-.637-.634-1.496-.959-2.394-1.099l-12.527 256.233 89.762-19.418S223.972 58.8 223.774 57.34c-.201-1.46-1.48-2.268-2.537-2.357" fill="#5E8E3E"/><path d="M135.242 104.585l-11.069 32.926s-9.698-5.176-21.586-5.176c-17.428 0-18.305 10.937-18.305 13.693 0 15.038 39.2 20.8 39.2 56.024 0 27.713-17.577 45.558-41.277 45.558-28.44 0-42.984-17.7-42.984-17.7l7.615-25.16s14.95 12.835 27.565 12.835c8.243 0 11.596-6.49 11.596-11.232 0-19.616-32.16-20.491-32.16-52.724 0-27.129 19.472-53.382 58.778-53.382 15.145 0 22.627 4.338 22.627 4.338" fill="#FFF"/></g></svg></span>
<span><svg viewBox="0 0 60 40" aria-label="WooCommerce"><g transform="translate(0,2.1) scale(0.234)"><path d="M23.759 0h208.378C245.325 0 256 10.675 256 23.863v79.541c0 13.188-10.675 23.863-23.863 23.863H157.41l10.257 25.118-45.109-25.118H23.863c-13.187 0-23.862-10.675-23.862-23.863V23.863C-.104 10.78 10.57 0 23.759 0z" fill="#9B5C8F"/><path d="M14.578 21.75c1.457-1.978 3.642-3.018 6.556-3.226 5.308-.417 8.326 2.08 9.054 7.492 3.226 21.75 6.764 40.17 10.51 55.259l22.79-43.395c2.082-3.955 4.684-6.036 7.806-6.244 4.579-.312 7.388 2.601 8.533 8.741 2.602 13.84 5.932 25.6 9.886 35.59 2.706-26.432 7.285-45.476 13.737-57.235 1.56-2.914 3.85-4.371 6.868-4.58 2.394-.207 4.579.521 6.556 2.082 1.977 1.561 3.018 3.538 3.226 5.932.104 1.873-.208 3.434-1.04 4.995-4.059 7.493-7.39 20.085-10.095 37.567-2.601 16.963-3.538 30.18-2.914 39.65.209 2.6-.208 4.89-1.248 6.868-1.25 2.289-3.122 3.538-5.516 3.746-2.706.208-5.515-1.04-8.221-3.85-9.678-9.887-17.379-24.664-22.998-44.332-6.765 13.32-11.76 23.31-14.986 29.97-6.14 11.76-11.343 17.796-15.714 18.108-2.81.208-5.203-2.186-7.284-7.18-5.307-13.633-11.031-39.962-17.17-78.986-.417-2.706.207-5.1 1.664-6.972zm223.636 16.338c-3.746-6.556-9.262-10.51-16.65-12.072-1.978-.416-3.85-.624-5.62-.624-9.99 0-18.107 5.203-24.455 15.61-5.412 8.845-8.117 18.627-8.117 29.346 0 8.013 1.665 14.881 4.995 20.605 3.746 6.556 9.262 10.51 16.65 12.071 1.977.417 3.85.625 5.62.625 10.094 0 18.211-5.203 24.455-15.61 5.411-8.95 8.117-18.732 8.117-29.45.104-8.117-1.665-14.882-4.995-20.501zm-13.112 28.826c-1.457 6.868-4.059 11.967-7.91 15.401-3.017 2.706-5.827 3.85-8.428 3.33-2.498-.52-4.58-2.705-6.14-6.764-1.25-3.226-1.873-6.452-1.873-9.47 0-2.601.208-5.203.728-7.596.937-4.267 2.706-8.43 5.515-12.384 3.435-5.1 7.077-7.18 10.823-6.452 2.498.52 4.58 2.706 6.14 6.764 1.249 3.226 1.873 6.452 1.873 9.47 0 2.706-.208 5.307-.728 7.7zm-52.033-28.826c-3.746-6.556-9.366-10.51-16.65-12.072-1.977-.416-3.85-.624-5.62-.624-9.99 0-18.107 5.203-24.455 15.61-5.411 8.845-8.117 18.627-8.117 29.346 0 8.013 1.665 14.881 4.995 20.605 3.746 6.556 9.262 10.51 16.65 12.071 1.978.417 3.85.625 5.62.625 10.094 0 18.211-5.203 24.455-15.61 5.412-8.95 8.117-18.732 8.117-29.45 0-8.117-1.665-14.882-4.995-20.501zm-13.216 28.826c-1.457 6.868-4.059 11.967-7.909 15.401-3.018 2.706-5.828 3.85-8.43 3.33-2.497-.52-4.578-2.705-6.14-6.764-1.248-3.226-1.872-6.452-1.872-9.47 0-2.601.208-5.203.728-7.596.937-4.267 2.706-8.43 5.516-12.384 3.434-5.1 7.076-7.18 10.822-6.452 2.498.52 4.58 2.706 6.14 6.764 1.25 3.226 1.873 6.452 1.873 9.47.105 2.706-.208 5.307-.728 7.7z" fill="#FFF"/></g></svg></span>
<span><svg viewBox="0 0 60 40" aria-label="BigCommerce"><g transform="translate(10,0) scale(1.667)"><path d="M12.645 13.663h3.027c.861 0 1.406-.474 1.406-1.235 0-.717-.545-1.234-1.406-1.234h-3.027c-.1 0-.187.086-.187.172v2.125c.015.1.086.172.187.172zm0 4.896h3.128c.961 0 1.535-.488 1.535-1.35 0-.746-.545-1.35-1.535-1.35h-3.128c-.1 0-.187.087-.187.173v2.34c.015.115.086.187.187.187zM23.72.053l-8.953 8.93h1.464c2.281 0 3.63 1.435 3.63 3 0 1.235-.832 2.14-1.722 2.541-.143.058-.143.259.014.316 1.033.402 1.765 1.48 1.765 2.742 0 1.78-1.19 3.202-3.5 3.202h-6.342c-.1 0-.187-.086-.187-.172V13.85L.062 23.64c-.13.13-.043.359.143.359h23.631a.16.16 0 0 0 .158-.158V.182c.043-.158-.158-.244-.273-.13z" fill="#34313F"/></g></svg></span>
<span><svg viewBox="0 0 60 40" aria-label="Etsy"><g transform="translate(-12.8,-1.75) scale(0.177)"><path d="M108.783 100.639V55.192c0-1.684.168-2.694 3.031-2.694h38.545c6.734 0 10.437 5.724 13.131 16.496l2.188 8.586h6.564c1.177-24.406 2.186-35.011 2.186-35.011s-16.495 1.851-26.258 1.851H98.854l-26.431-.842v7.07l8.923 1.683c6.228 1.179 7.74 2.524 8.249 8.249 0 0 .506 16.832.506 44.607 0 27.771-.506 44.437-.506 44.437 0 5.049-2.021 6.9-8.249 8.082l-8.923 1.684v7.066l26.431-.84h44.101c9.931 0 32.991.84 32.991.84.503-6.061 3.872-33.498 4.377-36.524h-6.228l-6.565 14.981c-5.219 11.78-12.792 12.623-21.21 12.623h-25.082c-8.417 0-12.457-3.367-12.457-10.604v-38.379s18.347 0 24.742.506c4.714.338 7.574 1.684 9.091 8.248l2.021 8.753h7.234l-.503-22.053 1.009-22.217h-7.236l-2.355 9.762c-1.517 6.396-2.525 7.577-9.091 8.248-7.405.844-24.913.675-24.913.675v.167h.003v-.003zM208.599 59.906c-2.357 10.436-4.714 18.515-12.962 23.902-5.049 3.365-10.1 4.542-12.117 4.711v6.396h14.98v51.675c0 14.478 9.596 21.549 22.387 21.549 9.932 0 20.198-4.208 23.734-12.963l-3.536-4.545c-1.684 2.863-7.067 7.07-13.801 7.07-7.405 0-11.445-5.051-11.445-17.841V94.245l24.914 1.853 1.345-11.449-26.258 1.011V60.073l-7.241-.167zM261.791 139.39l-6.396.168c.336 3.702.506 8.417.506 12.793 0 4.545-.168 8.753-.506 10.772 0 0 12.793 4.709 25.754 4.709 17.506 0 31.478-8.416 31.478-24.912 0-28.275-42.418-24.066-42.418-43.09 0-7.91 7.069-10.941 14.812-10.941 6.06 0 11.109 2.188 12.119 5.389l4.209 12.624 6.229-.336c.506-6.734.841-14.477 1.852-20.704-5.388-2.357-16.667-3.706-23.731-3.706-16.5 0-29.795 7.239-29.795 23.399 0 28.109 41.406 22.386 41.406 43.093 0 7.403-4.547 12.622-14.812 12.622-9.424 0-14.139-4.88-15.987-9.764l-4.72-12.116zM363.244 158.836c-9.745 27.221-21.674 34.273-32.426 34.273-4.539 0-6.721-2.018-7.396-5.205l-2.52-13.109-7.058.336c-1.344 7.73-2.688 16.302-4.534 23.357 4.201 3.188 11.254 4.872 16.801 4.872 11.596 0 29.236-1.515 45.363-39.821l27.053-63.845c2.186-5.21 3.023-5.714 9.408-8.236l3.529-1.341v-5.881l-15.963.84-17.137-.84v5.881l4.366 1.341c4.367 1.347 6.387 3.026 6.387 6.051 0 1.511-.506 3.024-1.348 5.374-2.52 6.389-18.146 44.359-22.342 52.426l4.195-1.515c-7.394-18.313-18.646-48.895-20.328-54.099-.336-1.009-.504-1.849-.504-2.693 0-2.687 1.848-4.872 5.881-5.711l5.545-1.173v-5.881l-23.021.84-18.313-.84v5.881l3.025 1.007c4.2 1.344 5.209 2.521 7.729 8.401 13.941 31.925 20.498 49.396 29.399 72.249l4.209-12.939z" fill="#F56400"/></g></svg></span>
<span><svg viewBox="0 0 60 40" aria-label="Amazon"><text x="5" y="19" font-family="Arial,sans-serif" font-size="14" font-weight="700" letter-spacing="-0.5" fill="#232F3E">amazon</text><path d="M 7 24 Q 30 33 52 24" stroke="#FF9900" stroke-width="2.5" fill="none" stroke-linecap="round"/><path d="M 48 22 L 52 24 L 50 28" stroke="#FF9900" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
<span><svg viewBox="0 0 60 40" aria-label="eBay"><text x="4" y="28" font-family="Arial,sans-serif" font-size="22" font-weight="700"><tspan fill="#E53238">e</tspan><tspan fill="#0064D2">B</tspan><tspan fill="#F5AF02">a</tspan><tspan fill="#86B817">y</tspan></text></svg></span>
<span><svg viewBox="0 0 60 40" aria-label="Custom API"><path d="M 18 10 L 10 20 L 18 30" stroke="#3b82f6" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M 42 10 L 50 20 L 42 30" stroke="#3b82f6" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M 34 8 L 26 32" stroke="#3b82f6" stroke-width="2.5" fill="none" stroke-linecap="round"/></svg></span>
</div>
</div>
</div>
</div>
</section>

<!-- ENTERPRISE -->
<section class="ent-section">
<div class="container">
<h2 class="st c">Enterprise shipping rates without enterprise commitments</h2>
<div style="height:1.5rem"></div>
<div class="ent-grid">

<div class="ent-card fade-in">
<div class="ent-head">
<h3>Save $1-$2 on average per shipping label</h3>
<div class="ent-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div>
</div>
<div class="ent-visual"><canvas id="ent-cv-1"></canvas></div>
</div>

<div class="ent-card fade-in">
<div class="ent-head">
<h3>Ship anywhere across<br>all 48 states</h3>
<div class="ent-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div>
</div>
<div class="ent-visual"><canvas id="ent-cv-2"></canvas></div>
</div>

<div class="ent-card fade-in">
<div class="ent-head">
<h3>No hidden zone fees or dimensional weight charges</h3>
<div class="ent-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg></div>
</div>
<div class="ent-visual"><canvas id="ent-cv-3"></canvas></div>
</div>

</div>
</div>
</section>

<!-- HOW IT WORKS -->
<section style="padding:5rem 0;background:var(--bg-alt)" id="how-shipzen-works">
<div class="container">
<p class="sl c">How It Works</p>
<h2 class="st c">Three things that make our rates unbeatable</h2>
<p class="sd c">It&rsquo;s not a workaround or a loophole. It&rsquo;s how enterprise logistics pricing has always worked.</p>
<div style="height:2rem"></div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2rem;max-width:1020px;margin:0 auto">

<div class="fade-in hiw-mod">
<div class="hiw-header">
<div class="hiw-icon">
<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
</div>
<h4 class="hiw-title">We optimize your lanes</h4>
</div>
<p class="hiw-desc">Your shipments get consolidated into predictable, high-frequency routes. UPS builds our volume directly into daily truck schedules, eliminating wasted miles and empty trucks.</p>
<div class="hiw-result">
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
Lower per-package cost
</div>
</div>

<div class="fade-in hiw-mod">
<div class="hiw-header">
<div class="hiw-icon">
<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
</div>
<h4 class="hiw-title">We validate every address</h4>
</div>
<p class="hiw-desc">Every address is verified and standardized before a label prints. No correction fees, no failed deliveries, no surprise surcharges. Clean data means lower cost-to-serve.</p>
<div class="hiw-result">
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
Zero hidden fees
</div>
</div>

<div class="fade-in hiw-mod">
<div class="hiw-header">
<div class="hiw-icon">
<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
</div>
<h4 class="hiw-title">We commit 100% to UPS</h4>
</div>
<p class="hiw-desc">No multi-carrier rate-shopping. Our long-term, dedicated UPS Ground commitment gives them the certainty they need to unlock enterprise pricing that aggregators can never access.</p>
<div class="hiw-result">
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
Enterprise-tier rates
</div>
</div>

</div>
</div>
</section>

<!-- AGGREGATORS vs 3PLs vs SHIPZEN -->
<section style="padding:4.5rem 0;background:var(--bg)">
<div class="container">
<p class="sl c">See The Difference</p>
<h2 class="st c">Why our rates are structurally lower</h2>
<p class="sd c">Aggregators and 3PLs offer good rates compared to retail -but their models can&rsquo;t unlock the lowest pricing tiers.</p>
<div style="height:1.5rem"></div>
<div class="fade-in" style="max-width:860px;margin:0 auto;overflow-x:auto">
<table style="width:100%;border-collapse:separate;border-spacing:0;font-size:.85rem;background:#fff;border-radius:var(--radius-xl);border:1px solid var(--border-light);overflow:hidden">
<thead>
<tr style="background:var(--bg-alt)">
<th style="padding:.85rem 1rem;text-align:left;font-weight:600;border-bottom:1px solid var(--border-light);width:22%"></th>
<th style="padding:.85rem 1rem;text-align:center;font-weight:600;border-bottom:1px solid var(--border-light);width:26%;color:var(--text-sec)">Aggregators<br><span style="font-weight:400;font-size:.75rem;color:#888">Pirate Ship, EasyShip</span></th>
<th style="padding:.85rem 1rem;text-align:center;font-weight:600;border-bottom:1px solid var(--border-light);width:26%;color:var(--text-sec)">3PLs<br><span style="font-weight:400;font-size:.75rem;color:#888">ShipStation, ShipHero</span></th>
<th style="padding:.85rem 1rem;text-align:center;font-weight:700;border-bottom:2px solid var(--accent);width:26%;color:var(--accent);background:rgba(59,130,246,.04)">ShipZen</th>
</tr>
</thead>
<tbody>
<tr><td style="padding:.75rem 1rem;font-weight:600;border-bottom:1px solid var(--border-light)">Volume Type</td><td style="padding:.75rem 1rem;text-align:center;border-bottom:1px solid var(--border-light);color:var(--text-sec)">Pooled from random, unrelated sellers</td><td style="padding:.75rem 1rem;text-align:center;border-bottom:1px solid var(--border-light);color:var(--text-sec)">Fragmented across many businesses</td><td style="padding:.75rem 1rem;text-align:center;border-bottom:1px solid var(--border-light);font-weight:600;background:rgba(59,130,246,.04)">Consolidated into predictable lanes</td></tr>
<tr><td style="padding:.75rem 1rem;font-weight:600;border-bottom:1px solid var(--border-light)">Carrier Relationship</td><td style="padding:.75rem 1rem;text-align:center;border-bottom:1px solid var(--border-light);color:var(--text-sec)">Shared commercial account</td><td style="padding:.75rem 1rem;text-align:center;border-bottom:1px solid var(--border-light);color:var(--text-sec)">Multi-carrier, rate-shopping</td><td style="padding:.75rem 1rem;text-align:center;border-bottom:1px solid var(--border-light);font-weight:600;background:rgba(59,130,246,.04)">Direct enterprise UPS partnership</td></tr>
<tr><td style="padding:.75rem 1rem;font-weight:600;border-bottom:1px solid var(--border-light)">Predictability</td><td style="padding:.75rem 1rem;text-align:center;border-bottom:1px solid var(--border-light);color:var(--text-sec)">Low -random origins &amp; destinations</td><td style="padding:.75rem 1rem;text-align:center;border-bottom:1px solid var(--border-light);color:var(--text-sec)">Moderate -high volume but inconsistent</td><td style="padding:.75rem 1rem;text-align:center;border-bottom:1px solid var(--border-light);font-weight:600;background:rgba(59,130,246,.04)">High -repeat routes, consistent usage</td></tr>
<tr><td style="padding:.75rem 1rem;font-weight:600;border-bottom:1px solid var(--border-light)">Data Quality</td><td style="padding:.75rem 1rem;text-align:center;border-bottom:1px solid var(--border-light);color:var(--text-sec)">Varies by seller</td><td style="padding:.75rem 1rem;text-align:center;border-bottom:1px solid var(--border-light);color:var(--text-sec)">Varies by client</td><td style="padding:.75rem 1rem;text-align:center;border-bottom:1px solid var(--border-light);font-weight:600;background:rgba(59,130,246,.04)">Validated &amp; standardized before every label</td></tr>
<tr><td style="padding:.75rem 1rem;font-weight:600;border-bottom:1px solid var(--border-light)">Carrier Commitment</td><td style="padding:.75rem 1rem;text-align:center;border-bottom:1px solid var(--border-light);color:var(--text-sec)">None -volume shifts daily</td><td style="padding:.75rem 1rem;text-align:center;border-bottom:1px solid var(--border-light);color:var(--text-sec)">Split across multiple carriers</td><td style="padding:.75rem 1rem;text-align:center;border-bottom:1px solid var(--border-light);font-weight:600;background:rgba(59,130,246,.04)">Dedicated, long-term UPS commitment</td></tr>
<tr><td style="padding:.75rem 1rem;font-weight:600">Pricing Tier</td><td style="padding:.75rem 1rem;text-align:center;color:var(--text-sec)">Standard commercial</td><td style="padding:.75rem 1rem;text-align:center;color:var(--text-sec)">Commercial + volume discounts</td><td style="padding:.75rem 1rem;text-align:center;font-weight:700;color:var(--accent);background:rgba(59,130,246,.04)">Enterprise</td></tr>
</tbody>
</table>
</div>
</div>
</section>

<!-- FAQ -->
<section class="faq-s" id="faq">
<div class="container">
<h2 class="st c">FAQs</h2>
<p class="sd c">Everything you need to know about ShipZen and discounted shipping labels.</p>
<div class="faq-wrap">
<div class="faq-i"><button class="faq-q" onclick="tFaq(this)">How does ShipZen offer such low shipping rates?<svg class="faq-ch" viewBox="0 0 20 20" fill="none"><path d="M5 7.5l5 5 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button><div class="faq-a"><div class="faq-ai">ShipZen operates under a direct enterprise-level UPS Ground agreement. We consolidate shipments into predictable, high-frequency lanes so UPS can plan trucks and routes around our volume. We also validate every address before printing, which eliminates correction fees. This combination of lane optimization, clean data, and committed volume qualifies us for enterprise pricing that aggregator platforms simply cannot access.</div></div></div>
<div class="faq-i"><button class="faq-q" onclick="tFaq(this)">How is ShipZen different from Pirate Ship, EasyShip, or other aggregators?<svg class="faq-ch" viewBox="0 0 20 20" fill="none"><path d="M5 7.5l5 5 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button><div class="faq-a"><div class="faq-ai">Aggregators pool thousands of unrelated sellers onto a shared account. The result is &ldquo;noisy&rdquo; volume -random origins, random destinations, no repeat patterns. UPS can&rsquo;t optimize routes around that, so the pricing reflects the uncertainty. They also rate-shop across multiple carriers, so no single carrier has a reason to offer their deepest discounts. ShipZen is the opposite: dedicated UPS commitment, predictable lanes, and validated data -which unlocks enterprise-tier pricing.</div></div></div>
<div class="faq-i"><button class="faq-q" onclick="tFaq(this)">How is ShipZen different from 3PLs like ShipStation or ShipHero?<svg class="faq-ch" viewBox="0 0 20 20" fill="none"><path d="M5 7.5l5 5 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button><div class="faq-a"><div class="faq-ai">3PLs handle fragmented volume from thousands of businesses with different packaging, destinations, and timing. They&rsquo;re also structured for multi-carrier flexibility -optimizing across UPS, FedEx, and USPS simultaneously -so no single carrier relationship is deep enough for enterprise pricing. ShipZen focuses exclusively on UPS Ground with lane-optimized routes, giving us the consistency UPS rewards with its deepest discounts.</div></div></div>
<div class="faq-i"><button class="faq-q" onclick="tFaq(this)">Why can&rsquo;t aggregators or 3PLs match your rates?<svg class="faq-ch" viewBox="0 0 20 20" fill="none"><path d="M5 7.5l5 5 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button><div class="faq-a"><div class="faq-ai">Enterprise pricing tiers require predictable volume, consistent Ground usage, and repeat lanes. Aggregators can&rsquo;t provide that because their volume is inherently unpredictable and impossible to lane-optimize. 3PLs can&rsquo;t either because their business model is built around variety and multi-carrier flexibility. ShipZen is structured around the exact behaviors UPS incentivizes -and that&rsquo;s why our per-package cost is lower.</div></div></div>
<div class="faq-i"><button class="faq-q" onclick="tFaq(this)">What shipping services does ShipZen support?<svg class="faq-ch" viewBox="0 0 20 20" fill="none"><path d="M5 7.5l5 5 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button><div class="faq-a"><div class="faq-ai">ShipZen offers UPS Ground service across the lower 48 states with flat-rate pricing. Our intentional focus on a single carrier and service is what allows us to offer enterprise-tier rates.</div></div></div>
<div class="faq-i"><button class="faq-q" onclick="tFaq(this)">What are the weight limits for flat-rate pricing?<svg class="faq-ch" viewBox="0 0 20 20" fill="none"><path d="M5 7.5l5 5 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button><div class="faq-a"><div class="faq-ai">Flat rates apply to packages up to 3 lbs. This covers the majority of e-commerce shipments and is where you see the biggest savings compared to Pirate Ship, EasyShip, or ShipStation.</div></div></div>
<div class="faq-i"><button class="faq-q" onclick="tFaq(this)">Are there any monthly fees or minimums?<svg class="faq-ch" viewBox="0 0 20 20" fill="none"><path d="M5 7.5l5 5 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button><div class="faq-a"><div class="faq-ai">No monthly fees, no volume commitments, no minimums. You pay per label, that&rsquo;s it. Cancel anytime.</div></div></div>
<div class="faq-i"><button class="faq-q" onclick="tFaq(this)">What e-commerce platforms does ShipZen integrate with?<svg class="faq-ch" viewBox="0 0 20 20" fill="none"><path d="M5 7.5l5 5 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button><div class="faq-a"><div class="faq-ai">ShipZen works with Shopify, WooCommerce, BigCommerce, Etsy, Amazon, eBay, and offers API access for custom integrations. Most merchants go live within 24 hours.</div></div></div>
<div class="faq-i"><button class="faq-q" onclick="tFaq(this)">What about zone fees or dimensional weight charges?<svg class="faq-ch" viewBox="0 0 20 20" fill="none"><path d="M5 7.5l5 5 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button><div class="faq-a"><div class="faq-ai">None. Our flat-rate pricing is possible because lane optimization averages out distance costs across our network, and address validation removes the hidden fees and risk premiums that make flat rates too risky for aggregator platforms.</div></div></div>
<div class="faq-i"><button class="faq-q" onclick="tFaq(this)">Can I see real savings examples?<svg class="faq-ch" viewBox="0 0 20 20" fill="none"><path d="M5 7.5l5 5 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button><div class="faq-a"><div class="faq-ai">Absolutely. Across hundreds or thousands of shipments per month, the per-package savings add up to a meaningful difference in your bottom line -without changing carriers, sacrificing delivery speed, or adding complexity. Request a custom quote to see your exact savings.</div></div></div>
<div class="faq-i"><button class="faq-q" onclick="tFaq(this)">How quickly can I start using ShipZen?<svg class="faq-ch" viewBox="0 0 20 20" fill="none"><path d="M5 7.5l5 5 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button><div class="faq-a"><div class="faq-ai">Most merchants can integrate and start printing labels within 24 hours. Just connect your store and start saving immediately.</div></div></div>
<div class="faq-i"><button class="faq-q" onclick="tFaq(this)">Is there a contract or cancellation fee?<svg class="faq-ch" viewBox="0 0 20 20" fill="none"><path d="M5 7.5l5 5 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button><div class="faq-a"><div class="faq-ai">No contracts, no cancellation fees. Use ShipZen as much or as little as you want. Cancel anytime.</div></div></div>
</div>
</div>
</section>



<!-- CTA -->
<section class="cta-section">
<canvas id="cta-rain"></canvas>
<div class="container">
<div class="cta-card fade-in">
<h2>Start saving on every shipment today.</h2>
<p>You&rsquo;re still shipping UPS Ground with full tracking and the same delivery network.<br><strong>The only thing that changes is what you pay.</strong></p>
<a href="#contact" class="btn-cta">Get Your Savings Quote</a>
</div>
</div>
</section>

<!-- FOOTER -->
<footer class="footer">
<div class="container">
<div class="footer-in">
<a href="#" class="footer-brand">
<svg width="20" height="20" viewBox="0 0 40 40" fill="none"><path d="M4,2L36,2Q39,2 39,5L39,14L7,29L1,14L1,5Q1,2 4,2Z" fill="#1e3a8a"/><path d="M33,11L39,26L39,35Q39,38 36,38L4,38Q1,38 1,35L1,26Z" fill="#00b4d8" opacity=".80"/></svg>
ShipZen
</a>
<ul class="footer-links">
<li><a href="#">Privacy Policy</a></li>
<li><a href="#">Terms &amp; Conditions</a></li>
</ul>
</div>
</div>
</footer>

<script>
function tFaq(b){var i=b.parentElement,o=i.classList.contains('open');document.querySelectorAll('.faq-i.open').forEach(function(e){e.classList.remove('open')});if(!o)i.classList.add('open')}

document.getElementById('lead-form').addEventListener('submit',function(e){
e.preventDefault();
var b=document.getElementById('submit-btn'),m=document.getElementById('form-msg');
m.className='form-msg';m.textContent='';
document.querySelectorAll('.err').forEach(function(e){e.classList.remove('err')});
var d={email:document.getElementById('email').value.trim(),phone:document.getElementById('phone').value.trim(),website:document.getElementById('website').value.trim(),monthly_shipments:document.getElementById('monthly_shipments').value};
var errs=[];
if(!d.email){errs.push(1);document.getElementById('email').classList.add('err')}
else if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email)){errs.push(1);document.getElementById('email').classList.add('err')}
if(errs.length){m.className='form-msg err';m.textContent='Please enter a valid email address.';return}
b.disabled=true;b.textContent='Submitting...';
fetch('/api/lead',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)})
.then(function(r){return r.json().then(function(j){return{ok:r.ok,data:j}})})
.then(function(r){if(r.ok){m.className='form-msg ok';m.textContent='Thank you! We\'ll send your savings quote within 24 hours.';document.getElementById('lead-form').reset()}else{m.className='form-msg err';m.textContent='Oops! Something went wrong while submitting the form.'}})
.catch(function(){m.className='form-msg err';m.textContent='Oops! Something went wrong while submitting the form.'})
.finally(function(){b.disabled=false;b.innerHTML='\uD83D\uDCE6 Get Your Savings Quote'});
});

var obs=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)e.target.classList.add('visible')})},{threshold:.1,rootMargin:'0px 0px -30px 0px'});
document.querySelectorAll('.fade-in').forEach(function(e){obs.observe(e)});
document.querySelectorAll('a[href^="#"]').forEach(function(a){a.addEventListener('click',function(e){var t=document.querySelector(this.getAttribute('href'));if(t){e.preventDefault();t.scrollIntoView({behavior:'smooth',block:'start'})}})});

/* Counter animation for dashboard stats + floating badges */
(function(){
var counted=false;
function animateCounters(){
if(counted)return;
counted=true;
document.querySelectorAll('[data-count]').forEach(function(el){
var target=parseFloat(el.getAttribute('data-count'));
var prefix=el.getAttribute('data-prefix')||'';
var suffix=el.getAttribute('data-suffix')||'';
var dec=parseInt(el.getAttribute('data-decimal'))||0;
var duration=1400;
var start=performance.now();
function step(now){
var elapsed=now-start;
var progress=Math.min(elapsed/duration,1);
var ease=1-Math.pow(1-progress,3);
var current=ease*target;
if(dec>0){el.textContent=prefix+current.toFixed(dec)+suffix}
else{el.textContent=prefix+Math.round(current).toLocaleString()+suffix}
if(progress<1)requestAnimationFrame(step);
}
requestAnimationFrame(step);
});
}
function animateBars(){
document.querySelectorAll('.dash-bar').forEach(function(bar,i){
var h=bar.style.height;
bar.style.height='0';
setTimeout(function(){bar.style.height=h},100+i*60);
});
}
var dashObs=new IntersectionObserver(function(entries){
entries.forEach(function(entry){
if(entry.isIntersecting){animateCounters();animateBars();dashObs.disconnect()}
});
},{threshold:.2});
var dw=document.querySelector('.dash-wrap');
if(dw)dashObs.observe(dw);
})();

/* ── Visibility-based animation pausing ── */
var visMap=new Map();
var visObs=new IntersectionObserver(function(entries){
entries.forEach(function(e){visMap.set(e.target,e.isIntersecting)});
},{threshold:0,rootMargin:'50px'});
function isVisible(el){return visMap.get(el)!==false}
function observeCanvas(el){visMap.set(el,true);visObs.observe(el)}

/* ── WebGL animated mesh gradient (blue/indigo theme) ── */
(function(){
var c=document.getElementById('gradient-canvas');
if(!c)return;
var gl=c.getContext('webgl')||c.getContext('experimental-webgl');
if(!gl){
c.style.display='none';
c.parentElement.style.background='linear-gradient(135deg,#eff6ff 0%,#dbeafe 25%,#bfdbfe 50%,#93c5fd 75%,#e0f2fe 100%)';
return;
}

function resize(){
var hero=c.closest('.hero');
var dpr=Math.min(window.devicePixelRatio||1,2);
c.width=hero.offsetWidth*dpr;
c.height=hero.offsetHeight*dpr;
c.style.width=hero.offsetWidth+'px';
c.style.height=hero.offsetHeight+'px';
gl.viewport(0,0,c.width,c.height);
}
resize();
window.addEventListener('resize',resize);

var vsrc='attribute vec2 p;void main(){gl_Position=vec4(p,0,1);}';
var fsrc=[
'precision highp float;',
'uniform float t;',
'uniform vec2 res;',
'',
'vec3 cBg=vec3(1.0,1.0,1.0);',
'vec3 c1=vec3(0.231,0.510,0.965);',
'vec3 c2=vec3(0.145,0.388,0.922);',
'vec3 c3=vec3(0.376,0.647,0.992);',
'vec3 c4=vec3(0.118,0.251,0.686);',
'vec3 c5=vec3(0.859,0.914,0.996);',
'vec3 c6=vec3(0.576,0.773,0.992);',
'',
'float ribbon(vec2 uv,float offset,float freq,float amp,float width,float speed){',
'  float diag=uv.x*0.7+uv.y*0.3;',
'  float wave=amp*sin(diag*freq+t*speed+offset);',
'  float perp=-uv.x*0.3+uv.y*0.7;',
'  float d=abs(perp-wave-offset*0.15);',
'  return smoothstep(width,width*0.08,d);',
'}',
'',
'void main(){',
'  vec2 uv=gl_FragCoord.xy/res;',
'  float aspect=res.x/res.y;',
'  vec2 p=vec2(uv.x*aspect,uv.y);',
'  p.x-=aspect*0.5;',
'  p.y-=0.5;',
'  float s=t*0.08;',
'  float r1=ribbon(p, 0.0, 3.5, 0.18, 0.28, 0.15);',
'  float r2=ribbon(p, 0.6, 4.0, 0.22, 0.22, 0.12);',
'  float r3=ribbon(p,-0.5, 3.0, 0.15, 0.35, 0.18);',
'  float r4=ribbon(p, 1.2, 4.5, 0.12, 0.18, 0.10);',
'  float r5=ribbon(p,-1.0, 3.8, 0.20, 0.25, 0.14);',
'  float r6=ribbon(p, 0.3, 2.5, 0.25, 0.32, 0.20);',
'  vec3 col=cBg;',
'  col=mix(col,c5,r6*0.5);',
'  col=mix(col,c3,r3*0.6);',
'  col=mix(col,c6,r5*0.55);',
'  col=mix(col,c1,r1*0.75);',
'  col=mix(col,c4,r2*0.7);',
'  col=mix(col,c2,r4*0.65);',
'  float edge1=ribbon(p, 0.0, 3.5, 0.18, 0.06, 0.15);',
'  float edge2=ribbon(p, 0.6, 4.0, 0.22, 0.05, 0.12);',
'  col=mix(col,vec3(1.0),edge1*0.3);',
'  col=mix(col,vec3(0.94,0.96,1.0),edge2*0.25);',
'  float fade=smoothstep(0.0,0.45,uv.x);',
'  col=mix(cBg,col,fade);',
'  float bfade=smoothstep(0.0,0.15,uv.y);',
'  col=mix(cBg,col,bfade);',
'  gl_FragColor=vec4(col,1.0);',
'}'
].join('\n');

function mkShader(src,type){
var s=gl.createShader(type);
gl.shaderSource(s,src);
gl.compileShader(s);
return s;
}
var vs=mkShader(vsrc,gl.VERTEX_SHADER);
var fs=mkShader(fsrc,gl.FRAGMENT_SHADER);
var prog=gl.createProgram();
gl.attachShader(prog,vs);
gl.attachShader(prog,fs);
gl.linkProgram(prog);
gl.useProgram(prog);

var buf=gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER,buf);
gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
var pLoc=gl.getAttribLocation(prog,'p');
gl.enableVertexAttribArray(pLoc);
gl.vertexAttribPointer(pLoc,2,gl.FLOAT,false,0,0);

var tLoc=gl.getUniformLocation(prog,'t');
var rLoc=gl.getUniformLocation(prog,'res');

observeCanvas(c);
var start=performance.now();
function frame(){
if(isVisible(c)){
var elapsed=(performance.now()-start)/1000;
gl.uniform1f(tLoc,elapsed);
gl.uniform2f(rLoc,c.width,c.height);
gl.drawArrays(gl.TRIANGLE_STRIP,0,4);
}
requestAnimationFrame(frame);
}
frame();
})();

/* Nav transparency toggle on scroll */
(function(){
var nav=document.querySelector('.nav');
var hero=document.querySelector('.hero');
if(!nav||!hero)return;
function onScroll(){
var heroBottom=hero.getBoundingClientRect().bottom;
if(heroBottom<=56){nav.classList.add('nav-scrolled');}
else{nav.classList.remove('nav-scrolled');}
}
window.addEventListener('scroll',onScroll,{passive:true});
onScroll();
})();

/* ── Enterprise card canvas animations ── */
(function(){
function setupCanvas(id){
var c=document.getElementById(id);
if(!c)return null;
var ctx=c.getContext('2d');
function sz(){var r=c.parentElement.getBoundingClientRect();var d=window.devicePixelRatio||1;c.width=r.width*d;c.height=r.height*d;ctx.scale(d,d);c._w=r.width;c._h=r.height;}
sz();window.addEventListener('resize',sz);
return{c:c,ctx:ctx};
}

/* Card 1: Savings accumulator — cost bars comparing ShipZen vs Others */
var s1=setupCanvas('ent-cv-1');
if(s1)(function(){
var ctx=s1.ctx,c=s1.c;
observeCanvas(c);
var tick=0;
var startSaved=8000+Math.floor(Math.random()*1000);
var packages=[];var totalSaved=startSaved;var savedHistory=[];var maxHistory=180;
function spawnPkg(){
var weight=Math.random()<.5?1:Math.random()<.6?2:3;
var saved=Math.random()*1.5+0.8;
totalSaved+=saved;
packages.push({x:1.05,y:.3+Math.random()*.4,vx:-(Math.random()*.006+.004),saved:saved,weight:weight,o:1,age:0});
}
function draw(){
if(!isVisible(c)){requestAnimationFrame(draw);return;}
var w=c._w,h=c._h;
ctx.clearRect(0,0,w,h);
tick++;
ctx.fillStyle='#f0f5ff';ctx.fillRect(0,0,w,h);
var gbx=w*(.5+Math.sin(tick*.004)*.12);
var gby=h*(.5+Math.cos(tick*.006)*.1);
var glow=ctx.createRadialGradient(gbx,gby,0,gbx,gby,w*.5);
glow.addColorStop(0,'rgba(59,130,246,.07)');glow.addColorStop(1,'rgba(255,255,255,0)');
ctx.fillStyle=glow;ctx.fillRect(0,0,w,h);
/* spawn packages */
if(tick%18===0)spawnPkg();
/* record savings history */
if(tick%3===0){savedHistory.push(totalSaved);if(savedHistory.length>maxHistory)savedHistory.shift();}
/* draw savings chart */
var chartL=w*.08,chartR=w*.92,chartT=h*.55,chartB=h*.9;
var chartW=chartR-chartL,chartH=chartB-chartT;
ctx.strokeStyle='rgba(59,130,246,.06)';ctx.lineWidth=.5;
for(var gy=0;gy<4;gy++){var ly=chartT+gy*(chartH/3);ctx.beginPath();ctx.moveTo(chartL,ly);ctx.lineTo(chartR,ly);ctx.stroke();}
if(savedHistory.length>1){
var maxVal=Math.max.apply(null,savedHistory)*1.1||10;
ctx.save();
ctx.beginPath();
var stepX=chartW/(maxHistory-1);
ctx.moveTo(chartR-(savedHistory.length-1)*stepX,chartB-chartH*(savedHistory[0]/maxVal));
for(var i=1;i<savedHistory.length;i++){
var px=chartR-(savedHistory.length-1-i)*stepX;
var py=chartB-chartH*(savedHistory[i]/maxVal);
ctx.lineTo(px,py);
}
ctx.lineTo(chartR,chartB);ctx.lineTo(chartR-(savedHistory.length-1)*stepX,chartB);ctx.closePath();
var areaGrad=ctx.createLinearGradient(0,chartT,0,chartB);
areaGrad.addColorStop(0,'rgba(16,185,129,.15)');areaGrad.addColorStop(1,'rgba(16,185,129,.02)');
ctx.fillStyle=areaGrad;ctx.fill();
ctx.beginPath();
ctx.moveTo(chartR-(savedHistory.length-1)*stepX,chartB-chartH*(savedHistory[0]/maxVal));
for(var i=1;i<savedHistory.length;i++){
var px=chartR-(savedHistory.length-1-i)*stepX;
var py=chartB-chartH*(savedHistory[i]/maxVal);
ctx.lineTo(px,py);
}
ctx.strokeStyle='rgba(16,185,129,.6)';ctx.lineWidth=2;ctx.stroke();
ctx.restore();
}
/* flying packages */
for(var i=packages.length-1;i>=0;i--){
var p=packages[i];p.x+=p.vx;p.age++;
if(p.x<-.05){packages.splice(i,1);continue;}
var px=p.x*w,py=p.y*h;
ctx.save();
ctx.fillStyle='rgba(59,130,246,'+(p.o*.6)+')';
ctx.fillRect(px-6,py-5,12,10);
ctx.strokeStyle='rgba(59,130,246,'+(p.o*.3)+')';ctx.lineWidth=.5;
ctx.strokeRect(px-6,py-5,12,10);
ctx.restore();
/* savings label */
if(p.age<60){
ctx.font='600 '+Math.round(w*.025)+'px Inter,system-ui,sans-serif';
ctx.fillStyle='rgba(16,185,129,'+(Math.min(p.age/15,1)*(1-Math.max(0,(p.age-40)/20)))+')';
ctx.textAlign='center';
ctx.fillText('saved',px,py-12);
}
}
/* total savings display */
var txtX=w*.5;var txtY=h*.28;
ctx.save();ctx.textAlign='center';ctx.textBaseline='middle';
ctx.font='800 '+Math.round(w*.11)+'px Inter,system-ui,sans-serif';
ctx.fillStyle='rgba(16,185,129,.8)';
ctx.fillText(totalSaved.toFixed(0)+'+',txtX,txtY);
ctx.font='600 '+Math.round(w*.028)+'px Inter,system-ui,sans-serif';
ctx.fillStyle='rgba(59,130,246,.35)';
ctx.fillText('PACKAGES OPTIMIZED',txtX,txtY+w*.075);
ctx.restore();
requestAnimationFrame(draw);
}
draw();
})();

/* Card 2: Flat-rate map — packages shipping to different states, same price */
var s2=setupCanvas('ent-cv-2');
if(s2)(function(){
var ctx=s2.ctx,c=s2.c;
observeCanvas(c);
var tick=0;
/* Accurate US lower-48 outline — 234 points from real geographic data */
var usPath=[
[.0021,.0415],[.0272,.0555],[.0364,.0943],[.0407,.0835],[.0379,.0497],
[.032,.016],[.0812,.016],[.1326,.016],[.1497,.016],[.2025,.016],[.2536,.016],
[.3056,.016],[.3576,.016],[.4164,.016],[.4757,.016],[.5116,.016],[.5116,.0002],
[.5175,0],[.5175,0],[.5205,.0226],[.5259,.0295],[.538,.0321],[.5557,.0386],
[.5725,.0514],[.5866,.046],[.6079,.0567],[.6135,.0563],[.629,.0447],
[.6453,.0596],[.6622,.0755],[.6762,.0892],[.6897,.1024],[.6914,.1132],
[.6955,.1173],[.6944,.1213],[.699,.1226],[.7024,.1183],[.7033,.1281],
[.7068,.1346],[.7115,.1346],[.7141,.1396],[.7119,.1469],[.73,.1663],
[.7337,.2036],[.7371,.2393],[.7321,.2636],[.7239,.2863],[.7201,.3007],
[.7197,.305],[.7217,.3108],[.7276,.3173],[.7319,.3173],[.752,.2954],
[.7699,.2889],[.7925,.2684],[.7929,.2643],[.7913,.2517],[.7885,.2436],
[.7963,.2371],[.8134,.2369],[.8293,.237],[.8348,.2209],[.837,.2177],
[.8553,.1881],[.8631,.1805],[.8894,.1802],[.9213,.1802],[.9231,.1701],
[.9286,.168],[.936,.1616],[.9421,.1429],[.9474,.1109],[.9606,.0799],
[.9664,.0907],[.978,.0837],[.9857,.0955],[.9857,.1516],[.997,.1749],[1,.1884],
[.9815,.2083],[.9637,.2225],[.9454,.2347],[.9362,.2591],[.9333,.2684],
[.9331,.2902],[.9388,.312],[.946,.313],[.9442,.298],[.9494,.3071],[.948,.3189],
[.9363,.3256],[.928,.3248],[.9152,.3319],[.9077,.334],[.8976,.336],[.8831,.3479],
[.9086,.3402],[.9137,.348],[.8895,.3603],[.8784,.3604],[.8789,.3554],
[.8737,.3668],[.8788,.3686],[.875,.3982],[.8624,.4299],[.8611,.4193],
[.8573,.4172],[.8516,.4069],[.8552,.429],[.8595,.4363],[.8598,.4519],
[.8543,.4679],[.8445,.5007],[.8429,.4991],[.8483,.4711],[.8394,.4554],
[.8374,.4212],[.8341,.439],[.8378,.4651],[.8263,.4586],[.8382,.4719],[.839,.511],
[.844,.5139],[.8458,.5281],[.8482,.5693],[.8372,.5998],[.8193,.612],
[.8079,.6361],[.7992,.6388],[.7904,.6539],[.788,.6677],[.769,.6944],[.7592,.714],
[.751,.7383],[.7484,.7676],[.7514,.7961],[.7572,.8313],[.7649,.8605],
[.765,.8782],[.7732,.926],[.7726,.9537],[.7719,.9697],[.7676,.9948],[.7624,1],
[.7539,.995],[.7511,.977],[.7445,.9675],[.7354,.9321],[.7273,.9007],
[.7247,.8846],[.7283,.8573],[.7234,.8346],[.7099,.8002],[.7031,.7939],
[.6857,.8126],[.6826,.8105],[.6742,.7913],[.6633,.7812],[.6437,.7863],
[.6283,.7818],[.6151,.7846],[.608,.791],[.6111,.802],[.6108,.8186],[.6145,.8268],
[.6112,.8322],[.6048,.8261],[.5983,.8339],[.5857,.8326],[.5727,.8109],
[.5576,.816],[.545,.8065],[.5343,.8094],[.5197,.819],[.5039,.8495],[.4867,.8672],
[.4772,.8869],[.4733,.9054],[.4731,.9338],[.4739,.9535],[.4772,.9675],
[.4705,.9687],[.4582,.9597],[.4447,.9469],[.4398,.9276],[.436,.8988],
[.4258,.8754],[.4198,.8512],[.4111,.8231],[.3989,.8067],[.3847,.8075],
[.3738,.84],[.3594,.8276],[.3505,.8152],[.3462,.7926],[.3404,.7711],[.3301,.753],
[.3213,.74],[.3149,.7254],[.2849,.7254],[.2849,.7424],[.2712,.7424],
[.2367,.7427],[.1972,.7137],[.171,.6937],[.1727,.6857],[.1506,.6901],
[.131,.6933],[.128,.6723],[.1168,.6486],[.1087,.6437],[.1068,.6319],
[.0971,.6298],[.0909,.6187],[.0748,.6147],[.0704,.608],[.0683,.5855],
[.0515,.5441],[.0371,.4869],[.0377,.4774],[.03,.4638],[.0166,.4294],
[.0142,.3958],[.005,.3734],[.0088,.3393],[.0082,.304],[.0027,.2725],
[.0094,.2337],[.0115,.1964],[.0137,.159],[.0105,.1038],[.0051,.0687],[0,.0496],
[.0021,.0415]
];
/* City positions mapped to accurate US coordinates */
var cities=[
{name:'LA',x:.12,y:.63},{name:'SF',x:.04,y:.48},{name:'SEA',x:.03,y:.06},
{name:'DEN',x:.25,y:.40},{name:'DAL',x:.40,y:.76},{name:'CHI',x:.58,y:.28},
{name:'ATL',x:.68,y:.60},{name:'MIA',x:.76,y:.92},{name:'NYC',x:.88,y:.28},
{name:'BOS',x:.94,y:.18},{name:'PHX',x:.18,y:.62},{name:'MSP',x:.48,y:.18},
{name:'KC',x:.45,y:.46},{name:'PDX',x:.03,y:.14},{name:'SLC',x:.20,y:.36}
];
var shipments=[];var deliveries=[];
function spawnShipment(){
var from=cities[Math.floor(Math.random()*cities.length)];
var to=cities[Math.floor(Math.random()*cities.length)];
while(to===from)to=cities[Math.floor(Math.random()*cities.length)];
shipments.push({fx:from.x,fy:from.y,tx:to.x,ty:to.y,progress:0,speed:.006+Math.random()*.004,city:to.name});
}
/* Map a normalized 0-1 coordinate to canvas pixel with padding */
var pad=.06;/* 6% padding on each side */
function mx(nx,w){return pad*w+nx*(1-2*pad)*w;}
function my(ny,h){return pad*h+ny*(1-2*pad)*h*.88;}/* .88 leaves room for bottom label */
function tracePath(w,h){
ctx.beginPath();
for(var i=0;i<usPath.length;i++){
var px=mx(usPath[i][0],w),py=my(usPath[i][1],h);
if(i===0)ctx.moveTo(px,py);else ctx.lineTo(px,py);
}
ctx.closePath();
}
function draw(){
if(!isVisible(c)){requestAnimationFrame(draw);return;}
var w=c._w,h=c._h;
ctx.clearRect(0,0,w,h);
ctx.fillStyle='#f0f5ff';ctx.fillRect(0,0,w,h);
tick++;
/* subtle animated background glow */
var gbx=w*(.5+Math.sin(tick*.003)*.1);
var gby=h*(.5+Math.cos(tick*.004)*.08);
var glow=ctx.createRadialGradient(gbx,gby,0,gbx,gby,w*.5);
glow.addColorStop(0,'rgba(59,130,246,.06)');glow.addColorStop(1,'rgba(255,255,255,0)');
ctx.fillStyle=glow;ctx.fillRect(0,0,w,h);
/* spawn shipments */
if(tick%35===0)spawnShipment();
/* Draw US silhouette */
ctx.save();
tracePath(w,h);
var usGrad=ctx.createLinearGradient(0,0,w,h);
usGrad.addColorStop(0,'rgba(59,130,246,.07)');
usGrad.addColorStop(.5,'rgba(59,130,246,.12)');
usGrad.addColorStop(1,'rgba(59,130,246,.06)');
ctx.fillStyle=usGrad;ctx.fill();
ctx.strokeStyle='rgba(59,130,246,.22)';ctx.lineWidth=1.5;ctx.stroke();
ctx.restore();
/* Inner pulsing glow clipped to US shape */
ctx.save();
tracePath(w,h);ctx.clip();
var pulseR=w*(.25+Math.sin(tick*.008)*.05);
var iglow=ctx.createRadialGradient(w*.5,h*.4,0,w*.5,h*.4,pulseR);
iglow.addColorStop(0,'rgba(59,130,246,.1)');iglow.addColorStop(1,'rgba(59,130,246,0)');
ctx.fillStyle=iglow;ctx.fillRect(0,0,w,h);
ctx.restore();
/* draw city dots */
for(var i=0;i<cities.length;i++){
var ci=cities[i];
var cx=mx(ci.x,w),cy=my(ci.y,h);
var pulse=Math.sin(tick*.03+i)*.3+.7;
ctx.beginPath();ctx.arc(cx,cy,7,0,Math.PI*2);
ctx.fillStyle='rgba(59,130,246,.06)';ctx.fill();
ctx.beginPath();ctx.arc(cx,cy,3,0,Math.PI*2);
ctx.fillStyle='rgba(59,130,246,'+(.4*pulse)+')';ctx.fill();
ctx.font='500 '+Math.round(w*.02)+'px Inter,system-ui,sans-serif';
ctx.fillStyle='rgba(59,130,246,.3)';ctx.textAlign='center';
ctx.fillText(ci.name,cx,cy-10);
}
/* draw shipment arcs */
for(var i=shipments.length-1;i>=0;i--){
var s=shipments[i];s.progress+=s.speed;
if(s.progress>=1){
deliveries.push({x:mx(s.tx,w),y:my(s.ty,h),r:0,o:.6});
shipments.splice(i,1);continue;
}
var t=s.progress;
var ease=t<.5?2*t*t:(1-Math.pow(-2*t+2,2)/2);
var acx=mx(s.fx,w)+(mx(s.tx,w)-mx(s.fx,w))*.5;
var acy=Math.min(my(s.fy,h),my(s.ty,h))-h*.12;
var px=(1-ease)*(1-ease)*mx(s.fx,w)+2*(1-ease)*ease*acx+ease*ease*mx(s.tx,w);
var py=(1-ease)*(1-ease)*my(s.fy,h)+2*(1-ease)*ease*acy+ease*ease*my(s.ty,h);
ctx.beginPath();
for(var tt=0;tt<=t;tt+=.02){
var e2=tt<.5?2*tt*tt:(1-Math.pow(-2*tt+2,2)/2);
var tx2=(1-e2)*(1-e2)*mx(s.fx,w)+2*(1-e2)*e2*acx+e2*e2*mx(s.tx,w);
var ty2=(1-e2)*(1-e2)*my(s.fy,h)+2*(1-e2)*e2*acy+e2*e2*my(s.ty,h);
if(tt===0)ctx.moveTo(tx2,ty2);else ctx.lineTo(tx2,ty2);
}
ctx.strokeStyle='rgba(59,130,246,.18)';ctx.lineWidth=1.2;ctx.stroke();
ctx.beginPath();ctx.arc(px,py,3.5,0,Math.PI*2);
ctx.fillStyle='rgba(59,130,246,.8)';ctx.fill();
ctx.beginPath();ctx.arc(px,py,7,0,Math.PI*2);
ctx.fillStyle='rgba(59,130,246,.1)';ctx.fill();
}
/* delivery ripples */
for(var i=deliveries.length-1;i>=0;i--){
var d=deliveries[i];d.r+=1;d.o-=.015;
if(d.o<=0){deliveries.splice(i,1);continue;}
ctx.beginPath();ctx.arc(d.x,d.y,d.r,0,Math.PI*2);
ctx.strokeStyle='rgba(16,185,129,'+d.o+')';ctx.lineWidth=1.5;ctx.stroke();
}
/* bottom label */
ctx.save();ctx.textAlign='center';ctx.textBaseline='middle';
ctx.font='700 '+Math.round(w*.032)+'px Inter,system-ui,sans-serif';
ctx.fillStyle='rgba(59,130,246,.15)';
ctx.fillText('SAME RATE EVERYWHERE',w*.5,h*.95);
ctx.restore();
requestAnimationFrame(draw);
}
draw();
})();

/* Card 3: Simple vs complex pricing comparison */
var s3=setupCanvas('ent-cv-3');
if(s3)(function(){
var ctx=s3.ctx,c=s3.c;
observeCanvas(c);
var tick=0;
function draw(){
if(!isVisible(c)){requestAnimationFrame(draw);return;}
var w=c._w,h=c._h;
ctx.clearRect(0,0,w,h);
ctx.fillStyle='#f0f5ff';ctx.fillRect(0,0,w,h);
tick++;
var gbx=w*(.5+Math.sin(tick*.004)*.1);
var gby=h*(.5+Math.cos(tick*.005)*.08);
var glow=ctx.createRadialGradient(gbx,gby,0,gbx,gby,w*.5);
glow.addColorStop(0,'rgba(59,130,246,.05)');glow.addColorStop(1,'rgba(255,255,255,0)');
ctx.fillStyle=glow;ctx.fillRect(0,0,w,h);
/* Two columns: ShipZen (left) vs Others (right) */
var colW=w*.38;var gap=w*.06;
var lx=w*.5-gap/2-colW;var rx=w*.5+gap/2;
var topY=h*.12;
/* ShipZen side — clean, simple */
ctx.save();
ctx.fillStyle='rgba(59,130,246,.04)';
ctx.beginPath();ctx.moveTo(lx+8,topY);ctx.lineTo(lx+colW-8,topY);ctx.quadraticCurveTo(lx+colW,topY,lx+colW,topY+8);
ctx.lineTo(lx+colW,h*.88-8);ctx.quadraticCurveTo(lx+colW,h*.88,lx+colW-8,h*.88);
ctx.lineTo(lx+8,h*.88);ctx.quadraticCurveTo(lx,h*.88,lx,h*.88-8);
ctx.lineTo(lx,topY+8);ctx.quadraticCurveTo(lx,topY,lx+8,topY);ctx.closePath();ctx.fill();
ctx.strokeStyle='rgba(59,130,246,.1)';ctx.lineWidth=1;ctx.stroke();
ctx.restore();
/* ShipZen header */
ctx.font='700 '+Math.round(w*.035)+'px Inter,system-ui,sans-serif';
ctx.fillStyle='rgba(59,130,246,.6)';ctx.textAlign='center';
ctx.fillText('ShipZen',lx+colW/2,topY+h*.06);
/* Simple single label */
var priceY=topY+h*.25;
ctx.font='800 '+Math.round(w*.065)+'px Inter,system-ui,sans-serif';
ctx.fillStyle='rgba(37,99,235,.75)';
ctx.fillText('Flat Rate',lx+colW/2,priceY);
ctx.font='500 '+Math.round(w*.025)+'px Inter,system-ui,sans-serif';
ctx.fillStyle='rgba(59,130,246,.35)';
ctx.fillText('simple, predictable',lx+colW/2,priceY+h*.06);
/* Checkmarks */
var checks=['No zone fees','No DIM weight','No surcharges','No monthly fee'];
for(var i=0;i<checks.length;i++){
var cy=priceY+h*.14+i*h*.08;
ctx.font='500 '+Math.round(w*.028)+'px Inter,system-ui,sans-serif';
ctx.fillStyle='rgba(16,185,129,.6)';ctx.textAlign='center';
ctx.fillText('\u2713 '+checks[i],lx+colW/2,cy);
}
/* Others side — complex, messy */
ctx.save();
ctx.fillStyle='rgba(220,38,38,.03)';
ctx.beginPath();ctx.moveTo(rx+8,topY);ctx.lineTo(rx+colW-8,topY);ctx.quadraticCurveTo(rx+colW,topY,rx+colW,topY+8);
ctx.lineTo(rx+colW,h*.88-8);ctx.quadraticCurveTo(rx+colW,h*.88,rx+colW-8,h*.88);
ctx.lineTo(rx+8,h*.88);ctx.quadraticCurveTo(rx,h*.88,rx,h*.88-8);
ctx.lineTo(rx,topY+8);ctx.quadraticCurveTo(rx,topY,rx+8,topY);ctx.closePath();ctx.fill();
ctx.strokeStyle='rgba(220,38,38,.08)';ctx.lineWidth=1;ctx.stroke();
ctx.restore();
/* Others header */
ctx.font='700 '+Math.round(w*.035)+'px Inter,system-ui,sans-serif';
ctx.fillStyle='rgba(220,38,38,.45)';ctx.textAlign='center';
ctx.fillText('Others',rx+colW/2,topY+h*.06);
/* Complex breakdown */
var fees=[
{label:'Base rate',val:'varies',y:0},
{label:'Zone surcharge',val:'+ extra',y:1},
{label:'Fuel surcharge',val:'+ extra',y:2},
{label:'DIM weight adj.',val:'+ extra',y:3},
{label:'Residential fee',val:'+ extra',y:4}
];
var startY=topY+h*.16;
for(var i=0;i<fees.length;i++){
var fy=startY+i*h*.09;
var wobble=Math.sin(tick*.02+i*1.5)*1;
ctx.font='500 '+Math.round(w*.024)+'px Inter,system-ui,sans-serif';
ctx.fillStyle='rgba(220,38,38,.35)';ctx.textAlign='left';
ctx.fillText(fees[i].label,rx+w*.02,fy+wobble);
ctx.textAlign='right';ctx.fillStyle='rgba(220,38,38,.5)';
ctx.fillText(fees[i].val,rx+colW-w*.02,fy+wobble);
/* strikethrough line */
if(i>0){
ctx.beginPath();ctx.moveTo(rx+w*.02,fy+wobble+1);ctx.lineTo(rx+colW-w*.02,fy+wobble+1);
ctx.strokeStyle='rgba(220,38,38,.06)';ctx.lineWidth=.5;ctx.stroke();
}
}
/* total */
var totalY=startY+5*h*.09+h*.03;
ctx.font='700 '+Math.round(w*.04)+'px Inter,system-ui,sans-serif';
ctx.fillStyle='rgba(220,38,38,.5)';ctx.textAlign='center';
ctx.fillText('$$$',rx+colW/2,totalY);
ctx.font='500 '+Math.round(w*.022)+'px Inter,system-ui,sans-serif';
ctx.fillStyle='rgba(220,38,38,.3)';
ctx.fillText('total after fees',rx+colW/2,totalY+h*.05);
/* VS badge in center */
var vsY=h*.45;
ctx.beginPath();ctx.arc(w*.5,vsY,w*.04,0,Math.PI*2);
ctx.fillStyle='#fff';ctx.fill();
ctx.strokeStyle='rgba(59,130,246,.15)';ctx.lineWidth=1;ctx.stroke();
ctx.font='800 '+Math.round(w*.028)+'px Inter,system-ui,sans-serif';
ctx.fillStyle='rgba(59,130,246,.5)';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText('VS',w*.5,vsY);
ctx.textBaseline='alphabetic';
requestAnimationFrame(draw);
}
draw();
})();

/* ── CTA rain ripple animation ── */
var ctaCv=document.getElementById('cta-rain');
if(ctaCv)(function(){
var ctx=ctaCv.getContext('2d');
observeCanvas(ctaCv);
var w,h,dpr;
function sz(){
var r=ctaCv.parentElement.getBoundingClientRect();
dpr=window.devicePixelRatio||1;
ctaCv.width=r.width*dpr;ctaCv.height=r.height*dpr;
ctx.scale(dpr,dpr);w=r.width;h=r.height;
}
sz();window.addEventListener('resize',sz);
var ripples=[];
var tick=0;
function maxDiag(){return Math.sqrt(w*w+h*h);}
function spawnDrop(){
var diag=maxDiag();
var dx=Math.random()*w, dy=Math.random()*h;
var cornerDist=Math.max(
Math.sqrt(dx*dx+dy*dy),
Math.sqrt((w-dx)*(w-dx)+dy*dy),
Math.sqrt(dx*dx+(h-dy)*(h-dy)),
Math.sqrt((w-dx)*(w-dx)+(h-dy)*(h-dy))
);
ripples.push({
x:dx, y:dy,
r:0,maxR:cornerDist+20+Math.random()*40,
o:.15+Math.random()*.08,
speed:.12+Math.random()*.1,
rings:[],born:tick
});
var last=ripples[ripples.length-1];
last.rings.push({r:0,o:last.o*.5,delay:18});
last.rings.push({r:0,o:last.o*.3,delay:40});
last.rings.push({r:0,o:last.o*.15,delay:65});
}
function draw(){
if(!isVisible(ctaCv)){requestAnimationFrame(draw);return;}
tick++;
ctx.fillStyle='#2563eb';ctx.fillRect(0,0,w,h);
var sx1=w*(.3+Math.sin(tick*.0008)*.25);
var sy1=h*(.4+Math.cos(tick*.001)*.2);
var sheen=ctx.createRadialGradient(sx1,sy1,0,sx1,sy1,w*.5);
sheen.addColorStop(0,'rgba(96,165,250,.07)');sheen.addColorStop(1,'rgba(255,255,255,0)');
ctx.fillStyle=sheen;ctx.fillRect(0,0,w,h);
var sx2=w*(.7+Math.cos(tick*.0009)*.2);
var sy2=h*(.6+Math.sin(tick*.0012)*.15);
var sheen2=ctx.createRadialGradient(sx2,sy2,0,sx2,sy2,w*.45);
sheen2.addColorStop(0,'rgba(255,255,255,.03)');sheen2.addColorStop(1,'rgba(255,255,255,0)');
ctx.fillStyle=sheen2;ctx.fillRect(0,0,w,h);
if(tick%45===0)spawnDrop();
if(tick%67===0)spawnDrop();
if(tick%97===0)spawnDrop();
for(var i=ripples.length-1;i>=0;i--){
var rp=ripples[i];
rp.r+=rp.speed;
var life=rp.r/rp.maxR;
var fade=1-life*life;
var alpha=rp.o*fade*fade;
if(life>=1){ripples.splice(i,1);continue;}
ctx.beginPath();ctx.arc(rp.x,rp.y,rp.r,0,Math.PI*2);
ctx.strokeStyle='rgba(255,255,255,'+alpha.toFixed(4)+')';
ctx.lineWidth=Math.max(.2,1.2*(1-life));ctx.stroke();
if(life<.6){
var glowA=alpha*.25*(1-life/.6);
ctx.beginPath();ctx.arc(rp.x,rp.y,rp.r,0,Math.PI*2);
ctx.strokeStyle='rgba(255,255,255,'+glowA.toFixed(4)+')';
ctx.lineWidth=Math.max(.2,3*(1-life/.6));ctx.stroke();
}
for(var j=0;j<rp.rings.length;j++){
var ring=rp.rings[j];
var age=tick-rp.born;
if(age<ring.delay)continue;
var rr=rp.r-ring.delay*rp.speed;
if(rr<0)continue;
var rLife=rr/rp.maxR;
if(rLife>=1)continue;
var rFade=1-rLife*rLife;
var rAlpha=ring.o*rFade*rFade;
ctx.beginPath();ctx.arc(rp.x,rp.y,rr,0,Math.PI*2);
ctx.strokeStyle='rgba(255,255,255,'+rAlpha.toFixed(4)+')';
ctx.lineWidth=Math.max(.15,.9*(1-rLife));ctx.stroke();
}
if(life<.05){
var dotO=(1-life/.05)*rp.o*.4;
ctx.beginPath();ctx.arc(rp.x,rp.y,2*(1-life/.05),0,Math.PI*2);
ctx.fillStyle='rgba(255,255,255,'+dotO.toFixed(4)+')';ctx.fill();
}
}
requestAnimationFrame(draw);
}
draw();
})();

})();
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n  ShipZen Landing Page running at: http://localhost:8421\n")
    app.run(debug=True, host="0.0.0.0", port=8421)
