"""Scenes 6-13: built live, verified, sequence diagrams, evidence, difference, limits, about."""
import math
from PIL import Image
from lib import *
from scenes_a import shell, draw_caption, pop, title, icon, cap_layer


def _fill(text_w, size, bold=False): return int(tw(text_w, size, bold))


# ---------------------------------------------------------------- 6. built live ----
def build_built(T, st, sents):
    base = shell("Built live"); tl = title("Built live on a personal SAP BTP trial", "Real screens from this build")
    items = [("hana_size", "SAP HANA Cloud free tier", "16 GB · created in HANA Cloud Central", st[1] + 0.3),
             ("hana_review", "Review and create instance", "govsandbox · Cloud Foundry runtime", st[1] + 1.2),
             ("hana_list", "govsandbox on Cloud Foundry", "SAP HANA database instance", st[1] + 2.1),
             ("bas_running", "Business Application Studio", "dev space govsandbox_dev running", st[1] + 3.0),
             ("cf_deploy", "MTA deploy to Cloud Foundry", "service, HDI container and XSUAA", st[1] + 3.9),
             ("cf_apps", "Apps and services on CF", "srv started · hana-free · hdi-shared", st[1] + 4.8),
             ("dest_cockpit", "Destination in the cockpit", "GovStockService · OAuth2 client", st[2] + 0.3)]
    CW, CH, GX, GY = 420, 330, 40, 26; X0, Y0 = 60, 218; cards = []
    for i, (nm, t1, t2, t0) in enumerate(items):
        x = X0 + (i % 4) * (CW + GX); y = Y0 + (i // 4) * (CH + GY)
        c = card(x, y, CW, CH, r=16); img, _, _ = shot(nm, CW - 24, 226, bg=(248, 250, 253), r=8)
        s = SS(CW, CH); s.text((16, 250), t1, 25, INK, bold=True); s.text((16, 286), t2, 20, MUTE)
        c.im.alpha_composite(s.done(), (26, 26)); c.im.alpha_composite(img, (26 + 12, 26 + 12)); cards.append((c, t0, x, y))
    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.2) for l in tl]
        newest = None
        for c, t0, x, y in cards:
            appear(f, c, t, t0, 0.55, rise=26)
            if t >= t0: newest = (x, y, t0)
        if newest:
            x, y, t0 = newest; a = 0.5 + 0.5 * math.sin((t - t0) * 4.0)
            if t - t0 < 4.5: ImageDraw.Draw(f).rounded_rectangle((x - 5, y - 5, x + CW + 5, y + CH + 5), 20, outline=mix(LINE, GOLD, clamp(a)), width=5)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- 1b. standard build ----
def build_standard(T, st, sents):
    base = shell("Problem"); tl = title("The standard build, step by step", "Joule Studio, from the SAP learning journey")
    i3, _, _ = shot("joule_tools", 1000); c3 = card(80, 230, 1000, i3.height, r=14); c3.im.alpha_composite(i3, (26, 26))
    l3 = chip(80, 230 + i3.height + 40, "3   Five tools attached to one agent; the model chains them", 25, fg=BLUE, bg=PALE, outline=BLUE)
    i1, _, _ = shot("joule_dest_var", 380); c1 = card(1130, 230, 380, i1.height, r=14); c1.im.alpha_composite(i1, (26, 26))
    l1 = chip(1545, 230 + i1.height // 2 - 24, "1  Destination", 24, fg=BLUE, bg=PALE, outline=BLUE)
    y2 = 230 + i1.height + 50
    i2, _, _ = shot("joule_skill", 380); c2 = card(1130, y2, 380, i2.height, r=14); c2.im.alpha_composite(i2, (26, 26))
    l2 = chip(1545, y2 + i2.height // 2 - 24, "2  Skill", 24, fg=BLUE, bg=PALE, outline=BLUE)
    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.2) for l in tl]
        appear(f, c1, t, st[1] + 0.2, 0.6); appear(f, l1, t, st[1] + 0.5)
        appear(f, c2, t, st[2] + 0.2, 0.6); appear(f, l2, t, st[2] + 0.5)
        appear(f, c3, t, st[3] + 0.2, 0.6); appear(f, l3, t, st[3] + 0.5)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- 7. verified ----
def build_verified(T, st, sents):
    base = shell("Verified"); tl = title("Verified live: deployed service on SAP HANA Cloud", "Called with a real OAuth token, not a mock")
    ok = chip(80, 204, "Material 41:  needs 1.7  ·  has 500  ·  SUFFICIENT", 27, fg=GREEN, bg=PALEGREEN, outline=GREEN)
    bad = chip(960, 204, "Material 42:  needs 10  ·  has 8.8  ·  SHORT by 1.2", 27, fg=RED, bg=PALERED, outline=RED)
    i1, _, _ = shot("live_tests", 1560); c1 = card(180, 276, 1560, i1.height, r=14); c1.im.alpha_composite(i1, (26, 26))
    i2, _, _ = shot("dest_created", 1400); c2 = card(260, 618, 1400, i2.height, r=14); c2.im.alpha_composite(i2, (26, 26))
    t2 = chip(260, 572, "Destination created (201), looked up (200), then called through it (200)", 21, fg=(120, 80, 0), bg=PALEGOLD, outline=GOLD, bold=False)
    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.2) for l in tl]
        appear(f, c1, t, st[0] + 0.3, 0.6); appear(f, ok, t, st[2] + 0.3); appear(f, bad, t, st[2] + 2.3)
        appear(f, c2, t, st[3] + 0.4, 0.6); appear(f, t2, t, st[3] + 0.3)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- sequence engine ----
def _lifeline_header(x, ttl, sub, col, w=250, y=96):
    c = card(x - w // 2, y, w, 78, r=14, accent=col); s = SS(w, 78); s.text((24, 10), ttl, 22, INK, bold=True); s.text((24, 42), sub, 17, MUTE)
    c.im.alpha_composite(s.done(), (26, 26)); return c

def _label(x, y, text, size=20, fg=INK, bg=WHITE, outline=None):
    w = int(tw(text, size, True)) + 26; h = int(size * 1.3) + 10
    s = SS(w + 4, h + 4); s.rr((2, 2, 2 + w, 2 + h), 9, fill=bg, outline=outline, width=2); s.text((2 + w / 2, 2 + h / 2 + 1), text, size, fg, bold=True, anchor="mm")
    return L(s.done(), int(x - w / 2 - 2), int(y - h / 2 - 2))


def build_seq1(T, st, sents):
    base = shell("Sequence"); tl = []
    LL = [("User", "browser", TEAL), ("Chat app", "sap-gov-agent", BLUE), ("LLM", "non-SAP", MUTE), ("Destination", "service", GOLD), ("CAP service", "/stock", BLUE), ("HANA Cloud", "HDI · AuditLog", GREEN)]
    X = [190 + i * 308 for i in range(6)]; heads = [_lifeline_header(X[i], *LL[i]) for i in range(6)]
    Y0, DY = 256, 54
    life = SS(W, H, k=1)
    for x in X: life.line([(x, 200), (x, 930)], (190, 202, 220, 255), 3, dash=(10, 8))
    life = L(life.done(), 0, 0)
    M = [(0, 1, "1  Is order 1000001 ready?", BLUE, False), (1, 2, "2  question + 6 tool definitions", BLUE, False), (2, 1, "3  call validate_order_stock(1000001)", MUTE, True),
         (1, 3, "4  get token for GovStockService", GOLD, False), (3, 1, "5  Bearer token · scope agent", GOLD, True), (1, 4, "6  GET validateOrderStock · x-correlation-id", BLUE, False),
         (4, 5, "7  read order, components, stock", GREEN, False), ("note", 4, "8  sum stock per material in code → verdict", ORANGE, False),
         (4, 5, "9  INSERT AuditLog (OK · 200 · conv id)", GREEN, False), (4, 1, "10  verdict JSON per material", BLUE, True),
         (1, 2, "11  tool result", BLUE, False), (2, 1, "12  answer in plain text", MUTE, True), (1, 0, "13  answer + tool trace + conv id", BLUE, True)]
    groups = [(1, 0, 3), (2, 3, 6), (3, 6, 10), (4, 10, 13)]; times = [0.0] * 13; times[0] = st[1] - 0.2
    for si, a, b in groups:
        nxt = st[si + 1] if si + 1 < len(st) else T - 0.8; span = max(1.0, nxt - st[si] - 0.6)
        for k in range(a, b): times[k] = st[si] + 0.2 + (k - a) * span / (b - a)
    times[0] = st[1] + 0.1
    els = []
    for k, (a, b, txt, col, ret) in enumerate(M):
        y = Y0 + k * DY
        if a == "note":
            w_ = int(tw(txt.replace("→", "to"), 20, True)) + 30; lay = _label(X[b] - 40 - w_ / 2, y - 6, txt.replace("→", "to"), 20, fg=(120, 70, 0), bg=PALEGOLD, outline=ORANGE); els.append((k, None, lay, None, y, col)); continue
        x1 = X[a] + (10 if b > a else -10); x2 = X[b] - (10 if b > a else -10)
        arr, ln = arrow_layer([(x1, y), (x2, y)], col, 4, dash=(9, 6) if ret else None, head=13)
        lab = _label((x1 + x2) / 2, y - 22, txt, 19, outline=None); els.append((k, arr, lab, ((x1, y), (x2, y)), y, col))
    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.2) for l in tl]
        for i, h in enumerate(heads): appear(f, h, t, 0.3 + i * 0.12, 0.4, rise=10)
        blit(f, life, a=prog(t, 0.6, 0.5))
        d = ImageDraw.Draw(f)
        # activation bars
        for xi, a0, a1, col in ((1, 0, 12, BLUE), (4, 5, 9, BLUE)):
            if t >= times[a0]:
                top = Y0 + a0 * DY - 10; full = Y0 + a1 * DY + 14
                bot = full if t >= times[a1] else top + 6 + (full - top - 6) * prog(t, times[a0], max(0.1, times[a1] - times[a0]))
                d.rounded_rectangle((X[xi] - 8, top, X[xi] + 8, max(top + 6, bot)), 4, fill=mix(WHITE, col, 0.85), outline=col, width=2)
        for k, arr, lab, pts, y, col in els:
            p = prog(t, times[k], 0.5)
            if p <= 0: continue
            if arr is None: appear(f, lab, t, times[k], 0.4, rise=8); continue
            blit(f, arr, clip=(0, 0, max(2, int(arr.w * ease_io(p))), arr.h) if pts[0][0] < pts[1][0] else (arr.w - max(2, int(arr.w * ease_io(p))), 0, arr.w, arr.h))
            if p > 0.5: appear(f, lab, t, times[k] + 0.2, 0.3, rise=6)
            if p >= 1:  # highlight current message with a gold marker
                cur = k == max(i for i in range(13) if times[i] <= t)
                if cur: d.ellipse((pts[0][0] - 28, y - 7, pts[0][0] - 14, y + 7), fill=GOLD)
        draw_caption(f, t, st, sents)
    return draw


def build_seq2(T, st, sents):
    base = shell("Failures"); tl = title("Failures are evidence too", "401, 403 and 404 each leave an audit row")
    X = [250, 900, 1560]; LLs = [("Caller", "any client", TEAL), ("Auth gate + CAP", "/stock", BLUE), ("HANA Cloud", "AuditLog", GREEN)]
    heads = [_lifeline_header(X[i], *LLs[i], w=300, y=214) for i in range(3)]
    life = SS(W, H, k=1)
    for x in X: life.line([(x, 296), (x, 930)], (190, 202, 220, 255), 3, dash=(10, 8))
    life = L(life.done(), 0, 0)
    cases = [("A", RED, "GET getMaterialDetails(41) · no token", "401 Unauthorized", "INSERT AuditLog · DENIED · 401", "caller: unauthenticated", st[1]),
             ("B", ORANGE, "same call · token without agent scope", "403 Forbidden", "INSERT AuditLog · DENIED · 403", "caller: auditor", st[2]),
             ("C", GOLD, "GET validateOrderStock(999999) · valid token", "404 order not found", "INSERT after rollback · ERROR · 404", "separate transaction", st[3])]
    rows = []
    for ci, (lt, col, rq, rs, ins, note, t0) in enumerate(cases):
        y = 380 + ci * 190
        a1, _ = arrow_layer([(X[0] + 8, y), (X[1] - 10, y)], BLUE, 4, head=13); a2, _ = arrow_layer([(X[1] - 10, y + 52), (X[0] + 8, y + 52)], RED if ci < 2 else ORANGE, 4, dash=(9, 6), head=13)
        a3, _ = arrow_layer([(X[1] + 10, y + 104), (X[2] - 10, y + 104)], GREEN, 4, head=13)
        badge = chip(80, y - 24, lt, 28, fg=WHITE if ci < 2 else INK, bg=col, padx=14, pady=4)
        l1 = _label((X[0] + X[1]) / 2, y - 22, rq, 19); l2 = _label((X[0] + X[1]) / 2, y + 30, rs, 20, fg=RED if ci < 2 else (150, 80, 0)); l3 = _label((X[1] + X[2]) / 2, y + 82, ins, 19)
        nt = chip(X[2] + 40, y + 74, note, 19, fg=GREEN, bg=PALEGREEN, outline=GREEN, bold=False)
        rows.append((badge, a1, l1, a2, l2, a3, l3, nt, t0))
    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.2) for l in tl]
        for i, h in enumerate(heads): appear(f, h, t, 0.3 + i * 0.12, 0.4, rise=10)
        blit(f, life, a=prog(t, 0.6, 0.5))
        for badge, a1, l1, a2, l2, a3, l3, nt, t0 in rows:
            appear(f, badge, t, t0 + 0.0, 0.3)
            for k, (arr, lab, off) in enumerate(((a1, l1, 0.2), (a2, l2, 1.2), (a3, l3, 2.2))):
                p = prog(t, t0 + off, 0.5)
                if p > 0:
                    fwd = k != 1; w_ = max(2, int(arr.w * ease_io(p)))
                    blit(f, arr, clip=(0, 0, w_, arr.h) if fwd else (arr.w - w_, 0, arr.w, arr.h))
                    if p > 0.5: appear(f, lab, t, t0 + off + 0.2, 0.3, rise=6)
            appear(f, nt, t, t0 + 3.2, 0.4)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- 10. evidence ----
def build_evidence(T, st, sents):
    base = shell("Evidence"); tl = title("Evidence: rows read back from SAP HANA Cloud")
    i1, _, _ = shot("audit_rows", 1300); c1 = card(310, 252, 1300, i1.height, r=14); c1.im.alpha_composite(i1, (26, 26))
    i2, _, _ = shot("smoke_ids", 1300); c2 = card(310, 600, 1300, i2.height, r=14); c2.im.alpha_composite(i2, (26, 26))
    cp1 = chip(310, 202, "After the first live run: OK, ERROR and DENIED rows", 22, fg=BLUE, bg=PALE, outline=BLUE, bold=False)
    cp2 = chip(310, 550, "After the browser chat: full conversation ids", 22, fg=BLUE, bg=PALE, outline=BLUE, bold=False)
    legend = [chip(1240 + i * 0, 146, "", 1) for i in range(0)]
    lg = [chip(1010, 202, "OK 200", 21, fg=GREEN, bg=PALEGREEN, outline=GREEN), chip(1130, 202, "ERROR 404", 21, fg=(150, 80, 0), bg=PALEGOLD, outline=GOLD),
          chip(1290, 202, "DENIED 403", 21, fg=RED, bg=PALERED, outline=RED), chip(1460, 202, "DENIED 401", 21, fg=RED, bg=PALERED, outline=RED)]
    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.2) for l in tl]
        appear(f, cp1, t, st[0] + 0.1); appear(f, c1, t, st[0] + 0.3, 0.6)
        for i, c in enumerate(lg): appear(f, c, t, st[1] + 0.2 + i * 0.3, 0.3, rise=8)
        appear(f, cp2, t, st[2] + 0.1); appear(f, c2, t, st[2] + 0.3, 0.6)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- 11. difference ----
ROWS = [("Ask", "Navigate transactions or apps: order, then components, then stock", "Ask in plain language: “Is order 1000001 ready?”"),
        ("Who joins the dots", "A person reads screens and compares the numbers", "The agent chains the lookups; a tested service computes the verdict"),
        ("Where the logic lives", "In transactions and individual judgment", "In one versioned, unit-tested service function per question"),
        ("Audit trail", "Change documents and logs, not tied to the question that was asked", "One row per call, allowed or denied, tied to the conversation"),
        ("Extending", "Custom development and transports", "Add a function and a tool definition, redeploy the MTA")]
def build_difference(T, st, sents):
    base = shell("Difference"); tl = title("How is this different from conservative SAP?")
    X1, X2, X3, RW, RH, Y0 = 60, 400, 1120, 1800, 100, 232
    h1 = chip(X2, 168, "Conservative SAP", 28, fg=WHITE, bg=(86, 104, 124)); h2 = chip(X3, 168, "Governed SAP agents", 28, fg=WHITE, bg=BLUE)
    rows = []
    for i, (lab, a, b) in enumerate(ROWS):
        y = Y0 + i * (RH + 10); c = card(X1, y, RW, RH, r=14); s = SS(RW, RH)
        s.text((26, RH / 2), lab, 26, BLUE, bold=True, anchor="lm"); s.line([(X2 - X1 - 24, 14), (X2 - X1 - 24, RH - 14)], LINE, 2); s.line([(X3 - X1 - 24, 14), (X3 - X1 - 24, RH - 14)], LINE, 2)
        c.im.alpha_composite(s.done(), (26, 26))
        def txt(x, t_, col, wd):
            ls = wrap(t_, 24, wd); return text_layer(x, y + RH / 2 - len(ls) * 15, ls, 24, col, gap=1.25)
        rows.append((c, txt(X2, a, TEXT, 680), txt(X3, b, INK, 700)))
    band = card(X1, Y0 + 5 * (RH + 10) + 4, RW, 70, r=14, fill=PALEGREEN, outline=GREEN, accent=GREEN); sb = SS(RW, 76)
    sb.text((34, 38), "Unchanged:  SAP HANA  ·  SAP BTP  ·  the SAP security model (OAuth, XSUAA)  ·  your SAP data", 27, GREEN, bold=True, anchor="lm"); band.im.alpha_composite(sb.done(), (26, 26))
    foot = text_layer(64, Y0 + 5 * (RH + 10) + 84, "Not a replacement for S/4HANA: a governed layer on top of it.", 24, MUTE)
    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.2) for l in tl]
        appear(f, h1, t, st[1] - 0.1, 0.4); appear(f, h2, t, st[2] - 0.1, 0.4)
        sp1 = (st[2] - st[1]) * 0.85 / 5; sp2 = (st[3] - st[2]) * 0.8 / 5
        for i, (c, a, b) in enumerate(rows):
            appear(f, c, t, st[0] + 0.4 + i * 0.2, 0.4, rise=14); appear(f, a, t, st[1] + 0.4 + i * sp1, 0.45, rise=10); appear(f, b, t, st[2] + 0.4 + i * sp2, 0.45, rise=10)
        appear(f, band, t, st[3] + 0.2, 0.5); appear(f, foot, t, st[3] + 1.2, 0.5)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- 12. limits ----
def build_limits(T, st, sents):
    base = shell("Limits"); tl = title("Honest limits, and what comes next")
    specs = [(ORANGE, "Sample data, trial account", ["Stands in for an S/4HANA backend.", "Free-tier HANA stops nightly and", "is deleted after 30 idle days."], st[1]),
             (RED, "The model is not an SAP model", ["Prompts and tool results go to", "an outside language model.", "Real regulated data needs an", "approved one."], st[2]),
             (GREEN, "Next", ["Real SAP APIs through the destination", "An audit dashboard", "A model inside your approved boundary"], st[3])]
    cards = []
    for i, (col, ttl, ls_, t0) in enumerate(specs):
        x = 60 + i * 610; c = card(x, 230, 570, 440, r=20, accent=col); s = SS(570, 440)
        s.ellipse((36, 36, 104, 104), fill=col); s.text((70, 70), str(i + 1) if i < 2 else "→".replace("→", ">"), 36, WHITE, bold=True, anchor="mm")
        s.text((36, 134), ttl, 32, INK, bold=True)
        for j, l in enumerate(ls_): s.text((36, 196 + j * 46), l, 27, TEXT)
        c.im.alpha_composite(s.done(), (26, 26)); cards.append((c, t0))
    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.2) for l in tl]
        for c, t0 in cards: appear(f, c, t, t0 + 0.1, 0.5, rise=24)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- 13. about ----
def build_about(T, st, sents):
    bg = Image.new("RGB", (1, H))
    for y in range(H): bg.putpixel((0, y), mix((0, 132, 250), (0, 78, 192), y / H))
    bg = bg.resize((W, H)); ov = SS(W, H, k=1)
    ov.ellipse((1250, -330, 2150, 570), outline=(255, 255, 255, 70), width=3); ov.ellipse((-260, 700, 620, 1580), outline=(255, 255, 255, 60), width=3); ov.ellipse((1500, 650, 2300, 1450), fill=(255, 255, 255, 22))
    bg.paste(ov.done(), (0, 0), ov.done())
    sw = int(tw("SAP", 54, True)) + 40; aw = int(tw("Agents", 54, True)) + 40
    s0 = SS(900, 100); s0.rr((0, 8, sw, 84), 18, fill=WHITE); s0.text((sw / 2, 47), "SAP", 54, BLUE, bold=True, anchor="mm")
    s0.rr((sw + 16, 8, sw + 16 + aw, 84), 18, fill=GOLD); s0.text((sw + 16 + aw / 2, 47), "Agents", 54, INK, bold=True, anchor="mm"); top = L(s0.done(), 140, 90)
    c = card(300, 260, 1320, 520, r=26); s = SS(1320, 520)
    s.ellipse((60, 60, 260, 260), fill=BLUE); s.text((160, 160), "YA", 78, WHITE, bold=True, anchor="mm")
    s.text((310, 70), "Yuvaraj Aravindan", 64, INK, bold=True); s.text((310, 152), "Founder, AI Agentic Enterprises", 36, BLUE, bold=True)
    s.text((310, 214), "Governed AI agents for regulated industries,", 30, TEXT); s.text((310, 256), "on enterprise platforms like SAP.", 30, TEXT)
    c.im.alpha_composite(s.done(), (26, 26))
    chips, cx = [], 336
    for txt_, fg_, bg_, ol_ in (("Enterprise applications", BLUE, PALE, BLUE), ("AI agents & governance", (120, 80, 0), PALEGOLD, GOLD), ("SAP BTP · HANA", GREEN, PALEGREEN, GREEN)):
        ch_ = chip(cx, 600, txt_, 26, fg=fg_, bg=bg_, outline=ol_); chips.append(ch_); cx += ch_.w + 6
    site = text_layer(336, 690, "ai-agentic-enterprises.com", 40, BLUE, bold=True)
    note = text_layer(300, 830, "Independent demonstration on an SAP BTP trial account. Not an SAP product announcement.", 26, (255, 255, 255, 235))
    def draw(f, t):
        f.paste(bg, (0, 0)); appear(f, top, t, 0.2); appear(f, c, t, 0.5, 0.6, rise=26)
        for i, ch in enumerate(chips): appear(f, ch, t, st[0] + 1.0 + i * 0.4, 0.4)
        appear(f, site, t, st[0] + 2.4, 0.5); appear(f, note, t, st[1] + 0.2, 0.6)
        draw_caption(f, t, st, sents)
    draw.shell = False; return draw


BUILD = {"standard": build_standard, "built": build_built, "verified": build_verified, "seq1": build_seq1, "seq2": build_seq2, "evidence": build_evidence,
         "difference": build_difference, "limits": build_limits, "about": build_about}
