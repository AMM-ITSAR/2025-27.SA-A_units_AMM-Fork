Se utilizzo GitHub Codespace non è necessario attivare un virtualenv!

1. fork https://github.com/aaglietti-itsrizzoli/2025-27.SA-A_units
2. avviate un GitHub Codespace
3. capire il contenuto di ecommerce.py (modulo da testare)
4. ecommerce.gherkin.txt contiene un esempio di come utilizzare Gherkin per pront engineering
5. rispettando il DSL Gherkin estendetelo descrivendo i test che ritenete efficaci
6. chiedete all’LLM di turno di implementare ciò che è descritto in ecommerce.gherkin.txt senza dare visibilità di ecommerce.py
7. riportate il contenuto generato in ecommerce_test.py
8. pytest --cov
9. restart from 5. finchè code coverage < 90%
11. crea Pull Request che includa il file gherkin e il file di test
