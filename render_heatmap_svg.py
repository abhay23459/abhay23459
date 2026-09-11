#!/usr/bin/env python3
import json, math
from datetime import datetime, timedelta

DATA="data/contributions.json"
OUT="contrib-heatmap.svg"
PAL=["#161b22","#0e4429","#006d32","#26a641","#39d353"]
with open(DATA,encoding="utf-8") as f: data=json.load(f)

days={d["date"]:d for d in data.get("days",[])}
if days:
    dates=sorted(days)
    end=datetime.strptime(dates[-1],"%Y-%m-%d").date()
else:
    end=datetime.utcnow().date()
# Align to Saturday, then take 53 weeks
end=end + timedelta(days=(5-end.weekday())%7)
start=end-timedelta(days=7*53-1)
start=start-timedelta(days=(start.weekday())%7)

cell=13; gap=3; left=40; top=44
width=left+53*(cell+gap)+20
height=top+7*(cell+gap)+58

svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
svg += [f'<rect width="100%" height="100%" rx="14" fill="#0d1117" stroke="#30363d"/>',
        '<style>@keyframes pop{from{opacity:0;transform:translateY(-5px)}to{opacity:1;transform:translateY(0)}}.day{animation:pop .45s ease-out both}</style>']
svg.append('<text x="20" y="27" fill="#c9d1d9" font-family="monospace" font-size="14">GitHub contributions • last year</text>')
for i,wd in enumerate(["Mon","Wed","Fri"]):
    y=top+(i*2+0.8)*(cell+gap)
    svg.append(f'<text x="6" y="{y:.1f}" fill="#8b949e" font-family="monospace" font-size="10">{wd}</text>')

colors=PAL
for i in range(53):
    for j in range(7):
        d=start+timedelta(days=i*7+j)
        if d>end: continue
        key=d.isoformat()
        n=days.get(key,{}).get("count",0)
        level=days.get(key,{}).get("level",0)
        x=left+i*(cell+gap); y=top+j*(cell+gap)
        delay=(i+j)*0.012
        svg.append(f'<rect class="day" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{colors[min(level,4)]}" style="animation-delay:{delay:.3f}s"><title>{key}: {n} contribution{"s" if n!=1 else ""}</title></rect>')

# legend and footer
lx=left+250
for k,c in enumerate(colors):
    svg.append(f'<rect x="{lx+k*18}" y="{height-31}" width="12" height="12" rx="3" fill="{c}"/>')
svg.append(f'<text x="{left+185}" y="{height-21}" fill="#8b949e" font-family="monospace" font-size="10">Less</text>')
svg.append(f'<text x="{lx+len(colors)*18+4}" y="{height-21}" fill="#8b949e" font-family="monospace" font-size="10">More</text>')
svg.append(f'<text x="20" y="{height-21}" fill="#39d353" font-family="monospace" font-size="11">{data.get("total_last_year",0):,} contributions in the last year</text>')
svg.append('</svg>')
open(OUT,'w',encoding="utf-8").write("\n".join(svg))
print(f"Wrote {OUT}")
