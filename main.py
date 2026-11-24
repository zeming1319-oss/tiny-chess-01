import json as j,os as o,urllib.request as u
U=o.environ.get("MAKEFUN_ENV_URL","")
B=[0]*128
s=1
c=e=-1
w=b=v=0
H=[]
V=(0,100,320,330,500,900,0)
N=(33,31,18,14,-33,-31,-18,-14)
D=(17,15,-17,-15)
O=(1,-1,16,-16)
K=O+D
C={0:13,7:14,112:7,119:11}
S=[[0]*128 for _ in range(13)]
for p in range(1,7):
 S[p+6]=[V[p]if p>1 else 100+8*((x>>4)-1)+((x>>4)==6)*12+(1<(x&15)<5)*6 for x in range(128)]
 S[6-p]=[-S[p+6][119-x]for x in range(128)]
def A(k,sd):
 for d in(-15,-17):
  t=k+d*sd
  if not t&136 and B[t]==sd:return 1
 for d in N:
  t=k+d
  if not t&136 and B[t]==2*sd:return 1
 for d in K:
  t=k+d
  if not t&136 and B[t]==6*sd:return 1
 for ds in D,O:
  for d in ds:
   t=k+d
   while not t&136:
    v=B[t]
    if v:
     v*=sd
     if v==5 or(v==3 and ds is D)or(v==4 and ds is O):return 1
     break
    t+=d
 return 0
def G():
 m=[];sd=s;a=m.append
 for f in range(128):
  if f&136:continue
  p=B[f]
  if p*sd<=0:continue
  g=p*sd
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
    elif t==e:a((f,t,0))
  elif g<3 or g==6:
   for d in N if g==2 else K:
    t=f+d
    if not t&136 and B[t]*sd<=0:a((f,t,0))
  else:
   for d in(D,O,K)[g-3]:
    t=f+d
    while not t&136:
     if B[t]*sd>0:break
     a((f,t,0))
     if B[t]:break
     t+=d
 return m
Q={}
def P(m):
 global s,c,e,w,b,v
 f,t,p=m;p=B[f];q=B[t]
 B0=tuple(B)
 H.append([B0,s,c,e,w,b,v,0])
 v-=S[p+6][f]
 if q:v-=S[q+6][t]
 if p==s and t==e and(t-f)%16:
  v-=S[6-s][t-16*s];B[t-16*s]=0
 B[f]=0
 n=p
 if m[2]>1:n=m[2]if p>0 else-m[2]
 B[t]=n;v+=S[n+6][t]
 if p==6*s:
  if s>0:w=t
  else:b=t
  if abs(t-f)==2:
   r=f+3 if t>f else f-4
   u=f+1 if t>f else f-1
   k=B[r];B[r]=0;B[u]=k
   v+=S[k+6][u]-S[k+6][r]
 n=c&(C.get(f,15)&C.get(t,15))
 if p==6*s:n&=12 if s>0 else 3
 c=n
 e=(f+t)//2 if p==s and abs(t-f)==32 else-1
 k=(tuple(B),-s,c,e)
 Q[k]=Q.get(k,0)+1
 H[-1][7]=k
 s=-s
def Z():
 global s,c,e,w,b,v
 h=H.pop()
 B[:]=h[0]
 s,c,e,w,b,v=h[1:7]
 Q[h[7]]-=1
def F(t):
 global s,c,e,w,b,v
 B[:]=[0]*128
 p=t.split()
 for rr,row in enumerate(p[0].split("/")):
  f=0
  for ch in row:
   if ch.isdigit():f+=int(ch);continue
   x=(7-rr)*16+f
   q="PNBRQK".find(ch.upper())+1
   if ch.islower():q=-q
   B[x]=q
   if q==6:w=x
   if q==-6:b=x
   f+=1
 s=1 if p[1]=="w" else-1
 c=sum((ch in p[2])<<n for n,ch in enumerate("KQkq"))
 e=I.get(p[3],-1)
 v=sum(S[B[x]+6][x]for x in range(128)if B[x])
M=200000
n=X=0
HH={}
def W(d,al,be):
 global n
 n+=1
 if n>X:1/0
 i=A(w if s>0 else b,-s)
 g=-2*M
 if d<=0:
  if i:d=1
  else:
   g=v if s>0 else-v
   if g>=be:return g
   if g>al:al=g
   d=0
 l=sorted(((-(V[abs(B[m[1]])]*16+m[2]*90)if B[m[1]]or m[2]else 0)-HH.get(m,0),m)for m in(G()if d>0 else[m for m in G()if B[m[1]]or m[2]]))
 y=0
 for _,m in l:
  P(m)
  if A(w if s<0 else b,s):Z();continue
  y=1
  sc=-W(d-1,-be,-al)
  Z()
  if sc>g:g=sc
  if sc>al:
   al=sc
   if al>=be:
    HH[m]=HH.get(m,0)+d*d
    break
 if d>0 and not y:return-M if i else 0
 if Q.get((tuple(B),s,c,e),0)>=3:return 0
 return g
I={chr(97+(x&15))+str((x>>4)+1):x for x in range(128)if not x&136}
J={x:n for n,x in I.items()}
def T():
 global n,X
 l=G()
 if not l:return None
 n=0;X=M*10
 bm=l[0]
 for d in range(1,4):
  al=-2*M;cm=0
  try:
   for m in l:
    P(m)
    if A(w if s<0 else b,s):Z();continue
    sc=-W(d-1,-2*M,-al);Z()
    if sc>al:al=sc;cm=m
   if cm:bm=cm
   if not cm and d<3:return None
  except ZeroDivisionError:break
 return bm
def p(p,b):return j.load(u.urlopen(u.Request(U+p,data=b)))
def r():
 while 1:
  g=p("/game",b"{}")
  while g["status"]=="your_move":
   F(g["start_fen"])
   for x in g["moves"]:P((I[x[:2]],I[x[2:4]],"  nbrq".find(x[4])if len(x)>4 else 0))
   m=T()
   l=g["legal_moves"]
   x=J[m[0]]+J[m[1]]+"q"*(m[2]>0)if m else l[0]
   if x not in l:x=l[0]
   g=p("/move",('{"game":%d,"move":"%s"}'%(g["game"],x)).encode())
  if g["status"]=="done":break
if U:r()
