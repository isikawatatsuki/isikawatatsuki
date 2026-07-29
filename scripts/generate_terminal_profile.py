import base64
import json
import math
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
USERNAME = "isikawatatsuki"


def gh(*args):
    result = subprocess.run(
        ["gh", "api", *args], check=True, capture_output=True, text=True, encoding="utf-8"
    )
    return json.loads(result.stdout)


query = """
query($login:String!) {
  user(login:$login) {
    followers { totalCount }
    following { totalCount }
    repositories(first:100, ownerAffiliations:OWNER, privacy:PUBLIC) {
      totalCount
      nodes { stargazerCount forkCount languages(first:10) { edges { size node { name color } } } }
    }
    contributionsCollection {
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount weekday } }
      }
    }
  }
}
"""

data = gh("graphql", "-F", f"login={USERNAME}", "-f", f"query={query}")["data"]["user"]
repos = data["repositories"]
contrib = data["contributionsCollection"]
calendar = contrib["contributionCalendar"]

stars = sum(repo["stargazerCount"] for repo in repos["nodes"])
forks = sum(repo["forkCount"] for repo in repos["nodes"])
languages = Counter()
colors = {}
for repo in repos["nodes"]:
    for edge in repo["languages"]["edges"]:
        name = edge["node"]["name"]
        languages[name] += edge["size"]
        colors[name] = edge["node"].get("color") or "#67e8f9"

avatar_bytes = (ROOT / "assets" / "avatar-terminal.png").read_bytes()
avatar_uri = "data:image/png;base64," + base64.b64encode(avatar_bytes).decode()


def text(x, y, value, size=18, fill="#f8e7c4", weight="400", anchor="start"):
    escaped = str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{escaped}</text>'


parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1536" height="1024" viewBox="0 0 1536 1024" style="font-family:Ubuntu Mono,DejaVu Sans Mono,monospace">',
    "<defs>",
    '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#180016"/><stop offset="0.55" stop-color="#2c001e"/><stop offset="1" stop-color="#12000f"/></linearGradient>',
    '<filter id="glow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
    "</defs>",
    '<rect width="1536" height="1024" fill="#0d1117"/>',
    '<rect x="52" y="32" width="1432" height="952" rx="16" fill="url(#bg)" stroke="#4b5563" stroke-width="2"/>',
    '<rect x="52" y="32" width="1432" height="52" rx="16" fill="#27272a"/>',
    '<rect x="52" y="68" width="1432" height="16" fill="#27272a"/>',
    '<circle cx="82" cy="58" r="9" fill="#ff5f57"/><circle cx="112" cy="58" r="9" fill="#febc2e"/><circle cx="142" cy="58" r="9" fill="#28c840"/>',
    text(768, 66, "tatsuki@github: ~", 18, "#f8e7c4", "600", "middle"),
    text(78, 119, "tatsuki@github:~$ whoami", 20, "#e95420", "600"),
    text(78, 150, "tatsuki_ishikawa", 20),
    text(78, 184, "tatsuki@github:~$ neofetch", 20, "#e95420", "600"),
    f'<image x="98" y="205" width="350" height="326" href="{avatar_uri}" xlink:href="{avatar_uri}" preserveAspectRatio="xMidYMid meet"/>',
    text(535, 226, "tatsuki@github", 23, "#e95420", "700"),
    text(535, 252, "----------------", 18, "#e95420"),
]

info = [
    ("OS", "Ubuntu GitHub Edition x86_64"),
    ("Host", "Developer Workstation"),
    ("Kernel", "Web Developer"),
    ("Location", "Osaka, Japan"),
    ("Shell", "zsh 5.9"),
    ("Focus", "Web Apps / AI / Automation"),
    ("Status", "Always learning, always shipping"),
]
for index, (label, value) in enumerate(info):
    y = 286 + index * 34
    parts += [text(535, y, f"{label}:", 18, "#e95420", "700"), text(665, y, value, 18)]

parts += [
    '<rect x="1010" y="250" width="390" height="258" rx="4" fill="#210018" stroke="#e95420" stroke-width="2"/>',
    text(1040, 296, "Web Developer · Osaka, Japan", 21, "#f8e7c4", "600"),
    text(1040, 330, "--------------------------------", 16, "#e95420"),
    text(1040, 378, ">  Building practical web apps", 18),
    text(1040, 420, ">  Automating development workflows", 18),
    text(1040, 462, ">  Learning, improving, shipping", 18),
    text(78, 560, "tatsuki@github:~$ ls ~/skills", 20, "#e95420", "600"),
    text(78, 593, "PHP   Laravel   TypeScript   Vue   Go   MySQL   Docker   Git", 19, "#67e8f9", "600"),
    text(78, 632, "tatsuki@github:~$ ./show-activity.sh", 20, "#e95420", "600"),
]

cards = [(72, 662, 270, 270), (362, 662, 430, 270), (812, 662, 620, 270)]
for x, y, w, h in cards:
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#210018" stroke="#e95420" stroke-width="2"/>')

parts += [
    text(94, 700, "SYSTEM ONLINE", 20, "#67e8f9", "700"),
    text(94, 726, "-------------", 16, "#67e8f9"),
]
stats = [
    ("Repos", repos["totalCount"]), ("Commits", contrib["totalCommitContributions"]),
    ("Pull requests", contrib["totalPullRequestContributions"]), ("Issues", contrib["totalIssueContributions"]),
    ("Reviews", contrib["totalPullRequestReviewContributions"]), ("Followers", data["followers"]["totalCount"]),
]
for i, (label, value) in enumerate(stats):
    y = 760 + i * 27
    parts += [text(94, y, label, 17), text(318, y, value, 17, "#f8e7c4", "400", "end")]

parts += [text(385, 700, "LANGUAGES", 20, "#67e8f9", "700"), text(385, 726, "---------", 16, "#67e8f9")]
top_languages = languages.most_common(5)
largest = top_languages[0][1] if top_languages else 1
for i, (name, size) in enumerate(top_languages):
    y = 764 + i * 34
    width = 250 * size / largest
    parts += [text(385, y, name, 16), f'<rect x="520" y="{y-14}" width="{width:.1f}" height="15" fill="{colors[name]}" opacity="0.9"/>']
parts += [text(385, 925, f"stars {stars}    forks {forks}    contributions {calendar['totalContributions']}", 16, "#f8e7c4", "600")]

parts += [text(836, 700, "CONTRIBUTIONS IN THE LAST YEAR", 20, "#67e8f9", "700"), text(836, 726, "------------------------------", 16, "#67e8f9")]
weeks = calendar["weeks"][-52:]
palette = ["#351427", "#6b2635", "#a83b32", "#e95420", "#ff8a3d"]
maximum = max((day["contributionCount"] for week in weeks for day in week["contributionDays"]), default=1)
for wx, week in enumerate(weeks):
    by_day = {day["weekday"]: day["contributionCount"] for day in week["contributionDays"]}
    for weekday in range(7):
        count = by_day.get(weekday, 0)
        level = 0 if count == 0 else min(4, 1 + math.floor(3 * count / maximum))
        x = 838 + wx * 10.7
        y = 748 + weekday * 22
        parts.append(f'<rect x="{x:.1f}" y="{y}" width="8.5" height="16" rx="1" fill="{palette[level]}"/>')
parts += [
    text(836, 920, "May   Jun   Jul   Aug   Sep   Oct   Nov   Dec   Jan   Feb   Mar   Apr", 14, "#f8e7c4"),
    text(1450, 960, "[ SYSTEM READY ]", 16, "#67e8f9", "600", "end"),
    "</svg>",
]

(ROOT / "assets" / "ubuntu-terminal-profile.svg").write_text("".join(parts), encoding="utf-8")
