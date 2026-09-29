import pytest
from datetime import date
import ecommerce

# ---------------------------------------------------------------------------
# Catalogo e prezzi
# ---------------------------------------------------------------------------

def test_calcola_prezzo_scontato_senza_sconto():
    assert ecommerce.calcola_prezzo_scontato(100, 0) == 100

def test_calcola_prezzo_scontato_con_sconto():
    assert ecommerce.calcola_prezzo_scontato(100, 20) == 80

def test_calcola_prezzo_scontato_sconto_totale():
    assert ecommerce.calcola_prezzo_scontato(100, 100) == 0

def test_calcola_prezzo_scontato_prezzo_zero():
    assert ecommerce.calcola_prezzo_scontato(0, 20) == 0

def test_calcola_prezzo_scontato_arrotondamento():
    assert ecommerce.calcola_prezzo_scontato(10, 33) == 6.7

def test_calcola_prezzo_scontato_prezzo_negativo():
    with pytest.raises(ValueError):
        ecommerce.calcola_prezzo_scontato(-10, 20)

def test_calcola_prezzo_scontato_sconto_negativo():
    with pytest.raises(ValueError):
        ecommerce.calcola_prezzo_scontato(100, -1)

def test_calcola_prezzo_scontato_sconto_superiore_al_cento():
    with pytest.raises(ValueError):
        ecommerce.calcola_prezzo_scontato(100, 101)

def test_applica_codice_sconto_codice_valido():
    tabella_codici = {"SCONTO20": 20}
    assert ecommerce.applica_codice_sconto(100, tabella_codici, "SCONTO20") == 80

def test_applica_codice_sconto_codice_inesistente():
    tabella_codici = {"ALTROSCONTO": 10}
    assert ecommerce.applica_codice_sconto(100, tabella_codici, "SCONTO20") == 100

def test_applica_codice_sconto_tabella_vuota():
    assert ecommerce.applica_codice_sconto(100, {}, "SCONTO20") == 100

def test_calcola_iva_aliquota_default():
    assert ecommerce.calcola_iva(100) == 122

def test_calcola_iva_aliquota_personalizzata():
    assert ecommerce.calcola_iva(100, aliquota=10) == 110

def test_calcola_iva_aliquota_zero():
    assert ecommerce.calcola_iva(100, aliquota=0) == 100

def test_calcola_iva_prezzo_zero():
    assert ecommerce.calcola_iva(0, aliquota=22) == 0

def test_calcola_iva_prezzo_negativo():
    with pytest.raises(ValueError):
        ecommerce.calcola_iva(-10, aliquota=22)

def test_calcola_iva_aliquota_negativa():
    with pytest.raises(ValueError):
        ecommerce.calcola_iva(100, aliquota=-1)


# ---------------------------------------------------------------------------
# Carrello
# ---------------------------------------------------------------------------

def test_crea_riga_carrello_prodotto_valido():
    riga = ecommerce.crea_riga_carrello("Mouse", 20, 2)
    assert riga["nome"] == "Mouse"
    assert riga["prezzo_unitario"] == 20
    assert riga["quantita"] == 2
    assert riga["subtotale"] == 40

def test_crea_riga_carrello_quantita_uno():
    riga = ecommerce.crea_riga_carrello("Mouse", 20, 1)
    assert riga["subtotale"] == 20

def test_crea_riga_carrello_prezzo_zero():
    riga = ecommerce.crea_riga_carrello("Prodotto gratuito", 0, 2)
    assert riga["subtotale"] == 0

def test_crea_riga_carrello_quantita_zero():
    with pytest.raises(ValueError):
        ecommerce.crea_riga_carrello("Mouse", 20, 0)

def test_crea_riga_carrello_quantita_negativa():
    with pytest.raises(ValueError):
        ecommerce.crea_riga_carrello("Mouse", 20, -1)

def test_crea_riga_carrello_prezzo_negativo():
    with pytest.raises(ValueError):
        ecommerce.crea_riga_carrello("Mouse", -20, 1)

def test_crea_riga_carrello_arrotondamento_subtotale():
    riga = ecommerce.crea_riga_carrello("Prodotto", 10.123, 2)
    assert riga["subtotale"] == 20.25

def test_calcola_totale_carrello_carrello_vuoto():
    assert ecommerce.calcola_totale_carrello([]) == 0

def test_calcola_totale_carrello_una_riga():
    carrello = [{"subtotale": 25}]
    assert ecommerce.calcola_totale_carrello(carrello) == 25

def test_calcola_totale_carrello_piu_righe():
    carrello = [{"subtotale": 10}, {"subtotale": 20}, {"subtotale": 30}]
    assert ecommerce.calcola_totale_carrello(carrello) == 60

def test_calcola_totale_carrello_arrotondamento():
    carrello = [{"subtotale": 10.123}, {"subtotale": 20.456}]
    assert ecommerce.calcola_totale_carrello(carrello) == 30.58

def test_svuota_articoli_esauriti_tutti_disponibili():
    carrello = [{"nome": "Mouse"}, {"nome": "Tastiera"}]
    magazzino = {"Mouse": 10, "Tastiera": 5}
    nuovo_carrello = ecommerce.svuota_articoli_esauriti(carrello, magazzino)
    assert len(nuovo_carrello) == 2

def test_svuota_articoli_esauriti_prodotto_esaurito():
    carrello = [{"nome": "Mouse"}, {"nome": "Tastiera"}]
    magazzino = {"Mouse": 0, "Tastiera": 5}
    nuovo_carrello = ecommerce.svuota_articoli_esauriti(carrello, magazzino)
    assert len(nuovo_carrello) == 1
    assert nuovo_carrello[0]["nome"] == "Tastiera"

def test_svuota_articoli_esauriti_prodotto_assente():
    carrello = [{"nome": "Mouse"}]
    magazzino = {"Tastiera": 5}
    nuovo_carrello = ecommerce.svuota_articoli_esauriti(carrello, magazzino)
    assert len(nuovo_carrello) == 0

def test_svuota_articoli_esauriti_carrello_vuoto():
    nuovo_carrello = ecommerce.svuota_articoli_esauriti([], {})
    assert len(nuovo_carrello) == 0

def test_svuota_articoli_esauriti_non_modifica_lista_originale():
    carrello = [{"nome": "Mouse"}, {"nome": "Tastiera"}]
    magazzino = {"Mouse": 0, "Tastiera": 5}
    nuovo_carrello = ecommerce.svuota_articoli_esauriti(carrello, magazzino)
    assert len(carrello) == 2
    assert carrello is not nuovo_carrello

def test_calcola_totale_ordine_senza_sconto():
    carrello = [{"nome": "Mouse", "subtotale": 100}]
    magazzino = {"Mouse": 10}
    totale_netto, totale_lordo = ecommerce.calcola_totale_ordine(carrello, magazzino)
    assert totale_netto == 100
    assert totale_lordo == 122

def test_calcola_totale_ordine_rimuove_esauriti():
    carrello = [{"nome": "Esaurito", "subtotale": 100}, {"nome": "Disponibile", "subtotale": 50}]
    magazzino = {"Esaurito": 0, "Disponibile": 10}
    righe_valide, totale_netto = ecommerce.calcola_totale_ordine(carrello, magazzino)
    assert len(righe_valide) == 1
    assert righe_valide[0]["nome"] == "Disponibile"
    assert totale_netto == 50

def test_calcola_totale_ordine_con_codice_sconto():
    carrello = [{"nome": "Mouse", "subtotale": 100}]
    magazzino = {"Mouse": 10}
    tabella_codici = {"SCONTO20": 20}
    totale_netto, totale_lordo = ecommerce.calcola_totale_ordine(carrello, magazzino, codice_sconto="SCONTO20", tabella_codici=tabella_codici)
    assert totale_netto == 80
    assert totale_lordo == 97.6

def test_calcola_totale_ordine_codice_inesistente():
    carrello = [{"nome": "Mouse", "subtotale": 100}]
    magazzino = {"Mouse": 10}
    tabella_codici = {"SCONTO20": 20}
    totale_netto, totale_lordo = ecommerce.calcola_totale_ordine(carrello, magazzino, codice_sconto="FALSO", tabella_codici=tabella_codici)
    assert totale_netto == 100
    assert totale_lordo == 122

def test_calcola_totale_ordine_tabella_codici_vuota():
    carrello = [{"nome": "Mouse", "subtotale": 100}]
    magazzino = {"Mouse": 10}
    totale_netto, totale_lordo = ecommerce.calcola_totale_ordine(carrello, magazzino, codice_sconto="SCONTO20", tabella_codici={})
    assert totale_netto == 100
    assert totale_lordo == 122

def test_calcola_totale_ordine_senza_codice_sconto():
    carrello = [{"nome": "Mouse", "subtotale": 100}]
    magazzino = {"Mouse": 10}
    totale_netto, totale_lordo = ecommerce.calcola_totale_ordine(carrello, magazzino, codice_sconto=None)
    assert totale_netto == 100
    assert totale_lordo == 122

def test_calcola_totale_ordine_carrello_vuoto():
    righe_valide, totale_netto, totale_lordo = ecommerce.calcola_totale_ordine([], {})
    assert len(righe_valide) == 0
    assert totale_netto == 0
    assert totale_lordo == 0


# ---------------------------------------------------------------------------
# Spedizione
# ---------------------------------------------------------------------------

def test_calcola_costo_spedizione_parametri_base():
    assert ecommerce.calcola_costo_spedizione(10, 100, espressa=False) == 10

def test_calcola_costo_spedizione_peso_zero():
    assert ecommerce.calcola_costo_spedizione(0, 100, espressa=False) == 5

def test_calcola_costo_spedizione_distanza_zero():
    assert ecommerce.calcola_costo_spedizione(10, 0, espressa=False) == 8

def test_calcola_costo_spedizione_peso_massimo():
    costo = ecommerce.calcola_costo_spedizione(30, 100, espressa=False)
    assert costo == 15

def test_calcola_costo_spedizione_espressa():
    assert ecommerce.calcola_costo_spedizione(10, 100, espressa=True) == 20

def test_calcola_costo_spedizione_peso_negativo():
    with pytest.raises(ValueError):
        ecommerce.calcola_costo_spedizione(-1, 100)

def test_calcola_costo_spedizione_distanza_negativa():
    with pytest.raises(ValueError):
        ecommerce.calcola_costo_spedizione(10, -1)

def test_calcola_costo_spedizione_peso_superiore_al_massimo():
    with pytest.raises(ValueError):
        ecommerce.calcola_costo_spedizione(30.01, 100)

def test_calcola_costo_spedizione_arrotondamento():
    costo = ecommerce.calcola_costo_spedizione(1, 1, espressa=False)
    assert round(costo, 2) == costo

def test_stima_data_consegna_zero_giorni_lavorativi():
    data_ordine = date(2024, 1, 1)  # Lunedì
    assert ecommerce.stima_data_consegna(data_ordine, 0) == data_ordine

def test_stima_data_consegna_un_giorno_lavorativo():
    data_ordine = date(2024, 1, 1)  # Lunedì
    assert ecommerce.stima_data_consegna(data_ordine, 1) == date(2024, 1, 2)

def test_stima_data_consegna_salva_il_weekend():
    data_ordine = date(2024, 1, 5)  # Venerdì
    assert ecommerce.stima_data_consegna(data_ordine, 1) == date(2024, 1, 8)  # Lunedì

def test_stima_data_consegna_due_giorni_da_venerdi():
    data_ordine = date(2024, 1, 5)  # Venerdì
    assert ecommerce.stima_data_consegna(data_ordine, 2) == date(2024, 1, 9)  # Martedì

def test_stima_data_consegna_da_sabato():
    data_ordine = date(2024, 1, 6)  # Sabato
    assert ecommerce.stima_data_consegna(data_ordine, 1) == date(2024, 1, 8)  # Lunedì

def test_stima_data_consegna_da_domenica():
    data_ordine = date(2024, 1, 7)  # Domenica
    assert ecommerce.stima_data_consegna(data_ordine, 1) == date(2024, 1, 8)  # Lunedì

def test_stima_data_consegna_giorni_lavorativi_negativi():
    with pytest.raises(ValueError):
        ecommerce.stima_data_consegna(date(2024, 1, 1), -1)


# ---------------------------------------------------------------------------
# Fedeltà cliente / punti
# ---------------------------------------------------------------------------

def test_calcola_punti_fedelta_zero_punti_per_dieci_euro_acquisto():
    assert ecommerce.calcola_punti_fedelta(3) == 0

def test_calcola_punti_fedelta_dieci_euro():
    assert ecommerce.calcola_punti_fedelta(10) == 1

def test_calcola_punti_fedelta_multipli_di_dieci():
    assert ecommerce.calcola_punti_fedelta(50) == 5

def test_calcola_punti_fedelta_importo_non_intero():
    assert ecommerce.calcola_punti_fedelta(25) == 2

def test_calcola_punti_fedelta_moltiplicatore():
    assert ecommerce.calcola_punti_fedelta(50, moltiplicatore=2) == 10

def test_calcola_punti_fedelta_importo_zero():
    assert ecommerce.calcola_punti_fedelta(0) == 0

def test_calcola_punti_fedelta_totale_negativo():
    with pytest.raises(ValueError):
        ecommerce.calcola_punti_fedelta(-10)

def test_calcola_punti_fedelta_moltiplicatore_zero():
    with pytest.raises(ValueError):
        ecommerce.calcola_punti_fedelta(100, moltiplicatore=0)

def test_calcola_punti_fedelta_moltiplicatore_negativo():
    with pytest.raises(ValueError):
        ecommerce.calcola_punti_fedelta(100, moltiplicatore=-1)

def test_promuovi_livello_cliente_zero_punti():
    assert ecommerce.promuovi_livello_cliente(0) == "bronze"

def test_promuovi_livello_cliente_limite_bronze():
    assert ecommerce.promuovi_livello_cliente(99) == "bronze"

def test_promuovi_livello_cliente_limite_silver():
    assert ecommerce.promuovi_livello_cliente(100) == "silver"

def test_promuovi_livello_cliente_limite_gold():
    assert ecommerce.promuovi_livello_cliente(500) == "gold"

def test_promuovi_livello_cliente_limite_platinum():
    assert ecommerce.promuovi_livello_cliente(2000) == "platinum"

def test_promuovi_livello_cliente_punti_negativi():
    with pytest.raises(ValueError):
        ecommerce.promuovi_livello_cliente(-1)

def test_riepilogo_cliente_valori_base():
    riepilogo = ecommerce.riepilogo_cliente(100)
    assert riepilogo["totale_speso"] == 100
    assert riepilogo["punti"] == 10
    assert riepilogo["livello"] == "bronze"

def test_riepilogo_cliente_livello_silver():
    riepilogo = ecommerce.riepilogo_cliente(1000)
    assert riepilogo["totale_speso"] == 1000
    assert riepilogo["punti"] == 100
    assert riepilogo["livello"] == "silver"

def test_riepilogo_cliente_livello_gold():
    riepilogo = ecommerce.riepilogo_cliente(5000)
    assert riepilogo["totale_speso"] == 5000
    assert riepilogo["punti"] == 500
    assert riepilogo["livello"] == "gold"

def test_riepilogo_cliente_livello_platinum():
    riepilogo = ecommerce.riepilogo_cliente(20000)
    assert riepilogo["totale_speso"] == 20000
    assert riepilogo["punti"] == 2000
    assert riepilogo["livello"] == "platinum"

def test_riepilogo_cliente_con_moltiplicatore():
    riepilogo = ecommerce.riepilogo_cliente(100, moltiplicatore=2)
    assert riepilogo["totale_speso"] == 100
    assert riepilogo["punti"] == 20
    assert riepilogo["livello"] == "bronze"

def test_riepilogo_cliente_totale_negativo():
    with pytest.raises(ValueError):
        ecommerce.riepilogo_cliente(-100)

def test_riepilogo_cliente_moltiplicatore_non_valido():
    with pytest.raises(ValueError):
        ecommerce.riepilogo_cliente(100, moltiplicatore=0)