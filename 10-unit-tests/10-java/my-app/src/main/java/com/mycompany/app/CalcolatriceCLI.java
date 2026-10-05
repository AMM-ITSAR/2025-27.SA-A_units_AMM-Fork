package com.mycompany.app;

import java.util.Scanner;

public class CalcolatriceCLI {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("=== CALCOLATRICE CLI ===");

        System.out.print("Inserisci l'operazione (addizione, sottrazione, moltiplicazione, divisione): ");
        String operazione = scanner.nextLine().trim().toLowerCase();

        System.out.print("Inserisci il primo numero (var1): ");
        int var1 = scanner.nextInt();

        System.out.print("Inserisci il secondo numero (var2): ");
        int var2 = scanner.nextInt();

        eseguiCalcolo(operazione, var1, var2);

        scanner.close();
    }

    public static void eseguiCalcolo(String operazione, int var1, int var2) {
        if (operazione.equals("addizione")) {
            int risultato = var1 + var2;
            stampaRisultato(operazione, var1, var2, risultato);
        } else if (operazione.equals("sottrazione")) {
            int risultato = var1 - var2;
            stampaRisultato(operazione, var1, var2, risultato);
        } else if (operazione.equals("moltiplicazione")) {
            int risultato = var1 * var2;
            stampaRisultato(operazione, var1, var2, risultato);
        } else if (operazione.equals("divisione")) {
            if (var2 == 0) {
                System.out.println("Errore: Impossibile dividere per zero!");
                return;
            }
            double risultato = (double) var1 / var2;
            stampaRisultato(operazione, var1, var2, risultato);
        } else {
            System.out.println("Operazione non riconosciuta. Scegli tra: addizione, sottrazione, moltiplicazione, divisione.");
        }
    }

    private static void stampaRisultato(String operazione, int var1, int var2, Object risultato) {
        System.out.println("\n--- RISULTATO ---");
        System.out.println("Operazione : " + operazione);
        System.out.println("Var1       : " + var1);
        System.out.println("Var2       : " + var2);
        System.out.println("Risultato  : " + risultato);
    }
}