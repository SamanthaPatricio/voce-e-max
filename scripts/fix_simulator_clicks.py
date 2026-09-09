from pathlib import Path
p=Path('index.html')
s=p.read_text()
# Fallback robusto: seleção acontece no próprio botão, sem depender do registro de listeners.
s=s.replace('class="initiative" data-status=', 'onclick="this.classList.toggle(\'active\')" class="initiative" data-status=')
s=s.replace('class="initiative active" data-status=', 'onclick="this.classList.toggle(\'active\')" class="initiative active" data-status=')
s=s.replace('class="goalBtn active" data-goal=', 'onclick="document.querySelectorAll(\'.goalBtn\').forEach(x=>x.classList.remove(\'active\'));this.classList.add(\'active\')" class="goalBtn active" data-goal=')
s=s.replace('class="goalBtn" data-goal=', 'onclick="document.querySelectorAll(\'.goalBtn\').forEach(x=>x.classList.remove(\'active\'));this.classList.add(\'active\')" class="goalBtn" data-goal=')
# Mantém as coleções usadas pelo cálculo, mas remove listeners duplicados para evitar toggle duplo.
s=s.replace("roadmapButtons.forEach(b=>b.addEventListener('click',()=>b.classList.toggle('active')));\n",'')
s=s.replace("goalBtns.forEach(b=>b.addEventListener('click',()=>{goalBtns.forEach(x=>x.classList.remove('active'));b.classList.add('active')}));\n",'')
# Garante tipo button nos objetivos para não haver submit implícito.
s=s.replace('<button onclick="document.querySelectorAll(\'.goalBtn\')', '<button type="button" onclick="document.querySelectorAll(\'.goalBtn\')')
p.write_text(s)
