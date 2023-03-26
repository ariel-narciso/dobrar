--CREATE database dobrar;
drop table if exists acao;
create table acao(
	id integer primary key autoincrement,
	cnpj char(14),
	codigo varchar(10) not null unique,
	nome varchar(255) not null,
	tipo_mercado char(1) default 'F' check (
		tipo_mercado in ('V', 'F')
	),
	tipo char(3) check(
		tipo in ('ON', 'PNA', 'PNB', 'PNC', 'PND')
	)
);

drop table if exists nota;
create table nota(
	id integer primary key autoincrement,
	data_pregao text not null,
	data_liquidacao text not null
	-- taxa_liquidacao real not null check (taxa_liquidacao >= 0),
	-- emolumentos real not null check (emolumentos >= 0),
	-- corretagem real not null check (corretagem >= 0),
	-- iss real not null check (iss >= 0),
	-- irrf real not null check (irrf >= 0)
);

drop table if exists ordem;
create table ordem(
	id integer primary key autoincrement,
	acao_id integer not null,
	nota_id integer not null,
	tipo char(1) not null check (tipo in ('C', 'V')),
	preco real not null,
	quantidade integer not null,
	taxas real not null check (taxas >= 0),
	irrf real not null check (irrf >= 0),
	foreign key(acao_id) references acao(id)
	foreign key(nota_id) references nota(id)
);