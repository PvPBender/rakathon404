# 💉 Zpracování dat výkonů VYK

Tento skript slouží ke zpracování datových souborů zdravotnických výkonů (VYK) pro roky 2023 a 2024. Zajišťuje načtení, čištění, sjednocení a anotaci dat pomocí číselníků názvů výkonů.

## 📂 Struktura souborů

Soubory jsou očekávány ve složce:
```
rakathon404/data/DATA/VYK_{rok}/
```
Každý rok obsahuje tyto CSV soubory:
- `vyk_{rok}_vykony.csv` – výkony poskytnuté pacientům.
- `vyk_{rok}_material.csv` – použité zdravotnické materiály.
- `vyk_{rok}_vykpac.csv` – relace výkony–pacient.

## ⚙️ Co skript dělá

1. **Načtení dat** z CSV souborů pro daný rok.
2. **Čištění identifikátorů** (`CISPAC`, `CDOKL`, `KOD`) – odstranění mezer.
3. **Převod sloupců `DATUM` na datetime** typ, s varováním při neúspěchu.
4. **Automatický převod typů** sloupců typu `object` na čísla, pokud je to možné.
5. **Spojení tabulek**:
   - `vykony + vykpac` → `df_vykony_full`
   - `material + vykpac` → `df_material_full`
6. **Odstranění prázdných sloupců** (s `NaN` ve všech řádcích).
7. **Spojení dat za oba roky** (2023 i 2024).
8. **Anotace kódů výkonů** názvy podle číselníku (`vykony_kody_nazvy.csv`) pomocí funkce `annotate_vykony_with_names`.

## 🧩 Výstupy

- Spojený DataFrame výkonů: `df_vykony_all`
- Spojený DataFrame materiálů: `df_material_all`
- Anotovaný DataFrame výkonů: `df_vykony_annotated`
- Výstupní CSV soubor s anotacemi: `vykony_annotated.csv`


