# Szabályok

A Hackathon során a [Csapatok](#csapatok) a saját (virtuális) szállító drónjaikat irányítják egy közös pályán.

A cél a legtöbb pontszám elérése a Hackathon végéig, [Csomagok](#csomagok) leszállításával.

A virtuális világot egy szerver szimulálja, amit a megadott [API](api.md)-n keresztül lehet elérni információk lekérdezéséhez és utasítások kiadásához.

A szimulált világ egy téglalap alakú terület a *47°39'N 16°33'E és 47°42'N 16°38'E koordináták?* között.
A Föld görbületét elhanyagoljuk.

## Entitások

A virtuális világban az alábbi elemek lehetnek jelen, a felsorolt jellemzőikkel.

### Csapatok

- Csapat ID
- Csapatnév
- Titkos kulcs (az utasítások adásához)
- Pontszám
- [Drónok](#dronok) flottája

### Drónok

- Drón ID
- Pozíció (szélességi és hosszúsági fok)
- Úticél
- Max. sebesség
- Szállítás alatt lévő [Csomagok](#csomagok)
- Csomagkapacitás
- Akkumulátor
    - Töltöttségi szint
    - Repülési fogyasztási ráta (állóhelyzetben nem merül)
- Állapot
    - Tétlen
    - Repül
    - Töltődik
    - Lemerült

### Csomagok

- Csomag ID
- Feladás helye
- Kiszállítás helye
- Jutalom a kiszállításért
- *Tömeg?*

Ha egy csomaghoz még nem indult el egy drón sem, akkor növekedhet az érte járó jutalom, vagy visszavonásra kerülhet a megrendelt szállítás.

### Töltőállomások

A drónok töltőállomásokra leszállva tudják tölteni az akkumulátorukat.

Minden állomáson végtelen számú drón töltésére van elegendő hely és elektromos teljesítmény.
A drónok száma nem befolyásolja a töltési rátát.

- Állomás ID
- Pozíció
- Töltési ráta

## Műveletek

A drónoknak egyesével lehet utasításokat küldeni egy-egy HTTP request segítségével.

Amihez nem tartozik sebesség/ráta, azok egy pillanat alatt megtörténnek, tehát például nem kerül időbe a le- és felszállás, fordulás, csomag felvétele vagy lerakása.
A gyorsítás/lassítás is azonnal megtörténik 0-ról maxra, vagy fordítva.

- Mozgás adott pozícióra
    - A pozíció beállításra kerül úticélnak, ami felé maximális sebességgel fog haladni, míg el nem éri, vagy más utasítást nem kap
    - Ha útközben lemerül, akkor *30(?) percet* kell várni, hogy egy karbantartó odamenjen és kicserélje az akksiját egy 100%-osra (addig más műveletre nem képes)
- Megadott csomag felvétele
    - A csomagnak kellő távolságon belül kell lennie
    - A drónnak kell, hogy legyen elegendő szabad kapacitása
- Megadott csomag lerakása
    - A csomagnak a drón tulajdonában kell lennie
    - A csomag úticéljától kellő távolságon belül kell lennie *(vagy nem? ott lehet hagyni az útszélen büntetlenül?)*
- Töltés indítása megadott állomáson
    - A töltőállomásnak kellő távolságon belül kell lennie
    - Lehet csomag a drónnál *(vagy nem? itt pl. érdekes lenne, hogy a töltés idejére el kell engednie, és egy másik elhappolhatja)*
    - Tetszőleges egyéb művelet megadása vagy 100%-os töltöttség elérése megszakítja a töltést
        - *Vagy muszáj legyen teljesen feltölteni?*
