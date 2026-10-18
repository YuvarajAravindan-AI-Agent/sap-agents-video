"""Scenes 1-5: banner, problem, workflow, live app, architecture."""
import math
from functools import lru_cache
from PIL import Image
from lib import *

# ---------------------------------------------------------------- shared chrome ----
NAV = ["Problem", "Idea", "Live", "Architecture", "Built live", "Verified", "Sequence", "Failures", "Evidence", "Difference", "Limits", "About"]

@lru_cache(None)
def bg_base():
    col = Image.new("RGB", (1, H))
    for y in range(H): col.putpixel((0, y), mix((246, 249, 253), (236, 243, 252), y / H))
    return col.resize((W, H))

@lru_cache(None)
def shell(nav_label):
    img = bg_base().copy()
    bar = Image.new("RGB", (W, 1))
    for x in range(W): bar.putpixel((x, 0), mix(HBLUE, (0, 150, 250), x / W))
    img.paste(bar.resize((W, 78)), (0, 0))
    ov = SS(W, 90)
    ov.rr((30, 17, 30 + tw("SAP", 30, True) + 30, 61), 12, fill=WHITE); ov.text((45, 39), "SAP", 30, BLUE, bold=True, anchor="lm")
    x0 = 30 + tw("SAP", 30, True) + 30 + 12; wa = tw("Agents", 30, True) + 30
    ov.rr((x0, 17, x0 + wa, 61), 12, fill=GOLD); ov.text((x0 + 15, 39), "Agents", 30, INK, bold=True, anchor="lm")
    ov.text((x0 + wa + 22, 40), "governed by design", 22, (255, 255, 255, 230), anchor="lm")
    widths = [tw(n, 19, True) + 30 for n in NAV]; x = W - 28 - sum(widths) - 6 * (len(NAV) - 1) // 1
    x = W - 24 - (sum(widths) + 6 * (len(NAV) - 1))
    for n, wd in zip(NAV, widths):
        if n == nav_label: ov.rr((x, 22, x + wd, 58), 18, fill=WHITE); ov.text((x + wd / 2, 40), n, 19, BLUE, bold=True, anchor="mm")
        else: ov.text((x + wd / 2, 40), n, 19, (255, 255, 255, 215), bold=False, anchor="mm")
        x += wd + 6
    img.paste(ov.done(), (0, 0), ov.done())
    return img

@lru_cache(None)
def cap_layer(text):
    lines = wrap(text, 31, 1480); h = 24 + len(lines) * 42 + 8
    c = card(190, 1046 - h, 1540, h, accent=BLUE, r=16); s = SS(1540, h)
    for i, l in enumerate(lines): s.text((38, 18 + i * 42), l, 31, TEXT)
    c.im.alpha_composite(s.done(), (26, 26)); return c

def draw_caption(frame, t, st, sentences):
    k = -1
    for j, s in enumerate(st):
        if t >= s - 0.05: k = j
    if k < 0: return
    a = prog(t, st[k] - 0.05, 0.25); blit(frame, cap_layer(sentences[k]), a=a, dy=int((1 - a) * 10))

def pop(frame, lay, t, t0, dur=0.5):
    p = prog(t, t0, dur)
    if p <= 0: return
    e = ease_out(p); sc = 0.88 + 0.12 * e
    im = lay.im.resize((max(1, int(lay.w * sc)), max(1, int(lay.h * sc))), Image.LANCZOS); m = im.getchannel("A").point(lambda v: int(v * e))
    frame.paste(im, (lay.x + (lay.w - im.width) // 2, lay.y + (lay.h - im.height) // 2), m)

def title(text, sub=None):
    ls = [text_layer(80, 108, text, 46, INK, bold=True)]
    if sub: ls.append(text_layer(82, 166, sub, 26, MUTE))
    return ls

def icon(kind, size=84, bg=BLUE):
    s = SS(size, size); s.ellipse((0, 0, size, size), fill=bg); c = size / 2; w = (255, 255, 255, 255)
    if kind == "db":
        for k in range(3):
            y = size * (0.30 + k * 0.17); s.ellipse((size * 0.27, y - size * 0.07, size * 0.73, y + size * 0.07), fill=w)
        s.rect((size * 0.27, size * 0.30, size * 0.73, size * 0.64), fill=w)
        for k in range(3): s.ellipse((size * 0.27, size * (0.30 + k * 0.17) - size * 0.07, size * 0.73, size * (0.30 + k * 0.17) + size * 0.07), outline=bg, width=2)
    elif kind == "cloud":
        s.ellipse((size * .25, size * .42, size * .50, size * .67), fill=w); s.ellipse((size * .36, size * .27, size * .64, size * .62), fill=w)
        s.ellipse((size * .50, size * .38, size * .76, size * .66), fill=w); s.rect((size * .37, size * .50, size * .64, size * .66), fill=w)
    elif kind == "shield":
        s.poly([(c, size * .22), (size * .74, size * .33), (size * .70, size * .60), (c, size * .79), (size * .30, size * .60), (size * .26, size * .33)], w)
        s.line([(size * .39, size * .50), (size * .47, size * .59), (size * .62, size * .41)], bg, 5)
    elif kind == "chat":
        s.rr((size * .24, size * .28, size * .76, size * .62), 10, fill=w); s.poly([(size * .36, size * .62), (size * .36, size * .76), (size * .50, size * .62)], w)
    elif kind == "gear":
        for a in range(0, 360, 45): x = c + math.cos(math.radians(a)) * size * .26; y = c + math.sin(math.radians(a)) * size * .26; s.ellipse((x - 6, y - 6, x + 6, y + 6), fill=w)
        s.ellipse((size * .30, size * .30, size * .70, size * .70), fill=w); s.ellipse((size * .42, size * .42, size * .58, size * .58), fill=bg)
    return s.done()


# ---------------------------------------------------------------- 1. banner ----
def build_banner(T, st, sents):
    bg = Image.new("RGB", (1, H))
    for y in range(H): bg.putpixel((0, y), mix((0, 132, 250), (0, 78, 192), y / H))
    bg = bg.resize((W, H)); ov = SS(W, H, k=1)
    ov.ellipse((1250, -330, 2150, 570), outline=(255, 255, 255, 70), width=3); ov.ellipse((1380, -200, 2020, 440), fill=(255, 255, 255, 28))
    ov.ellipse((-260, 700, 620, 1580), outline=(255, 255, 255, 60), width=3); ov.ellipse((1500, 650, 2300, 1450), fill=(255, 255, 255, 22))
    bg.paste(ov.done(), (0, 0), ov.done())
    kicker = text_layer(140, 112, "INDEPENDENT DEMO   ·   SAP BTP TRIAL   ·   GOVERNED AI", 26, (255, 255, 255, 235), bold=True)
    kb = SS(1300, 44); kb.text((2, 4), "INDEPENDENT DEMO  ·  SAP BTP TRIAL  ·  GOVERNED AI AGENTS", 25, (255, 255, 255, 235), bold=True, spacing=3); kicker = L(kb.done(), 140, 112)
    sw = int(tw("SAP", 190, True)) + 120; aw = int(tw("Agents", 190, True)) + 120; ch = 270
    def chipimg(w, fill, fg, txt):
        s = SS(w + 60, ch + 60); s.rr((30, 30, 30 + w, 30 + ch), 46, fill=fill); s.text((30 + w / 2, 30 + ch / 2 + 6), txt, 190, fg, bold=True, anchor="mm")
        im = Image.new("RGBA", s.im.size if False else (w + 60, ch + 60), (0, 0, 0, 0)); sh = Image.new("RGBA", (w + 60, ch + 60), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((30, 42, 30 + w, 42 + ch), 46, fill=(0, 30, 90, 90)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14))); im.alpha_composite(s.done()); return im
    chip_sap = L(chipimg(sw, WHITE, BLUE, "SAP"), 140 - 30, 190 - 30); chip_ag = L(chipimg(aw, GOLD, INK, "Agents"), 140 + sw + 44 - 30, 190 - 30)
    line2 = text_layer(140, 500, "that show their work.", 92, WHITE, bold=True)
    sub = text_layer(142, 636, "Governed answers from SAP data  ·  every call audited  ·  every number traceable", 38, (255, 255, 255, 240))
    tiles = []
    for i, (ic, ttl, sb) in enumerate([("db", "SAP HANA Cloud", "the data"), ("cloud", "SAP BTP", "the services"), ("shield", "Audit trail", "the evidence")]):
        x = 140 + i * 560; c = card(x, 712, 520, 170, r=22); s = SS(520, 170); s.text((120, 48), ttl, 38, INK, bold=True); s.text((120, 98), sb, 28, MUTE)
        c.im.alpha_composite(s.done(), (26, 26)); c.im.alpha_composite(icon(ic, 84), (26 + 26, 26 + 43)); tiles.append(c)
    def draw(f, t):
        f.paste(bg, (0, 0)); appear(f, kicker, t, 0.3); pop(f, chip_sap, t, 0.6, 0.6); pop(f, chip_ag, t, 1.0, 0.6)
        if t > 1.6:  # gold underline sweep under 'Agents'
            p = ease_out(prog(t, 1.7, 0.7)); x0 = 140 + sw + 44 + 10; x1 = x0 + int((aw - 20) * p)
            ImageDraw.Draw(f).rounded_rectangle((x0, 482, max(x0 + 4, x1), 492), 5, fill=GOLD)
        appear(f, line2, t, 1.6); appear(f, sub, t, 2.2)
        for i, c in enumerate(tiles): appear(f, c, t, 3.0 + i * 0.45, 0.5, rise=24)
        draw_caption(f, t, st, sents)
    draw.shell = False; return draw


# ---------------------------------------------------------------- 2. problem ----
def build_problem(T, st, sents):
    base = shell("Problem"); tl = title("The standard build: right data, wrong answer", "A Joule agent from the SAP learning journey, asked about Maintenance Order 25")
    SW = 1000; img, sc, (ox, oy) = shot("joule_answer", SW)
    left = card(80, 214, SW, img.height, r=14, pad=24); left.im.alpha_composite(img, (24, 24)); X0, Y0 = 80, 214
    def box(b, col):  # source px -> frame coords
        x0, y0, x1, y1 = b; return (X0 + x0 * sc, Y0 + y0 * sc, X0 + x1 * sc, Y0 + y1 * sc)
    gbox, rbox = box((568, 96, 772, 182), GREEN), box((572, 394, 1126, 426), RED)
    def marks(f, t):
        d = ImageDraw.Draw(f)
        for b, col, t0 in ((gbox, GREEN, st[2]), (rbox, RED, st[3])):
            p = ease_out(prog(t, t0, 0.5))
            if p > 0: x0, y0, x1, y1 = b; d.rounded_rectangle((x0 - 6, y0 - 6, x0 - 6 + (x1 - x0 + 12) * p, y1 + 6), 8, outline=col, width=5)
    cA = card(1130, 214, 710, 150, accent=GREEN, r=16); sA = SS(710, 150); sA.text((36, 18), "What the data said", 26, GREEN, bold=True); sA.text((36, 62), "Material 41", 38, INK, bold=True)
    sA.text((36, 108), "required 1.7  ·  available 500  ·  status Available", 30, TEXT, mono=False); cA.im.alpha_composite(sA.done(), (26, 26))
    cB = card(1130, 392, 710, 150, accent=RED, r=16, fill=PALERED); sB = SS(710, 150); sB.text((36, 18), "What the agent said", 26, RED, bold=True)
    sB.text((36, 62), "“Material ID 41 is short by 1.2 units.”", 33, INK, bold=True); sB.text((36, 110), "The model did the arithmetic.", 28, TEXT); cB.im.alpha_composite(sB.done(), (26, 26))
    lg, lsc, _ = shot("joule_logs", 710); cL = card(1130, 618, 710, lg.height, r=14, pad=24); cL.im.alpha_composite(lg, (24, 24))
    why = card(80, 722, 1000, 190, r=16, accent=ORANGE); sw_ = SS(1000, 190); sw_.text((36, 16), "Why this fails an audit", 27, ORANGE, bold=True)
    for j, l in enumerate(["The language model did the arithmetic", "The logs list steps, not what each tool returned", "No way to prove which number came from where"]): sw_.text((36, 62 + j * 38), "•  " + l, 26, TEXT)
    why.im.alpha_composite(sw_.done(), (26, 26))
    lab = chip(1130, 566, "Request Logs: steps listed, no tool outputs", 22, fg=BLUE, bg=PALE, outline=BLUE)
    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.2) for l in tl]; appear(f, left, t, st[0] + 0.1, 0.6); marks(f, t)
        appear(f, cA, t, st[2] + 0.2); appear(f, cB, t, st[3] + 0.2); appear(f, lab, t, st[3] + 1.8); appear(f, cL, t, st[3] + 2.0); appear(f, why, t, st[3] + 1.2)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- 3. workflow ----
STEPS = [("1", "Ask", "LLM", "User asks in plain language", "Is order 1000001 ready?"),
         ("2", "Choose a tool", "LLM", "Model picks one governed function", "validate_order_stock(1000001)"),
         ("3", "Look up", "SAP", "Service reads orders, components, stock on HANA", "SELECT … FROM HANA"),
         ("4", "Compute in code", "SAP", "Sum locations, compare, per material", "8.8 available vs 10 required"),
         ("5", "Answer", "LLM", "Model phrases what the tool returned", "Material 42 short by 1.2"),
         ("6", "Audit row", "SAP", "Tool, outcome, status, conversation id", "OK · 200 · conv-…")]
def build_workflow(T, st, sents):
    base = shell("Idea"); tl = title("One question, six steps, two responsibilities", "The model talks. The SAP service looks up, computes and records.")
    cards = []; CW, GAP, X0 = 280, 24, 60
    for i, (n, ttl, who, desc, ex) in enumerate(STEPS):
        x = X0 + i * (CW + GAP); acc = BLUE if who == "LLM" else GOLD
        c = card(x, 250, CW, 340, r=20, accent=acc); s = SS(CW, 340)
        s.ellipse((34, 24, 84, 74), fill=acc); s.text((59, 49), n, 28, WHITE if who == "LLM" else INK, bold=True, anchor="mm")
        s.text((34, 92), ttl, 27, INK, bold=True)
        for j, l in enumerate(wrap(desc, 22, CW - 56)): s.text((34, 140 + j * 30), l, 22, MUTE)
        tag = "LLM" if who == "LLM" else "SAP service"
        s.rr((34, 262, CW - 22, 308), 22, fill=PALE if who == "LLM" else PALEGOLD, outline=acc, width=2); s.text((CW / 2 + 6, 285), tag, 22, BLUE if who == "LLM" else (130, 85, 0), bold=True, anchor="mm")
        c.im.alpha_composite(s.done(), (26, 26)); cards.append(c)
    exs = []; EXL = [["Is order 1000001", "ready?"], ["validate_order_stock", "(1000001)"], ["SELECT order,", "components, stock"], ["8.8 available", "vs 10 required"], ["Material 42", "short by 1.2"], ["OK · 200", "conv-e0f1c8dd…"]]
    for i, ls_ in enumerate(EXL):
        x = X0 + i * (CW + GAP); c = card(x, 636, CW, 96, r=14, fill=(250, 252, 255)); ss_ = SS(CW, 96)
        for j, l in enumerate(ls_): ss_.text((CW / 2, 14 + j * 36), l, 20, INK, mono=True, anchor="ma")
        c.im.alpha_composite(ss_.done(), (26, 26)); exs.append(c)
    leg1 = chip(80, 784, "LLM: understands the question, writes the answer. Never calculates.", 25, fg=BLUE, bg=PALE, outline=BLUE)
    leg2 = chip(80, 852, "SAP service: looks up, computes in code, records every call.", 25, fg=(120, 80, 0), bg=PALEGOLD, outline=GOLD)
    arrows = [arrow_layer([(X0 + i * (CW + GAP) + CW + 2, 420), (X0 + (i + 1) * (CW + GAP) - 2, 420)], MUTE, 4, head=11)[0] for i in range(5)]
    hi = ["", "", "", "", "", ""]
    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.2) for l in tl]
        t0 = st[1] if len(st) > 1 else 1.0
        for i in range(6):
            ti = st[0] + 0.3 + i * 0.35 if i < 2 else st[min(2, len(st) - 1)] + (i - 2) * 1.5
            appear(f, cards[i], t, ti, 0.5, rise=22); appear(f, exs[i], t, ti + 0.3)
            if i < 5: appear(f, arrows[i], t, ti + 0.5, 0.3, rise=0)
        # moving gold highlight under the active card
        act = 0 if t < st[1] else (1 if t < st[2] else (2 + min(3, int((t - st[2]) / max(0.1, (st[3] - st[2]) / 2.0)) if t < st[3] else 3)))
        if t > st[0] + 2.5:
            x = X0 + act * (CW + GAP); ImageDraw.Draw(f).rounded_rectangle((x, 600, x + CW, 610), 5, fill=GOLD)
        appear(f, leg1, t, st[1] + 0.2); appear(f, leg2, t, st[2] + 0.2)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- 4. live ----
def build_live(T, st, sents):
    base = shell("Live"); tl = title("The live agent on SAP BTP", "sap-gov-agent.cfapps.us10-001.hana.ondemand.com   ·   Cloud Foundry trial")
    crop = (615, 160, 1372, 585); CWD = 1100; img, sc, _ = shot("chat_ui", CWD, crop=crop)
    left = card(70, 214, CWD, img.height, r=14, pad=24); left.im.alpha_composite(img, (24, 24)); X0, Y0 = 70, 214
    def pt(x, y): return (X0 + (x - crop[0]) * sc, Y0 + (y - crop[1]) * sc)
    items = [("1", "The numbers come from the tool", "required 10 · available 8.8 · SHORT, shortBy 1.2. Nothing is estimated.", (642, 430, 1160, 472), st[2]),
             ("2", "One governed tool call", "validate_order_stock, expandable to see the exact arguments and result.", (640, 526, 778, 541), st[1]),
             ("3", "Conversation id", "The same id is sent to the service and stored in the audit row.", (640, 548, 1050, 563), st[3])]
    cards = []
    for i, (n, ttl, desc, _, _) in enumerate(items):
        y = 214 + i * 232; c = card(1230, y, 600, 200, r=18, accent=BLUE); s = SS(600, 200)
        s.ellipse((34, 22, 82, 70), fill=BLUE); s.text((58, 46), n, 28, WHITE, bold=True, anchor="mm"); s.text((98, 28), ttl, 29, INK, bold=True)
        for j, l in enumerate(wrap(desc, 25, 520)): s.text((34, 92 + j * 33), l, 25, MUTE)
        c.im.alpha_composite(s.done(), (26, 26)); cards.append(c)
    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.2) for l in tl]; appear(f, left, t, st[0] + 0.2, 0.6)
        d = ImageDraw.Draw(f)
        for i, (n, ttl, desc, b, t0) in enumerate(items):
            appear(f, cards[i], t, t0 + 0.2)
            p = ease_out(prog(t, t0 + 0.1, 0.5))
            if p > 0:
                a, b2 = pt(b[0], b[1]), pt(b[2], b[3]); d.rounded_rectangle((a[0] - 6, a[1] - 5, a[0] - 6 + (b2[0] - a[0] + 12) * p, b2[1] + 5), 8, outline=GOLD, width=4)
                if p > 0.9:
                    cx, cy = (b2[0] + 24, (a[1] + b2[1]) / 2) if i != 0 else (b2[0] - 18, a[1] - 22)
                    d.ellipse((cx - 17, cy - 17, cx + 17, cy + 17), fill=GOLD, outline=WHITE, width=3); d.text((cx, cy), n, font=F(22, True), fill=INK, anchor="mm")
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- 5. architecture ----
def build_arch(T, st, sents):
    base = shell("Architecture"); tl = title("Architecture on SAP BTP")
    def box(x0, y0, x1, y1, ttl, sub, accent=BLUE, fill=WHITE, dashed=False, ic=None):
        w, h = x1 - x0, y1 - y0; c = card(x0, y0, w, h, r=16, fill=fill, shadow=not dashed, outline=MUTE if dashed else LINE); s = SS(w, h)
        if dashed: s.rr((3, 3, w - 3, h - 3), 14, outline=MUTE, width=3)
        s.rr((0, 14, 8, h - 14), 3, fill=accent); tx = 28 + (66 if ic else 0)
        s.text((tx, 14), ttl, 24, INK, bold=True)
        for j, l in enumerate(wrap(sub, 20, w - tx - 14)[:3]): s.text((tx, 50 + j * 26), l, 20, MUTE)
        c.im.alpha_composite(s.done(), (26, 26))
        if ic: c.im.alpha_composite(icon(ic, 50, accent), (26 + 22, 26 + 16))
        return c
    N = dict(user=box(70, 252, 380, 372, "Browser", "chat UI with sign-in", TEAL, ic="chat"),
             agent=box(510, 252, 900, 372, "sap-gov-agent", "Node app on Cloud Foundry; holds the tool loop", BLUE, ic="gear"),
             dest=box(1130, 252, 1520, 372, "Destination service", "GovStockService · OAuth2 client credentials", GOLD, ic="cloud"),
             cap=box(510, 470, 900, 590, "CAP service /stock", "six governed functions + audit", BLUE, ic="gear"),
             xs=box(1130, 470, 1520, 590, "XSUAA", "scopes: agent · auditor", GOLD, ic="shield"),
             hana=box(510, 700, 1000, 850, "SAP HANA Cloud (free tier)", "HDI container: orders · components · stock · AuditLog", GREEN, ic="db"),
             llm=box(1640, 252, 1880, 372, "LLM API", "non-SAP · tool results only", MUTE, fill=(248, 248, 248), dashed=True, ic=None),
             bas=box(70, 470, 380, 590, "Build & deploy", "Business Application Studio · MTA", TEAL, dashed=True, ic="gear"))
    cont = SS(1130, 684); cont.rr((2, 2, 1128, 682), 24, fill=(230, 242, 255, 255), outline=BLUE, width=3); cont.text((26, 12), "SAP BTP  ·  Cloud Foundry (trial subaccount)", 24, BLUE, bold=True)
    cont = L(cont.done(), 470, 196)
    E = [("1", [(380, 312), (510, 312)], TEAL, None, (445, 286)),
         ("2", [(620, 372), (620, 420), (1760, 420), (1760, 372)], MUTE, (8, 6), (1190, 398)),
         ("3", [(900, 312), (1130, 312)], GOLD, None, (1015, 286)),
         ("4", [(790, 372), (790, 470)], BLUE, None, (590, 447)),
         ("5", [(1325, 372), (1325, 470)], GOLD, None, (1445, 447)),
         ("6", [(900, 530), (1130, 530)], GOLD, None, (1015, 503)),
         ("7", [(705, 590), (705, 700)], GREEN, None, (880, 646)),
         ("·", [(380, 530), (510, 530)], TEAL, (8, 6), None)]
    labels = {"1": "ask", "2": "prompt + tools", "3": "get token", "4": "call + token + conv id", "5": "token", "6": "validate scope", "7": "SQL + audit insert"}
    els = []
    for n, pts, col, dash, lp in E:
        lay, L_ = arrow_layer(pts, col, 5, dash=dash); els.append((n, pts, lay, L_, col, lp))
    badges = {}
    for n, pts, lay, L_, col, lp in els:
        if n == "·": continue
        txt = f"{n}  {labels[n]}"; w_ = tw(txt, 20, True) + 24; badges[n] = chip(lp[0] - w_ / 2, lp[1] - 18, txt, 20, fg=INK, bg=WHITE, outline=col, bold=True, padx=12, pady=4)
    sched = {"user": st[0] + 0.3, "agent": st[1] + 0.2, "dest": st[2] + 0.2, "cap": st[3] + 0.2, "xs": st[3] + 0.9, "hana": st[3] + 1.6, "llm": st[4] + 0.2, "bas": st[4] + 2.5}
    edge_t = {"1": st[1] + 0.3, "2": st[4] + 0.3, "3": st[2] + 0.5, "4": st[3] + 0.5, "5": st[2] + 2.2, "6": st[3] + 1.3, "7": st[3] + 2.0, "·": st[4] + 3.0}
    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.2) for l in tl]; appear(f, cont, t, 0.4, 0.6, rise=0)
        for k, lay in N.items(): appear(f, lay, t, sched[k], 0.5, rise=18)
        for n, pts, lay, L_, col, lp in els:
            p = prog(t, edge_t[n], 0.7)
            if p <= 0: continue
            blit(f, lay, clip=reveal_clip(lay, pts, ease_io(p)) if p < 1 else None)
            if p >= 1 and n in badges: appear(f, badges[n], t, edge_t[n] + 0.7, 0.3, rise=6)
            if p >= 1 and n != "·":
                d = ((t - edge_t[n] - 0.7) * 260) % (L_ + 60)
                if d <= L_: paste_dot(f, path_point(pts, d), col, 7)
        draw_caption(f, t, st, sents)
    return draw
