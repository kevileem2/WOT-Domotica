# WOT-Domotica

SmartHome-applicatie waarmee een geauthenticeerde bezoeker (client) devices kan sturen en/of uitlezen. De client draait op GitHub pages en maak gebruikt van Google Firebase . Op de Raspberry Pi draait een programma die kan anticiperen op wijzigingen binnen Google Firebase Firestore.

## Functionaliteiten

- stuur alle lichtpunten
- stuur alle stopcontacten
- stuur de voor- en achterdeur
- lees de temperatuur en humidity uit
- alert knop (bijvoorbeeld inbraak): laat alle lichtpunten flikkeren, open alle deuren, speel een alarmgeluid af.

## Structuur repository

- README.md (geef omschrijving van het project, vermeld jouw prof. information)
- index.html (client)
  - assets (folder)
    - js (folder)
      - app.js
    - css (folder)
      - app.css
- pi (folder)
  - app_domotica.py
