from PIL import Image, ImageDraw, ImageFont
import math, os, subprocess
from pathlib import Path
from functools import lru_cache

BASE=Path(__file__).resolve().parent
ASSETS=BASE/'assets'
ASSETS.mkdir(exist_ok=True)
BG='#F5F1E8'; INK='#19332D'; INK2='#213C34'; WINE='#D45032'; RUST='#A9442A'; LIME='#E1EE9B'; SOFT='#D1D9C8'; MUTED='#62756B'; CREAM='#F8F5E9'; DARK='#17342E'; MINT='#B5D1AC'; PALE='#E6EBDC'; SHADOW='#3C614F'
font_paths={x:subprocess.check_output(['fc-match',x,'-f','%{file}']).decode() for x in ['Archivo Black','Space Grotesk','IBM Plex Mono']}
@lru_cache(None)
def font(family,size,weight=None):
    f=ImageFont.truetype(font_paths[family],size)
    if weight and family=='Space Grotesk':f.set_variation_by_axes([weight])
    return f

def txt(d,xy,string,size=24,color=INK,family='Space Grotesk',weight=500,spacing=0,anchor=None):
    f=font(family,size,weight)
    if spacing:
        x,y=xy
        for ch in string:
            d.text((x,y),ch,font=f,fill=color,anchor=anchor)
            x+=d.textlength(ch,font=f)+spacing
        return x
    d.text(xy,string,font=f,fill=color,anchor=anchor)
    return d.textlength(string,font=f)

def line(d,coords,color=INK,width=2):d.line(coords,fill=color,width=width,joint='curve')
def roundrect(d,box,radius,fill,outline=None,width=1):d.rounded_rectangle(box,radius=radius,fill=fill,outline=outline,width=width)

def schematic(d,cx,cy,radius,angle=0,mobile=False):
    for r,c,w in [(radius,SHADOW,2),(radius-30,'#617A58',2),(radius-64,'#4F7159',2)]:d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=c,width=w)
    for a in [12,55,111,176,250,315]:
        rr=math.radians(a)
        x1=cx+math.cos(rr)*(radius-64); y1=cy+math.sin(rr)*(radius-64)
        x2=cx+math.cos(rr)*radius; y2=cy+math.sin(rr)*radius
        line(d,[(x1,y1),(x2,y2)],SHADOW,1)
    for a,rr,col in [(angle,radius,WINE),(angle+2.45,radius-30,LIME),(angle+4.4,radius-64,CREAM)]:
        px=int(cx+math.cos(a)*rr);py=int(cy+math.sin(a)*rr)
        d.ellipse((px-7,py-7,px+7,py+7),fill=col)
    mid='A·T'; size=57 if mobile else 78
    f=font('Archivo Black',size)
    box=d.textbbox((0,0),mid,font=f)
    d.text((cx-(box[2]-box[0])/2,cy-(box[3]-box[1])/2-10),mid,font=f,fill=CREAM)

def hero(desktop=True,frame=0):
    w,h=(1200,430) if desktop else (720,650)
    im=Image.new('RGB',(w,h),BG);d=ImageDraw.Draw(im)
    if desktop:
        # Meticulous index grid, deliberately not a card layout.
        for x in range(52,745,24):
            for y in range(40,328,24):
                if (x+y)%3==0:d.ellipse((x,y,x+2,y+2),fill='#DEE1D1')
        line(d,[(42,31),(748,31)],SOFT,2)
        txt(d,(52,46),'A/T',24,RUST,'Archivo Black')
        txt(d,(129,52),'THE BUILD LOG   /   2026',17,INK,'IBM Plex Mono')
        txt(d,(52,103),'ABHAY',125,INK,'Archivo Black')
        txt(d,(50,224),'TIWARI.',125,INK,'Archivo Black')
        # Animated coral cursor sweep below the title.
        line(d,[(53,346),(679,346)],SOFT,2)
        x2=53+int(485*abs(math.sin(math.pi*frame/36)))
        roundrect(d,(53,342,x2+34,350),3,WINE)
        txt(d,(53,366),'I make complex things feel simple.',27,INK,'Space Grotesk',700)
        txt(d,(56,405),'WEB  /  AI  /  SYSTEMS  /  PROBLEM SOLVING',12,MUTED,'IBM Plex Mono')
        d.rectangle((777,24,1174,406),fill=DARK)
        # Fine lattice and offset registration marks.
        for y in range(70,370,23):line(d,[(792,y),(1160,y)],'#285044',1)
        for x in range(804,1160,23):line(d,[(x,69),(x,346)],'#285044',1)
        txt(d,(802,41),'FIELD NOTES / NO. 026',14,LIME,'IBM Plex Mono')
        schematic(d,976,206,112,2*math.pi*frame/36,False)
        txt(d,(806,340),'NOW EXPLORING',13,MINT,'IBM Plex Mono')
        phrases=['AI learning tools','full-stack systems','clean algorithms']
        which=(frame//12)%3;step=frame%12;shown=phrases[which][:max(1,min(len(phrases[which]),step*3))]
        txt(d,(805,360),shown,20,CREAM,'Space Grotesk',700)
        if frame%8<5:txt(d,(805+int(d.textlength(shown,font=font('Space Grotesk',20,700)))+4,359),'▌',19,WINE,'Space Grotesk',700)
        d.polygon([(1117,24),(1174,24),(1174,83)],fill=WINE)
        txt(d,(1125,37),'++',16,DARK,'IBM Plex Mono')
    else:
        for x in range(41,685,27):
            for y in range(62,374,27):
                if (x+y)%4==0:d.ellipse((x,y,x+2,y+2),fill='#DEE1D1')
        line(d,[(36,30),(684,30)],SOFT,2)
        txt(d,(45,43),'A/T',25,RUST,'Archivo Black')
        txt(d,(138,51),'THE BUILD LOG   /   2026',17,INK,'IBM Plex Mono')
        txt(d,(38,108),'ABHAY',132,INK,'Archivo Black')
        txt(d,(34,233),'TIWARI.',132,INK,'Archivo Black')
        x2=42+int(380*abs(math.sin(math.pi*frame/36)))
        line(d,[(42,368),(678,368)],SOFT,2)
        roundrect(d,(42,364,x2+30,372),3,WINE)
        txt(d,(43,383),'Making the complex feel simple.',32,INK,'Space Grotesk',700)
        d.rectangle((0,433,720,650),fill=DARK)
        for x in range(20,705,28):line(d,[(x,434),(x,649)],'#285044',1)
        for y in range(452,650,28):line(d,[(0,y),(720,y)],'#285044',1)
        txt(d,(42,456),'NOW EXPLORING',16,MINT,'IBM Plex Mono')
        phrases=['AI + WEB','JAVA + DSA','SYSTEMS']
        which=(frame//12)%3;step=frame%12;shown=phrases[which][:max(1,min(len(phrases[which]),step*2))]
        txt(d,(42,494),shown,42,CREAM,'Archivo Black')
        if frame%8<5:txt(d,(42+int(d.textlength(shown,font=font('Archivo Black',42)))+6,494),'▌',39,WINE,'Space Grotesk',700)
        txt(d,(44,602),'BUILD  /  TEST  /  LEARN  /  REPEAT',17,LIME,'IBM Plex Mono')
        schematic(d,581,528,87,2*math.pi*frame/36,True)
        d.polygon([(625,433),(720,433),(720,528)],fill=WINE)
    return im

def make_gif(name,mobile=False):
    frames=[hero(not mobile,i) for i in range(36)]
    still=frames[10]
    still.save(ASSETS/(name+'-still.png'),optimize=True)
    # One global palette reduces flash and keeps tiny details consistent.
    pal=frames[0].quantize(colors=64,method=Image.Quantize.FASTOCTREE,dither=Image.Dither.NONE)
    pframes=[frame.quantize(palette=pal,dither=Image.Dither.NONE) for frame in frames]
    pframes[0].save(ASSETS/(name+'.gif'),save_all=True,append_images=pframes[1:],loop=0,duration=105,optimize=True,disposal=1,comment=b'Abhay Tiwari / Build log animation')
    print(name,'GIF KB',round((ASSETS/(name+'.gif')).stat().st_size/1024),'still KB',round((ASSETS/(name+'-still.png')).stat().st_size/1024))

def mini_icon(desktop,idx,d,x,y):
    if idx==0:
        # A note becoming a flashcard.
        d.polygon([(x+32,y+29),(x+248,y+11),(x+257,y+139),(x+43,y+158)],fill='#729578')
        roundrect(d,(x,y,x+204,y+136),12,CREAM)
        txt(d,(x+20,y+15),'Q.',44,INK,'Archivo Black')
        line(d,[(x+20,y+79),(x+165,y+79)],SOFT,5)
        line(d,[(x+20,y+99),(x+125,y+99)],SOFT,5)
        d.ellipse((x+159,y+96,x+181,y+118),fill=WINE)
    elif idx==1:
        d.ellipse((x-4,y-13,x+175,y+166),outline='#8EAB61',width=3)
        d.ellipse((x+37,y+27,x+136,y+126),outline=INK,width=5)
        for j in range(8):
            xx=x+5+j*21
            yy=y+78-int(39*math.sin(j*1.35))
            if j:line(d,[(oldx,oldy),(xx,yy)],WINE,5)
            oldx,oldy=xx,yy
        d.ellipse((x+107,y+66,x+119,y+78),fill=INK)
        txt(d,(x+18,y+149),'SIMULATED TELEMETRY',12,INK,'IBM Plex Mono')
    else:
        roundrect(d,(x-10,y+9,x+213,y+140),20,CREAM)
        d.polygon([(x+40,y+135),(x+55,y+151),(x+78,y+135)],fill=CREAM)
        roundrect(d,(x+54,y-10,x+250,y+78),18,LIME)
        d.polygon([(x+204,y+76),(x+218,y+95),(x+228,y+77)],fill=LIME)
        txt(d,(x+6,y+36),'...',54,INK,'Archivo Black')
        txt(d,(x+92,y+0),'AI',35,INK,'Archivo Black')

def poster(idx,mobile=False):
    w,h=(720,330) if mobile else (1200,230)
    backs=[DARK,LIME,'#DF6A4A']; bg=backs[idx]
    col=CREAM if idx in (0,2) else INK
    desc=[('STUDYAI','Notes in. Flashcards + quizzes out.','AI LEARNING / REACT + GEMINI'),('DIGITAL TWIN','Transformer health, simulated and visualized.','PROTOTYPE / SIMULATED SENSOR DATA'),('INTERVIEW COPILOT','An experiment in AI-assisted interview prep.','WEB APPLICATION / JAVA + JS')]
    title,sub,kicker=desc[idx]
    im=Image.new('RGB',(w,h),bg);d=ImageDraw.Draw(im)
    # Full-bleed project identities rather than identical cards.
    if mobile:
        x=40
        txt(d,(x,24),f'0{idx+1} / SELECTED WORK',17,col,'IBM Plex Mono')
        line(d,[(x,62),(678,62)],col,2)
        if idx==2:
            txt(d,(x,77),'INTERVIEW',61,col,'Archivo Black');txt(d,(x,141),'COPILOT',61,col,'Archivo Black')
            yy=220
        elif idx==1:
            txt(d,(x,95),'DIGITAL',70,col,'Archivo Black');txt(d,(x,168),'TWIN',70,col,'Archivo Black')
            yy=254
        else:
            txt(d,(x,101),title,92,col,'Archivo Black'); yy=217
        short_sub=['Notes → flashcards → quizzes.','Transformer health, visualized.','AI-assisted interview practice.'][idx]
        txt(d,(x,yy),short_sub,30,col,'Space Grotesk',700)
        txt(d,(x,301),kicker,16,col,'IBM Plex Mono')
        if idx==0: mini_icon(mobile,idx,d,496,158)
        elif idx==1:mini_icon(mobile,idx,d,502,61)
        else:mini_icon(mobile,idx,d,507,159)
        # cover accidental collision: mobile icons intentionally crop into panel edge
    else:
        for xx in range(900,1200,23):
            for yy in range(22,210,23):
                if (xx+yy)%3==0:d.ellipse((xx,yy,xx+2,yy+2),fill='#345B4B' if idx==0 else '#B8D679' if idx==1 else '#E99075')
        x=54
        txt(d,(x,23),f'0{idx+1}  /  SELECTED WORK',16,col,'IBM Plex Mono')
        txt(d,(x,62),title,69,col,'Archivo Black')
        txt(d,(x,147),sub,26,col,'Space Grotesk',700)
        line(d,[(x,197),(1147,197)],col,1)
        txt(d,(x,207),kicker,13,col,'IBM Plex Mono')
        mini_icon(False,idx,d,871,37 if idx!=1 else 30)
    return im

def make_poster(idx,name):
    for mobile in (False,True):
        im=poster(idx,mobile)
        path=ASSETS/(name+('-mobile' if mobile else '')+'.png')
        im.save(path,optimize=True)
        print(path.name,round(path.stat().st_size/1024),'KB')

def pulse():
    frames=[]
    for i in range(16):
        im=Image.new('RGB',(42,28),DARK);d=ImageDraw.Draw(im)
        # Eye outline and one iris blink / scan pulse.
        d.arc((4,5,38,23),200,340,fill=LIME,width=3);d.arc((4,5,38,23),20,160,fill=LIME,width=3)
        r=4+(1 if i%8<4 else 0)
        d.ellipse((21-r,14-r,21+r,14+r),fill=WINE)
        if i in (2,3,10,11):d.line((3,25,39,25),fill=WINE,width=2)
        frames.append(im.quantize(colors=16))
    frames[0].save(ASSETS/'visitor-pulse.gif',save_all=True,append_images=frames[1:],duration=120,loop=0,optimize=True,disposal=1)

def tape(mobile=False):
    w,h=(720,95) if mobile else (1200,105)
    frames=[]
    for i in range(24):
        im=Image.new('RGB',(w,h),WINE);d=ImageDraw.Draw(im)
        line(d,[(0,0),(w,0)],INK,3);line(d,[(0,h-2),(w,h-2)],INK,3)
        text='BUILD   •   TEST   •   LEARN   •   REPEAT   •   '
        ft=font('Archivo Black',36 if mobile else 43)
        ts=int(d.textlength(text,font=ft));shift=int((i/24)*ts)
        for n in range(-1,5):d.text((24+n*ts-shift,19 if mobile else 22),text,font=ft,fill=CREAM)
        frames.append(im)
    pal=frames[0].quantize(colors=24)
    frames=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in frames]
    name='build-tape-mobile' if mobile else 'build-tape'
    frames[0].save(ASSETS/(name+'.gif'),save_all=True,append_images=frames[1:],duration=90,loop=0,optimize=True,disposal=1)
    frames[3].convert('RGB').save(ASSETS/(name+'-still.png'),optimize=True)
    print(name,round((ASSETS/(name+'.gif')).stat().st_size/1024),'KB')

def footer(mobile=False):
    w,h=(720,240) if mobile else (1200,225)
    im=Image.new('RGB',(w,h),LIME);d=ImageDraw.Draw(im)
    for xx in range(0,w,27):
        for yy in range(0,h,27):
            if (xx+yy)%4==0:d.ellipse((xx,yy,xx+2,yy+2),fill='#BCD47B')
    if mobile:
        txt(d,(41,23),"LET'S BUILD",70,INK,'Archivo Black')
        txt(d,(41,109),'SOMETHING REAL.',62,INK,'Archivo Black')
        txt(d,(42,191),'HAVE A GOOD PROBLEM? MY INBOX IS OPEN.',18,INK,'IBM Plex Mono')
        d.ellipse((576,181,669,274),fill=WINE);txt(d,(597,184),'↗',60,CREAM,'Space Grotesk',700)
    else:
        txt(d,(52,33),'GOT A PROBLEM',83,INK,'Archivo Black')
        txt(d,(52,116),'WORTH SOLVING?',83,INK,'Archivo Black')
        d.ellipse((1011,33,1169,191),fill=WINE);txt(d,(1040,41),'↗',103,CREAM,'Space Grotesk',700)
    return im

def stack_map(mobile=False):
    if mobile:
        w,h=720,485
        im=Image.new('RGB',(w,h),'#EDECDD');d=ImageDraw.Draw(im)
        txt(d,(37,26),'MY TOOLBOX',51,INK,'Archivo Black')
        txt(d,(40,89),'CODE / DESIGN / SHIP',17,RUST,'IBM Plex Mono')
        items=[('01  INTERFACES','React · JavaScript · Tailwind · HTML/CSS'),('02  BEHIND THE SCENES','Node.js · Express · MongoDB'),('03  THINKING TOOLS','Java · C++ · data structures'),('04  DAILY DRIVERS','Git · GitHub · Postman · Figma')]
        for i,(name,tools) in enumerate(items):
            y=145+i*82
            line(d,[(40,y-15),(678,y-15)],SOFT,2)
            txt(d,(40,y),name,23,RUST,'IBM Plex Mono')
            txt(d,(40,y+29),tools,31,INK,'Space Grotesk',700)
        return im
    w,h=1200,302
    im=Image.new('RGB',(w,h),'#EDECDD');d=ImageDraw.Draw(im)
    txt(d,(48,20),'MY',69,INK,'Archivo Black')
    txt(d,(48,85),'TOOLBOX',69,INK,'Archivo Black')
    txt(d,(51,242),'CODE / DESIGN / SHIP',17,RUST,'IBM Plex Mono')
    items=[('INTERFACES','React · JavaScript · Tailwind · HTML/CSS'),('BEHIND THE SCENES','Node.js · Express · MongoDB'),('THINKING TOOLS','Java · C++ · data structures'),('DAILY DRIVERS','Git · GitHub · Postman · Figma')]
    for i,(name,tools) in enumerate(items):
        y=42+i*64
        line(d,[(410,y-11),(1150,y-11)],SOFT,2)
        txt(d,(410,y),f'0{i+1}  {name}',18,RUST,'IBM Plex Mono')
        txt(d,(410,y+25),tools,23,INK,'Space Grotesk',700)
    return im

if __name__=='__main__':
    make_gif('hero',False);make_gif('hero-mobile',True)
    for i,n in enumerate(('studyai','digital-twin','interview-copilot')):make_poster(i,n)
    tape(False);tape(True);pulse()
    footer(False).save(ASSETS/'footer.png',optimize=True)
    footer(True).save(ASSETS/'footer-mobile.png',optimize=True)
    stack_map(False).save(ASSETS/'toolbox.png',optimize=True)
    stack_map(True).save(ASSETS/'toolbox-mobile.png',optimize=True)
    print('TOTAL assets',sum(p.stat().st_size for p in ASSETS.iterdir())/1024/1024,'MB')
