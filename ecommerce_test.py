import pytest
from datetime import date
import ecommerce

# 0 Punti fedeltà
def test_calcola_punti_fedelta_zero_punti_per_dieci_euro_acquisto():
    acquisto = 3
    punti = ecommerce.calcola_punti_fedelta(acquisto)
    assert punti == 0

# Prezzo scontato senza sconto
def test_calcola_prezzo_scontato_senza_sconto():
    prezzo = 100
    sconto = 0
    prezzo_finale = ecommerce.calcola_prezzo_scontato(prezzo, sconto)
    assert prezzo_finale == 100

# Prezzo scontato con sconto
def test_calcola_prezzo_scontato_con_sconto():
    prezzo = 100
    sconto = 20
    prezzo_finale = ecommerce.calcola_prezzo_scontato(prezzo, sconto)
    assert prezzo_finale == 80

# Prezzo scontato con sconto totale
def test_calcola_prezzo_scontato_sconto_totale():
    prezzo = 100
    sconto = 100
    prezzo_finale = ecommerce.calcola_prezzo_scontato(prezzo, sconto)
    assert prezzo_finale == 0

# Prezzo negativo
def test_calcola_prezzo_scontato_prezzo_negativo():
    prezzo = -10
    sconto = 20
    with pytest.raises(ValueError):
        ecommerce.calcola_prezzo_scontato(prezzo, sconto)

# IVA con aliquota default
def test_calcola_iva_con_aliquota_default():
    prezzo_netto = 100
    prezzo_lordo = ecommerce.calcola_iva(prezzo_netto)
    assert prezzo_lordo == 122

# IVA con aliquota personalizzata
def test_calcola_iva_con_aliquota_personalizzata():
    prezzo_netto = 100
    aliquota = 10
    prezzo_lordo = ecommerce.calcola_iva(prezzo_netto, aliquota)
    assert prezzo_lordo == 110

# IVA con prezzo negativo
def test_calcola_iva_prezzo_negativo():
    prezzo_netto = -10
    with pytest.raises(ValueError):
        ecommerce.calcola_iva(prezzo_netto)

# Creazione di una riga del carrello
def test_crea_riga_carrello():
    nome = "Mouse"
    prezzo = 20
    quantita = 2
    riga = ecommerce.crea_riga_carrello(nome, prezzo, quantita)
    
    assert riga["nome"] == "Mouse"
    assert riga["prezzo"] == 20
    assert riga["quantita"] == 2
    assert riga["subtotale"] == 40

# Creazione riga con quantità non valida
def test_crea_riga_carrello_quantita_non_valida():
    nome = "Mouse"
    prezzo = 20
    quantita = 0
    with pytest.raises(ValueError):
        ecommerce.crea_riga_carrello(nome, prezzo, quantita)

# Totale carrello vuoto
def test_calcola_totale_carrello_vuoto():
    carrello = []
    totale = ecommerce.calcola_totale_carrello(carrello)
    assert totale == 0

# Totale carrello con prodotti
def test_calcola_totale_carrello_con_prodotti():
    carrello = [
        {"nome": "Prodotto 1", "prezzo": 20, "quantita": 1, "subtotale": 20},
        {"nome": "Prodotto 2", "prezzo": 15, "quantita": 2, "subtotale": 30}
    ]
    totale = ecommerce.calcola_totale_carrello(carrello)
    assert totale == 50

# Costo della spedizione
def test_calcola_costo_spedizione():
    peso = 10
    distanza = 100
    costo = ecommerce.calcola_costo_spedizione(peso, distanza)
    assert costo == 10

# Costo della spedizione espressa
def test_calcola_costo_spedizione_espressa():
    peso = 10
    distanza = 100
    espressa = True
    costo = ecommerce.calcola_costo_spedizione(peso, distanza, espressa=espressa)
    assert costo == 20

# Costo della spedizione con peso negativo
def test_calcola_costo_spedizione_peso_negativo():
    peso = -1
    distanza = 100
    with pytest.raises(ValueError):
        ecommerce.calcola_costo_spedizione(peso, distanza)

# Punti fedeltà con 10 euro
def test_calcola_punti_fedelta_dieci_euro():
    acquisto = 10
    punti = ecommerce.calcola_punti_fedelta(acquisto)
    assert punti == 1

# Punti fedeltà con moltiplicatore
def test_calcola_punti_fedelta_con_moltiplicatore():
    acquisto = 20
    moltiplicatore = 2
    punti = ecommerce.calcola_punti_fedelta(acquisto, moltiplicatore=moltiplicatore)
    assert punti == 4

# Punti fedeltà con totale negativo
def test_calcola_punti_fedelta_totale_negativo():
    acquisto = -10
    with pytest.raises(ValueError):
        ecommerce.calcola_punti_fedelta(acquisto)

# Livello cliente bronze
def test_promuovi_livello_cliente_bronze():
    punti = 50
    livello = ecommerce.promuovi_livello_cliente(punti)
    assert livello == "bronze"

# Livello cliente silver
def test_promuovi_livello_cliente_silver():
    punti = 100
    livello = ecommerce.promuovi_livello_cliente(punti)
    assert livello == "silver"

# Livello cliente gold
def test_promuovi_livello_cliente_gold():
    punti = 500
    livello = ecommerce.promuovi_livello_cliente(punti)
    assert livello == "gold"

# Livello cliente con punti negativi
def test_promuovi_livello_cliente_punti_negativi():
    punti = -1
    with pytest.raises(ValueError):
        ecommerce.promuovi_livello_cliente(punti)

# Applicazione di un codice sconto valido
def test_applica_codice_sconto_valido():
    prezzo = 100
    codice = "SCONTO20"
    tabella_codici = {"SCONTO20": 20, "SCONTO10": 10}
    prezzo_finale = ecommerce.applica_codice_sconto(prezzo, codice, tabella_codici)
    assert prezzo_finale == 80

# Applicazione di un codice sconto inesistente
def test_applica_codice_sconto_inesistente():
    prezzo = 100
    codice = "SCONTO20"
    tabella_codici = {"SCONTO10": 10}
    prezzo_finale = ecommerce.applica_codice_sconto(prezzo, codice, tabella_codici)
    assert prezzo_finale == 100

# Rimozione dei prodotti esauriti
def test_svuota_articoli_esauriti():
    carrello = ["Mouse", "Tastiera"]
    magazzino = {"Mouse": 5, "Tastiera": 0}  # Quantità disponibili in magazzino
    carrello_aggiornato = ecommerce.svuota_articoli_esauriti(carrello, magazzino)
    
    assert "Mouse" in carrello_aggiornato
    assert "Tastiera" not in carrello_aggiornato
    assert len(carrello_aggiornato) == 1

# Data di consegna durante la settimana
def test_stima_data_consegna_giorno_lavorativo():
    # 1 gennaio 2024 è un lunedì
    data_ordine = date(2024, 1, 1)
    giorni_lavorativi_consegna = 2
    data_consegna = ecommerce.stima_data_consegna(data_ordine, giorni_lavorativi_consegna)
    
    # Ci aspettiamo mercoledì 3 gennaio 2024
    assert data_consegna == date(2024, 1, 3)

# Data di consegna saltando il weekend
def test_stima_data_consegna_salta_weekend():
    # 5 gennaio 2024 è un venerdì
    data_ordine = date(2024, 1, 5)
    giorni_lavorativi_consegna = 1
    data_consegna = ecommerce.stima_data_consegna(data_ordine, giorni_lavorativi_consegna)
    
    # 1 giorno lavorativo dopo venerdì ci aspettiamo lunedì 8 gennaio 2024
    assert data_consegna == date(2024, 1, 8)

# Riepilogo del cliente
def test_riepilogo_cliente():
    totale_speso = 1000
    riepilogo = ecommerce.riepilogo_cliente(totale_speso)
    
    assert riepilogo["totale_speso"] == 1000
    assert riepilogo["punti"] == 100
    assert riepilogo["livello"] == "silver"