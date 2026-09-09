from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="unimax"' in s:
    raise SystemExit(0)
css=Path('scripts/unimax.css').read_text()
section=Path('scripts/unimax-section.html').read_text()
js=Path('scripts/unimax.js').read_text()
s=s.replace('</style>',css+'\n</style>',1)
s=s.replace('    <section class="finish">',section+'\n    <section class="finish">',1)
s=s.replace('    </script>',js+'\n    </script>',1)
p.write_text(s)
