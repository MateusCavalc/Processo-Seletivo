import sqlite3
import pandas as pd
from datetime import datetime

DATABASE = 'infos.db'

# Query de criação de tabela
CREATE_QUERY = 'CREATE TABLE IF NOT EXISTS infos (DATA DATE, REG_ANS BIGINT, CD_CONTA_CONTABIL BIGINT, DESCRICAO TEXT, VL_SALDO_FINAL money)'

# Query 'último trimestre'
SELECT_QUERY_3MONTHS = 'SELECT REG_ANS, COUNT(DESCRICAO), SUM(VL_SALDO_FINAL) AS TOTAL FROM infos WHERE DESCRICAO=\'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR \' AND DATA > date(\'now\', \'-3 months\') GROUP BY REG_ANS ORDER BY TOTAL DESC LIMIT 10'

# Query 'último ano'
SELECT_QUERY_1YEAR = 'SELECT REG_ANS, COUNT(DESCRICAO), SUM(VL_SALDO_FINAL) AS TOTAL FROM infos WHERE DESCRICAO=\'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR \' AND DATA > date(\'now\', \'-1 year\') GROUP BY REG_ANS ORDER BY TOTAL DESC LIMIT 10'

def create_table(c, query): # Cria a tabela usando a 'query' passada
    c.execute(query)

def import_data(conn, c, csv_file): # Realiza a inserção dos dados do arquivo 'csv_file' na tabela criada
    print('\nLoading data from \'' + csv_file + '\' ...')
    data = pd.read_csv(csv_file, index_col=False, delimiter=';', encoding="utf-8")
    data.head()

    count = 0
 
    # Os dados dão inseridos em "pacotes" de 10000 para otimização, ou seja, é efetuado um commit pro banco a cada 10000 chamadas de execução do insert
    for i,row in data.iterrows():
        # Para cada comando de insert, é efetuado uma conversão da data do arquivo .csv (dd/mm/yyyy para yyyy-mm-dd)
        c.execute("INSERT INTO infos(DATA, REG_ANS, CD_CONTA_CONTABIL, DESCRICAO, VL_SALDO_FINAL) VALUES (?,?,?,?,?)", (datetime.strptime(row['DATA'], "%d/%m/%Y").strftime("%Y-%m-%d"), row['REG_ANS'], row['CD_CONTA_CONTABIL'], row['DESCRICAO'], row['VL_SALDO_FINAL']))
        count += 1
        if count == 10000:
            conn.commit()
            count = 0
            print(i)

    conn.commit()

    print('\nDone\n')

def select_data(conn, c, query, comp_str): # Realiza a query de select de acordo com o parâmetro 'query' fornecido
    rows = c.execute(query).fetchall()

    print('# 10 operadoras que mais tiveram despesas com "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" ' + comp_str + ' #\n')
    print(' REG_ANS\tCOUNT\t\tTOTAL')
    for row in rows:
        print(' ' + str(row[0]) + '\t\t' + str(row[1]) + '\t\t' + str(row[2]))

    print()

def main():
    conn = sqlite3.connect(DATABASE)
    if conn is not None:
        print('\nConnected to \'' + DATABASE + '\' database\n')
        c = conn.cursor()

        # Cria a tabela
        create_table(c, CREATE_QUERY)

        # Realiza a importação dos arquivos
        # import_data(conn, c, '1T2020.csv')
        # import_data(conn, c, '2T2020.csv')
        # import_data(conn, c, '3T2020.csv')
        # import_data(conn, c, '4T2020.csv')
        # import_data(conn, c, '1T2021.csv')
        # import_data(conn, c, '2T2021.csv')
        # import_data(conn, c, '3T2021.csv')

        # Realiza a aquisição dos dados desejados do banco de acordo com as queries SELECT_QUERY_3MONTHS e SELECT_QUERY_1YEAR
        select_data(conn, c, SELECT_QUERY_3MONTHS, "no último trimestre")
        select_data(conn, c, SELECT_QUERY_1YEAR, "no último ano")
        
    else:
        print('\nCould not connect to \'' + DATABASE + '\' database\n')

    c.close()
    conn.close()

if __name__=='__main__':
    main()
