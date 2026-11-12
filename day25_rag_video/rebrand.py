"""Swap the cool navy/blue palette for the Plural Labs crimson / gold / cream brand."""
import re, glob
HEX = {
 '#2dd4bf':'#2fb872','#8e9bc4':'#cfa999','#ffd23f':'#f5b700','#ff4d6d':'#e63946','#38bdf8':'#ffd9a0','#04223a':'#3b0a10',
 '#a78bfa':'#f7a1b0','#160b3a':'#3b0a10','#0b1130':'#24050a','#dfe6ff':'#fff1dc','#56628c':'#8f6a62','#3a4687':'#7a2a33',
 '#1c2559':'#4a1018','#111a3f':'#3a0a12','#eef2ff':'#fff8ee','#cfd8ff':'#f6e2cc','#cdd6ff':'#f6e2cc','#cdd6f7':'#f6e2cc',
 '#cfd7ff':'#f6e2cc','#d5ddfa':'#f6e2cc','#e8ecff':'#fff1dc','#aab4dd':'#d9b8a6','#9aa5cf':'#d9b8a6','#0d1433':'#26050a',
 '#ccfbf1':'#d9f7e6','#7dd3fc':'#ffd9a0','#1d2a6e':'#55121c','#151a35':'#3b0a10','#c9d1ee':'#e8d7c4','#c6cfee':'#e8d7c4',
 '#c5cdea':'#e8d7c4','#c4b5fd':'#f7c9a8','#0c3b3a':'#0f3a24','#134e4a':'#155a37','#123b39':'#0f3a24','#1b2558':'#4a0f18',
 '#16205a':'#4a0e17','#172152':'#4a0e17','#141d4a':'#3a0a12','#141a3a':'#300810','#121a40':'#300810','#121a46':'#300810',
 '#1a2463':'#4a0e17','#0f1740':'#2c060c','#101943':'#2c060b','#2a3a8f':'#7a1622','#2c3878':'#6e1e29','#2a3570':'#6e1e29',
 '#3a4ba8':'#8a2430','#4053b5':'#9b2a35','#0f2a5a':'#4a1a10','#12306a':'#5a2414','#5a6bd0':'#c2484f','#0b1030':'#2a0509',
 '#060a1c':'#1a0306','#0a1030':'#2a0509','#121c4a':'#4a0a12','#5b3df5':'#9b1b23','#5b7bd5':'#c9963b','#3b82f6':'#b07a2a',
 '#e0f2fe':'#fff1dc','#d7f5ef':'#d9f7e6','#0f6256':'#0b5a33','#1a1f3d':'#3b0a10','#4a5175':'#6b4a44','#f7f9ff':'#fff8ee',
 '#f4f6ff':'#fff8ee','#062a26':'#062a16','#06231f':'#062a16','#a3e635':'#f5b700',
}
RGB = {'255,77,109':'230,57,70','56,189,248':'255,217,160','45,212,191':'47,184,114','91,61,245':'155,27,35',
       '14,165,233':'245,183,0','140,160,255':'255,214,170','5,8,24':'28,3,7','120,140,220':'240,180,150',
       '125,211,252':'255,217,160','255,210,63':'245,183,0'}
files = glob.glob('src/*.css') + glob.glob('src/*.html') + ['src/components.js', 'src/main.js'] + glob.glob('src/scenes/*.js')
for f in files:
    s = open(f).read(); o = s
    s = re.sub(r'#[0-9a-fA-F]{6}\b', lambda m: HEX.get(m.group(0).lower(), m.group(0)), s)
    s = re.sub(r'rgba\((\d+,\d+,\d+)', lambda m: 'rgba(' + RGB.get(m.group(1), m.group(1)), s)
    if s != o: open(f, 'w').write(s); print('rebranded', f)
