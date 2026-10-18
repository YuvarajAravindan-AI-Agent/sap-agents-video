"""Driver: timeline from narration durations, per-scene frames, preview + render."""
import json, os, sys, subprocess, shutil, wave
from PIL import Image
from lib import *
import content
import scenes_a
try: import scenes_b
except ImportError: scenes_b = None

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = json.load(open(os.path.join(HERE, "durations.json")))
LEAD, TAIL, TRANS = 0.35, 0.7, 0.5

BUILD = {"banner": scenes_a.build_banner, "problem": scenes_a.build_problem, "workflow": scenes_a.build_workflow,
         "live": scenes_a.build_live, "architecture": scenes_a.build_arch}
if scenes_b: BUILD.update(scenes_b.BUILD)

def timeline(sc):
    sp = [s[1] for s in sc["sentences"]]; tot = sum(len(x) for x in sp); a = DUR[sc["id"]]; cum = 0; st = []
    for x in sp: st.append(LEAD + a * cum / tot); cum += len(x)
    return LEAD + a + TAIL, st, [s[0] for s in sc["sentences"]]

_cache = {}
def scene(i):
    if i not in _cache:
        sc = content.SCENES[i]; T, st, sents = timeline(sc); _cache[i] = (BUILD[sc["id"]](T, st, sents), T, st)
    return _cache[i]

def frame_at(i, t):
    draw, T, st = scene(i); f = Image.new("RGB", (W, H), WHITE); draw(f, min(t, T)); return f

def full_frame(i, t):
    """Frame with slide-in transition over the previous scene's last frame."""
    cur = frame_at(i, t)
    if i == 0 or t >= TRANS: return cur if i else _fade_in(cur, t)
    prev = frame_at(i - 1, scene(i - 1)[1]); e = ease_io(t / TRANS); out = Image.new("RGB", (W, H))
    out.paste(prev, (-int(e * W * 0.22), 0)); out.paste(cur, (int((1 - e) * W), 0))
    return out

def _fade_in(cur, t):
    if t >= 0.5: return cur
    return Image.blend(Image.new("RGB", (W, H), WHITE), cur, ease_out(t / 0.5))

def preview(i, times, out):
    os.makedirs(out, exist_ok=True)
    for t in times: full_frame(i, t).save(f"{out}/s{i:02d}_{t:05.1f}.png")

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        i = int(sys.argv[2]); T = scene(i)[1]; ts = [float(x) for x in sys.argv[3:]] or [T * f for f in (0.15, 0.4, 0.7, 0.98)]
        preview(i, ts, os.path.join(HERE, "preview")); print("scene", i, content.SCENES[i]["id"], "T=%.1f" % T)
