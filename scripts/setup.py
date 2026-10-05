from pathlib import Path
import secrets
p=Path(__file__).resolve().parent.parent
if (p/'.env').exists(): raise SystemExit('.env already exists; preserved.')
text=(p/'.env.example').read_text()
while 'GENERATE_ME' in text: text=text.replace('GENERATE_ME',secrets.token_hex(24),1)
(p/'.env').write_text(text)
(p/'.env').chmod(0o600)
print('Created .env with random secrets. View locally; never share or commit it.')
