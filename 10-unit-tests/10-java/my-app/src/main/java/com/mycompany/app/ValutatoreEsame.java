package com.mycompany.app;

public class ValutatoreEsame {

    public boolean isPromosso(int voto) {
        return voto >= 18;
    }

    public String calcolaGiudizio(int voto) {
        if (voto < 18) {
            return "Insufficiente";
        } else if (voto <= 23) {
            return "Sufficiente";
        } else if (voto <= 27) {
            return "Buono";
        } else {
            return "Ottimo";
        }
    }
}
