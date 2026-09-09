from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
# Limpa onclick duplicado criado por execuções anteriores.
s=re.sub(r'(onclick="this\.classList\.toggle\(\'active\'\)")\s+\1', r'\1', s)
s=re.sub(r'(onclick="document\.querySelectorAll\(\'.goalBtn\'\)\.forEach\(x=>x\.classList\.remove\(\'active\'\)\);this\.classList\.add\(\'active\'\)")\s+\1', r'\1', s)
# Garante seleção visual robusta.
s=s.replace('class="initiative" data-status=', 'onclick="this.classList.toggle(\'active\')" class="initiative" data-status=')
s=s.replace('class="initiative active" data-status=', 'onclick="this.classList.toggle(\'active\')" class="initiative active" data-status=')
s=s.replace('class="goalBtn active" data-goal=', 'onclick="document.querySelectorAll(\'.goalBtn\').forEach(x=>x.classList.remove(\'active\'));this.classList.add(\'active\')" class="goalBtn active" data-goal=')
s=s.replace('class="goalBtn" data-goal=', 'onclick="document.querySelectorAll(\'.goalBtn\').forEach(x=>x.classList.remove(\'active\'));this.classList.add(\'active\')" class="goalBtn" data-goal=')
# Coleções usadas pelo motor.
anchor='function renderAlignment(selected){'
if 'const roadmapButtons=' not in s: s=s.replace(anchor,"const roadmapButtons=[...document.querySelectorAll('.initiative')];\n"+anchor,1)
if 'const goalBtns=' not in s: s=s.replace(anchor,"const goalBtns=[...document.querySelectorAll('.goalBtn')];\n"+anchor,1)
# Substitui o listener antigo por uma função nomeada, chamada diretamente pelo botão.
start="document.querySelector('.generateRoadmap')?.addEventListener('click',()=>{"
if start in s:
    s=s.replace(start,'function runMaxSimulation(){',1)
    marker="out.scrollIntoView({behavior:'smooth',block:'start'})});"
    s=s.replace(marker,"out.scrollIntoView({behavior:'smooth',block:'start'});}\n",1)
# O botão chama a função diretamente: sem depender de registro de listener.
s=re.sub(r'<button[^>]*class="generateRoadmap"[^>]*>', '<button type="button" class="generateRoadmap" onclick="runMaxSimulation()">', s, count=1)
p.write_text(s)
