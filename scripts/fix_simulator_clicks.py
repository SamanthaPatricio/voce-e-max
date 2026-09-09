from pathlib import Path
p=Path('index.html')
s=p.read_text()
# Os cards e objetivos usam onclick inline para seleção visual robusta.
s=s.replace('class="initiative" data-status=', 'onclick="this.classList.toggle(\'active\')" class="initiative" data-status=')
s=s.replace('class="initiative active" data-status=', 'onclick="this.classList.toggle(\'active\')" class="initiative active" data-status=')
s=s.replace('class="goalBtn active" data-goal=', 'onclick="document.querySelectorAll(\'.goalBtn\').forEach(x=>x.classList.remove(\'active\'));this.classList.add(\'active\')" class="goalBtn active" data-goal=')
s=s.replace('class="goalBtn" data-goal=', 'onclick="document.querySelectorAll(\'.goalBtn\').forEach(x=>x.classList.remove(\'active\'));this.classList.add(\'active\')" class="goalBtn" data-goal=')
# Remove listeners antigos para evitar toggle duplo.
s=s.replace("roadmapButtons.forEach(b=>b.addEventListener('click',()=>b.classList.toggle('active')));\n",'')
s=s.replace("goalBtns.forEach(b=>b.addEventListener('click',()=>{goalBtns.forEach(x=>x.classList.remove('active'));b.classList.add('active')}));\n",'')
# CORREÇÃO PRINCIPAL: o motor ainda referencia estas coleções; recria-as antes do cálculo.
anchor='function renderAlignment(selected){'
decls="const roadmapButtons=[...document.querySelectorAll('.initiative')];\nconst goalBtns=[...document.querySelectorAll('.goalBtn')];\n"
if 'const roadmapButtons=' not in s:
    s=s.replace(anchor,decls+anchor,1)
elif 'const goalBtns=' not in s:
    s=s.replace(anchor,"const goalBtns=[...document.querySelectorAll('.goalBtn')];\n"+anchor,1)
# Garante type=button.
s=s.replace('<button class="generateRoadmap">','<button type="button" class="generateRoadmap">')
p.write_text(s)
