# clima.py - Previsao do tempo via API Open-Meteo (gratuita, sem chave)

import requests

LAT = -6.757   # Sousa - PB
LON = -38.229


def consultar_clima():
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        "&current=temperature_2m,precipitation,weathercode"
        "&daily=precipitation_sum,temperature_2m_max,temperature_2m_min"
        "&timezone=America%2FFortaleza&forecast_days=3"
    )
    try:
        resp = requests.get(url, timeout=5)
        dados = resp.json()

        atual = dados.get('current', {})
        daily = dados.get('daily', {})

        previsao = []
        for i in range(len(daily.get('time', []))):
            previsao.append({
                'data':      daily['time'][i],
                'chuva_mm':  daily['precipitation_sum'][i],
                'temp_max':  daily['temperature_2m_max'][i],
                'temp_min':  daily['temperature_2m_min'][i]
            })

        return {
            'temperatura': atual.get('temperature_2m', 'N/D'),
            'precipitacao': atual.get('precipitation', 0),
            'codigo': atual.get('weathercode', 0),
            'previsao': previsao
        }
    except Exception:
        return None


def descrever_tempo(codigo):
    tabela = {
        0: 'Ceu limpo', 1: 'Principalmente claro', 2: 'Parcialmente nublado',
        3: 'Nublado', 45: 'Neblina', 51: 'Garoa leve', 61: 'Chuva leve',
        63: 'Chuva moderada', 65: 'Chuva forte', 80: 'Pancadas de chuva',
        95: 'Trovoada'
    }
    return tabela.get(codigo, 'Condicao desconhecida')