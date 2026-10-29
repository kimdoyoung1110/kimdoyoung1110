#!/usr/bin/env python3
"""프로필 README용 SVG 카드 생성기.

- assets/terminal-dark.svg / terminal-light.svg : 이름 로고 · 기여 잔디 + neofetch 스타일 소개 카드
- assets/cards/<id>-dark.svg / <id>-light.svg     : 프로젝트 카드

GitHub 통계(레포 · 팔로워 · 스타 · 최근 1년 기여)는 실행할 때마다 새로 가져오고,
가져오지 못하면 assets/stats.json 에 남은 마지막 값을 씁니다.
GitHub Actions(.github/workflows/profile-cards.yml)에서 매일 실행됩니다.
"""
from __future__ import annotations

import base64
import datetime as dt
import html
import json
import os
import re
import unicodedata
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
USER = "kimdoyoung1110"
KST = dt.timezone(dt.timedelta(hours=9))

THEMES = {
    "dark": {
        "bg": "#0d1117", "border": "#30363d", "text": "#e6edf3", "muted": "#7d8590",
        "key": "#79c0ff", "accent": "#58a6ff", "ascii": "#3b82f6", "dots": "#30363d",
        "chip_bg": "#132344", "chip_text": "#93c5fd", "title": "#ffffff",
    },
    "light": {
        "bg": "#ffffff", "border": "#d0d7de", "text": "#1f2328", "muted": "#656d76",
        "key": "#0550ae", "accent": "#0969da", "ascii": "#2563eb", "dots": "#d0d7de",
        "chip_bg": "#ddf4ff", "chip_text": "#0550ae", "title": "#1f2328",
    },
}

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono','D2Coding',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Pretendard','Apple SD Gothic Neo','Malgun Gothic','Noto Sans KR','Segoe UI',sans-serif"


# ---------------------------------------------------------------- stats
def _get(url: str, headers: dict | None = None) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "profile-cards", **(headers or {})})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode()


def fetch_stats() -> dict:
    cache = ASSETS / "stats.json"
    stats = json.loads(cache.read_text()) if cache.exists() else {}
    auth = {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"} if os.environ.get("GITHUB_TOKEN") else {}
    try:
        user = json.loads(_get(f"https://api.github.com/users/{USER}", auth))
        repos = json.loads(_get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner", auth))
        stats["repos"] = user["public_repos"]
        stats["followers"] = user["followers"]
        stats["stars"] = sum(r["stargazers_count"] for r in repos if not r["fork"])
    except Exception as e:  # noqa: BLE001
        print("REST stats failed:", e)
    try:
        page = _get(f"https://github.com/users/{USER}/contributions", {"X-Requested-With": "XMLHttpRequest"})
        m = re.search(r"([\d,]+)\s+contributions?\s+in the last year", re.sub(r"\s+", " ", page))
        if m:
            stats["contributions"] = int(m.group(1).replace(",", ""))
        days = re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*?data-level="(\d)"', page)
        if days:
            stats["calendar"] = sorted([d, int(l)] for d, l in days)
    except Exception as e:  # noqa: BLE001
        print("contributions failed:", e)
    stats["updated"] = dt.datetime.now(KST).strftime("%Y.%m.%d")
    cache.write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n")
    return stats


# ---------------------------------------------------------------- helpers
def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def text_width(s: str, size: float) -> float:
    """대략적인 글자 폭 추정 (한글·전각 = 1em, 그 외 = 0.56em)."""
    w = 0.0
    for ch in s:
        w += size * (1.0 if unicodedata.east_asian_width(ch) in "WF" else 0.56)
    return w


def wrap(s: str, size: float, max_w: float) -> list[str]:
    lines, cur = [], ""
    for word in s.split(" "):
        trial = f"{cur} {word}".strip()
        if text_width(trial, size) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def data_uri(path: Path) -> str:
    mime = "image/jpeg" if path.suffix in (".jpg", ".jpeg") else "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"



# ---------------------------------------------------------------- left panel

LOGOTYPE = {
    "DO": [
        "██████╗  ██████╗ ",
        "██╔══██╗██╔═══██╗",
        "██║  ██║██║   ██║",
        "██║  ██║██║   ██║",
        "██████╔╝╚██████╔╝",
        "╚═════╝  ╚═════╝ ",
    ],
    "YOUNG": [
        "██╗   ██╗ ██████╗ ██╗   ██╗███╗   ██╗ ██████╗ ",
        "╚██╗ ██╔╝██╔═══██╗██║   ██║████╗  ██║██╔════╝ ",
        " ╚████╔╝ ██║   ██║██║   ██║██╔██╗ ██║██║  ███╗",
        "  ╚██╔╝  ██║   ██║██║   ██║██║╚██╗██║██║   ██║",
        "   ██║   ╚██████╔╝╚██████╔╝██║ ╚████║╚██████╔╝",
        "   ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ",
    ],
}
HEAT = {
    "dark": ["#161b22", "#0e2a5c", "#1d4ed8", "#3b82f6", "#93c5fd"],
    "light": ["#ebeef2", "#bfdbfe", "#60a5fa", "#2563eb", "#1e3a8a"],
}


def heatmap(t: dict, theme: str, stats: dict, x0: int, y0: int, weeks: int = 26) -> list[str]:
    cal = stats.get("calendar", [])[-weeks * 7:]
    if not cal:
        return []
    cell, gap = 11, 3
    first = dt.date.fromisoformat(cal[0][0])
    pad = (first.weekday() + 1) % 7  # 일요일 시작
    out, month_seen = [], set()
    for i, (day, level) in enumerate(cal):
        k = i + pad
        col, row = k // 7, k % 7
        x, y = x0 + col * (cell + gap), y0 + 16 + row * (cell + gap)
        out.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" fill="{HEAT[theme][int(level)]}"/>')
        d = dt.date.fromisoformat(day)
        if d.day <= 7 and row == 0 and d.month not in month_seen and col < weeks - 1:
            month_seen.add(d.month)
            out.append(f'<text x="{x}" y="{y0 + 8}" font-size="10" fill="{t["muted"]}">{d.month}월</text>')
    return out


def left_panel(t: dict, stats: dict) -> list[str]:
    theme = "dark" if t is THEMES["dark"] else "light"
    out: list[str] = []
    # logo: 이름 로고타입(픽셀 블록) + 최근 26주 기여 잔디
    cw, ch = 6.2, 9.5
    y = 92.0
    shadow = "#0e2a5c" if theme == "dark" else "#bfdbfe"
    for word in ("DO", "YOUNG"):
        for r, line in enumerate(LOGOTYPE[word]):
            for c, char in enumerate(line):
                if char == "█":
                    x = 34 + c * cw
                    out.append(f'<rect x="{x + 2:.1f}" y="{y + r * ch + 2:.1f}" width="{cw:.1f}" height="{ch:.1f}" fill="{shadow}"/>')
        for r, line in enumerate(LOGOTYPE[word]):
            for c, char in enumerate(line):
                if char == "█":
                    x = 34 + c * cw
                    out.append(f'<rect x="{x:.1f}" y="{y + r * ch:.1f}" width="{cw + 0.3:.1f}" height="{ch + 0.3:.1f}" fill="{t["ascii"]}"/>')
        y += 6 * ch + 12
    y = int(y)
    out.append(f'<text x="34" y="{y + 18}" font-family="{SANS}" font-size="15" fill="{t["muted"]}">'
               f'<tspan fill="{t["title"]}" font-weight="700">김도영</tspan>  ·  Frontend Engineer · from build to launch</text>')
    hy = y + 60
    out.append(f'<text x="34" y="{hy}" font-size="12" fill="{t["accent"]}" font-weight="700">$ git log --since="6 months"</text>')
    out += heatmap(t, theme, stats, 34, hy + 14)
    total = stats.get("contributions", 0)
    out.append(f'<text x="34" y="{hy + 14 + 16 + 7 * 14 + 18}" font-size="11" fill="{t["muted"]}">'
               f'{total:,} contributions in the last year</text>')
    return out

# ---------------------------------------------------------------- terminal card
def terminal_card(theme: str, stats: dict) -> str:
    t = THEMES[theme]
    fs, lh = 14, 20  # 정보 영역 글자 크기 · 줄 간격
    x_info, key_w = 420, 14  # 정보 시작 x, key 열 폭(문자 수)

    def kv(key: str, value: str) -> tuple:
        return ("kv", key, value)

    def head(label: str) -> tuple:
        return ("head", label)

    contrib = f"{stats.get('contributions', 0):,}"
    rows = [
        ("title", f"{USER}@github"),
        ("rule",),
        kv("Role", "Frontend Engineer · 풀스택 지향"),
        kv("Now", "TIME Korea · Frontend Intern"),
        kv("Prev", "Slunch Factory · Frontend (2026.05–10)"),
        kv("Research", "인천대 글로벌 앱센터 · LLM / RAG"),
        kv("Education", "인천대학교 컴퓨터공학부 (2029.02)"),
        kv("Shipped", "VeggieVerse · 광클스탑"),
        ("cont", "CartrAIder · Unibloom"),
        ("blank",),
        head("Stack"),
        kv("Frontend", "React, Next.js, TypeScript, Tailwind"),
        kv("Mobile", "React Native, Expo"),
        kv("Backend", "Spring Boot, Python"),
        kv("Quality", "Playwright, Vitest, Lighthouse CI"),
        ("blank",),
        head("Contact"),
        kv("Email", "from.dozero@gmail.com"),
        kv("Blog", "velog.io/@kdy9883"),
        kv("Portfolio", "doyoungkim-portfolio.vercel.app"),
        ("blank",),
        head("GitHub Stats"),
        ("stats", [("Repos", stats.get("repos", 0)), ("Stars", stats.get("stars", 0)), ("Followers", stats.get("followers", 0))]),
        ("stats", [("Contributions (1y)", contrib)]),
    ]

    height = 40 + len(rows) * lh + 30
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="900" height="{height}" '
        f'viewBox="0 0 900 {height}" font-family="{MONO}" font-size="{fs}" role="img" aria-label="{USER} profile card">',
        f'<rect x="0.5" y="0.5" width="899" height="{height - 1}" rx="12" fill="{t["bg"]}" stroke="{t["border"]}"/>',
    ]
    out += left_panel(t, stats)
    out.append(f'<text x="{x_info}" y="40" fill="{t["text"]}" xml:space="preserve">')
    for i, row in enumerate(rows):
        y = 40 + i * lh
        kind = row[0]
        if kind == "title":
            out.append(f'<tspan x="{x_info}" y="{y}" fill="{t["accent"]}" font-weight="700">{esc(row[1])}</tspan>')
        elif kind == "rule":
            out.append(f'<tspan x="{x_info}" y="{y}" fill="{t["dots"]}">{"—" * 28}</tspan>')
        elif kind == "head":
            label = f"- {row[1]} "
            out.append(f'<tspan x="{x_info}" y="{y}" fill="{t["accent"]}" font-weight="700">{esc(label)}</tspan>'
                       f'<tspan fill="{t["dots"]}">{"—" * max(2, 26 - len(label) // 2)}</tspan>')
        elif kind == "kv":
            _, key, value = row
            dots = "." * (key_w - len(key) - 2)
            out.append(f'<tspan x="{x_info}" y="{y}" fill="{t["key"]}">{esc(key)}</tspan>'
                       f'<tspan fill="{t["dots"]}"> {dots} </tspan>'
                       f'<tspan fill="{t["text"]}">{esc(value)}</tspan>')
        elif kind == "cont":
            out.append(f'<tspan x="{x_info}" y="{y}" fill="{t["text"]}">{" " * key_w}{esc(row[1])}</tspan>')
        elif kind == "stats":
            parts = []
            for j, (k, v) in enumerate(row[1]):
                if j:
                    parts.append(f'<tspan fill="{t["dots"]}"> | </tspan>')
                parts.append(f'<tspan fill="{t["key"]}">{esc(k)}</tspan><tspan fill="{t["dots"]}">: </tspan>'
                             f'<tspan fill="{t["text"]}" font-weight="700">{esc(v)}</tspan>')
            out.append(f'<tspan x="{x_info}" y="{y}">' + "".join(parts) + "</tspan>")
    out.append("</text>")
    out.append(f'<text x="870" y="{height - 16}" text-anchor="end" font-size="11" fill="{t["muted"]}">'
               f'updated {esc(stats.get("updated", ""))} KST</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- project cards
PROJECTS = [
    {
        "id": "veggieverse", "logo": "slunch.png", "name": "VeggieVerse",
        "org": "Slunch Factory", "meta": "2026.05 – 10 · Frontend 전담",
        "desc": "비건 식단 구독 자사몰 B2C 커머스를 초기 구축부터 1차 런칭·운영까지 프론트엔드 혼자 맡았어요.",
        "chips": ["커밋 620+", "PR 245", "결제 끊김 8케이스 방어"],
        "tech": "Next.js · TypeScript · Toss Payments · Playwright",
    },
    {
        "id": "timekorea", "logo": "timekorea.png", "name": "TIME Korea",
        "org": "korea.time.com", "meta": "2026.09 – 현재 · Frontend Intern",
        "desc": "글로벌 미디어 TIME의 한국 뉴스 플랫폼. 성능·SEO, CI 자동화, 본사 서체·시안 정합을 맡고 있어요.",
        "chips": ["실사용자 LCP 1.4s", "SEO 92 → 100", "PR 56"],
        "tech": "Next.js · Vercel · GitHub Actions · Lighthouse CI",
    },
    {
        "id": "gcstop", "logo": "gcstop.jpg", "name": "광클스탑",
        "org": "gcstop.co.kr", "meta": "2026.10 – 현재 · Frontend",
        "desc": "전국 대학 실제 화면을 재현한 수강신청 연습 서비스. 정각 타이밍 연습과 실시간 선착순 배틀까지.",
        "chips": ["26개 대학 UI", "실시간 배틀", "서버시간 측정"],
        "tech": "React 19 · TanStack Query · Tailwind · SSE",
    },
    {
        "id": "cartraider", "logo": "cartraider.png", "name": "CartrAIder",
        "org": "카트라이더 · 창의공학설계", "meta": "2026 · Frontend 전담",
        "desc": "기존 카트에 붙이고 스마트폰을 화면으로 쓰는 스마트 AI 카트. 고객·관리자 앱을 혼자 만들었어요.",
        "chips": ["🏆 인기상", "화면 23개", "이미지 68MB → 1.4MB"],
        "tech": "React Native · Expo · TypeScript · SSE",
    },
    {
        "id": "unibloom", "logo": "unibloom.png", "name": "Unibloom",
        "org": "SoftBank Hackathon 2026", "meta": "2026.10 · 팀장 · Web",
        "desc": "AI가 Terraform을 만들고 검증해 같은 앱을 온프레미스·AWS·Azure·GCP에 동시에 배포해요.",
        "chips": ["6인 팀장", "클라우드 4곳", "6일 PR 100+"],
        "tech": "React 19 · TypeScript · SSE · Terraform",
    },
]


def project_card(p: dict, theme: str) -> str:
    t = THEMES[theme]
    W, H = 440, 220
    logo = data_uri(ASSETS / "logos" / p["logo"])
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="{SANS}" role="img" aria-label="{esc(p["name"])}">',
        '<defs><clipPath id="lc"><rect x="22" y="22" width="52" height="52" rx="12"/></clipPath></defs>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>',
        f'<rect x="22" y="22" width="52" height="52" rx="12" fill="#ffffff"/>',
        f'<image x="22" y="22" width="52" height="52" clip-path="url(#lc)" href="{logo}" xlink:href="{logo}" preserveAspectRatio="xMidYMid slice"/>',
        f'<rect x="22" y="22" width="52" height="52" rx="12" fill="none" stroke="{t["border"]}"/>',
        f'<text x="90" y="44" font-size="19" font-weight="700" fill="{t["title"]}">{esc(p["name"])}</text>',
        f'<text x="90" y="66" font-size="12.5" fill="{t["muted"]}">{esc(p["org"])}  ·  {esc(p["meta"])}</text>',
    ]
    y = 102
    for line in wrap(p["desc"], 13.5, W - 44)[:2]:
        out.append(f'<text x="22" y="{y}" font-size="13.5" fill="{t["text"]}">{esc(line)}</text>')
        y += 21
    # chips
    x, cy = 22, 150
    for c in p["chips"]:
        w = text_width(c, 12) + 20
        out.append(f'<rect x="{x}" y="{cy}" width="{w:.0f}" height="24" rx="12" fill="{t["chip_bg"]}"/>')
        out.append(f'<text x="{x + w / 2:.0f}" y="{cy + 16.5}" font-size="12" font-weight="600" text-anchor="middle" fill="{t["chip_text"]}">{esc(c)}</text>')
        x += w + 8
    out.append(f'<text x="22" y="200" font-size="12" font-family="{MONO}" fill="{t["muted"]}">{esc(p["tech"])}</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> None:
    stats = fetch_stats()
    (ASSETS / "cards").mkdir(exist_ok=True)
    for theme in THEMES:
        (ASSETS / f"terminal-{theme}.svg").write_text(terminal_card(theme, stats))
        for p in PROJECTS:
            (ASSETS / "cards" / f"{p['id']}-{theme}.svg").write_text(project_card(p, theme))
    print("stats:", stats)


if __name__ == "__main__":
    main()
