from tabulate import tabulate
from mods.TradeNoteReader import TradeNoteReader as tnr
from mods.ticket_cnpj_find import findCnpj
import pathlib
import os

# def compar(dir: pathlib.Path):
# 	return str(dir.name)

# if not os.path.isdir('out'):
# 	os.mkdir('out')
# rootDir = pathlib.Path('notas')
# for yearDir in sorted(rootDir.iterdir(), key=compar):
# 	if not os.path.isdir('out/{}'.format(yearDir.name)):
# 		os.mkdir('out/{}'.format(yearDir.name))
# 	for file in sorted(yearDir.iterdir(), key=compar):
# 		out = open('out/{}/{}'.format(
# 			yearDir.name,
# 			str(file.name).replace('.pdf', '.txt')
# 		), 'w')
# 		t = tnr(str(file))
# 		out.write(str(t))
# 		out.close()

t = tnr('notas/2022/12.pdf')
tickets = t.getTickets()
for tick in tickets:
	print('{}\t{}'.format(tick, findCnpj(tick, tick != 'IVVB11')))

# print(tabulate(t.table, headers=[
#   'Mercado', 'C/V', 'Especificação', 'Quantidade',
#   'Preço/Ajuste', 'Valor/Ajuste', 'D/C'
# ]))
