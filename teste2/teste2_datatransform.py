import camelot
import pandas as pd
from zipfile import ZipFile
# import matplotlib.pyplot

FILE = "padrao-tiss_componente-organizacional_202111.pdf"

def get_tables(filename): # Recebe o nome do arquivo .pdf e efetua a leitura das tabela, retornando a estrutura com as informações das páginas 114-120 (tabelas 30, 31 e 32)
    print('\nImporting tables from file \'' + filename + '\' ...')
    return camelot.read_pdf(filename, pages='114-120', flavor='lattice', line_scale=40, strip_text=' .\n')

def merge_tables(tables, a, b): # Recebe uma lista de tabelas e efetua a concatenação das tabelas entre 'tabelas[a]' e 'tabelas[b]'
    print('Merging tables ...')
    return pd.concat([tables[i].df for i in range(a, b+1)], ignore_index=True)

def save_csv(table, filename): # Recebe a tabela e salva no arquivo 'filename'
    print('Saving table to file \'' + filename + '\' ...')
    table.to_csv(filename)

def main():
    tables = get_tables(FILE)
    print('Found ' + str(tables.n) + ' tables')

    merged_table = merge_tables(tables, 1, 6) # Tabela 31 do arquivo .pdf se encontra segmentada nas tabelas tables[1] - tables[6]
    
    save_csv(tables[0], 'table_1.csv') # Salva tabela 30 no arquivo 'table_1.csv'
    # camelot.plot(tables[0], kind='grid').show()

    save_csv(merged_table, 'table_2.csv') # Salva tabela 31 no arquivo 'table_2.csv'
    # camelot.plot(merged_table, kind='grid').show()

    save_csv(tables[7], 'table_3.csv') # Salva tabela 32 no arquivo 'table_3.csv'
    # camelot.plot(tables[7], kind='grid').show()

    # Cria o .zip com os arquivos .csv gerados
    zipObj = ZipFile('Teste_Mateus.zip', 'w')
    zipObj.write('table_1.csv')
    zipObj.write('table_2.csv')
    zipObj.write('table_3.csv')
    zipObj.close()

if __name__=='__main__':
    main()
