create table RECEITAS(
    ID int unsigned auto_increment primary key,
    VALOR double,
    DATA_PAGAMENTO date,    
    DATA_PAGAMENTO_ESPERADO date,
    TIPO varchar(100),
    
    ID_CONTA int unsigned,
    foreign key (ID_CONTA) references CONTAS(ID)
)