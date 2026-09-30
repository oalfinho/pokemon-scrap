import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

URL = "https://pokemondb.net/pokedex/all"
HEADERS = {"User-Agent": "Mozilla/5.0 (projeto universitario)"}

GERACOES = [
    (1, 151), (152, 251), (252, 386), (387, 493), (494, 649),
    (650, 721), (722, 809), (810, 905), (906, 1025),
]

def geracao(numero: int) -> int:
    for i, (ini, fim) in enumerate(GERACOES, start=1):
        if ini <= numero <= fim:
            return i
    return 0 

def coletar() -> pd.DataFrame:
    resp = requests.get(URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    tabela = BeautifulSoup(resp.text, "html.parser").find("table", id="pokedex")

    dados = []
    for linha in tabela.tbody.find_all("tr"):
        cols = linha.find_all("td")
        dados.append({
            "numero": int(cols[0].get_text(strip=True)),
            "nome": cols[1].get_text(strip=True),
            "tipos": "/".join(a.get_text() for a in cols[2].find_all("a")),
            "total": int(cols[3].text),
        })
    df = pd.DataFrame(dados)
    df = df.drop_duplicates(subset="numero", keep="first")
    df["geracao"] = df["numero"].apply(geracao)
    return df

def main():
    df = coletar()
    df.to_csv("pokemon.csv", index=False)

    dist = df["geracao"].value_counts().sort_index()
    print(dist)

    ax = dist.plot(kind="bar", color="#EE1515", edgecolor="black")
    ax.set_title("Pokémon por geração")
    ax.set_xlabel("Geração")
    ax.set_ylabel("Quantidade")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("distribuicao_geracao.png", dpi=150)
    plt.show()

if __name__ == "__main__":
    main()