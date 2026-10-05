package com.mycompany.app;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class ValutatoreEsameTest {

    @Test
    public void testStudenteBocciato() {
        ValutatoreEsame valutatore = new ValutatoreEsame();
        int voto = 15;

        boolean promosso = valutatore.isPromosso(voto);
        String giudizio = valutatore.calcolaGiudizio(voto);

        assertFalse(promosso);
        assertEquals("Insufficiente", giudizio);
    }

    @Test
    public void testStudentePromossoConOttimo() {
        ValutatoreEsame valutatore = new ValutatoreEsame();
        int voto = 30;

        boolean promosso = valutatore.isPromosso(voto);
        String giudizio = valutatore.calcolaGiudizio(voto);

        assertTrue(promosso);
        assertEquals("Ottimo", giudizio);
    }

    @Test
    public void testGiudiziIntermedi() {
        ValutatoreEsame valutatore = new ValutatoreEsame();

        assertEquals("Sufficiente", valutatore.calcolaGiudizio(20));
        assertEquals("Buono", valutatore.calcolaGiudizio(25));
    }
}
