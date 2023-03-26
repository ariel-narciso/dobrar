from DataBaseConnection import ConnectionDB
import requests

ret: list[dict[str,str|int]] = requests.get(
  'https://brapi.dev/api/quote/list'
).json()['stocks']

conn = ConnectionDB('dobrar.db')
acoes = []
for x in ret:
	acoes.append({'codigo': x['stock'], 'nome': x['name']})
print(conn.insert('acao', acoes))
print(conn.select('acao', ('codigo', 'PETR4')))