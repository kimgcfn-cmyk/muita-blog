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

CSS = """
@font-face{font-family:NK;font-weight:400;src:url('../fonts/r.otf')}
@font-face{font-family:NK;font-weight:500;src:url('../fonts/m.otf')}
@font-face{font-family:NK;font-weight:700;src:url('../fonts/n.otf')}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1080px;font-family:NK,sans-serif;color:#1B2A4A;background:#F7F4EC;position:relative;overflow:hidden;word-break:keep-all}
.bar{position:absolute;left:0;top:0;width:100%;height:14px;background:var(--ac)}
.head{position:absolute;left:80px;right:80px;top:56px;display:flex;justify-content:space-between;font-size:26px;font-weight:500;color:#7a8394}
.head b{color:#1B2A4A;font-weight:700}
.main{position:absolute;left:80px;right:80px;top:130px;bottom:120px;display:flex;flex-direction:column;justify-content:center}
.foot{position:absolute;left:80px;right:80px;bottom:44px;display:flex;justify-content:space-between;font-size:24px;color:#8b93a1}
.dots i{display:inline-block;width:14px;height:14px;border-radius:50%;background:#d8d3c4;margin-left:8px}
.dots i.on{background:var(--ac);width:34px;border-radius:8px}
h1{font-weight:700;line-height:1.28;letter-spacing:-1px}
.line{font-size:34px;line-height:1.5;color:#4a5468;margin-top:26px;font-weight:500}
.ac{color:var(--ac)}
.tag{display:inline-block;align-self:flex-start;background:#1B2A4A;color:#fff;font-size:32px;font-weight:500;padding:12px 28px;border-radius:40px;margin-bottom:36px}
.items{margin-top:36px;display:flex;flex-direction:column;gap:14px}
.it{display:flex;align-items:center;gap:24px;background:#fff;border-radius:22px;padding:20px 32px;font-size:37px;font-weight:500;box-shadow:0 4px 14px rgba(27,42,74,.07)}
.it .n{flex:none;width:58px;height:58px;border-radius:50%;background:var(--ac);color:#fff;font-weight:700;font-size:30px;display:flex;align-items:center;justify-content:center}
.it .d{flex:none;width:16px;height:16px;border-radius:50%;background:var(--ac)}
.bub{background:#fff;border-radius:34px 34px 34px 6px;padding:34px 40px;font-size:37px;font-weight:500;line-height:1.4;box-shadow:0 4px 14px rgba(27,42,74,.08);border:3px solid var(--ac);max-width:920px}
.bub:nth-child(even){align-self:flex-end;border-radius:34px 34px 6px 34px}
.bubs{display:flex;flex-direction:column;gap:30px;margin-top:56px}
.cmp{display:flex;gap:28px;margin-top:48px}
.cmp>div{flex:1;background:#fff;border-radius:26px;padding:40px 34px;box-shadow:0 4px 14px rgba(27,42,74,.08)}
.cmp h3{font-size:42px;color:#fff;background:var(--ac);display:inline-block;padding:8px 22px;border-radius:14px;margin-bottom:26px}
.cmp:last-child{}
.cmp p{font-size:36px;line-height:1.55;font-weight:500}
.cmp>div:last-child h3{background:#1B2A4A}
.closeb{background:#1B2A4A;color:#fff}
.closeb .head{color:#9aa4b8}.closeb .head b{color:#fff}
.closeb .foot{color:#7d879c}.closeb .dots i{background:#3b4a6b}.closeb .dots i.on{background:var(--ac)}
.closeb .line{color:#d5dae6}
.tags{margin-top:44px;font-size:32px;color:var(--ac);font-weight:500;line-height:1.8}
.note{position:absolute;left:0;right:0;bottom:0;font-size:23px;color:#aab3c6;line-height:1.5;border-top:1px solid #3b4a6b;padding-top:16px}
.rule{width:90px;height:8px;background:var(--ac);border-radius:4px;margin-bottom:34px}
"""
def size(title, base):
    n = max(len(x.strip()) for x in title.split("/"))
    return base if n<=11 else base-6 if n<=14 else base-14 if n<=17 else base-22 if n<=22 else base-30

def card(si, ci, st):
    name, ac, cards = st
    c = cards[ci]; k = c["k"]; cls = "closeb" if k=="close" else ""
    dots = "".join('<i class="on"></i>' if i==ci else "<i></i>" for i in range(5))
    body = ""
    if k=="cover":
        its = "".join(f'<div class="it"><span class="n">{i+1}</span>{E(t)}</div>' for i,t in enumerate(c["items"]))
        body = f'<div class="tag">{E(c["tag"])}</div><h1 style="font-size:{size(c["title"],104)}px">{br(c["title"])}</h1><div class="line">{E(c["line"])}</div><div class="items">{its}</div>'
    elif k=="bubbles":
        its = "".join(f'<div class="bub">{E(t)}</div>' for t in c["items"])
        body = f'<div class="rule"></div><h1 style="font-size:{size(c["title"],80)}px">{br(c["title"])}</h1><div class="bubs">{its}</div>'
    elif k=="list":
        its = "".join(f'<div class="it"><span class="d"></span>{E(t)}</div>' for t in c["items"])
        line = f'<div class="line">{E(c["line"])}</div>' if c.get("line") else ""
        body = f'<div class="rule"></div><h1 style="font-size:{size(c["title"],80)}px">{br(c["title"])}</h1>{line}<div class="items">{its}</div>'
    elif k=="steps":
        its = "".join(f'<div class="it"><span class="n" style="width:auto;padding:0 22px;height:56px;border-radius:30px;font-size:26px;white-space:nowrap">STEP {n}</span>{E(t)}</div>' for n,t in c["items"])
        body = f'<div class="rule"></div><h1 style="font-size:84px">{br(c["title"])}</h1><div class="items">{its}</div>'
    elif k=="compare":
        a,b = c["a"],c["b"]
        body = f'<div class="rule"></div><h1 style="font-size:84px">{br(c["title"])}</h1><div class="cmp"><div><h3>{E(a[0])}</h3><p>{E(a[1])}</p></div><div><h3>{E(b[0])}</h3><p>{E(b[1])}</p></div></div>'
    elif k=="close":
        extra = f'<div class="tags">{E(c["tags"])}</div>' if c.get("tags") else ""
        note = f'<div class="note">{E(c["note"])}</div>' if c.get("note") else ""
        body = f'<div class="rule"></div><h1 style="font-size:{size(c["title"],84)}px">{br(c["title"])}</h1><div class="line">{E(c["line"])}</div>{extra}{note}'
    h = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>:root{{--ac:{ac}}}{CSS}</style></head>
<body class="{cls}"><div class="bar"></div>
<div class="head"><b>청담별의원</b><span>{si+1} / 6 · {E(name)}</span></div>
<div class="main">{body}</div>
<div class="foot"><span>종아리신경차단</span><span class="dots">{dots}</span></div></body></html>'''
    fn = f"set{si+1}_card{ci+1}.html"
    open(os.path.join(OUT, fn), "w", encoding="utf-8").write(h)
    return fn

files = [card(si,ci,st) for si,st in enumerate(S) for ci in range(5)]
json.dump(files, open(os.path.join(OUT,"_files.json"),"w"))
print(len(files))
