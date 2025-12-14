# Day 2: Gift Shop

## Part 1

Går gjennom alle tallene i de oppgitte intervallene og ser etter de
enkleste ugyldige ID-ene: tall som består av to helt like halvdeler.
Ved å splitte tallet i midten og sammenligne delene kan jeg raskt
avgjøre om ID-en er ugyldig. Alle slike ID-er summeres til slutt.

## Part 2

Leter etter ID-er som består av et mønster som gjentas to eller
flere ganger. For hvert tall prøver jeg ulike mønsterlengder og
sjekker om hele tallet kan bygges ved repetisjon av det mønsteret.
Finner jeg minst ett slikt repeterende mønster, regnes ID-en som
ugyldig og tas med i summen.
