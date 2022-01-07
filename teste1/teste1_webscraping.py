from bs4 import BeautifulSoup
import requests

URL = "https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss"
FILE_TYPE = ".pdf"

def get_file_url(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')

    desired_url = '';
    
    for link in soup.find_all('a'):

        a_class = link.get('class')

        if a_class == None: pass
        elif len(a_class) == 2:
            if a_class[0] == 'alert-link' and a_class[1] == 'internal-link':
                temp_file_url = link.get('href')
                if temp_file_url.find('padrao-tiss-2013-novembro-2021'):
                    desired_url = temp_file_url
                    break

    return desired_url

def download_file(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')

    for td in soup.find_all('td'):
        a = td.find('a')
        if a != None:
            pdf_file = a.get('href')
            if FILE_TYPE in pdf_file and pdf_file.find('padrao-tiss_componente-organizacional'):
                filename = pdf_file[pdf_file.rindex('/')+1:]
                print('\n- Baixando arquivo \'' + filename + '\' ...')
                try:
                    with open(filename, 'wb') as file:
                        response = requests.get(pdf_file)
                        file.write(response.content)
                except Exception as e:
                    print('- Erro durante o download!')
                    print('|-- ' + e)
                else:
                    print('- Download completo\n')


def main():
    file_url = get_file_url(URL)
    download_file(file_url)

if __name__=='__main__':
    main()