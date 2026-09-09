from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
# Limpa atributos duplicados e mantém apenas um clique por card/objetivo.
s=re.sub(r'\s+onclick="this\.classList\.toggle\(\'active\'\)"(?=\s+onclick="this\.classList\.toggle\(\'active\'\)")','',s)
s=re.sub(r'\s+onclick="document\.querySelectorAll\(\'.goalBtn\'\)\.forEach\(x=>x\.classList\.remove\(\'active\'\)\);this\.classList\.add\(\'active\'\)"(?=\s+onclick=)','',s)
# Garante seleção visual somente quando ainda não existe onclick.
s=re.sub(r'<button type="button" class="initiative([^\"]*)"', lambda m:'<button type="button" onclick="this.classList.toggle(\'active\')" class="initiative'+m.group(1)+'"', s)
s=re.sub(r'<button type="button" class="goalBtn([^\"]*)"', lambda m:'<button type="button" onclick="document.querySelectorAll(\'.goalBtn\').forEach(x=>x.classList.remove(\'active\'));this.classList.add(\'active\')" class="goalBtn'+m.group(1)+'"', s)
# Botão chama um motor global isolado.
s=re.sub(r'<button[^>]*class="generateRoadmap"[^>]*>', '<button type="button" class="generateRoadmap" onclick="window.runMaxSimulation()">', s, count=1)
# Remove rescue anterior, se houver.
s=re.sub(r'<script id="max-simulator-rescue">.*?</script>','',s,flags=re.S)
# Motor independente: fica em outro script, portanto funciona mesmo se algum JS legado anterior falhar.
rescue=r'''<script id="max-simulator-rescue">
(function(){
const dims=['Cultura','Desenvolvimento','Experiência','Eficiência','Dados','Prevenção'];
const data={
'Max em Movimento':{w:[18,8,24,2,2,30],goal:'Bem-estar, vínculo e prevenção',result:'Fortalece convivência, movimento, saúde e bem-estar das mulheres da Max.',q:['Manter calendário e adesão','Conectar às ações preventivas','Acompanhar participação','Avaliar aprendizados e continuidade']},
'NR-1 & Saúde Mental':{w:[15,8,16,5,10,40],goal:'Prevenção e gestão de riscos psicossociais',result:'Estrutura prevenção, escuta, evidências e acompanhamento de fatores psicossociais.',q:['Mapear riscos e evidências','Definir plano preventivo','Executar e acompanhar ações','Revisar evidências e plano']},
'GPTW':{w:[35,8,30,3,8,8],goal:'Cultura e experiência',result:'Organiza escuta e plano de evolução da experiência e cultura.',q:['Kick-off e diagnóstico','Escuta e plano de ação','Atuar sobre prioridades','Medir evolução da jornada']},
'UNIMAX + PDI':{w:[20,40,18,8,8,2],goal:'Desenvolvimento, retenção e formação interna',result:'Conecta avaliação, PDI e aprendizagem por função.',q:['Mapear competências e desenhar PDIs','Publicar Fundação Ser Max e trilhas','Direcionar trilhas pelos gaps','Revisar PDIs e evolução']},
'LNT & T&D':{w:[12,35,15,5,8,8],goal:'Capacitação direcionada',result:'Transforma necessidades em calendário e ações de desenvolvimento.',q:['Priorizar necessidades do LNT','Executar calendário por público','Acompanhar adesão e aplicação','Medir efetividade e planejar 2028']},
'Onboarding':{w:[18,18,35,12,5,5],goal:'Experiência e integração',result:'Padroniza a chegada, acelera adaptação e reforça cultura.',q:['Desenhar jornada 0–90 dias','Implantar materiais e rituais','Medir experiência de entrada','Ajustar jornada pelos dados']},
'Sólides':{w:[8,18,10,20,22,3],goal:'Perfil, atração e apoio à gestão',result:'Adiciona perfil comportamental e estrutura de R&S.',q:['Configurar processos e perfis','Aplicar no R&S e jornadas','Cruzar aprendizados com desenvolvimento','Avaliar uso e aderência']},
'Desempenho':{w:[15,38,15,8,20,3],goal:'Performance e desenvolvimento',result:'Cria ciclo de competências, feedback, PDI e evolução.',q:['Definir modelo e competências','Rodar primeiro ciclo','Converter gaps em PDI e UNIMAX','Calibrar e medir evolução']},
'People Analytics':{w:[5,8,5,30,45,5],goal:'Decisão orientada por dados',result:'Consolida indicadores para decisões de liderança.',q:['Definir KPIs e fontes','Construir painéis prioritários','Criar rotina de análise','Consolidar tendências e decisões']},
'Pesquisas':{w:[22,8,28,5,28,12],goal:'Escuta e diagnóstico',result:'Transforma percepção em diagnóstico e planos de ação.',q:['Definir calendário de escuta','Aplicar pesquisas e priorizar temas','Executar planos de ação','Medir evolução das percepções']},
'Automação':{w:[3,3,8,45,25,3],goal:'Eficiência operacional',result:'Reduz tarefas manuais e libera capacidade do RH.',q:['Mapear gargalos e fluxos','Automatizar rotinas prioritárias','Integrar dados e alertas','Medir ganho operacional']},
'MAX PEOPLE':{w:[8,10,20,38,38,4],goal:'Experiência digital e centralização',result:'Centraliza serviços, dados e IA em uma experiência própria.',q:['Priorizar módulos e arquitetura','Implantar fluxos essenciais','Conectar analytics e Maxiane','Consolidar adoção e evolução']}
};
const align={Desenvolvimento:{'UNIMAX + PDI':98,'Desempenho':96,'LNT & T&D':94,'Sólides':68,'People Analytics':62,'Pesquisas':58,'MAX PEOPLE':55,'Onboarding':52,'GPTW':48,'NR-1 & Saúde Mental':30,'Automação':28,'Max em Movimento':25},Turnover:{Pesquisas:88,Onboarding:84,'UNIMAX + PDI':84,'People Analytics':82,GPTW:78,Desempenho:76,'LNT & T&D':68,'NR-1 & Saúde Mental':65,Sólides:62,'Max em Movimento':55,'MAX PEOPLE':50,Automação:32},Cultura:{GPTW:96,Pesquisas:94,Onboarding:86,'Max em Movimento':75,'UNIMAX + PDI':72,Desempenho:70,'LNT & T&D':62,'NR-1 & Saúde Mental':58,'People Analytics':55,Sólides:48,'MAX PEOPLE':45,Automação:25},Lideranca:{Desempenho:94,'UNIMAX + PDI':92,'LNT & T&D':88,'People Analytics':75,Sólides:72,Pesquisas:68,GPTW:55,'MAX PEOPLE':55,'NR-1 & Saúde Mental':48,Automação:38,Onboarding:35,'Max em Movimento':20},Experiencia:{Onboarding:96,Pesquisas:95,GPTW:92,'Max em Movimento':82,'MAX PEOPLE':82,'NR-1 & Saúde Mental':78,'UNIMAX + PDI':70,Desempenho:66,'LNT & T&D':60,'People Analytics':58,Automação:58,Sólides:50},Eficiencia:{Automação:100,'MAX PEOPLE':96,'People Analytics':88,Sólides:72,Onboarding:48,Desempenho:45,Pesquisas:42,'LNT & T&D':38,'UNIMAX + PDI':35,'NR-1 & Saúde Mental':25,GPTW:20,'Max em Movimento':10},Dados:{'People Analytics':100,'MAX PEOPLE':94,Pesquisas:90,Automação:88,Desempenho:82,Sólides:78,GPTW:55,'UNIMAX + PDI':55,'LNT & T&D':52,'NR-1 & Saúde Mental':48,Onboarding:30,'Max em Movimento':15},Carreira:{'UNIMAX + PDI':98,Desempenho:96,'LNT & T&D':86,'People Analytics':72,Sólides:65,Pesquisas:48,'MAX PEOPLE':48,Onboarding:35,GPTW:28,Automação:22,'NR-1 & Saúde Mental':15,'Max em Movimento':10}};
const labels={Desenvolvimento:'Desenvolver pessoas',Turnover:'Reduzir turnover',Cultura:'Fortalecer cultura',Lideranca:'Preparar lideranças',Experiencia:'Melhorar experiência',Eficiencia:'Automatizar o RH',Dados:'Decidir com dados',Carreira:'Estruturar carreira'};
window.runMaxSimulation=function(){
 try{
  const selected=[...document.querySelectorAll('.initiative.active')].map(b=>b.dataset.item).filter(x=>data[x]);
  const out=document.querySelector('.strategyResult'); if(!out)return;
  out.classList.add('show');
  if(!selected.length){document.querySelector('#alignmentScore').textContent='—';document.querySelector('#strategyTitle').textContent='Selecione pelo menos uma prioridade';document.querySelector('#strategyText').textContent='Escolha uma ou mais iniciativas para gerar o cenário.';out.scrollIntoView({behavior:'smooth',block:'start'});return;}
  const goal=document.querySelector('.goalBtn.active')?.dataset.goal||'Desenvolvimento';
  const vals=selected.map(x=>align[goal]?.[x]||10).sort((a,b)=>b-a);let score=Math.min(100,Math.round(vals[0]+vals.slice(1).reduce((a,v)=>a+v*.1,0)));
  const level=score>=90?'MUITO ALTA':score>=75?'ALTA':score>=55?'BOA':score>=35?'PARCIAL':'BAIXA';
  document.querySelector('#alignmentScore').textContent=score+'% • '+level;document.querySelector('#alignmentTitle').textContent='Objetivo: '+labels[goal];
  const ranked=selected.slice().sort((a,b)=>(align[goal]?.[b]||0)-(align[goal]?.[a]||0));
  document.querySelector('#alignmentDiagnosis').textContent='A leitura compara a contribuição das iniciativas selecionadas para o objetivo escolhido.';
  document.querySelector('#alignmentStrength').textContent='Maiores contribuições: '+ranked.slice(0,3).map(x=>x+' ('+(align[goal]?.[x]||10)+'%)').join(', ')+'.';
  const missing=Object.entries(align[goal]||{}).filter(([x])=>!selected.includes(x)).sort((a,b)=>b[1]-a[1]);
  document.querySelector('#alignmentGap').textContent=missing.length?'Para ampliar o cenário: '+missing.slice(0,2).map(x=>x[0]).join(' + ')+'.':'As principais frentes já estão contempladas.';
  document.querySelector('#alignmentRecommendation').textContent=missing.length?'Próximo complemento sugerido: '+missing[0][0]+' ('+missing[0][1]+'% de aderência individual).':'Concentre a próxima etapa em execução e mensuração.';
  let scores=[0,0,0,0,0,0];selected.forEach(x=>data[x].w.forEach((v,i)=>scores[i]+=v));const max=Math.max(...scores)||1;scores=scores.map(v=>Math.round(v/max*100));
  document.querySelector('#impactGrid').innerHTML=dims.map((d,i)=>'<div class="impactCard"><div class="impactHead"><span>'+d+'</span><span>'+scores[i]+'%</span></div><div class="impactBar"><div class="impactFill" style="width:'+scores[i]+'%"></div></div></div>').join('');
  const order=scores.map((v,i)=>[v,i]).sort((a,b)=>b[0]-a[0]),top=dims[order[0][1]],second=dims[order[1][1]],low=dims[order[order.length-1][1]];
  document.querySelector('#strategyTitle').textContent='Estratégia formada: '+top+' + '+second;document.querySelector('#strategyText').textContent='Sua combinação concentra maior impacto em '+top.toLowerCase()+' e '+second.toLowerCase()+'.';
  document.querySelector('#strategyFlow').innerHTML=['DIAGNOSTICAR','PRIORIZAR','EXECUTAR','MEDIR'].map(x=>'<span>'+x+'</span>').join('<b>→</b>');document.querySelector('#strategyAttention').innerHTML='<b>Ponto de atenção:</b> '+low+' aparece com menor ênfase neste cenário.';
  document.querySelector('#initiativeImpact').innerHTML=selected.map(x=>'<article><small>IMPACTO ESTRATÉGICO</small><h4>'+x+'</h4><b>'+data[x].goal+'</b><p>'+data[x].result+'</p></article>').join('');
  ['q1','q2','q3','q4'].forEach((id,i)=>document.querySelector('#'+id).innerHTML=selected.map(x=>'<li><b>'+x+':</b> '+data[x].q[i]+'</li>').join(''));
  out.scrollIntoView({behavior:'smooth',block:'start'});
 }catch(e){console.error('MAX simulator',e);const out=document.querySelector('.strategyResult');if(out){out.classList.add('show');out.innerHTML='<div class="alignmentBox"><h3>Não foi possível gerar o cenário.</h3><p>Atualize a página e tente novamente.</p></div>';}}
};
})();
</script>'''
s=s.replace('</body>',rescue+'\n</body>',1)
p.write_text(s)
