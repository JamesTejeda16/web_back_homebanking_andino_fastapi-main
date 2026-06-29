from sqlalchemy import create_engine, text
from pathlib import Path
import sys

# Local .env parsing (simple)
root = Path(__file__).resolve().parent
env_file = root / '.env'
if not env_file.exists():
    env_file = root / '..' / '.env'
    env_file = env_file.resolve()
if not env_file.exists():
    print('No se encontró .env en el repo backend', file=sys.stderr)
    sys.exit(2)

config = {}
with open(env_file, 'r', encoding='utf-8') as f:
    for line in f:
        if '=' in line:
            k, v = line.strip().split('=', 1)
            config[k.strip()] = v.strip()

DATABASE_URL = config.get('DATABASE_URL')
if not DATABASE_URL:
    print('DATABASE_URL no definido en .env', file=sys.stderr)
    sys.exit(3)

engine = create_engine(DATABASE_URL, future=True)
with engine.connect() as conn:
    # Mostrar columnas de dcliente
    cols = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'dcliente' ORDER BY ordinal_position;"))
    col_list = [c[0] for c in cols.fetchall()]
    print('Columnas dcliente:', col_list)

    # Mostrar una fila de ejemplo de dcliente
    sample = conn.execute(text('SELECT * FROM dcliente LIMIT 1')).mappings().all()
    print('Ejemplo dcliente:', sample)

    # Intento de buscar usuario por codcliente/username (sin suponer columna dni)
    qry = text('''
    SELECT u.pkusuario,u.pkcliente,u.username,u.password_hash,u.intentos_fallidos,u.bloqueado,u.activo,
           c.codcliente
    FROM usuarios_homebanking u
    JOIN dcliente c ON c.pkcliente = u.pkcliente
    WHERE LOWER(c.codcliente) = LOWER(:cc) OR LOWER(u.username) = LOWER(:uname)
    ''')
    params = {"cc": "cli000001", "uname": "cli000001"}
    rows = conn.execute(qry, params).mappings().all()
    if not rows:
        print('No se encontró usuario por codcliente/username')
    else:
        for r in rows:
            print(dict(r))
