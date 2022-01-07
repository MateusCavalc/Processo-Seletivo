import camelot
import pandas as pd
from zipfile import ZipFile
# import matplotlib.pyplot

FILE = "padrao-tiss_componente-organizacional_202111.pdf"

def get_tables(filename):
    print('\nImporting tables from file \'' + filename + '\' ...')
    return camelot.read_pdf(filename, pages='114-120', flavor='lattice', line_scale=40, strip_text=' .\n')

def merge_tables(tables, a, b):
    print('Merging tables ...')
    return pd.concat([tables[i].df for i in range(a, b+1)], ignore_index=True)

def save_csv(table, filename):
    print('Saving table to file \'' + filename + '\' ...')
    table.to_csv(filename)

def main():
    tables = get_tables(FILE)
    print('Found ' + str(tables.n) + ' tables')

    merged_table = merge_tables(tables, 1, 6)
    
    save_csv(tables[0], 'table_1.csv')  
    # camelot.plot(tables[0], kind='grid').show()

    save_csv(merged_table, 'table_2.csv') 
    # camelot.plot(merged_table, kind='grid').show()

    save_csv(tables[7], 'table_3.csv')  
    # camelot.plot(tables[7], kind='grid').show()

    zipObj = ZipFile('Teste_Mateus.zip', 'w')
    zipObj.write('table_1.csv')
    zipObj.write('table_2.csv')
    zipObj.write('table_3.csv')
    zipObj.close()

if __name__=='__main__':
    main()