from pathlib import Path
p=Path('index.html')
s=p.read_text()
old="const dims=['Cultura','Desenvolvimento','Experiência','Eficiência','Dados','Prevenção'];\nconst goalBtns="
new="const dims=['Cultura','Desenvolvimento','Experiência','Eficiência','Dados','Prevenção'];\nconst roadmapButtons=[...document.querySelectorAll('.initiative')];\nroadmapButtons.forEach(b=>b.addEventListener('click',()=>b.classList.toggle('active')));\nconst goalBtns="
# Remove the earlier declaration/listener if present, then insert once immediately before simulator engine.
s=s.replace("const roadmapButtons=[...document.querySelectorAll('.initiative')];\nroadmapButtons.forEach(b=>b.addEventListener('click',()=>b.classList.toggle('active')));\n",'',1)
if old not in s: raise SystemExit('anchor not found')
s=s.replace(old,new,1)
p.write_text(s)
