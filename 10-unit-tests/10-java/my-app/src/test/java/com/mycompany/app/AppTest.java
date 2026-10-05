package com.mycompany.app;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import org.junit.jupiter.api.Test;

public class AppTest {

    @Test
    public void testMain() {
        // Esegue il metodo main per coprire la riga System.out.println
        App.main(new String[]{});
    }

    @Test
    public void testAppInstance() {
        // Istanzia la classe per coprire il costruttore vuoto di default
        App app = new App();
        assertNotNull(app);
    }
}
