import re
from typing import Union

class ExtratorURL:
    """
    Classe para extrair informações de uma URL válida do Bytebank.

    Atributos:
        url (str): A URL a ser processada.

    Métodos:
        __init__(self, url: str) -> None:
            Inicializa um objeto ExtratorURL com a URL fornecida e a valida.

        sanitiza_url(self, url: str) -> str:
            Remove espaços em branco antes e depois da URL.

        valida_url(self) -> None:
            Valida se a URL fornecida é válida, seguindo o padrão esperado da URL do Bytebank.

        get_url_base(self) -> str:
            Obtém a parte base da URL antes do primeiro '?'.

        get_url_parametros(self) -> str:
            Obtém a parte dos parâmetros da URL após o primeiro '?'.

        get_valor_parametro(self, parametro_busca: str) -> Union[int, float, str]:
            Obtém o valor associado ao parâmetro especificado em parametro_busca.

        __len__(self) -> int:
            Retorna o tamanho da URL.

        __str__(self) -> str:
            Retorna uma representação em string do objeto ExtratorURL com a URL completa,
            a base da URL e os parâmetros da URL.

        __eq__(self, other: object) -> bool:
            Verifica se dois objetos ExtratorURL são iguais, comparando suas URLs.
    """

    def __init__(self, url: str):
        self.url = self.sanitiza_url(url)
        self.valida_url()

    def sanitiza_url(self, url: str) -> str:
        return url.strip()
    
    def valida_url(self) -> None:
        if not self.url:
            raise ValueError('A URL está vazia.')
        
        padrao_url = re.compile('(http(s)?://)?(www.)?bytebank.com(.br)?/cambio')
        match = padrao_url.match(self.url)
        if not match:
            raise ValueError('A URL não é válida')
        
    def get_url_base(self) -> str:
        indice_interrogacao = self.url.find('?')
        url_base = self.url[:indice_interrogacao]
        return url_base

    def get_url_parametros(self) -> str:
        indice_interrogacao = self.url.find('?')
        url_parametros = self.url[indice_interrogacao+1:]
        return url_parametros
    
    def get_valor_parametro(self, parametro_busca: str) -> Union[int, float, str]:
        indice_parametro = self.get_url_parametros().find(parametro_busca)
        indice_valor = indice_parametro + len(parametro_busca) + 1

        indice_e_comercial = self.get_url_parametros().find('&', indice_valor)
        if indice_e_comercial == -1:
            valor = self.get_url_parametros()[indice_valor:]
        else:
            valor = self.get_url_parametros()[indice_valor:indice_e_comercial]
        
        return valor
    
    def __len__(self) -> int:
        return len(self.url)
    
    def __str__(self) -> str:
        return self.url + '\n' + 'Base da URL: ' + self.get_url_base() + '\n' + 'Parâmetros da URL: ' + self.get_url_parametros()
    
    def __eq__(self, other: object) -> bool:
        return self.url == other.url
    
url = "bytebank.com/cambio?quantidade=100&moedaOrigem=dolar&moedaDestino=real"
extrator_url = ExtratorURL(url)
extrator_url_2 = ExtratorURL(url)
print('O tamanho da URL é: ', len(extrator_url))
print('URL completa: ', extrator_url)
print('extrator_url == extrator_url_2? ', extrator_url == extrator_url_2)

VALOR_DOLAR = 5.50
moeda_origem = extrator_url.get_valor_parametro('moedaOrigem')
moeda_destino = extrator_url.get_valor_parametro('moedaDestino')
valor_quantidade = float(extrator_url.get_valor_parametro("quantidade"))
print('O valor da moeda origem é: ', valor_quantidade)

if moeda_destino.lower() == 'dolar':
    valor_convertido = valor_quantidade * VALOR_DOLAR
else:
    valor_convertido = valor_quantidade / VALOR_DOLAR

print('O valor da moeda destino é: ', valor_convertido)