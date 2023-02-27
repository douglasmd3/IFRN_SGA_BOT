drop database if exists dblocal;
create database dblocal;
use dblocal;

create table register(
	quantidade_de_usuario int not null

	);

create table interacao (
	quantidade_de_interacao int not null

	);
    
create table sugestao (
	nome varchar(250) not null,
	mensagem varchar (2000) /*será que é not null [entra em conversation e na hora de mandar texto, o cujo mandar mídia?] */
	
	);

create table satisfacao (
	_bom_ int not null,
	normal int not null,
	_ruim_ int not null
	
	);

select * from sugestao, register, interacao, satisfacao;

/*alter table sugestao add column data_hora;*/


select * from sugestao;
select quantidade_de_usuario from register;
select quantidade_de_interacao from interacao;
select * from satisfacao;
select * from sugestao, register, interacao, satisfacao;
