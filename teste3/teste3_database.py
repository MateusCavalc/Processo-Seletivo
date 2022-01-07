import sqlite3
import pandas as pd
from datetime import datetime

DATABASE = 'infos.db'
CREATE_QUERY = 'CREATE TABLE IF NOT EXISTS infos (DATA DATE, REG_ANS BIGINT, CD_CONTA_CONTABIL BIGINT, DESCRICAO TEXT, VL_SALDO_FINAL money)'
SELECT_QUERY_3MONTHS = 'SELECT REG_ANS, COUNT(DESCRICAO), SUM(VL_SALDO_FINAL) AS TOTAL FROM infos WHERE DESCRICAO=\'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR \' AND DATA > date(\'now\', \'-3 months\') GROUP BY REG_ANS ORDER BY TOTAL DESC LIMIT 10'
SELECT_QUERY_1YEAR = 'SELECT REG_ANS, COUNT(DESCRICAO), SUM(VL_SALDO_FINAL) AS TOTAL FROM infos WHERE DESCRICAO=\'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR \' AND DATA > date(\'now\', \'-1 year\') GROUP BY REG_ANS ORDER BY TOTAL DESC LIMIT 10'

def create_table(c, query):
    c.execute(query)

def import_data(conn, c, csv_file):
    print('\nLoading data from \'' + csv_file + '\' ...')
    data = pd.read_csv(csv_file, index_col=False, delimiter=';', encoding="utf-8")
    data.head()

    count = 0
 
    for i,row in data.iterrows():
        c.execute("INSERT INTO infos(DATA, REG_ANS, CD_CONTA_CONTABIL, DESCRICAO, VL_SALDO_FINAL) VALUES (?,?,?,?,?)", (datetime.strptime(row['DATA'], "%d/%m/%Y").strftime("%Y-%m-%d"), row['REG_ANS'], row['CD_CONTA_CONTABIL'], row['DESCRICAO'], row['VL_SALDO_FINAL']))
        count += 1
        if count == 10000:
            conn.commit()
            count = 0
            print(i)

    conn.commit()

    print('\nDone\n')

def select_data(conn, c, query, comp_str):
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

        create_table(c, CREATE_QUERY)

        # import_data(conn, c, '1T2020.csv')
        # import_data(conn, c, '2T2020.csv')
        # import_data(conn, c, '3T2020.csv')
        # import_data(conn, c, '4T2020.csv')
        # import_data(conn, c, '1T2021.csv')
        # import_data(conn, c, '2T2021.csv')
        # import_data(conn, c, '3T2021.csv')

        select_data(conn, c, SELECT_QUERY_3MONTHS, "no último trimestre")
        select_data(conn, c, SELECT_QUERY_1YEAR, "no último ano")
        
    else:
        print('\nCould not connect to \'' + DATABASE + '\' database\n')

    c.close()
    conn.close()

if __name__=='__main__':
    main()