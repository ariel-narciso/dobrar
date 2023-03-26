#import PyPDF2
from pypdf import PdfReader

def strToFloat(str: str):
	return float(str.replace('.', '').replace(',', '.'))

class TradeNoteReader:
	def __init__(self, filename: str) -> None:
		reader = PdfReader(open(filename, 'rb'))
		self.__file: list[str] = []
		for page in reader.pages:
			self.__file += page.extract_text().split('\n')
		self.table = self.__getTable()
	
	def __findTable(self) -> int:
		return self.__file.index('D/C') + 2
	
	def __getRow(self, index: int) -> tuple[list[str|int|float], int]:
		row = self.__file[index : index + 3]
		idx = index + 3
		n = len(self.__file)
		while idx < n:
			try:
				row.extend([
					int(self.__file[idx]),
					strToFloat(self.__file[idx + 1]),
					strToFloat(self.__file[idx + 2]),
					self.__file[idx + 3]
				])
				return row, idx + 4
			except ValueError:
				if (row[2][-1] != ' '):
					row[2] += ' '
				row[2] += self.__file[idx]
				idx += 1
	
	def __getTable(self):
		idx = self.__findTable()
		table: list[list[str]] = []
		n = len(self.__file)
		while idx < n and self.__file[idx] == 'BOVESPA':
			row, idx = self.__getRow(idx)
			table.append(row)
		return table
	
	def getTickets(self):
		ans = []
		for x in self.table:
			tick = findTicket(x[2])
			if tick not in ans:
				ans.append(tick)
		ans.sort()
		return ans
	
	def __getData(self, key: str, add: int = 1):
		return self.__file[
			self.__file.index(key) + add
		]
	
	def getTradeDate(self):
		return self.__getData('Data Pregão')
	
	def getSales(self):
		return strToFloat(self.__getData('Vendas à vista'))
	
	def getPurchases(self):
		return strToFloat(self.__getData('Compras à vista'))
	
	def getPreTaxValue(self):
		return strToFloat(self.__getData('Valor Líquido das Operações'))
	
	def getLiquidationTax(self):
		return strToFloat(self.__getData('Taxa de Liquidação'))
	
	def getEmoluments(self):
		return strToFloat(self.__getData('Emolumentos'))
	
	def getBrokerage(self):
		return strToFloat(self.__getData('Corretagem'))
	
	def getISS(self):
		return strToFloat(self.__getData('ISS (SÃO PAULO)'))
	
	def getIRRF(self):
		return strToFloat(self.__getData('I.R.R.F. s/ operações. Base 0,00'))
	
	def __str__(self) -> str:
		new = []
		for x in self.table:
			new.append([
				findTicket(x[2]),
				x[3] if x[1] == 'C' else -x[3],
				str(x[4]).replace('.', ','),
			])
		ans = ''
		for n in new:
			ans += '{0}\t{1}\t{2}\n'.format(n[0], n[1], n[2])
		ans += '\ntaxa l.\t{0}\nEmol.\t{1}\nCorr.\t{2}\nISS\t{3}\nIRRF\t{4}'.format(
			str(abs(self.getLiquidationTax())).replace('.', ','),
			str(abs(self.getEmoluments())).replace('.', ','),
			str(abs(self.getBrokerage())).replace('.', ','),
			str(abs(self.getISS())).replace('.', ','),
			str(abs(self.getIRRF())).replace('.', ',')
		)
		return ans
	
def findTicket(name: str):
	types = ['ON', 'PN', 'PNA', 'PNB', 'PNC', 'PND', 'CI']
	names = name.split(' ')
	for k, value in enumerate(names):
		if value in types:
			ans = names[k - 1]
			if (ans[-1] == 'F' and ans[-2].isdigit()):
				return ans[:-1]
			return ans
	


# -----------------------------------------------
# def getTableFlags():
# 	return [
# 		'Mercado', 'Mercado', 'C/V', 'C/V',
# 		'Tipo de Mercado', 'Tipo de Mercado',
# 		'Especificação do Título', 'Especificação do Título',
# 		'Observação', 'Observação',
# 		'Quantidade', 'Quantidade',
# 		'Preço/Ajuste', 'Preço/Ajuste',
# 		'Valor/Ajuste', 'Valor/Ajuste',
# 	]
# -----------------------------------------------