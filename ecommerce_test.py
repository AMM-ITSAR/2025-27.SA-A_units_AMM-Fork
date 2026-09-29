# i tuoi test di unità qua
import ecommerce
import pytest

def test_calcola_punti_fedelta_zero_punti_per_dieci_euro_acquisto():
    punti_fedelta = ecommerce.calcola_punti_fedelta(3,2)
    assert punti_fedelta == 0

# inferire la presenza di eccezioni
# buona pratica per test che cercano appositamente situazioni limite
# si verifica inoltre che il messaggio dell'eccezione sia esattamente quello che cercavamo
def test_calcola_punti_fedelta_zero_punti_per_dieci_euro_acquisto_raise():
    with pytest.raises(ValueError, match=r"^il totale speso non può essere negativo$"):
        ecommerce.calcola_punti_fedelta(-3)
