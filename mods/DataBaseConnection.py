import sqlite3

class ConnectionDB():
	def __init__(self, database: str) -> None:
		self.__database = database
	def save(self, query: str, data: list):
		conn = sqlite3.connect(self.__database)
		conn.executemany(query, data)
		conn.commit()
		conn.close()
	def delete(self, query: str):
		conn = sqlite3.connect(self.__database)
		conn.execute(query)
		conn.close()
	def select(self, table: str, filter: tuple[str, int|str] = None):
		conn = sqlite3.connect(self.__database)
		query = 'select * from ' + table
		if filter != None:
			query += ' where {} = ?'.format(filter[0])
			ret = conn.execute(query, (filter[1],)).fetchall()
		else:
			ret = conn.execute(query).fetchall()
		conn.close()
		return ret
	def insert(self, table: str, data: list[dict[str]]):
		keys = list(data[0].keys())
		cols = ':' + keys[0]
		for i in range(1, len(keys)):
			cols += ', :' + keys[i]
		return self.save((
			'insert into {}({}) values({})'.format(table, cols.replace(':', ''), cols)
		), data)
