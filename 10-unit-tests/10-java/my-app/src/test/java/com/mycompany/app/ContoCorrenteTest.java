package com.mycompany.app;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class ContoCorrenteTest {

    @Test
    public void testIstanza() {
        // Given / When: creazione dell'istanza di ContoCorrente
        ContoCorrente conto = new ContoCorrente();

        // Then: il saldo restituito da getSaldo() deve essere uguale a 0
        assertEquals(0, conto.getSaldo());
    }

    @Test
    public void testSetSaldo() {
        // Given: un conto corrente appena creato
        ContoCorrente conto = new ContoCorrente();

        // When: invochiamo la fn: setSaldo(100)
        conto.setSaldo(100);

        // Then: il saldo viene settato a 100
        assertEquals(100, conto.getSaldo());

        // Then: altrimenti (saldo != 0), viene restituito IllegalArgumentException
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            conto.setSaldo(50);
        });

        assertEquals("non è possibile impostare un nuovo saldo, è necessario fare un acconto", exception.getMessage());
    }

    @Test
    public void testDepositaNormale() {
        // Given: un conto corrente già creato
        ContoCorrente conto = new ContoCorrente();

        // When: invochiamo la fn: deposita() con un valore > 0
        boolean esito = conto.deposita(50);

        // Then: la funzione restituisce true e il saldo aumenta
        assertTrue(esito);
        assertEquals(50, conto.getSaldo());
    }

    @Test
    public void testDepositaZero() {
        // Given: un conto già creato
        ContoCorrente conto = new ContoCorrente();
        double saldoIniziale = conto.getSaldo();

        // When: invochiamo la fn: deposita(0)
        boolean esito = conto.deposita(0);

        // Then: la funzione restituisce false e il saldo non aumenta
        assertFalse(esito);
        assertEquals(saldoIniziale, conto.getSaldo());
    }

    @Test
    public void testDepositaNegativo() {
        // Given: un conto già creato
        ContoCorrente conto = new ContoCorrente();
        double saldoIniziale = conto.getSaldo();

        // When: invochiamo la fn: deposita() con un valore negativo (es. -50)
        boolean esito = conto.deposita(-50);

        // Then: la funzione restituisce false e il saldo rimane lo stesso
        assertFalse(esito);
        assertEquals(saldoIniziale, conto.getSaldo());
    }

    @Test
    void testPrelevaNormale() {
        ContoCorrente conto = new ContoCorrente();
        conto.setSaldo(100.0);
        double saldoIniziale = conto.getSaldo();

        boolean esito = conto.preleva(50.0);

        assertTrue(esito);
        assertEquals(saldoIniziale - 50.0, conto.getSaldo());
    }

    @Test
    void testPrelevaZero() {
        ContoCorrente conto = new ContoCorrente();
        conto.setSaldo(100.0);
        double saldoIniziale = conto.getSaldo();

        boolean esito = conto.preleva(0.0);

        assertTrue(esito);
        assertEquals(saldoIniziale, conto.getSaldo());
    }

    @Test
    void testPrelevaNegativo() {
        ContoCorrente conto = new ContoCorrente();
        conto.setSaldo(100.0);
        double saldoIniziale = conto.getSaldo();

        conto.preleva(-50.0);

        // Senza controllo sui prelievi negativi, l'operazione sottrae una quantità negativa, incrementando il saldo
        assertEquals(saldoIniziale - (-50.0), conto.getSaldo());
    }

    @Test
    void testPrelevaMaggioreSaldo() {
        ContoCorrente conto = new ContoCorrente();
        conto.setSaldo(100.0);
        double saldoIniziale = conto.getSaldo();

        boolean esito = conto.preleva(150.0);

        assertFalse(esito);
        assertEquals(saldoIniziale, conto.getSaldo());
    }
}