#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
# from lxml.html import fragment_fromstring
# from collections import OrderedDict
import json
from datetime import date
from datetime import datetime

today = datetime.today()

# dd/mm/YY
scraped_date = today
# print(scraped_date)

def extract_data_from(table, position):
    #print(table.select('.data .txt')[position].string.strip())
    return table.select('.data .txt')[position].string.strip()

def get_data():

    with open("tickers.txt", "r") as fundamentus_file:
        stocks = fundamentus_file.read().split()

    stocks_info = []
    for stock in stocks:
        try:
            print(stock)
            # print("Getting data for Stock {}".format(stock))
            stock_url = "{}detalhes.php?papel={}".format("http://fundamentus.com.br/", stock)
            #stock_url = ("http://fundamentus.com.br/" + str(stock))
            page = requests.get(stock_url)
            html = BeautifulSoup(page.text, 'html.parser')

            # Tabelas
            # 0 - Cotação
            tables = html.select("table.w728")
            #print(tables)
            print (extract_data_from(tables[0], 8))
            if extract_data_from(tables[0], 8) == "Bancos":
                print("é banco")

                stocks_info.append({
                    'scraped_date': str(scraped_date),
                    # 0
                    'codigo': stock,
                    'cotacao': float(extract_data_from(tables[0], 1).replace("-", "0").replace(".", "").replace(",", ".")),
                    'data_cotacao': str(datetime.strptime(extract_data_from(tables[0], 3), '%d/%m/%Y')),
                    'setor': extract_data_from(tables[0], 6),
                    'subsetor': extract_data_from(tables[0], 8),
                    # 1 - Valor de mercado
                    'valor_mercado': extract_data_from(tables[1], 0).replace(".", ""),
                    'valor_firma': extract_data_from(tables[1], 2).replace(".", ""),
                    'numero_acoes': extract_data_from(tables[1], 3).replace(".", ""),
                    # 2 - Indicadores fundamentalistas
                    'pl': float(extract_data_from(tables[2], 0).replace("-", "0").replace(".", "").replace(",", ".")),
                    'lpa': float(extract_data_from(tables[2], 1).replace("-", "0").replace(".", "").replace(",", ".")),
                    'pvp': float(extract_data_from(tables[2], 2).replace("-", "0").replace(".", "").replace(",", ".")),
                    'vpa': float(extract_data_from(tables[2], 3).replace("-", "0").replace(".", "").replace(",", ".")),
                    'pebit': float(extract_data_from(tables[2], 4).replace("-", "0").replace(".", "").replace(",", ".")),
                    'marg_bruta': float(extract_data_from(tables[2], 5).replace("-", "0").replace(".", "").replace(",", ".").replace("%", ""))/100,
                    'psr': float(extract_data_from(tables[2], 6).replace("-", "0").replace(".", "").replace(",", ".")),
                    'marg_ebit': float(extract_data_from(tables[2], 7).replace("-", "0").replace(".", "").replace(",", ".").replace("%", ""))/100,
                    'pativos': float(extract_data_from(tables[2], 8).replace("-", "0").replace(".", "").replace(",", ".")),
                    'marg_liquida': float(extract_data_from(tables[2], 9).replace("-", "0").replace(".", "").replace(",", ".").replace("%", ""))/100,
                    'p_cap_giro': float(extract_data_from(tables[2], 10).replace("-", "0").replace(".", "").replace(",", ".")),
                    'ebit_ativo': float(extract_data_from(tables[2], 11).replace(".", "").replace("-", "0").replace(",", ".").replace("%", ""))/100,
                    'p_ativ_circ_liq': float(extract_data_from(tables[2], 12).replace("-", "0").replace(".", "").replace(",", ".")),
                    'roic': float(extract_data_from(tables[2], 13).replace(".", "").replace("-", "0").replace(",", ".").replace("%", ""))/100,
                    'div_yield': float(extract_data_from(tables[2], 14).replace(".", "").replace("-", "0").replace(",", ".").replace("%", ""))/100,
                    'roe': float(extract_data_from(tables[2], 15).replace(".", "").replace("-", "0").replace(",", ".").replace("%", ""))/100,
                    'ev_ebitida': float(extract_data_from(tables[2], 16).replace("-", "0").replace(".", "").replace(",", ".")),
                    'liquidez_corr': float(extract_data_from(tables[2], 17).replace("-", "0").replace(".", "").replace(",", ".")),
                    'giro_ativos': float(extract_data_from(tables[2], 18).replace("-", "0").replace(".", "").replace(",", ".")),
                    'div_br_patrim': float(extract_data_from(tables[2], 19).replace("-", "0").replace(".", "").replace(",", ".")),
                    'cres_rec_5a': float(extract_data_from(tables[2], 20).replace(".", "").replace("-", "0").replace(",", ".").replace("%", ""))/100,
                    # 3 - Balanço patrimonial
                    'ativo': float(extract_data_from(tables[3], 0).replace("-", "0").replace(".", "").replace(",", ".")),
                    'disponibilidades': float(extract_data_from(tables[3], 2).replace("-", "0").replace(".", "").replace(",", ".")),
                    'ativo_circulante': " 0.0 ",
                    'div_bruta': " 0.0 ",
                    'div_liquida': " 0.0 ",
                    'patrimonio_liquido': float(extract_data_from(tables[3], 3).replace("-", "0").replace(".", "").replace(",", ".")),
                    # 4 - Demonstrativo de resultados
                    'receita_Liquida_12': float(extract_data_from(tables[4], 0).replace("-", "0").replace(".", "").replace(",", ".")),
                    'receita_Liquida_3': float(extract_data_from(tables[4], 1).replace("-", "0").replace(".", "").replace(",", ".")),
                    'ebit_12': float(extract_data_from(tables[4], 2).replace("-", "0").replace(".", "").replace(",", ".")),
                    'ebit_3': float(extract_data_from(tables[4], 3).replace("-", "0").replace(".", "").replace(",", ".")),
                    'lucro_liquido_12': float(extract_data_from(tables[4], 2).replace("-", "0").replace(".", "").replace(",", ".")),
                    'lucro_liquido_3': float(extract_data_from(tables[4], 3).replace("-", "0").replace(".", "").replace(",", ".")),

                })
                
            else:
                stocks_info.append({
                    'scraped_date': str(scraped_date),
                    # 0
                    'codigo': stock,
                    'cotacao': float(extract_data_from(tables[0], 1).replace("-", "0").replace(".", "").replace(",", ".")),
                    'data_cotacao': str(datetime.strptime(extract_data_from(tables[0], 3), '%d/%m/%Y')),
                    'setor': extract_data_from(tables[0], 6),
                    'subsetor': extract_data_from(tables[0], 8),
                    # 1 - Valor de mercado
                    'valor_mercado': extract_data_from(tables[1], 0).replace(".", ""),
                    'valor_firma': extract_data_from(tables[1], 2).replace(".", ""),
                    'numero_acoes': extract_data_from(tables[1], 3).replace(".", ""),
                    # 2 - Indicadores fundamentalistas
                    'pl': float(extract_data_from(tables[2], 0).replace("-", "0").replace(".", "").replace(",", ".")),
                    'lpa': float(extract_data_from(tables[2], 1).replace("-", "0").replace(".", "").replace(",", ".")),
                    'pvp': float(extract_data_from(tables[2], 2).replace("-", "0").replace(".", "").replace(",", ".")),
                    'vpa': float(extract_data_from(tables[2], 3).replace("-", "0").replace(".", "").replace(",", ".")),
                    'pebit': float(extract_data_from(tables[2], 4).replace("-", "0").replace(".", "").replace(",", ".")),
                    'marg_bruta': float(extract_data_from(tables[2], 5).replace("-", "0").replace(".", "").replace(",", ".").replace("%", ""))/100,
                    'psr': float(extract_data_from(tables[2], 6).replace("-", "0").replace(".", "").replace(",", ".")),
                    'marg_ebit': float(extract_data_from(tables[2], 7).replace("-", "0").replace(".", "").replace(",", ".").replace("%", ""))/100,
                    'pativos': float(extract_data_from(tables[2], 8).replace("-", "0").replace(".", "").replace(",", ".")),
                    'marg_liquida': float(extract_data_from(tables[2], 9).replace("-", "0").replace(".", "").replace(",", ".").replace("%", ""))/100,
                    'p_cap_giro': float(extract_data_from(tables[2], 10).replace("-", "0").replace(".", "").replace(",", ".")),
                    'ebit_ativo': float(extract_data_from(tables[2], 11).replace(".", "").replace("-", "0").replace(",", ".").replace("%", ""))/100,
                    'p_ativ_circ_liq': float(extract_data_from(tables[2], 12).replace("-", "0").replace(".", "").replace(",", ".")),
                    'roic': float(extract_data_from(tables[2], 13).replace(".", "").replace("-", "0").replace(",", ".").replace("%", ""))/100,
                    'div_yield': float(extract_data_from(tables[2], 14).replace(".", "").replace("-", "0").replace(",", ".").replace("%", ""))/100,
                    'roe': float(extract_data_from(tables[2], 15).replace(".", "").replace("-", "0").replace(",", ".").replace("%", ""))/100,
                    'ev_ebitida': float(extract_data_from(tables[2], 16).replace("-", "0").replace(".", "").replace(",", ".")),
                    'liquidez_corr': float(extract_data_from(tables[2], 17).replace("-", "0").replace(".", "").replace(",", ".")),
                    'giro_ativos': float(extract_data_from(tables[2], 18).replace("-", "0").replace(".", "").replace(",", ".")),
                    'div_br_patrim': float(extract_data_from(tables[2], 19).replace("-", "0").replace(".", "").replace(",", ".")),
                    'cres_rec_5a': float(extract_data_from(tables[2], 20).replace(".", "").replace("-", "0").replace(",", ".").replace("%", ""))/100,
                    # 3 - Balanço patrimonial
                    'ativo': float(extract_data_from(tables[3], 0).replace("-", "0").replace(".", "").replace(",", ".")),
                    'disponibilidades': float(extract_data_from(tables[3], 2).replace("-", "0").replace(".", "").replace(",", ".")),
                    'ativo_circulante': float(extract_data_from(tables[3], 4).replace("-", "0").replace(".", "").replace(",", ".")),
                    'div_bruta': float(extract_data_from(tables[3], 1).replace("-", "0").replace(".", "").replace(",", ".")),
                    'div_liquida': float(extract_data_from(tables[3], 3).replace("-", "0").replace(".", "").replace(",", ".")),
                    'patrimonio_liquido': float(extract_data_from(tables[3], 3).replace("-", "0").replace(".", "").replace(",", ".")),
                    # 4 - Demonstrativo de resultados
                    'receita_Liquida_12': float(extract_data_from(tables[4], 0).replace("-", "0").replace(".", "").replace(",", ".")),
                    'receita_Liquida_3': float(extract_data_from(tables[4], 1).replace("-", "0").replace(".", "").replace(",", ".")),
                    'ebit_12': float(extract_data_from(tables[4], 2).replace("-", "0").replace(".", "").replace(",", ".")),
                    'ebit_3': float(extract_data_from(tables[4], 3).replace("-", "0").replace(".", "").replace(",", ".")),
                    'lucro_liquido_12': float(extract_data_from(tables[4], 2).replace("-", "0").replace(".", "").replace(",", ".")),
                    'lucro_liquido_3': float(extract_data_from(tables[4], 3).replace("-", "0").replace(".", "").replace(",", ".")),

                })

        except Exception as ex: print(ex)
    #print(json.dumps(stocks_info))
    data = ""
    for x in stocks_info:
        data = data+(json.dumps(x)+"\n")

    with open('data2.json', 'w', encoding='utf-8') as f:
        f.write(data)
        f.close()

    print(data)
    # return json.dumps(stocks_info, indent=4)
    return data

def get_todays_data():
    with open('data2.json', encoding='utf-8') as json_file: 
        d = []
        for x in json_file:
            print (x)
            # d = d+(json.dumps(x)+"\n")
            d.append(x)
        print(d)
        return (', '.join(d))


# if __name__ == '__main__':
