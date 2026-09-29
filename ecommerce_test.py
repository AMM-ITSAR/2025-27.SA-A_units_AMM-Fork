# i tuoi test di unità qua
import ecommerce

def test_calcola_punti_fedelta_zero_punti_per_dieci_euro_acquisto():
    punti_fedelta = ecommerce.calcola_punti_fedelta(3,2)
    assert punti_fedelta == 3
