# Szabályok

A Hackathon során a csapatok ([Cégek](#cegek)) a saját (virtuális) szállító drónjaikat irányítják egy közös pályán.

A cél a legtöbb pontszám elérése a Hackathon végéig, [Csomagok](#csomagok) leszállításával.

A virtuális világot egy szerver szimulálja, amit a megadott [API](https://hackadrone.gazd.info/openapi/)-n keresztül lehet elérni információk lekérdezéséhez és utasítások kiadásához.

A szimulált világ egy téglalap alakú terület a 47°39'N 16°33'E és 47°42'N 16°38'E koordináták között.
A Föld görbületét elhanyagoljuk.

## Entitások

A virtuális világban az alábbi elemek lehetnek jelen, a felsorolt jellemzőikkel.

### Cégek

- Cég ID
- Cégnév
- Bázis helye (ahonnan indulnak a drónok)
- Titkos kulcs (az utasítások adásához)
- Pontszám
- [Drónok](#dronok) flottája

### Drónok

- Drón ID
- Pozíció (szélességi és hosszúsági fok)
- Úticél
- Max. sebesség
- Szállítás alatt lévő [Csomagok](#csomagok)
- Teherbírás
- Akkumulátor
    - Maximális kapacitás
    - Töltöttségi szint
    - Repülési fogyasztási ráta (állóhelyzetben nem merül)
      - Drón + szállítmány össztömegével arányos
    - Kapacitáscsökkenés lemerülés esetén
- Állapot
    - Tétlen
    - Repül
    - Töltődik
    - Lemerült
    - Mentésre vár

### Csomagok

- Csomag ID
- Feladás helye
- Kiszállítás helye
- Szállítási határidő
- Jutalom a kiszállításért (határidőre)
- Tömeg

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
    - Az akkumulátor a drón és a szállított csomagok össztömegével arányosan merül a repülés során
    - Ha útközben lemerül a drón akksija, akkor ott megáll, és a karbantartók érkezéséig működésképtelen
- Drón mentése
    - Az utasítás kiadásától számítva 1 órát kell várni, hogy javításra kerüljön a drón
    - Ezután az akkumulátor kapacitása 5%-kal kisebb lesz, de teljesen feltöltésre kerül
- Megadott csomag felvétele
    - A drónnak a csomag pozícióján kell várakoznia
    - A csomagnak gazdátlannak kell lennie
    - A drónnak kell, hogy legyen elegendő szabad teherkapacitása
- Megadott csomag lerakása
    - A csomagnak a drón tulajdonában kell lennie
    - A csomag úticéljától kellő távolságon belül kell lennie
    - Ha határidőn belül lett leszállítva, akkor a cég megkapja a jutalmat
    - Ha a határidő lejárt, akkor a jutalom 120%-a kerül levonásra büntetésként
- Töltés indítása megadott állomáson
    - A drónnak a töltőállomás felett kell lennie
    - Lehet csomag a drónnál
    - Tetszőleges egyéb művelet megadása vagy 100%-os töltöttség elérése megszakítja a töltést
