"""
ecommerce.py

Modulo didattico a tema e-commerce.
Nessuna funzione qui dentro tocca il filesystem o chiama API esterne:
sono tutte funzioni pure, così possono essere testate in isolamento
con semplici pytest.

Consegna per gli studenti: scrivere i test di unità per queste funzioni.
Suggerimento: pensate anche a input "cattivi" o limite (carrello vuoto,
quantità negative, codici sconto inesistenti, prezzi a zero...) oltre
ai casi "felici".
"""

from datetime import datetime


# ---------------------------------------------------------------------------
# Catalogo e prezzi
# ---------------------------------------------------------------------------

def calcola_prezzo_scontato(prezzo, percentuale_sconto):
    """
    Applica una percentuale di sconto a un prezzo.

    - prezzo: numero >= 0
    - percentuale_sconto: numero tra 0 e 100

    Solleva ValueError se prezzo è negativo o se la percentuale
    non è compresa tra 0 e 100.
    """
    if prezzo < 0:
        raise ValueError("il prezzo non può essere negativo")
    if not (0 <= percentuale_sconto <= 100):
        raise ValueError("la percentuale di sconto deve essere tra 0 e 100")

    prezzo_finale = prezzo * (1 - percentuale_sconto / 100)
    return round(prezzo_finale, 2)


def applica_codice_sconto(prezzo, codice, tabella_codici):
    """
    Applica uno sconto a partire da un codice promozionale.

    - tabella_codici: dizionario {codice: percentuale_sconto}
    - se il codice non esiste, il prezzo non viene scontato

    Riusa calcola_prezzo_scontato internamente.
    """
    percentuale = tabella_codici.get(codice, 0)
    return calcola_prezzo_scontato(prezzo, percentuale)


def calcola_iva(prezzo_netto, aliquota=22):
    """
    Calcola il prezzo lordo applicando l'IVA (default 22%).
    Solleva ValueError se prezzo_netto è negativo o aliquota è negativa.
    """
    if prezzo_netto < 0:
        raise ValueError("il prezzo netto non può essere negativo")
    if aliquota < 0:
        raise ValueError("l'aliquota non può essere negativa")

    return round(prezzo_netto * (1 + aliquota / 100), 2)


# ---------------------------------------------------------------------------
# Carrello
# ---------------------------------------------------------------------------

def crea_riga_carrello(nome_prodotto, prezzo_unitario, quantita):
    """
    Crea una singola riga del carrello come dizionario.
    Solleva ValueError se quantità <= 0 o prezzo_unitario < 0.
    """
    if quantita <= 0:
        raise ValueError("la quantità deve essere maggiore di zero")
    if prezzo_unitario < 0:
        raise ValueError("il prezzo unitario non può essere negativo")

    return {
        "nome": nome_prodotto,
        "prezzo_unitario": prezzo_unitario,
        "quantita": quantita,
        "subtotale": round(prezzo_unitario * quantita, 2),
    }


def calcola_totale_carrello(righe_carrello):
    """
    Somma i subtotali di tutte le righe di un carrello.
    Un carrello vuoto ha totale 0.
    """
    return round(sum(riga["subtotale"] for riga in righe_carrello), 2)


def svuota_articoli_esauriti(righe_carrello, magazzino):
    """
    Rimuove dal carrello le righe i cui prodotti non sono più
    disponibili in magazzino (quantità disponibile 0 o assente).

    - magazzino: dizionario {nome_prodotto: quantita_disponibile}

    Ritorna una NUOVA lista, senza modificare quella in input.
    """
    return [
        riga for riga in righe_carrello
        if magazzino.get(riga["nome"], 0) > 0
    ]


def calcola_totale_ordine(righe_carrello, magazzino, codice_sconto=None,
                           tabella_codici=None, aliquota_iva=22):
    """
    Funzione "orchestratore" che compone le altre:
    1. rimuove gli articoli esauriti
    2. calcola il totale del carrello residuo
    3. applica un eventuale codice sconto
    4. applica l'IVA

    Ritorna un dizionario con il dettaglio del calcolo.
    """
    righe_valide = svuota_articoli_esauriti(righe_carrello, magazzino)
    totale_netto = calcola_totale_carrello(righe_valide)

    if codice_sconto and tabella_codici:
        totale_netto = applica_codice_sconto(
            totale_netto, codice_sconto, tabella_codici
        )

    totale_lordo = calcola_iva(totale_netto, aliquota_iva)

    return {
        "righe_valide": righe_valide,
        "totale_netto": totale_netto,
        "totale_lordo": totale_lordo,
    }


# ---------------------------------------------------------------------------
# Spedizione
# ---------------------------------------------------------------------------

def calcola_costo_spedizione(peso_kg, distanza_km, espressa=False):
    """
    Calcola il costo di spedizione secondo una tariffa semplificata:
    - costo base: 3.0
    - + 0.5 per ogni kg
    - + 0.02 per ogni km
    - se espressa: costo finale raddoppiato

    Sopra i 30 kg la spedizione non è consentita (ValueError).
    Peso o distanza negativi sollevano ValueError.
    """
    if peso_kg < 0 or distanza_km < 0:
        raise ValueError("peso e distanza non possono essere negativi")
    if peso_kg > 30:
        raise ValueError("peso massimo consentito: 30 kg")

    costo = 3.0 + 0.5 * peso_kg + 0.02 * distanza_km
    if espressa:
        costo *= 2

    return round(costo, 2)


def stima_data_consegna(giorno_ordine, giorni_lavorativi):
    """
    Calcola la data di consegna stimata saltando i weekend.

    - giorno_ordine: oggetto datetime.date
    - giorni_lavorativi: intero >= 0, numero di giorni lavorativi da aggiungere

    Solleva ValueError se giorni_lavorativi è negativo.
    """
    if giorni_lavorativi < 0:
        raise ValueError("i giorni lavorativi non possono essere negativi")

    data_corrente = giorno_ordine
    giorni_aggiunti = 0

    while giorni_aggiunti < giorni_lavorativi:
        data_corrente = data_corrente.fromordinal(data_corrente.toordinal() + 1)
        # weekday(): lunedì=0 ... domenica=6
        if data_corrente.weekday() < 5:
            giorni_aggiunti += 1

    return data_corrente


# ---------------------------------------------------------------------------
# Fedeltà cliente / punti
# ---------------------------------------------------------------------------

def calcola_punti_fedelta(totale_speso, moltiplicatore=1):
    """
    Assegna 1 punto fedeltà ogni 10 euro spesi (arrotondato per difetto),
    moltiplicato per un eventuale moltiplicatore (es. periodo promozionale).

    Solleva ValueError se totale_speso è negativo o moltiplicatore <= 0.
    """
    if totale_speso < 0:
        raise ValueError("il totale speso non può essere negativo")
    if moltiplicatore <= 0:
        raise ValueError("il moltiplicatore deve essere positivo")

    punti_base = int(totale_speso // 10)
    return punti_base * moltiplicatore


def promuovi_livello_cliente(punti_totali):
    """
    Determina il livello fedeltà del cliente in base ai punti totali:
    - 0-99: "bronze"
    - 100-499: "silver"
    - 500-1999: "gold"
    - 2000+: "platinum"

    Solleva ValueError se punti_totali è negativo.
    """
    if punti_totali < 0:
        raise ValueError("i punti totali non possono essere negativi")

    if punti_totali >= 2000:
        return "platinum"
    if punti_totali >= 500:
        return "gold"
    if punti_totali >= 100:
        return "silver"
    return "bronze"


def riepilogo_cliente(totale_speso_storico, moltiplicatore=1):
    """
    Funzione che compone calcola_punti_fedelta e promuovi_livello_cliente
    per restituire un riepilogo completo del cliente.
    """
    punti = calcola_punti_fedelta(totale_speso_storico, moltiplicatore)
    livello = promuovi_livello_cliente(punti)

    return {
        "totale_speso": totale_speso_storico,
        "punti": punti,
        "livello": livello,
    }
