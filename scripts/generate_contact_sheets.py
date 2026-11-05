#!/usr/bin/env python3
"""Temporary image review sheets: numbered thumbnails and a UTF-8 base64 image for review."""
from pathlib import Path
import base64
import json
import re
from PIL import Image, ImageDraw, ImageFont, ImageOps

root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'data/media-manifest.json').read_text())
order=['uncategorized','fabrication-fieldwork','mak-studio','final-boards','architecture-diagrams','pvamu-presentation','design-presentation','lotus-flower','designhive','interiors','generative-research']
items=[f for f in manifest['files'] if f.get('mediaType')=='IMAGE' and f.get('localPath') and (root/f['localPath']).exists()]
items.sort(key=lambda f:(order.index(f.get('projectId')) if f.get('projectId') in order else 999, f.get('createdDate') or '',f.get('name','')))
W,H=270,244;cols,rows=4,5;per=cols*rows
output=root/'review';output.mkdir(exist_ok=True)
try:font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
except OSError:font=ImageFont.load_default()
try:big=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',16)
except OSError:big=font
index=[]
for n in range(0,len(items),per):
 page=n//per
 sheet=Image.new('RGB',(W*cols,H*rows),(246,246,244))
 d=ImageDraw.Draw(sheet)
 for j,item in enumerate(items[n:n+per]):
  i=n+j;col=j%cols;row=j//cols
  x=col*W;y=row*H
  path=root/item['localPath']
  try:
   with Image.open(path) as img:
    img=ImageOps.exif_transpose(img).convert('RGB')
    img.thumbnail((W-18,H-59),Image.Resampling.LANCZOS)
    sheet.paste(img,(x+(W-img.width)//2,y+3+(H-59-img.height)//2))
  except Exception:
   d.text((x+10,y+55),"Unreadable image",fill=(170,0,0),font=font)
  d.rectangle((x,y+H-53,x+W-2,y+H-2),fill=(244,245,244))
  d.text((x+6,y+H-51),f"#{i:03d}   {item['projectId'][:25]}",fill=(25,42,37),font=big)
  name=item['name']
  if len(name)>39:name=name[:36]+"..."
  d.text((x+7,y+H-28),name,fill=(30,30,30),font=font)
  d.rectangle((x,y,x+W-1,y+H-1),outline=(180,180,180),width=1)
  index.append({'number':i,'page':page,'fileName':item['name'],'projectId':item['projectId'],'localPath':item['localPath'],'sourceUrl':item['sourceUrl']})
 out=output/f"sheet-{page:02d}.jpg"
 sheet.save(out,quality=74,optimize=True,subsampling=0)
 (output/f"sheet-{page:02d}.txt").write_text(base64.b64encode(out.read_bytes()).decode('ascii'))
 print(f"Sheet {page:02d}: {len(items[n:n+per])} items, {out.stat().st_size} bytes")
(output/'index.json').write_text(json.dumps(index,indent=2))
print('TOTAL:',len(index),'images /',(len(items)+per-1)//per,'sheets')
