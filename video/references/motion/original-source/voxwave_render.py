import re,math,numpy as np,cairosvg,os
from svgpathtools import parse_path
s=open('/mnt/user-data/uploads/Logo_oficial.svg').read()
NM={'#02527d':'teal','#0a2a3b':'navy','#fe653c':'orange'}
sym={};word=[]
for col,d in re.findall(r'<path fill="(#[0-9a-f]+)" d="([^"]*)"',s):
    if col=='#f9f9f9':continue
    for sp in parse_path(d).continuous_subpaths():
        if sp.bbox()[3]<760: sym[NM[col]]=(sp,sp.d())
        else: word.append((col,sp.d()))
WC={}
for c,d in word:WC[c]=WC.get(c,'')+d
N=360;H=N//2;S=.7
def contour(sp):
    M=6000;pts=np.array([sp.point(i/M) for i in range(M)]);P=np.c_[pts.real,pts.imag]
    seg=np.r_[0,np.cumsum(np.hypot(*np.diff(np.r_[P,P[:1]],axis=0).T))];T=seg[-1]
    tg=np.arange(N)*T/N;x=np.interp(tg,seg,np.r_[P[:,0],P[0,0]]);y=np.interp(tg,seg,np.r_[P[:,1],P[0,1]])
    Q=np.c_[(x-627)*S+960,(y-635)*S+540]
    a=sum(Q[i,0]*Q[(i+1)%N,1]-Q[(i+1)%N,0]*Q[i,1] for i in range(N))
    if a<0:Q=Q[::-1]
    m=int(np.argmin(Q[:,0]));Q=np.roll(Q,-m,axis=0)
    T=np.roll(Q,-3,axis=0)-np.roll(Q,3,axis=0);L=np.hypot(T[:,0],T[:,1])[:,None];L[L==0]=1
    return Q,np.c_[-T[:,1],T[:,0]]/L
KEYS=['orange','navy','teal'];C=[contour(sym[k][0]) for k in KEYS]
COL={'orange':'#FF6E42','navy':'#092634','teal':'#004E72'};FILL={'orange':'#fe653c','navy':'#0a2a3b','teal':'#02527d'}
def sm(a,b,t):
    t=min(1,max(0,(t-a)/(b-a)));return t*t*(3-2*t)
def ease(t):return 4*t**3 if t<.5 else 1-(-2*t+2)**3/2
SY=[[.95,.12,.4],[1.3,.14,.65],[1.65,.12,.5],[2.15,.16,.95],[2.5,.13,.75],[2.85,.14,1],[3.6,.14,.55],[3.95,.15,.85],[4.25,.14,.6],[4.6,.2,.6],[5.0,.22,.35]]
def speech(t):
    v=.05*sm(.6,1,t)*(.5+.5*math.sin(7*t))
    v+=.22*sm(.9,1.3,t)*(1-sm(3,3.2,t))+.2*sm(3.45,3.7,t)*(1-sm(4.3,4.7,t))
    for a,w,k in SY:v+=k*math.exp(-((t-a)/w)**2)
    return min(1.1,v)
ph=[0,1.7,3.1];fq=[3.2,2.6,3.9];gq=[6.5,5.3,7.4];cw=[.19,.23,.16];off=[0,-.06,.07];sd=[0,.08,.16]
def amp(k,u,t):
    s=speech(t-sd[k]);c=.5+off[k]+.05*math.sin(.8*t+k*2);x=(u-c)/cw[k];w=math.exp(-x*x)
    r1=.5+.5*math.sin(fq[k]*6.283*(u-c)+1.3*math.sin(1.7*t+ph[k])+ph[k])
    r2=.5+.5*math.sin(gq[k]*6.283*(u-c)-1.1*math.sin(1.1*t+2*ph[k]))
    return 300*s*w*(.62*r1+.38*r2)
def pathD(P):
    mid=lambda a,b:"%.1f %.1f"%((a[0]+b[0])/2,(a[1]+b[1])/2)
    d="M"+mid(P[N-1],P[0])
    for i in range(N):d+="Q%.1f %.1f %s"%(P[i][0],P[i][1],mid(P[i],P[(i+1)%N]))
    return d+"Z"
TR='translate(960 540) scale(.7) translate(-627 -635)'
def svg(t):
    v=[1,sm(1.8,3,t),sm(2.2,3.4,t)];syn=sm(4.0,5.2,t);damp=1-.6*sm(4.6,5.8,t);q=sm(4.5,6.4,t);p=ease(q);w=16-14*q
    b=round(249*sm(6.1,7.1,t));o=[]
    for i in (1,2,0):
        k=KEYS[i];P=[]
        for j in range(N):
            side=-1 if j<=H else 1;u=(j if j<=H else N-j)/H
            A=amp(i,u,t);A+=(amp(0,u,t)-A)*syn;A*=damp*v[i]
            x=480+u*960;y=540+side*A;c=C[i][0][j]+C[i][1][j]*w/2;P.append((x+(c[0]-x)*p,y+(c[1]-y)*p))
        o.append((k,pathD(P),v[i]*(1-sm(6.8,7.4,t))))
    out='<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><rect width="1920" height="1080" fill="rgb(%d,%d,%d)"/>'%(b,b,b)
    out+='<g transform="%s" opacity="%.3f">'%(TR,sm(6.4,7.2,t))+''.join('<path fill="%s" d="%s"/>'%(FILL[k],sym[k][1]) for k in('navy','teal','orange'))+'</g>'
    out+='<g transform="%s" opacity="%.3f">'%(TR,sm(7.2,7.9,t))+''.join('<path fill="%s" d="%s"/>'%(c,d) for c,d in WC.items())+'</g>'
    out+=''.join('<path fill="none" stroke="%s" stroke-width="%.2f" stroke-linejoin="round" stroke-linecap="round" stroke-opacity="%.3f" d="%s"/>'%(COL[k],w,op,d) for k,d,op in o)
    return out+'</svg>'
if __name__=='__main__':
    os.makedirs('frames',exist_ok=True);FPS=30;END=9.5;n=int(END*FPS)+1
    for f in range(n):
        cairosvg.svg2png(bytestring=svg(min(END,f/FPS)).encode(),write_to='frames/%04d.png'%f)
    print(n)
