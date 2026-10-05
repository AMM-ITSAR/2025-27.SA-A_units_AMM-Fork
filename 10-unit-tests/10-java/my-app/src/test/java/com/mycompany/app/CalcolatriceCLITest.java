package com.mycompany.app;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class CalcolatriceCLITest {

    private final PrintStream originalOut = System.out;
    private final InputStream originalIn = System.in;

    private ByteArrayOutputStream output;

    @BeforeEach
    void setUp() {
        output = new ByteArrayOutputStream();
        System.setOut(new PrintStream(output, true, StandardCharsets.UTF_8));
    }

    @AfterEach
    void tearDown() {
        System.setOut(originalOut);
        System.setIn(originalIn);
    }

    /*
     * Scenario: test_istanziamento_classe
     *
     * Given la classe CalcolatriceCLI
     * When viene creata un'istanza della classe
     * Then L'oggetto viene creato con successo
     */
    @Test
    void test_istanziamento_classe() {
        CalcolatriceCLI calcolatrice = new CalcolatriceCLI();

        assertNotNull(calcolatrice);
    }

    /*
     * Scenario: test_calcola_addizione
     *
     * Given due numeri int e operazione = "addizione"
     * When viene chiamata eseguiCalcolo
     * Then viene stampato il risultato della somma
     */
    @Test
    void test_calcola_addizione() {
        CalcolatriceCLI calcolatrice = new CalcolatriceCLI();

        calcolatrice.eseguiCalcolo("addizione", 5, 10);

        String risultato = output.toString(StandardCharsets.UTF_8);

        assertTrue(
            risultato.contains("15"),
            "L'output dovrebbe contenere il risultato 15. Output: " + risultato
        );
    }

    /*
     * Scenario: test_calcola_sottrazione
     *
     * Given due numeri int e operazione = "sottrazione"
     * When viene chiamata eseguiCalcolo
     * Then viene stampato il risultato della sottrazione
     */
    @Test
    void test_calcola_sottrazione() {
        CalcolatriceCLI calcolatrice = new CalcolatriceCLI();

        calcolatrice.eseguiCalcolo("sottrazione", 5, 10);

        String risultato = output.toString(StandardCharsets.UTF_8);

        assertTrue(
            risultato.contains("5"),
            "L'output dovrebbe contenere il risultato 5. Output: " + risultato
        );
    }

    /*
     * Scenario: test_calcola_moltiplicazione
     *
     * Given due numeri int e operazione = "moltiplicazione"
     * When viene chiamata eseguiCalcolo
     * Then viene stampato il risultato della moltiplicazione
     */
    @Test
    void test_calcola_moltiplicazione() {
        CalcolatriceCLI calcolatrice = new CalcolatriceCLI();

        calcolatrice.eseguiCalcolo("moltiplicazione", 5, 10);

        String risultato = output.toString(StandardCharsets.UTF_8);

        assertTrue(
            risultato.contains("50"),
            "L'output dovrebbe contenere il risultato 50. Output: " + risultato
        );
    }

    /*
     * Scenario: test_calcola_divisione
     *
     * Given due numeri int con var2 != 0 e operazione = "divisione"
     * When viene chiamata eseguiCalcolo
     * Then viene stampato il risultato come double
     */
    @Test
    void test_calcola_divisione() {
        CalcolatriceCLI calcolatrice = new CalcolatriceCLI();

        calcolatrice.eseguiCalcolo("divisione", 10, 4);

        String risultato = output.toString(StandardCharsets.UTF_8);

        assertTrue(
            risultato.contains("2.5"),
            "L'output dovrebbe contenere il risultato 2.5. Output: " + risultato
        );
    }

    /*
     * Scenario: test_calcola_divisione_col_0
     *
     * Given due numeri int e operazione = "divisione"
     * When var2 = 0
     * Then viene stampato il messaggio di errore e l'esecuzione termina
     */
    @Test
    void test_calcola_divisione_col_0() {
        CalcolatriceCLI calcolatrice = new CalcolatriceCLI();

        assertDoesNotThrow(() ->
            calcolatrice.eseguiCalcolo("divisione", 10, 0)
        );

        String risultato = output.toString(StandardCharsets.UTF_8);

        assertTrue(
            risultato.contains("Errore: Impossibile dividere per zero!"),
            "L'output dovrebbe contenere il messaggio di errore. Output: " + risultato
        );
    }

    /*
     * Scenario: test_operazione_non_riconosciuta
     *
     * Given due numeri int e un'operazione non valida
     * When viene chiamata eseguiCalcolo
     * Then viene stampato il messaggio di errore
     */
    @Test
    void test_operazione_non_riconosciuta() {
        CalcolatriceCLI calcolatrice = new CalcolatriceCLI();

        calcolatrice.eseguiCalcolo("potenza", 10, 5);

        String risultato = output.toString(StandardCharsets.UTF_8);

        assertTrue(
            risultato.contains(
                "Operazione non riconosciuta. Scegli tra: " +
                "addizione, sottrazione, moltiplicazione, divisione."
            ),
            "L'output dovrebbe contenere il messaggio per operazione non riconosciuta. "
                + "Output: " + risultato
        );
    }

    /*
     * Scenario: test_main_cli_input_utente
     *
     * Given un flusso di input contenente:
     *   - nome dell'operazione
     *   - var1
     *   - var2
     *
     * When viene chiamata main
     * Then la calcolatrice legge gli input, applica trim e
     * lowerCase all'operazione ed esegue il calcolo.
     */
    @Test
    void test_main_cli_input_utente() {
        String input = "  AdDiZiOnE  \n10\n5\n";

        System.setIn(new ByteArrayInputStream(
            input.getBytes(StandardCharsets.UTF_8)
        ));

        assertDoesNotThrow(() -> CalcolatriceCLI.main(new String[0]));

        String risultato = output.toString(StandardCharsets.UTF_8);

        /*
         * L'uso di "AdDiZiOnE" con spazi iniziali/finali verifica
         * indirettamente trim() e toLowerCase().
         *
         * Se main non eseguisse queste trasformazioni,
         * l'operazione non verrebbe riconosciuta.
         */
        assertTrue(
            risultato.contains("15"),
            "main dovrebbe eseguire l'addizione e stampare 15. Output: "
                + risultato
        );

        /*
         * Verifica che main abbia effettivamente prodotto un output,
         * quindi abbia gestito il flusso CLI.
         */
        assertTrue(
            !risultato.isBlank(),
            "main dovrebbe produrre un output."
        );
    }
}
