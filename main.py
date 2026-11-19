import json as j,os as o,urllib.request as u
from base64 import b64decode as D
U=o.environ.get("MAKEFUN_ENV_URL","")
B=[0]*128
sm=1
ca=ep=-1
kw=kb=ev=0
H=[]
V=(0,100,320,330,500,900,0)
KN=(33,31,18,14,-33,-31,-18,-14)
DI=(17,15,-17,-15)
OR=(1,-1,16,-16)
KD=OR+DI
CD={0:13,7:14,112:7,119:11}
SC=[[0]*128 for _ in range(13)]
for p in range(1,7):
 SC[p+6]=[V[p]if p>1 else 100+8*((s>>4)-1)+((s>>4)==6)*12+(1<(s&15)<5)*6 for s in range(128)]
 SC[6-p]=[-SC[p+6][119-s]for s in range(128)]

def S(f):
 global sm,ca,ep,kw,kb,ev
 w=f.split();ev=0;r=7;c=0
 B[:]=[0]*128
 for ch in w[0]:
  if ch=="/":r-=1;c=0
  elif ch.isdigit():c+=int(ch)
  else:
   v="pnbrqk".find(ch.lower())+1
   sd=(1,-1)[ch>"Z"]
   s=c+16*r
   B[s]=v*sd;ev+=SC[v*sd+6][s]
   if v==6:
    if sd>0:kw=s
    else:kb=s
   c+=1
 sm=1 if w[1]=="w" else-1
 ca=sum(1<<i for i,x in enumerate("KQkq")if x in w[2])
 ep=ord(w[3][0])-97+16*(int(w[3][1])-1)if w[3]!="-" else-1
 H.clear()

def A(s,sd):
 for d in(-15,-17):
  t=s+d*sd
  if not t&136 and B[t]==sd:return 1
 for d in KN:
  t=s+d
  if not t&136 and B[t]==2*sd:return 1
 for d in KD:
  t=s+d
  if not t&136 and B[t]==6*sd:return 1
 for ds in DI,OR:
  for d in ds:
   t=s+d
   while not t&136:
    v=B[t]
    if v:
     v*=sd
     if v==5 or(v==3 and ds is DI)or(v==4 and ds is OR):return 1
     break
    t+=d
 return 0

def G():
 ms=[];sd=sm;a=ms.append
 for f in range(128):
  if f&136:continue
  pc=B[f]
  if pc*sd<=0:continue
  g=pc*sd
  if g==1:
   d=16*sd;t=f+d
   q=t>>4==(7,0)[sd<0]
   if not t&136 and not B[t]:
    a((f,t,5)if q else(f,t,0))
    if not q and f>>4==(1,6)[sd<0] and not B[t+d]:a((f,t+d,0))
   for dd in(d-1,d+1):
    t=f+dd
    if t&136:continue
    if B[t]*sd<0:a((f,t,5 if q else 0))
    elif t==ep:a((f,t,0))
  elif g<3 or g==6:
   for d in KN if g==2 else KD:
    t=f+d
    if not t&136 and B[t]*sd<=0:a((f,t,0))
  else:
   for d in(DI,OR,KD)[g-3]:
    t=f+d
    while not t&136:
     if B[t]*sd>0:break
     a((f,t,0))
     if B[t]:break
     t+=d
 return ms

def P(mv):
 global sm,ca,ep,kw,kb,ev
 f,t,p=mv
 pc=B[f];cp=B[t]
 H.append((tuple(B),sm,ca,ep,kw,kb,ev))
 ev-=SC[pc+6][f]
 if cp:ev-=SC[cp+6][t]
 if pc==sm and t==ep and(t-f)%16:
  ev-=SC[6-sm][t-16*sm];B[t-16*sm]=0
 B[f]=0
 np=p*sm if p else pc
 B[t]=np;ev+=SC[np+6][t]
 if pc==6*sm:
  if sm>0:kw=t
  else:kb=t
  if abs(t-f)==2:
   rf=f+3 if t>f else f-4
   rt=f+1 if t>f else f-1
   rk=B[rf];B[rf]=0;B[rt]=rk
   ev+=SC[rk+6][rt]-SC[rk+6][rf]
 nc=ca&(CD.get(f,15)&CD.get(t,15))
 if pc==6*sm:nc&=12 if sm>0 else 3
 ca=nc
 ep=(f+t)//2 if pc==sm and abs(t-f)==32 else-1
 sm=-sm

def O():
 global sm,ca,ep,kw,kb,ev
 b0,sm,ca,ep,kw,kb,ev=H.pop()
 B[:]=b0

M=100000
n=X=0
def W(d,al,be):
 global n
 n+=1
 if n>X:1/0
 ic=A(kw if sm>0 else kb,-sm)
 best=-2*M
 if d<=0:
  if ic:d=1
  else:
   best=ev if sm>0 else-ev
   if best>=be:return best
   if best>al:al=best
   d=0
 lm=sorted((-(V[abs(B[m[1]])]*16+m[2]*90)if B[m[1]]or m[2]else 0,m)for m in(G()if d>0 else[m for m in G()if B[m[1]]or m[2]]))
 anyl=0
 for _,m in lm:
  P(m)
  if A(kw if sm<0 else kb,sm):O();continue
  anyl=1
  v=-W(d-1,-be,-al)
  O()
  if v>best:best=v
  if v>al:
   al=v
   if al>=be:break
 if d>0 and not anyl:return-M if ic else 0
 return best

IX={chr(97+(s&15))+str((s>>4)+1):s for s in range(128)if not s&136}
IS={s:n for n,s in IX.items()}

def th():
 global n,X
 lm=G()
 if not lm:return None
 n=0;X=M
 best=lm[0]
 for d in range(1,64):
  al=-2*M;cur=0
  try:
   for m in lm:
    P(m)
    if A(kw if sm<0 else kb,sm):O();continue
    v=-W(d-1,-2*M,-al);O()
    if v>al:al=v;cur=m
   if cur:best=cur
   if not cur and d<3:return None
  except ZeroDivisionError:break
 return best

def po(p,b):return j.load(u.urlopen(u.Request(U+p,data=b)))

def run():
 while 1:
  g=po("/game",b"{}")
  while g["status"]=="your_move":
   S(g["start_fen"])
   for x in g["moves"]:P((IX[x[:2]],IX[x[2:4]],"  nbrq".find(x[4])if len(x)>4 else 0))
   m=th()
   l=g["legal_moves"]
   x=IS[m[0]]+IS[m[1]]+"q"*(m[2]>0)if m else l[0]
   g=po("/move",('{"game":%d,"move":"%s"}'%(g["game"],x)).encode())
  if g["status"]=="done":break
if U:run()
