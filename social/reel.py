#!/usr/bin/env python3
"""Rend une présentation HTML (moteur motion-deck) en MP4 + GIF pour les réseaux sociaux.

Rendu déterministe : chaque image fige toutes les animations CSS/Web Animations
au temps t via document.getAnimations(), puis capture l'écran.

Usage :
  python3 reel.py deck.html --storyboard story.json --format square --out reel
Formats : landscape 1920x1080 · square 1080x1080 · portrait 1080x1350 · story 1080x1920
"""
import argparse, base64, json, os, re, shutil, subprocess, sys, tempfile, glob
from playwright.sync_api import sync_playwright

FORMATS = {"landscape": (1920, 1080), "square": (1080, 1080), "portrait": (1080, 1350), "story": (1080, 1920)}

def font_css(fonts_dir):
    """@font-face en data URI depuis des fichiers @fontsource (<famille>-latin-<poids>-normal.woff2)."""
    if not fonts_dir:
        return ""
    css = []
    for f in sorted(glob.glob(os.path.join(fonts_dir, "**", "*-latin-*-normal.woff2"), recursive=True)):
        m = re.match(r"(.+)-latin-(\d+)-normal\.woff2$", os.path.basename(f))
        if not m:
            continue
        fam = " ".join(w.capitalize() if w not in ("ibm",) else "IBM" for w in m.group(1).split("-"))
        b64 = base64.b64encode(open(f, "rb").read()).decode()
        css.append(f"@font-face{{font-family:'{fam}';font-weight:{m.group(2)};font-style:normal;"
                   f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "\n".join(css)

def build_page(html, W, H, fonts, top, bottom):
    html = re.sub(r'<link[^>]+fonts\.(googleapis|gstatic)\.com[^>]*>', "", html)
    landscape = (W / H) > 1.5
    band_top = 0 if landscape else int((H - W * 9 / 16) * (0.42 if bottom else 0.5))
    stage_h = H if landscape else int(W * 9 / 16)
    override = f"""<meta charset="utf-8">
<style>
{fonts}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#16130F}}
.viewport{{inset:auto!important;left:0!important;top:{band_top}px!important;width:{W}px!important;height:{stage_h}px!important;padding:0!important}}
.controls,.notes{{display:none!important}}
.reelcap{{position:fixed;left:64px;right:64px;color:#F9F9F9;font-family:Epilogue,Arial,sans-serif;z-index:99}}
.reelcap.top{{top:0;height:{band_top}px;display:flex;flex-direction:column;justify-content:center;gap:14px}}
.reelcap.bot{{bottom:0;height:{H - band_top - stage_h}px;display:flex;align-items:center;justify-content:space-between;gap:24px}}
.reelcap .k{{font:500 22px/1 'IBM Plex Mono',monospace;letter-spacing:.18em;text-transform:uppercase;color:#FFB95C}}
.reelcap .h{{font:900 54px/1.02 Epilogue,Arial,sans-serif;letter-spacing:-.02em}}
.reelcap .b{{font:500 26px/1.3 'IBM Plex Mono',monospace;color:#ABA398}}
.reelcap .dot{{width:14px;height:14px;border-radius:50%;background:#FFB95C;box-shadow:0 0 18px #FFB95C;flex:none}}
</style>"""
    caps = ""
    if not landscape:
        if top:
            k, _, h = top.partition("|")
            caps += f'<div class="reelcap top"><div class="k">{k}</div><div class="h">{h}</div></div>'
        if bottom:
            caps += f'<div class="reelcap bot"><div class="b">{bottom}</div><div class="dot"></div></div>'
    return override + html + caps

SEEK_JS = """(t)=>{document.getAnimations().forEach(a=>{try{a.pause();a.currentTime=t}catch(e){}});return document.getAnimations().length}"""
SHOW_JS = """([i,fragGap])=>{
  const s=[...document.querySelectorAll('.slide')];
  s.forEach(x=>{x.classList.remove('on');x.style.transition='none'});
  const cur=s[i]; cur.style.transition=''; void cur.offsetWidth; cur.classList.add('on');
  cur.querySelectorAll('.f').forEach((f,j)=>{f.style.transitionDelay=(0.9+j*fragGap)+'s';f.classList.add('shown')});
  const p=document.getElementById('progress'); if(p) p.style.width=(i/(s.length-1)*100)+'%';
  return s.length}"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--storyboard", help='JSON : [{"slide":1,"seconds":8}, ...] (numérotation à partir de 1)')
    ap.add_argument("--format", default="square", choices=FORMATS)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--fonts", help="dossier contenant les woff2 @fontsource")
    ap.add_argument("--top", default="", help='bandeau haut "SURTITRE|Titre" (formats non paysage)')
    ap.add_argument("--bottom", default="", help="bandeau bas (formats non paysage)")
    ap.add_argument("--frag-gap", type=float, default=1.1, help="secondes entre deux fragments révélés")
    ap.add_argument("--gif-width", type=int, default=540)
    ap.add_argument("--gif-seconds", type=float, default=12, help="durée max du GIF (début de la vidéo)")
    ap.add_argument("--gif-fps", type=int, default=12)
    ap.add_argument("--out", default="reel")
    a = ap.parse_args()

    W, H = FORMATS[a.format]
    story = json.load(open(a.storyboard)) if a.storyboard else [{"slide": 1, "seconds": 8}]
    page_html = build_page(open(a.html, encoding="utf-8").read(), W, H, font_css(a.fonts), a.top, a.bottom)
    work = tempfile.mkdtemp(prefix="frames-")
    src = os.path.join(work, "page.html"); open(src, "w", encoding="utf-8").write(page_html)

    n = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.goto("file://" + src); pg.wait_for_timeout(600)
        pg.evaluate("document.fonts.ready.then(()=>1)")
        pg.evaluate("window.dispatchEvent(new Event('resize'))")
        for seg in story:
            pg.evaluate(SHOW_JS, [seg["slide"] - 1, a.frag_gap])
            frames = int(round(seg["seconds"] * a.fps))
            start_ms = seg.get("start", 0) * 1000
            for k in range(frames):
                pg.evaluate(SEEK_JS, start_ms + k * 1000 / a.fps)
                pg.screenshot(path=os.path.join(work, f"f_{n:05d}.jpg"), type="jpeg", quality=92)
                n += 1
            print(f"slide {seg['slide']} : {frames} images", flush=True)
        b.close()

    mp4, gif = a.out + ".mp4", a.out + ".gif"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(a.fps), "-i", os.path.join(work, "f_%05d.jpg"),
                    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", mp4], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-t", str(a.gif_seconds), "-i", mp4, "-vf",
                    f"fps={a.gif_fps},scale={a.gif_width}:-1:flags=lanczos,split[x][y];[x]palettegen=max_colors=128:stats_mode=diff[p];[y][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle",
                    "-loop", "0", gif], check=True)
    shutil.rmtree(work, ignore_errors=True)
    for f in (mp4, gif):
        print(f"{f} : {os.path.getsize(f)/1e6:.1f} Mo")

if __name__ == "__main__":
    main()
