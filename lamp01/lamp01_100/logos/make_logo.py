# Generate smooth logo footprints (gold = F.Cu+F.Mask, silk = F.SilkS) from a black-on-white PNG.
# Run with KiCad's bundled Python, e.g.:
#   /Applications/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 make_logo.py eunicorn_670.png ../logos.pretty 9,10,11,12,14
# The last argument is a comma-separated list of heights in mm.
# Smooth logo footprint: marching squares on the anti-aliased image, RDP simplify, nest holes, fracture.
import wx, sys, pcbnew, math
src, lib, sizes = sys.argv[1], sys.argv[2], [float(s) for s in sys.argv[3].split(',')]
app=wx.App(False); img=wx.Image(src); W,H=img.GetWidth(),img.GetHeight()
g=[[255.0]*(W+2) for _ in range(H+2)]           # padded with white
for y in range(H):
    row=g[y+1]
    for x in range(W): row[x+1]=(img.GetRed(x,y)+img.GetGreen(x,y)+img.GetBlue(x,y))/3
T=128.0; ins=lambda x,y: g[y][x]<T
segs={}
def add(a,b):
    segs.setdefault(a,[]).append(b); segs.setdefault(b,[]).append(a)
for y in range(H+1):
    for x in range(W+1):
        c=(ins(x,y)<<3)|(ins(x+1,y)<<2)|(ins(x+1,y+1)<<1)|ins(x,y+1)
        if c in (0,15): continue
        t=('h',x,y); r=('v',x+1,y); b=('h',x,y+1); l=('v',x,y)
        center=(g[y][x]+g[y][x+1]+g[y+1][x]+g[y+1][x+1])/4<T
        tab={1:[(l,b)],2:[(b,r)],3:[(l,r)],4:[(t,r)],6:[(t,b)],7:[(l,t)],8:[(l,t)],9:[(t,b)],11:[(t,r)],12:[(l,r)],13:[(b,r)],14:[(l,b)],
             5:[(l,t),(b,r)] if not center else [(l,b),(t,r)], 10:[(t,r),(l,b)] if not center else [(l,t),(b,r)]}
        for a,bb in tab[c]: add(a,bb)
def pt(k):
    d,x,y=k
    if d=='h': a,b=g[y][x],g[y][x+1]; return (x+(T-a)/(b-a) if b!=a else x+0.5, y)
    a,b=g[y][x],g[y+1][x]; return (x, y+(T-a)/(b-a) if b!=a else y+0.5)
loops=[]; seen=set()
for k0 in list(segs):
    if k0 in seen: continue
    loop=[k0]; seen.add(k0); prev=None; cur=k0
    while True:
        nxt=[n for n in segs[cur] if n!=prev and n not in seen]
        if not nxt: break
        prev,cur=cur,nxt[0]; seen.add(cur); loop.append(cur)
    if len(loop)>8: loops.append([pt(k) for k in loop])
def rdp(p,eps):
    if len(p)<3: return p
    a,b=p[0],p[-1]; dx,dy=b[0]-a[0],b[1]-a[1]; L=math.hypot(dx,dy) or 1e-9
    i,dm=0,0
    for j in range(1,len(p)-1):
        d=abs(dy*(p[j][0]-a[0])-dx*(p[j][1]-a[1]))/L
        if d>dm: i,dm=j,d
    return rdp(p[:i+1],eps)[:-1]+rdp(p[i:],eps) if dm>eps else [a,b]
def rdpc(l,eps):
    m=len(l)//2
    return rdp(l[:m+1],eps)[:-1]+rdp(l[m:]+[l[0]],eps)[:-1]
loops=[rdpc(l,0.35) for l in loops]
area=lambda p: sum(p[i][0]*p[i-1][1]-p[i-1][0]*p[i][1] for i in range(len(p)))/2
def inside(q,p):
    c=False; x,y=q
    for i in range(len(p)):
        (x1,y1),(x2,y2)=p[i],p[i-1]
        if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1)+x1: c=not c
    return c
loops=[l for l in loops if abs(area(l))>4]
info=[]
for i,l in enumerate(loops):
    q=l[0]; q=(q[0]+1e-3,q[1]+1e-3)
    par=[j for j,m in enumerate(loops) if j!=i and abs(area(m))>abs(area(l)) and inside(l[0],m)]
    info.append(par)
xs=[p[0] for l in loops for p in l]; ys=[p[1] for l in loops for p in l]
x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys)
for Hmm in sizes:
    s=Hmm/(y1-y0); cx,cy=(x0+x1)/2,(y0+y1)/2
    V=lambda p: pcbnew.VECTOR2I(pcbnew.FromMM((p[0]-cx)*s),pcbnew.FromMM((p[1]-cy)*s))
    depth={}
    for i,l in enumerate(loops):
        d=len(info[i]); depth.setdefault(d,pcbnew.SHAPE_POLY_SET())
        tgt=depth[d]; tgt.NewOutline(); n=tgt.OutlineCount()-1
        for p in l: tgt.Append(V(p), n)
    ps=pcbnew.SHAPE_POLY_SET()
    for d in sorted(depth):          # even depth = ink, odd depth = hole
        depth[d].Simplify()
        if d%2==0: ps.BooleanAdd(depth[d])
        else: ps.BooleanSubtract(depth[d])
    print('  depths',{d:depth[d].OutlineCount() for d in depth})
    ps.Fracture()
    for kind,layers in (('gold',(pcbnew.F_Cu,pcbnew.F_Mask)),('silk',(pcbnew.F_SilkS,))):
        name='eunicorn_%s_%gmm'%(kind,Hmm)
        fp=pcbnew.FOOTPRINT(None); fp.SetFPID(pcbnew.LIB_ID('logos',name))
        fp.SetReference('LOGO1'); fp.SetValue(name); fp.Reference().SetVisible(False); fp.Value().SetVisible(False)
        fp.Value().SetLayer(pcbnew.F_Fab)
        fp.SetAttributes(pcbnew.FP_BOARD_ONLY|pcbnew.FP_EXCLUDE_FROM_BOM|pcbnew.FP_EXCLUDE_FROM_POS_FILES)
        fp.SetLibDescription('Eunicorn logo, %g mm tall, traced from eunicorn_670.png'%Hmm)
        for L in layers:
            for o in range(ps.OutlineCount()):   # one fp_poly per (fractured) outline
                one=pcbnew.SHAPE_POLY_SET(); one.AddOutline(ps.Outline(o))
                sh=pcbnew.PCB_SHAPE(fp); sh.SetShape(pcbnew.SHAPE_T_POLY); sh.SetFilled(True)
                sh.SetWidth(0); sh.SetPolyShape(one); sh.SetLayer(L); fp.Add(sh)
        pcbnew.PCB_IO_KICAD_SEXPR().FootprintSave(lib, fp)
    print('%g mm: %.2f x %.2f mm, %d outline(s), %d pts'%(Hmm,(x1-x0)*s,Hmm,ps.OutlineCount(),ps.FullPointCount()))
