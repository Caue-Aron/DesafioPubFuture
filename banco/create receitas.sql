create table RECEITAS(
    ID int unsigned auto_increment primary key,
    VALOR double,
    DATA_RECEBIMENTO date,    
    DATA_RECEBIMENTO_PREVISTO date,
    TIPO varchar(100),
    DESCRICAO varchar(200),
    
    ID_CONTA int unsigned,
    foreign key (ID_CONTA) references CONTAS(ID)
)