from pathlib import Path
import html
ROOT=Path(__file__).resolve().parents[1]/'public/assets/projects'
def rect(x,y,w,h,fill,rx=0,stroke='none'):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'
def text(x,y,t,size=14,color='#29313d',weight=400):return f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}">{html.escape(t)}</text>'
def line(x,y,x2,y2,color):return f'<path d="M{x} {y}H{x2}" stroke="{color}"/>' if y==y2 else f'<path d="M{x} {y}L{x2} {y2}" stroke="{color}"/>'
def browser():return rect(0,0,900,560,'#eee9f7',12)+rect(22,22,856,516,'white',12,'#e5ddef')+rect(22,22,856,28,'#f9f7fc',12)+''.join(f'<circle cx="{38+i*12}" cy="36" r="3" fill="{c}"/>' for i,c in enumerate(['#dacfe9','#ddd3eb','#e3daee']))+rect(260,30,380,12,'#f0eaf6',4)+text(379,39,'CONCEPT UI PREVIEW',6,'#b1a1c2',600)
def output(name,s):ROOT.joinpath(name+'.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 560" role="img" aria-label="'+name+' illustrative interface concept">'+s+'</svg>')
# Multivendor delivery storefront.
s=browser()+text(55,83,'FastSheba',23,'#ed7046',700)+text(270,81,'Deliver to',9,'#9b8f8a')+text(270,95,'Your neighbourhood',11,'#51433f',600)+text(585,86,'Browse  •  Help',10,'#897b77')+rect(748,66,96,30,'#ed7046',7)+text(766,85,'Your basket',10,'white',600)
s+=rect(45,116,810,190,'#fff1e8',12)+text(75,161,'Your city.',33,'#50372b',700)+text(75,201,'Delivered.',37,'#ed7046',700)+text(77,226,'Local favourites, a little closer.',12,'#a28375')+rect(77,247,239,33,'white',6)+text(90,268,'What are you looking for?',9,'#bcaaa1')+rect(277,252,32,23,'#ed7046',5)+text(288,268,'→',14,'white')
# Stylised bag and grocery shapes, native vector artwork.
s+=rect(595,170,145,110,'#ed7046',13)+f'<path d="M625 175v-20a43 43 0 0 1 85 0v20" fill="none" stroke="#c85a34" stroke-width="8"/>'+rect(642,204,50,12,'#ffd4ba',6)+f'<ellipse cx="591" cy="274" rx="48" ry="12" fill="#f3d9c6"/><path d="M560 259q-16-38 12-58q36 22 12 58" fill="#96b784"/><path d="M570 267q-30-17-32-48q36-1 42 28" fill="#b9d19d"/>'+rect(742,214,54,65,'#ffc477',9)
s+=text(55,342,'What’s on your list?',20,'#44362e',700)+text(745,341,'View all →',10,'#ed7046')
for i,(name,color) in enumerate([('Groceries','#e5f0df'),('Fresh meals','#ffe8d6'),('Daily essentials','#ece6f9')]):
 x=55+i*267;s+=rect(x,362,251,128,'white',9,'#f0e7e0')+rect(x+13,375,84,83,color,8)+rect(x+33,397,44,46,'#ffffffaa',8)+text(x+110,412,name,13,'#655046',600)+text(x+110,434,'Explore stores',9,'#af9d93')+text(x+110,456,'Browse →',9,'#ed7046',600)
s+=text(56,519,'Illustrative design direction • Not a live project screenshot',8,'#b5a59d');output('fastsheba',s)
# Travel site with a vector landscape.
s=browser()+text(55,84,'RT Destination',21,'#276c6c',700)+text(420,84,'Destinations     Packages     About',10,'#8d9b98')+rect(741,64,103,31,'#276c6c',6)+text(759,84,'Plan a trip →',10,'white',600)
s+=rect(45,113,810,235,'#dfedeb',11)+f'<path d="M403 348V200q103-122 223-23t229 27v144" fill="#a4c3b7"/><path d="M418 348V290q125-128 237-53t200-2v113" fill="#7ba69a"/><path d="M447 348q137-102 265-39t143-30v69" fill="#61978d"/><path d="M700 348q-92-50-67-70t87-3q65 8 40 30t-17 43" fill="#c1dfdf"/><circle cx="761" cy="155" r="23" fill="#fbf1d4"/>'+text(76,164,'There’s more',31,'#285858',700)+text(76,204,'out there.',37,'#285858',700)+text(78,231,'Find your next beautiful escape.',12,'#6e9590')+rect(78,254,125,33,'#276c6c',6)+text(94,275,'Explore packages →',10,'white',600)
s+=rect(77,328,746,49,'white',8,'#e1eae7')+text(98,349,'DESTINATION',7,'#9fb2ab',600)+text(98,365,'Where do you want to go?',10,'#688278')+text(370,349,'TRAVEL STYLE',7,'#9fb2ab',600)+text(370,365,'Explore your options',10,'#688278')+rect(677,337,133,31,'#276c6c',5)+text(711,357,'Find a trip →',10,'white',600)
s+=text(55,414,'A little inspiration for your next trip.',18,'#355e58',700)
for i,(name,c) in enumerate([('Hills & trails','#c6ddd0'),('Coastal escapes','#bddce2'),('City discoveries','#d8d3c3')]):
 x=55+i*267;s+=rect(x,433,251,59,c,8)+f'<path d="M{x} 485l45-32 45 32 44-42 68 42 49-22v29H{x}Z" fill="#ffffff44"/>'+text(x+15,519,name,11,'#6a8279',600)
output('rt-destination',s)
# Investment admin UI.
s=browser()+rect(22,50,157,488,'#28324b',0)+text(48,88,'IMAS',25,'white',700)+text(48,107,'Investment workspace',8,'#98a5bf')
for i,t in enumerate(['Overview','Investments','Transactions','Reports','Settings']):
 y=154+i*47
 if i==0:s+=rect(36,y-22,128,33,'#46537b',6)
 s+=rect(48,y-11,10,10,'#7e8fb5',3)+text(70,y-2,t,10,'#d5dcec' if i==0 else '#9aa7c2')
s+=text(208,89,'Portfolio overview',22,'#36415a',700)+text(208,109,'A clearer view of investment administration.',10,'#9ca5b6')+rect(724,70,122,30,'#f5f6fa',6)+text(744,89,'Workspace view',9,'#94a0b6')
for i,(title,num) in enumerate([('Portfolio value','Overview'),('Active records','Tracked'),('Reporting','Organised')]):
 x=208+i*216;s+=rect(x,137,202,83,'#f8f9fc',8,'#e9edf5')+text(x+16,163,title,10,'#9ca7bb')+text(x+16,193,num,20,'#566585',600)
s+=rect(208,239,414,226,'white',8,'#e8edf4')+text(226,265,'Portfolio activity',12,'#6c7a93',600)
for y in [300,340,380,420]:s+=line(228,y,601,y,'#eef1f7')
s+='<path d="M228 418L282 399 328 407 376 367 419 373 463 330 509 345 550 300 601 285V435H228Z" fill="#efedff"/><path d="M228 418L282 399 328 407 376 367 419 373 463 330 509 345 550 300 601 285" fill="none" stroke="#8e7ac6" stroke-width="3"/>'
s+=rect(640,239,206,226,'#f9fafc',8,'#e9edf5')+text(658,265,'Allocation overview',11,'#77839a',600)+f'<circle cx="742" cy="347" r="55" fill="none" stroke="#e2e6ef" stroke-width="22"/><circle cx="742" cy="347" r="55" fill="none" stroke="#a294d4" stroke-width="22" stroke-dasharray="190 346" transform="rotate(-90 742 347)"/>'+text(718,353,'View',14,'#8b95ac',600)+text(208,500,'Illustrative interface • No actual financial data',9,'#abb3c4')
output('imas',s)
print('Created three clearly labelled project UI concept previews.')
