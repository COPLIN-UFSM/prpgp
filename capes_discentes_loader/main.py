import argparse
import os
import pandas as pd
from db2 import DB2Connection
from tqdm import tqdm
from datetime import datetime

def get_data_ingresso(date_string):
    #aceita ano com 2 ou 4 dígitos
    formats = ['%d%b%Y:%H:%M:%S', '%d%b%y:%H:%M:%S']
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unable to parse date: {date_string}")

def carrega_arquivo(credentials, *, arquivo):
    with (DB2Connection(credentials) as db2_conn):
        with open('instance\\dados.csv', mode='rb') as f:
            df = pd.read_csv(f,
                            sep=';',
                            encoding='iso8859-1',
                            quotechar='"',
                            )
            for index, row in tqdm(list(df.iterrows()), 'Carregando dados'):
                data_objeto = get_data_ingresso(row['DT_MATRICULA_DISCENTE'])
                codigo_emec = row['CD_ENTIDADE_EMEC']

                db2_conn.insert('BEE.DISCENTES_POS_GRADUACAO_SUCUPIRA',
                                {
                                    'ANO': row['AN_BASE'],
                                    'COD_AREA_AVALIACAO': row['CD_AREA_AVALIACAO'],
                                    'NOME_AREA_AVALIACAO': row['NM_AREA_AVALIACAO'],
                                    'COD_CAPES_IES': row['CD_ENTIDADE_CAPES'],
                                    'COD_EMEC_IES': None if (codigo_emec == "NI") else codigo_emec,
                                    'MODALIDADE': row['NM_MODALIDADE_PROGRAMA'],
                                    'COD_PROGRAMA': row['CD_PROGRAMA_IES'],
                                    'NOME_PROGRAMA': row['NM_PROGRAMA_IES'],
                                    'GRAU': row['DS_GRAU_ACADEMICO_DISCENTE'],
                                    'UF_PROGRAMA': row['SG_UF_PROGRAMA'],
                                    'MUNICIPIO_PROGRAMA': row['NM_MUNICIPIO_PROGRAMA_IES'],
                                    'CONCEITO_PROGRAMA': row['CD_CONCEITO_PROGRAMA'],
                                    'TIPO_DOCUMENTO': row['TP_DOCUMENTO_DISCENTE'],
                                    'NUMERO_DOCUMENTO': row['NR_DOCUMENTO_DISCENTE'],
                                    'NOME_DISCENTE': row['NM_DISCENTE'],
                                    'PAIS_NACIONALIDADE': row['NM_PAIS_NACIONALIDADE_DISCENTE'],
                                    'ANO_NASCIMENTO': row['AN_NASCIMENTO_DISCENTE'],
                                    'DESCR_SITUACAO': row['NM_SITUACAO_DISCENTE'],
                                    'DT_MATRICULA': data_objeto.date().isoformat()
                                })

def main():
    credentials = os.path.join('instance', 'credentials.json')

    carrega_arquivo(credentials, arquivo = 'instance\\dados.csv')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Carrega os dados dos discentes da capes, plataforma sucupira.'
    )

    main()