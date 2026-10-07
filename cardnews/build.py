import os, html, json
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html")
os.makedirs(OUT, exist_ok=True)
E = html.escape
def br(t): return "<br>".join(E(x.strip()) for x in t.split("/"))

# kind: cover / bubbles / list / compare / steps / close / doctor
S = [
 ("보톡스 반복 후 효과가 줄었다면", "#C9A857", [
  dict(k="cover", tag="종아리보톡스를 반복했는데", title="효과가 줄었다면", line="횟수보다 현재 근육 상태를 먼저 확인합니다", items=["이전 치료 이력 확인","현재 근육 상태 평가","치료 방법 재검토"]),
  dict(k="bubbles", title="보톡스를 반복한 뒤 / 이런 고민이신 분", items=["예전만큼 변화가 없는 것 같은 분","계속 보톡스를 반복해야 할지 고민이신 분","내성이 생긴 건 아닌지 걱정이신 분"]),
  dict(k="list", title="효과 감소의 원인은 / 내성만이 아닙니다", line="중화항체에 의한 이차성 비반응도 가능하지만 다른 요소도 함께 봅니다", items=["주사 용량","시술 간격","주사 위치와 표적 근육","현재 비복근 발달과 좌우 차이"]),
  dict(k="list", title="치료 이력, 이렇게 확인합니다", line="횟수만이 아니라 반응의 변화를 확인합니다", items=["시술 횟수와 마지막 시술 시점","대략적인 시술 간격","이전 반응과 최근 효과 변화","좌우 종아리의 치료 이력 차이"]),
  dict(k="close", title="몇 번 맞았는가보다 / 지금 종아리 구조가 중요합니다", line="같은 시술을 반복하기 전에 현재 상태부터 평가합니다", tags="#현재근육상태  #치료이력확인  #환자별치료계획"),
 ]),
 ("근육형 · 지방형 · 복합형", "#4FA3A5", [
  dict(k="cover", tag="종아리가 굵어 보이는 이유", title="근육형 · 지방형 · 복합형", line="치료보다 먼저 원인을 구분합니다", items=["근육형","지방형","복합형"]),
  dict(k="bubbles", title="종아리 굵기가 고민이신 분", items=["알 때문인지 살 때문인지 모르겠는 분","굵은 종아리는 다 같은 치료인지 궁금하신 분","좌우 굵기가 달라 고민이신 분"]),
  dict(k="list", title="종아리 윤곽에 관여하는 요소", line="비복근 하나만으로 설명되지 않습니다", items=["내측·외측 비복근","가자미근","피하지방","부종과 좌우 차이"]),
  dict(k="list", title="같은 굵기, 다른 원인", line="둘레가 같아도 치료계획은 달라질 수 있습니다", items=["근육형 - 특정 비복근 발달이 두드러짐","지방형 - 피하지방 비중이 높음","복합형 - 근육과 지방이 함께 영향"], plain=True),
  dict(k="close", title="굵은 종아리 = 종아리보톡스 X / 굵은 종아리 = 종아리신경차단 X", line="원인 구분이 치료 선택보다 먼저입니다", tags="#원인먼저  #유형구분  #환자별치료계획"),
 ]),
 ("정밀초음파검사", "#6C8EBF", [
  dict(k="cover", tag="종아리신경차단 전", title="정밀초음파검사", line="겉모양이 아닌 내부 구조를 확인합니다", items=["근육 두께와 형태","좌우 차이","근육층과 지방층"]),
  dict(k="bubbles", title="이런 분들께 필요한 확인입니다", items=["어느 부분이 윤곽에 영향을 주는지 궁금하신 분","근육인지 지방인지 확인하고 싶으신 분","보톡스를 반복해 현재 근육 상태가 궁금하신 분"]),
  dict(k="list", title="정밀초음파로 확인하는 것", items=["내측·외측 비복근","비복근과 가자미근의 관계","오른쪽·왼쪽 근육 차이","피하지방층과 근육층의 비율"]),
  dict(k="list", title="초음파로 계획하는 것", line="확인한 구조를 바탕으로 환자별 치료를 설계합니다", items=["치료 범위","접근 방향","치료 깊이"]),
  dict(k="close", title="초음파의 목적은 결과 보장이 아닙니다", line="내부 구조를 확인해 환자별 치료계획을 세우는 것이 핵심입니다", tags="#정밀초음파  #내부구조확인  #치료계획"),
 ]),
 ("종아리보톡스와 종아리신경차단", "#B5656F", [
  dict(k="cover", tag="종아리보톡스 vs 종아리신경차단", title="같은 치료가 아닙니다", line="작용 방식이 다릅니다", items=["같은 근육을 대상으로 할 수 있음","접근 원리는 다름","우열이 아닌 적합성"]),
  dict(k="bubbles", title="치료 선택이 고민이신 분", items=["보톡스와 신경차단 중 무엇이 맞는지 고민이신 분","반복 시술이 부담스러운 분","효과가 예전 같지 않아 다른 방법이 궁금하신 분"]),
  dict(k="compare", title="접근 원리의 차이", a=("종아리보톡스","보툴리눔 톡신으로 일정 기간 신경근 전달을 감소시킵니다"), b=("종아리신경차단","운동신경 가지와 근육 상태를 평가하고 치료 대상 범위를 정해 접근합니다")),
  dict(k="list", title="치료 선택 시 함께 보는 것", items=["근육 발달 정도","이전 치료 이력","지방 비율과 좌우 차이","반복치료 부담과 치료 목표"]),
  dict(k="close", title="어느 치료가 무조건 우수하다고 / 말할 수 없습니다", line="현재 상태를 확인한 뒤 적합한 방법을 검토합니다", tags="#작용방식차이  #현재상태확인  #적합성검토"),
 ]),
 ("어느 부위를 치료할 것인가", "#7FA66B", [
  dict(k="cover", tag="종아리신경차단은", title="많이 차단하는 치료가 아닙니다", line="어느 부위를 치료할지 판단하는 것이 핵심입니다", items=["치료 대상 평가","선택적 접근","환자별 범위 설정"]),
  dict(k="bubbles", title="신경차단이 궁금하신 분", items=["종아리 알을 없애는 주사라고만 알고 계신 분","안쪽 돌출이 특히 고민이신 분","어떤 원리의 치료인지 궁금하신 분"]),
  dict(k="list", title="신경차단, 이렇게 이해하세요", items=["운동신경 가지 중 치료 대상 부분을 평가","선택적으로 접근","과도하게 발달한 근육의 사용과 볼륨 변화 유도"]),
  dict(k="list", title="비복근만 보면 충분할까요?", line="종아리 윤곽은 하나의 근육만으로 설명되지 않을 수 있습니다", items=["내측 비복근 - 안쪽 돌출과 연관","가자미근 - 전체 볼륨과 윤곽에 영향","피하지방 - 근육이 발달해도 비율이 높을 수 있음"], plain=True),
  dict(k="close", title="비복근만 보는 것 X / 근육과 지방, 좌우 차이, 전체 윤곽을 함께 보는 것 O", line="둘레가 같아도 같은 범위를 치료하지 않는 이유입니다", tags="#치료대상판단  #선택적접근  #전체윤곽"),
 ]),
 ("청담별의원 종아리 진료 프로세스", "#C9A857", [
  dict(k="cover", tag="청담별의원 종아리 진료", title="평가가 먼저입니다", line="평가 → 구분 → 확인 → 계획 → 치료", items=["정밀 평가","정밀초음파","환자별 치료계획"]),
  dict(k="steps", title="치료 전 확인 단계", items=[("01","현재 종아리 형태 평가"),("02","근육형·지방형·복합형 구분"),("03","정밀초음파검사"),("04","과거 치료 이력 확인")]),
  dict(k="steps", title="치료와 경과 확인", items=[("05","치료 대상 범위 결정"),("06","종아리신경차단"),("07","경과 확인")]),
  dict(k="list", title="정우철 대표원장이 보는 것", line="종아리 둘레만이 아닙니다", items=["돌출된 근육의 위치","좌우 근육 발달 차이","지방과 근육의 관여 정도","과거 치료 이력과 초음파 구조"]),
  dict(k="close", title="치료를 먼저 정하지 않습니다 / 현재 구조를 먼저 확인합니다", line="정확한 평가가 치료 선택보다 먼저입니다", note="치료 후 통증, 부기, 멍, 감각 변화 등이 나타날 수 있으며 결과와 회복에는 개인차가 있습니다"),
 ]),
]

CSS1 = """
@font-face{font-family:NK;font-weight:300;src:url('../fonts/Light.otf')}
@font-face{font-family:NK;font-weight:400;src:url('../fonts/r.otf')}
@font-face{font-family:NK;font-weight:500;src:url('../fonts/m.otf')}
@font-face{font-family:NK;font-weight:700;src:url('../fonts/n.otf')}
@font-face{font-family:NK;font-weight:900;src:url('../fonts/Black.otf')}
*{box-sizing:border-box;margin:0;padding:0}
:root{--lime:#B8E80C;--ink:#0d2b1a;--black:#0a0a0a;--org:#FF7A1A}
body{width:1080px;height:1080px;font-family:NK,sans-serif;position:relative;overflow:hidden;word-break:keep-all}
body.lime{background:var(--lime);color:var(--ink)}
body.black{background:#050505;color:#fff}
body.green{background:linear-gradient(180deg,#04463a 0%,#1f9a68 60%,#4ccf86 100%);color:#fff}
.hd{position:absolute;left:60px;right:60px;top:52px;display:flex;justify-content:space-between;font-size:25px;font-weight:300;letter-spacing:4px;text-transform:uppercase}
.lime .hd{padding-bottom:22px;border-bottom:2px solid var(--ink);justify-content:center;letter-spacing:5px}
.black .hd{color:var(--lime)}
.green .hd{color:#d7fbe6}
.main{position:absolute;left:60px;right:60px;top:140px;bottom:110px;display:flex;flex-direction:column;justify-content:center;z-index:2}
.ft{position:absolute;left:60px;right:60px;bottom:44px;display:flex;justify-content:space-between;align-items:center;font-size:24px;font-weight:500;z-index:2}
.lime .ft{color:#3d5a14}.black .ft{color:#b9c97a}.green .ft{color:#d7fbe6}
.dots i{display:inline-block;width:14px;height:14px;border-radius:50%;margin-left:10px;border:2px solid currentColor;opacity:.55}
.dots i.on{background:currentColor;opacity:1}
h1{font-weight:900;line-height:1.22;letter-spacing:-2px}
h1 .l{font-weight:300}
.lime h1{color:var(--ink)}.black h1{color:var(--lime)}.green h1{color:#fff}
.line{font-size:34px;line-height:1.5;font-weight:400;margin-top:26px}
.lime .line{color:#27441b}.black .line{color:#e8f5b0}.green .line{color:#d7fbe6}
.tag{align-self:flex-start;border:2px solid var(--lime);color:var(--lime);font-size:30px;font-weight:500;padding:10px 28px;border-radius:40px;margin-bottom:32px}
.dot{position:absolute;border-radius:50%;z-index:1;
 background-image:radial-gradient(circle,var(--c,#B8E80C) 0 3.2px,transparent 3.8px);background-size:16px 16px;
 -webkit-mask-image:radial-gradient(circle,#000 25%,transparent 72%);mask-image:radial-gradient(circle,#000 25%,transparent 72%)}
.ring{position:absolute;border-radius:50%;border:2px solid var(--ink);z-index:1}
.pill{background:var(--black);color:var(--lime);border-radius:70px;padding:24px 44px;font-size:37px;font-weight:500;text-align:center;line-height:1.35}
.pills{display:flex;flex-direction:column;gap:16px;margin-top:44px}
.pills .pill:nth-child(odd){margin-right:40px}.pills .pill:nth-child(even){margin-left:40px}
.opill{background:var(--org);color:#0a0a0a;border-radius:70px;padding:20px 40px;font-size:38px;font-weight:900;align-self:flex-start;line-height:1.3}
.ocol{display:flex;flex-direction:column;gap:20px;margin-top:40px}
.ocol .opill:nth-child(even){align-self:flex-end}
.bub{background:#2f3d05;color:#eef7c4;border-radius:14px;padding:26px 36px;font-size:36px;font-weight:300;line-height:1.4;max-width:820px}
.bubs{display:flex;flex-direction:column;gap:24px;margin-top:52px}
.bub:nth-child(even){align-self:flex-end}
.bub:nth-child(odd){align-self:flex-start}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:44px}
.tile{background:rgba(255,255,255,.9);color:#0d3b2c;border-radius:4px;padding:34px 28px;min-height:210px;display:flex;flex-direction:column;justify-content:space-between}
.tile b{font-size:30px;font-weight:900;color:#1f9a68;letter-spacing:2px}
.tile span{font-size:35px;font-weight:700;line-height:1.35}
.rows{display:flex;flex-direction:column;gap:18px;margin-top:40px}
.row{display:flex;align-items:center;gap:26px;background:rgba(255,255,255,.16);border:2px solid rgba(255,255,255,.35);border-radius:70px;padding:16px 40px 16px 18px;font-size:37px;font-weight:700}
.row .c{flex:none;min-width:96px;height:80px;border-radius:50px;background:#58e69f;color:#05392c;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:28px;padding:0 20px}
.cmp{display:flex;gap:26px;margin-top:44px}
.cmp>div{flex:1;background:rgba(255,255,255,.92);color:#0d3b2c;border-radius:6px;padding:36px 30px}
.cmp h3{display:inline-block;font-size:38px;font-weight:900;padding:10px 24px;border-radius:50px;background:var(--black);color:var(--lime);margin-bottom:24px}
.cmp>div:last-child h3{background:var(--org);color:#0a0a0a}
.cmp p{font-size:34px;line-height:1.55;font-weight:500}
.hash{display:flex;flex-wrap:wrap;gap:16px;margin-top:40px}
.hash span{background:#58e69f;color:#05392c;border-radius:60px;padding:14px 30px;font-size:30px;font-weight:700}
.logo{display:flex;align-items:center;gap:12px;justify-content:center;font-weight:700;letter-spacing:2px}
.note{margin-top:40px;font-size:23px;line-height:1.5;color:#c8f3dc;border-top:1px solid rgba(255,255,255,.35);padding-top:16px;font-weight:300}
.ring2{position:absolute;border-radius:50%;border:2px solid rgba(255,255,255,.28);z-index:1}
"""
STAR='<svg width="30" height="30" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0l2.4 8.2L22 5l-4.6 7 6.6 5-8.3.2L12 24l-3.7-6.8L0 17l6.6-5L2 5l7.6 3.2z"/></svg>'

def title(t, size, light_last=False):
    parts=[x.strip() for x in t.split("/")]
    return "<br>".join(E(p) for p in parts)

def fs(t, base):
    n = max(len(x.strip()) for x in t.split("/"))
    return base if n<=9 else base-8 if n<=12 else base-16 if n<=15 else base-24 if n<=18 else base-32 if n<=23 else base-40

def card1(si, ci, st, _=False):
    name, _, cards = st
    c = cards[ci]; k = c["k"]
    theme = {"cover":"black","bubbles":"lime","close":"green","compare":"green","steps":"green"}.get(k)
    if k=="list": theme = "green" if ci==2 else "lime"
    dots = "".join('<i class="on"></i>' if i==ci else "<i></i>" for i in range(5))
    hd = '<div class="hd"><span>Cheongdam Star Clinic</span>' + ('' if theme=="lime" else '<span>Plastic Surgery</span>') + '</div>'
    deco = ""; body = ""
    if k=="cover":
        deco = '<div class="dot" style="right:-220px;bottom:60px;width:560px;height:560px"></div>'
        its = "".join(f'<div class="opill">{E(t)}</div>' for t in c["items"])
        body = f'<div class="tag">{E(c["tag"])}</div><h1 style="font-size:{fs(c["title"],112)}px">{title(c["title"],0)}</h1><div class="line">{E(c["line"])}</div><div class="ocol">{its}</div>'
    elif k=="bubbles":
        deco = '<div class="ring" style="right:-90px;top:250px;width:380px;height:380px"></div><div class="dot" style="--c:#2f3d05;left:-220px;bottom:70px;width:420px;height:420px"></div>'
        its = "".join(f'<div class="bub">{E(t)}</div>' for t in c["items"])
        body = f'<h1 style="font-size:{fs(c["title"],84)}px">{title(c["title"],0)}</h1><div class="bubs">{its}</div>'
    elif k=="list" and theme=="lime":
        deco = '<div class="dot" style="--c:#2f3d05;left:-170px;top:480px;width:420px;height:420px"></div>'
        its = "".join(f'<div class="pill">{E(t)}</div>' for t in c["items"])
        line = f'<div class="line">{E(c["line"])}</div>' if c.get("line") else ""
        body = f'<h1 style="font-size:{fs(c["title"],80)}px">{title(c["title"],0)}</h1>{line}<div class="pills">{its}</div>'
    elif k=="list":
        line = f'<div class="line">{E(c["line"])}</div>' if c.get("line") else ""
        deco = '<div class="dot" style="--c:#c9ffe0;right:-140px;top:60px;width:420px;height:420px;opacity:.5"></div>'
        if len(c["items"])==4:
            its = "".join(f'<div class="tile"><b>0{i+1}</b><span>{E(t)}</span></div>' for i,t in enumerate(c["items"]))
            body = f'<h1 style="font-size:{fs(c["title"],80)}px">{title(c["title"],0)}</h1>{line}<div class="tiles">{its}</div>'
        else:
            its = "".join(f'<div class="row"><span class="c">0{i+1}</span>{E(t)}</div>' for i,t in enumerate(c["items"]))
            body = f'<h1 style="font-size:{fs(c["title"],80)}px">{title(c["title"],0)}</h1>{line}<div class="rows">{its}</div>'
    elif k=="steps":
        deco = '<div class="ring2" style="right:-160px;top:-60px;width:520px;height:520px"></div>'
        its = "".join(f'<div class="row"><span class="c" style="font-size:26px">STEP {n}</span>{E(t)}</div>' for n,t in c["items"])
        body = f'<h1 style="font-size:84px">{title(c["title"],0)}</h1><div class="rows">{its}</div>'
    elif k=="compare":
        a,b=c["a"],c["b"]
        body = f'<h1 style="font-size:84px">{title(c["title"],0)}</h1><div class="cmp"><div><h3>{E(a[0])}</h3><p>{E(a[1])}</p></div><div><h3>{E(b[0])}</h3><p>{E(b[1])}</p></div></div>'
    elif k=="close":
        deco = '<div class="ring2" style="left:-200px;bottom:-200px;width:620px;height:620px"></div><div class="ring2" style="right:-120px;top:-100px;width:420px;height:420px"></div>'
        hash_ = '<div class="hash">'+"".join(f'<span>{E(h)}</span>' for h in c["tags"].split())+'</div>' if c.get("tags") else ""
        note = f'<div class="note">{E(c["note"])}</div>' if c.get("note") else ""
        body = f'<h1 style="font-size:{fs(c["title"],86)}px">{title(c["title"],0)}</h1><div class="line">{E(c["line"])}</div>{hash_}{note}'
    ft = f'<div class="ft"><span class="logo">{STAR} CHEONGDAM STAR CLINIC</span><span class="dots">{dots}</span></div>' if theme!="lime" else f'<div class="ft"><span>{si+1} / 6 · {E(name)}</span><span class="dots">{dots}</span></div>'
    h = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{CSS1}</style></head>
<body class="{theme}">{deco}{hd}<div class="main">{body}</div>{ft}</body></html>'''
    return h

FONTS = """
@font-face{font-family:NK;font-weight:300;src:url('../fonts/Light.otf')}
@font-face{font-family:NK;font-weight:400;src:url('../fonts/r.otf')}
@font-face{font-family:NK;font-weight:500;src:url('../fonts/m.otf')}
@font-face{font-family:NK;font-weight:700;src:url('../fonts/n.otf')}
@font-face{font-family:NK;font-weight:900;src:url('../fonts/Black.otf')}
"""
BASE = FONTS + """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1080px;font-family:NK,sans-serif;position:relative;overflow:hidden;word-break:keep-all;background:var(--bg);color:var(--fg)}
.hd{position:absolute;left:60px;right:60px;top:48px;display:flex;justify-content:space-between;align-items:center;font-size:24px;letter-spacing:4px;text-transform:uppercase;color:var(--mut);font-weight:500;z-index:4}
.ft{position:absolute;left:60px;right:60px;bottom:40px;display:flex;justify-content:space-between;align-items:center;font-size:24px;letter-spacing:2px;color:var(--mut);font-weight:500;z-index:4}
.main{position:absolute;left:60px;right:60px;top:130px;bottom:110px;display:flex;flex-direction:column;justify-content:center;z-index:2}
h1{font-weight:900;line-height:1.22;letter-spacing:-2px;color:var(--hc,var(--fg))}
.line{font-size:34px;line-height:1.5;font-weight:400;margin-top:24px;color:var(--lc,var(--fg))}
.tag{align-self:flex-start;font-size:30px;font-weight:700;padding:10px 26px;border-radius:40px;margin-bottom:30px}
.it b{display:block;font-weight:900}.it em{display:block;font-style:normal;font-weight:400;font-size:.82em;opacity:.8;margin-top:4px}
.dec{position:absolute;z-index:1}
.hash{display:flex;flex-wrap:wrap;gap:14px;margin-top:38px}
.hash span{border-radius:60px;padding:12px 28px;font-size:30px;font-weight:700}
.note{margin-top:36px;font-size:23px;line-height:1.5;font-weight:300;padding-top:16px;border-top:1px solid currentColor;opacity:.8}
"""
SET_CSS = {
2: """
:root{--bg:#FFF1E6;--fg:#2a1208;--ac:#FF5A36;--ac2:#FFB703;--mut:#8a5a44}
body.close{--bg:#FF5A36;--fg:#fff;--mut:#ffe2d6}
.s2 .bar{position:absolute;left:0;top:0;bottom:0;width:28px;background:var(--ac);z-index:3}.close .bar{background:#2a1208}
.s2 .wm{position:absolute;right:30px;bottom:50px;font-size:440px;font-weight:900;color:rgba(255,90,54,.10);line-height:.8;letter-spacing:-20px}.close .wm{color:rgba(255,255,255,.12)}
.s2 .main{left:96px}.s2 .hd{left:96px}.s2 .ft{left:96px}
.s2 .tag{background:var(--ac);color:#fff}
.cvs,.its,.bbs{display:flex;flex-direction:column;gap:22px;margin-top:40px}
.band{display:flex;align-items:center;gap:26px;border:4px solid var(--fg);border-radius:20px;padding:20px 34px;font-size:46px;font-weight:900;box-shadow:8px 8px 0 var(--fg)}
.band i{font-style:normal;font-size:28px;opacity:.7}
.cv:nth-child(1){background:var(--ac);color:#fff}.cv:nth-child(2){background:var(--ac2)}.cv:nth-child(3){background:#fff}
.bb{background:#fff;border:4px solid var(--fg);border-radius:40px 40px 40px 8px;padding:26px 38px;font-size:36px;font-weight:700;line-height:1.4;box-shadow:8px 8px 0 var(--ac);max-width:860px}
.bb:nth-child(even){align-self:flex-end;border-radius:40px 40px 8px 40px;box-shadow:-8px 8px 0 var(--ac2)}
.it{display:flex;gap:24px;align-items:center;background:#fff;border:4px solid var(--fg);border-radius:20px;padding:18px 28px;box-shadow:8px 8px 0 var(--ac);font-size:36px;font-weight:700;line-height:1.3}
.it .n{flex:none;width:62px;height:62px;background:var(--ac);color:#fff;border-radius:14px;font-weight:900;font-size:30px;display:flex;align-items:center;justify-content:center}
.close .hash span{background:#2a1208;color:#fff}
""",
3: """
:root{--bg:#06172a;--fg:#e6f7ff;--ac:#3de0ff;--ac2:#7aa7ff;--mut:#6f93ad}
body.close{--bg:#3de0ff;--fg:#06172a;--mut:#0b3a55}
.s3 .arc{inset:0;background:repeating-radial-gradient(circle at 85% -8%,transparent 0 64px,rgba(61,224,255,.16) 65px 67px);-webkit-mask-image:linear-gradient(180deg,#000 0,transparent 75%);mask-image:linear-gradient(180deg,#000 0,transparent 75%)}
.close .arc{background:repeating-radial-gradient(circle at 85% -8%,transparent 0 64px,rgba(6,23,42,.18) 65px 67px)}
.s3 .wedge{left:300px;top:-200px;width:900px;height:900px;background:conic-gradient(from 160deg at 70% 8%,transparent 0 0deg,rgba(61,224,255,.22) 22deg,transparent 44deg);filter:blur(2px)}
.close .wedge{display:none}
h1{color:var(--hc,#fff)}.close h1{color:#06172a}
.tag{border:2px solid var(--ac);color:var(--ac)}
.cvs{display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px;margin-top:44px}
.cv{border:2px solid var(--ac);padding:22px 22px 26px;min-height:200px;font-size:34px;font-weight:700;line-height:1.35;display:flex;flex-direction:column;justify-content:space-between;background:rgba(61,224,255,.06);position:relative}
.cv i{font-style:normal;color:var(--ac);font-size:26px;letter-spacing:3px}
.its,.bbs{display:flex;flex-direction:column;margin-top:36px}
.it{display:flex;gap:26px;align-items:center;border-top:2px solid rgba(61,224,255,.45);padding:22px 4px;font-size:37px;font-weight:700;line-height:1.3}
.it:last-child{border-bottom:2px solid rgba(61,224,255,.45)}
.it .n{flex:none;color:var(--ac);font-weight:500;font-size:28px;letter-spacing:3px;width:66px}
.bbs{gap:20px}
.bb{border:2px solid rgba(61,224,255,.5);border-left:10px solid var(--ac);background:rgba(61,224,255,.07);padding:26px 34px;font-size:36px;font-weight:500;line-height:1.4}
.close .hash span{background:#06172a;color:#3de0ff}
""",
4: """
:root{--bg:#EFE9FF;--fg:#2a1760;--ac:#FF4F8B;--pu:#3b1f8e;--mut:#7d6bb5}
body{background:linear-gradient(180deg,var(--pu) 0 470px,#EFE9FF 470px 100%)}
body.close{background:linear-gradient(180deg,#FF4F8B 0 470px,#3b1f8e 470px 100%);--fg:#fff}
.s4 .hd{color:#cdbff5}.close .hd{color:#ffe0ec}
.s4 .ft{color:var(--mut)}.close .ft{color:#cdbff5}
.s4 .tt{position:absolute;left:60px;right:60px;top:120px;height:330px;display:flex;flex-direction:column;justify-content:center;z-index:2}
.s4 h1{color:#fff}.s4 .line{color:#e4dbff}
.s4 .bd{position:absolute;left:60px;right:60px;top:520px;bottom:110px;display:flex;flex-direction:column;justify-content:center;z-index:2;color:var(--fg)}
.s4 .tag{background:var(--ac);color:#fff}
.vs{position:absolute;left:50%;top:470px;width:150px;height:150px;margin:-75px 0 0 -75px;border-radius:50%;background:var(--ac);color:#fff;font-weight:900;font-size:56px;display:flex;align-items:center;justify-content:center;z-index:3;border:8px solid #EFE9FF}
.cvs,.its,.bbs{display:flex;flex-direction:column;gap:16px}
.cv{background:#fff;border-radius:16px;padding:20px 30px 20px 30px;font-size:35px;font-weight:700;border-left:12px solid var(--ac);display:flex;gap:20px;align-items:center}
.cv i{font-style:normal;color:var(--ac);font-size:26px}
.cv:nth-child(even){border-left-color:var(--pu)}
.its{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.its.one{grid-template-columns:1fr}
.it{background:#fff;border-top:10px solid var(--ac);border-radius:14px;padding:22px 24px;font-size:34px;font-weight:700;line-height:1.35;min-height:150px;display:flex;flex-direction:column;justify-content:space-between}
.it .n{color:var(--ac);font-size:26px;font-weight:900;letter-spacing:2px}
.bb{background:#fff;border-radius:30px 30px 30px 6px;padding:24px 34px;font-size:35px;font-weight:700;line-height:1.4;max-width:840px;box-shadow:0 6px 0 #d9cff7}
.bb:nth-child(even){align-self:flex-end;background:var(--pu);color:#fff;border-radius:30px 30px 6px 30px;box-shadow:0 6px 0 #24125f}
.cmp{display:flex;gap:20px}
.cmp>div{flex:1;border-radius:18px;padding:28px 26px;background:#fff}
.cmp h3{font-size:36px;font-weight:900;margin-bottom:14px;color:var(--pu)}
.cmp>div:last-child{background:var(--pu);color:#fff}.cmp>div:last-child h3{color:#ff9fc2}
.cmp p{font-size:31px;line-height:1.5;font-weight:500}
.close .hash span{background:#fff;color:#3b1f8e}
""",
5: """
:root{--bg:#F3E9DC;--fg:#3a2418;--ac:#C4572B;--ol:#6B7A3A;--mut:#8b6f5a}
body.close{--bg:#C4572B;--fg:#F8EEDC;--mut:#f2cdb7}
.s5 .hd span:first-child{background:var(--ac);color:#fff;padding:6px 16px;letter-spacing:3px}.close .hd span:first-child{background:#F8EEDC;color:var(--ac)}
.rings{right:-170px;top:60px;width:560px;height:560px;border-radius:50%;background:repeating-radial-gradient(circle,transparent 0 40px,rgba(196,87,43,.28) 41px 43px);}
.rings::after{content:"";position:absolute;left:0;right:0;top:50%;height:2px;background:rgba(196,87,43,.35)}
.rings::before{content:"";position:absolute;top:0;bottom:0;left:50%;width:2px;background:rgba(196,87,43,.35)}
.close .rings{background:repeating-radial-gradient(circle,transparent 0 40px,rgba(248,238,220,.3) 41px 43px)}
.s5 .tag{padding:0 0 10px;border-radius:0;border-bottom:4px solid var(--ac);color:var(--ac);font-size:32px}
.cvs,.its,.bbs{display:flex;flex-direction:column;margin-top:40px}
.cvs{flex-direction:row;gap:0;border:3px solid var(--fg)}
.cv{flex:1;padding:24px 22px;font-size:34px;font-weight:900;line-height:1.3;min-height:190px;display:flex;flex-direction:column;justify-content:space-between;border-right:3px solid var(--fg)}
.cv:last-child{border-right:0}.cv:nth-child(2){background:var(--ac);color:#fff}
.cv i{font-style:normal;font-size:26px;letter-spacing:3px;color:var(--ac)}.cv:nth-child(2) i{color:#fff}
.it{display:flex;align-items:center;gap:22px;border-bottom:3px dashed rgba(58,36,24,.45);padding:22px 4px;font-size:36px;font-weight:700;line-height:1.3}
.it:first-child{border-top:3px solid var(--fg)}
.it .n{flex:none;width:58px;height:58px;border-radius:50%;background:var(--ac);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:26px}
.it .tx{flex:1}.it::after{content:"→";font-size:44px;color:var(--ac);font-weight:300}
.bbs{gap:26px}
.bb{background:#FFE9A8;padding:30px 36px;font-size:36px;font-weight:700;line-height:1.4;box-shadow:6px 8px 0 rgba(58,36,24,.18);max-width:800px;transform:rotate(-1.5deg)}
.bb:nth-child(even){align-self:flex-end;transform:rotate(1.5deg);background:#F6C9A8}
.close .hash span{border:2px solid #F8EEDC}
""",
6: """
:root{--bg:#14161a;--fg:#f2efe6;--ac:#D4AF37;--mut:#8a8f98}
body.close{--bg:#D4AF37;--fg:#14161a;--mut:#4d4210}
.s6 .tl{left:96px;top:140px;bottom:120px;width:3px;background:linear-gradient(180deg,var(--ac),rgba(212,175,55,.2))}
.s6 .tag{border:2px solid var(--ac);color:var(--ac)}
.flow{display:flex;align-items:center;justify-content:space-between;margin-top:44px}
.flow .nd{width:150px;height:150px;border-radius:50%;border:3px solid var(--ac);display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:900;color:var(--ac)}
.flow .nd:nth-child(1){background:var(--ac);color:#14161a}
.flow .ar{color:var(--ac);font-size:34px}
.cvs{display:flex;flex-direction:column;gap:14px;margin-top:44px}
.cv{display:flex;gap:20px;align-items:center;font-size:36px;font-weight:700;padding:16px 28px;border-left:6px solid var(--ac);background:rgba(212,175,55,.08)}
.cv i{font-style:normal;color:var(--ac);font-size:28px;font-weight:900}
.its{position:relative;display:flex;flex-direction:column;gap:20px;margin-top:40px;padding-left:70px}
.it{position:relative;background:rgba(255,255,255,.05);border:2px solid rgba(212,175,55,.45);border-radius:14px;padding:22px 30px;font-size:37px;font-weight:700;line-height:1.3;display:flex;align-items:center;gap:22px}
.it::before{content:"";position:absolute;left:-70px;top:50%;width:70px;height:3px;background:var(--ac);opacity:.5}
.it .n{flex:none;margin-left:-82px;width:62px;height:62px;border-radius:50%;background:var(--ac);color:#14161a;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:22px;z-index:2;text-align:center;line-height:1.05}
.s6 .its{padding-left:92px}.s6 .it{margin-left:0}.it .n{margin-left:-124px;margin-right:0}
.it .tx{margin-left:0}
.s6 .it{padding-left:52px}
.close .hash span{background:#14161a;color:#D4AF37}
""",
}
def sp(t):
    if " - " in t:
        a,b=t.split(" - ",1); return f"<b>{E(a)}</b><em>{E(b)}</em>"
    return E(t)
def title2(t): return "<br>".join(E(x.strip()) for x in t.split("/"))

def cardN(si, ci, st):
    name,_,cards = st; c=cards[ci]; k=c["k"]; n=si+1
    cls = "close" if k=="close" else ""
    T = f'<h1 style="font-size:{fs(c["title"],86 if k!="cover" else 108)}px">{title2(c["title"])}</h1>'
    if c.get("line") and not (n==6 and k=="cover"): T += f'<div class="line">{E(c["line"])}</div>'
    if k=="cover": T = f'<div class="tag">{E(c["tag"])}</div>' + T
    C=""; deco=""
    if k=="cover":
        if n==6:
            parts=[x.strip() for x in c["line"].split("→")]
            C='<div class="flow">'+'<span class="ar">›</span>'.join(f'<div class="nd">{E(p)}</div>' for p in parts)+'</div>'
        C += '<div class="cvs">'+"".join(f'<div class="cv {"band" if n==2 else ""}"><i>0{i+1}</i>{E(t)}</div>' for i,t in enumerate(c["items"]))+'</div>'
    elif k=="bubbles":
        C='<div class="bbs">'+"".join(f'<div class="bb">{E(t)}</div>' for t in c["items"])+'</div>'
    elif k in ("list","steps"):
        items=c["items"]
        lab=lambda i,t: (f"STEP<br>{t[0]}" if k=="steps" else f"0{i+1}")
        txt=lambda t: E(t[1]) if k=="steps" else sp(t)
        cl = "its one" if (n==4 and len(items)!=4) else "its"
        C=f'<div class="{cl}">'+"".join(f'<div class="it"><span class="n">{lab(i,t)}</span><span class="tx">{txt(t)}</span></div>' for i,t in enumerate(items))+'</div>'
    elif k=="compare":
        a,b=c["a"],c["b"]
        C=f'<div class="cmp"><div><h3>{E(a[0])}</h3><p>{E(a[1])}</p></div><div><h3>{E(b[0])}</h3><p>{E(b[1])}</p></div></div>'
    elif k=="close":
        if c.get("tags"): C+='<div class="hash">'+"".join(f'<span>{E(h)}</span>' for h in c["tags"].split())+'</div>'
        if c.get("note"): C+=f'<div class="note">{E(c["note"])}</div>'
    if n==2: deco=f'<div class="bar"></div><div class="wm dec">0{ci+1}</div>'
    if n==3: deco='<div class="dec arc"></div><div class="dec wedge"></div>'
    if n==5: deco='<div class="dec rings"></div>'
    if n==6 and k not in ("close","cover"): deco='<div class="dec tl"></div>'
    if n==4:
        vs='<div class="vs">VS</div>' if k=="cover" else ""
        main=f'{vs}<div class="tt">{T}</div><div class="bd">{C}</div>'
        if k=="compare": main=f'<div class="tt">{T}</div><div class="bd">{C}</div>'
    else:
        main=f'<div class="main">{T}{C}</div>'
    hdr=f'<div class="hd"><span>Cheongdam Star Clinic</span><span>{E(name) if n in (2,5) else "Set 0"+str(n)}</span></div>'
    ftr=f'<div class="ft"><span>{n} / 6</span><span>{ci+1} / 5</span></div>'
    return f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{BASE}{SET_CSS[n]}</style></head><body class="s{n} {cls}">{deco}{hdr}{main}{ftr}</body></html>'

def card(si,ci,st):
    fn=f"set{si+1}_card{ci+1}.html"
    h = card1(si,ci,st,True) if si==0 else cardN(si,ci,st)
    open(os.path.join(OUT,fn),"w",encoding="utf-8").write(h); return fn

files=[card(si,ci,st) for si,st in enumerate(S) for ci in range(5)]
json.dump(files, open(os.path.join(OUT,"_files.json"),"w"))
print(len(files))
