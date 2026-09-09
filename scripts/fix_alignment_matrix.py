from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
# Replace only the alignment engine, preserving UI and strategic roadmap.
start=s.index('const goalConfig=')
end=s.index("document.querySelector('.generateRoadmap')?.addEventListener", start)
engine=r'''const goalConfig={
Desenvolvimento:{label:'Desenvolver pessoas',why:'criar desenvolvimento contínuo e transformar gaps em evolução'},
Turnover:{label:'Reduzir turnover',why:'atuar sobre integração, experiência, escuta, desenvolvimento e causas de saída'},
Cultura:{label:'Fortalecer cultura',why:'reforçar pertencimento, comportamentos, escuta e experiência cultural'},
Lideranca:{label:'Preparar lideranças',why:'desenvolver competências de gestão, feedback e tomada de decisão'},
Experiencia:{label:'Melhorar experiência',why:'qualificar a jornada do colaborador e seus principais momentos de contato'},
Eficiencia:{label:'Automatizar o RH',why:'reduzir esforço operacional, centralizar fluxos e ganhar escala'},
Dados:{label:'Decidir com dados',why:'transformar informações de pessoas em diagnóstico e decisão'},
Carreira:{label:'Estruturar carreira',why:'conectar competências, desempenho, desenvolvimento e próximos passos'}};
// Aderência qualitativa de cada iniciativa a cada objetivo. Nenhuma iniciativa útil é tratada como contribuição zero.
const alignmentMatrix={
'Max em Movimento':{Desenvolvimento:25,Turnover:55,Cultura:75,Lideranca:20,Experiencia:82,Eficiencia:10,Dados:15,Carreira:10},
'NR-1 & Saúde Mental':{Desenvolvimento:30,Turnover:65,Cultura:58,Lideranca:48,Experiencia:78,Eficiencia:25,Dados:48,Carreira:15},
'GPTW':{Desenvolvimento:48,Turnover:78,Cultura:96,Lideranca:55,Experiencia:92,Eficiencia:20,Dados:55,Carreira:28},
'UNIMAX + PDI':{Desenvolvimento:98,Turnover:84,Cultura:72,Lideranca:92,Experiencia:70,Eficiencia:35,Dados:55,Carreira:98},
'LNT & T&D':{Desenvolvimento:94,Turnover:68,Cultura:62,Lideranca:88,Experiencia:60,Eficiencia:38,Dados:52,Carreira:86},
'Onboarding':{Desenvolvimento:52,Turnover:84,Cultura:86,Lideranca:35,Experiencia:96,Eficiencia:48,Dados:30,Carreira:35},
'Sólides':{Desenvolvimento:68,Turnover:62,Cultura:48,Lideranca:72,Experiencia:50,Eficiencia:72,Dados:78,Carreira:65},
'Desempenho':{Desenvolvimento:96,Turnover:76,Cultura:70,Lideranca:94,Experiencia:66,Eficiencia:45,Dados:82,Carreira:96},
'People Analytics':{Desenvolvimento:62,Turnover:82,Cultura:55,Lideranca:75,Experiencia:58,Eficiencia:88,Dados:100,Carreira:72},
'Pesquisas':{Desenvolvimento:58,Turnover:88,Cultura:94,Lideranca:68,Experiencia:95,Eficiencia:42,Dados:90,Carreira:48},
'Automação':{Desenvolvimento:28,Turnover:32,Cultura:25,Lideranca:38,Experiencia:58,Eficiencia:100,Dados:88,Carreira:22},
'MAX PEOPLE':{Desenvolvimento:55,Turnover:50,Cultura:45,Lideranca:55,Experiencia:82,Eficiencia:96,Dados:94,Carreira:48}};
const synergyRules=[
{items:['UNIMAX + PDI','Desempenho'],goals:['Desenvolvimento','Lideranca','Carreira'],bonus:8,label:'Avaliação + PDI/UNIMAX fecha o ciclo entre diagnóstico e desenvolvimento.'},
{items:['UNIMAX + PDI','LNT & T&D'],goals:['Desenvolvimento','Carreira'],bonus:6,label:'LNT + UNIMAX conecta necessidades coletivas e trilhas de aprendizagem.'},
{items:['Onboarding','GPTW'],goals:['Cultura','Experiencia','Turnover'],bonus:6,label:'Onboarding + GPTW conecta experiência de entrada à cultura desejada.'},
{items:['Onboarding','Pesquisas'],goals:['Experiencia','Turnover','Cultura'],bonus:6,label:'Onboarding + escuta permite medir e ajustar a experiência de entrada.'},
{items:['GPTW','Pesquisas'],goals:['Cultura','Experiencia','Turnover'],bonus:7,label:'GPTW + escuta transforma percepção em diagnóstico e plano de ação.'},
{items:['People Analytics','Pesquisas'],goals:['Dados','Turnover'],bonus:6,label:'Analytics + escuta combina indicadores objetivos e percepção das pessoas.'},
{items:['Automação','MAX PEOPLE'],goals:['Eficiencia','Dados','Experiencia'],bonus:8,label:'Automação + MAX PEOPLE centraliza a operação e cria escala digital.'},
{items:['MAX PEOPLE','People Analytics'],goals:['Dados','Eficiencia'],bonus:7,label:'MAX PEOPLE + Analytics conecta centralização, indicadores e decisão.'},
{items:['NR-1 & Saúde Mental','Pesquisas'],goals:['Experiencia','Cultura','Turnover'],bonus:5,label:'Prevenção + escuta amplia a leitura sobre fatores psicossociais e experiência.'}}];
const recommendedByGoal={
Desenvolvimento:['UNIMAX + PDI','Desempenho','LNT & T&D','People Analytics'],
Turnover:['Pesquisas','Onboarding','People Analytics','UNIMAX + PDI','GPTW'],
Cultura:['GPTW','Pesquisas','Onboarding','UNIMAX + PDI'],
Lideranca:['Desempenho','UNIMAX + PDI','LNT & T&D','Sólides'],
Experiencia:['Onboarding','Pesquisas','GPTW','MAX PEOPLE','NR-1 & Saúde Mental'],
Eficiencia:['Automação','MAX PEOPLE','People Analytics','Sólides'],
Dados:['People Analytics','MAX PEOPLE','Pesquisas','Automação','Desempenho'],
Carreira:['UNIMAX + PDI','Desempenho','LNT & T&D','People Analytics']};
function renderAlignment(selected){
 const key=goalBtns.find(b=>b.classList.contains('active'))?.dataset.goal||'Desenvolvimento',g=goalConfig[key];
 if(!selected.length){document.querySelector('#alignmentScore').textContent='—';return;}
 const vals=selected.map(x=>alignmentMatrix[x]?.[key]||10).sort((a,b)=>b-a);
 // Melhor iniciativa pesa mais; complementares elevam cobertura sem inflar artificialmente o resultado.
 let score=vals[0]; if(vals.length>1) score+=vals.slice(1).reduce((a,v)=>a+v*0.10,0);
 const activeSynergies=synergyRules.filter(r=>r.goals.includes(key)&&r.items.every(x=>selected.includes(x)));
 score+=activeSynergies.reduce((a,r)=>a+r.bonus,0); score=Math.min(100,Math.round(score));
 const level=score>=90?'MUITO ALTA':score>=75?'ALTA':score>=55?'BOA':score>=35?'PARCIAL':'BAIXA';
 document.querySelector('#alignmentScore').textContent=score+'% • '+level;
 document.querySelector('#alignmentTitle').textContent='Objetivo: '+g.label;
 const strongest=selected.slice().sort((a,b)=>(alignmentMatrix[b]?.[key]||0)-(alignmentMatrix[a]?.[key]||0)).slice(0,3);
 document.querySelector('#alignmentDiagnosis').textContent=(score>=75?'A combinação está bem alinhada para ':'O cenário contribui para ')+g.why+'. '+(activeSynergies[0]?.label||'A leitura considera a contribuição individual de cada iniciativa e como elas se complementam.');
 document.querySelector('#alignmentStrength').textContent='Maiores contribuições neste objetivo: '+strongest.map(x=>x+' ('+(alignmentMatrix[x]?.[key]||10)+'%)').join(', ')+'.';
 const candidates=recommendedByGoal[key].filter(x=>!selected.includes(x)).map(x=>[x,alignmentMatrix[x][key]]).sort((a,b)=>b[1]-a[1]);
 const weakDims=[]; const dimMap={Cultura:0,Desenvolvimento:1,Experiencia:2,Eficiencia:3,Dados:4,Prevenção:5};
 if(typeof strategyData!=='undefined'){Object.entries(dimMap).forEach(([d,i])=>{const avg=Math.round(selected.reduce((a,x)=>a+(strategyData[x]?.w[i]||0),0)/selected.length);if(avg<12)weakDims.push(d)})}
 document.querySelector('#alignmentGap').textContent=candidates.length?'Para ampliar a estratégia, ainda há espaço para '+candidates.slice(0,2).map(x=>x[0]).join(' + ')+'.'+(weakDims.length?' Dimensões pouco cobertas: '+weakDims.slice(0,2).join(' e ')+'.':''):'A seleção já cobre as principais iniciativas associadas ao objetivo. O foco passa a ser integração, execução e mensuração.';
 document.querySelector('#alignmentRecommendation').textContent=candidates.length?'Próximo complemento sugerido: '+candidates[0][0]+' — aderência individual de '+candidates[0][1]+'% a este objetivo.':'Mantenha o portfólio e defina indicadores de resultado para validar a evolução ao longo de 2027.';
}
'''
s=s[:start]+engine+s[end:]
p.write_text(s)
