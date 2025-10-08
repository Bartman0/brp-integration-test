# Integratie tests BRP API's

Deze programmatuur stelt je in staat een aantal functionele aanroepen uit te voeren en performance te testen op de
BRP API's.
Met als doel om een integratie test uit te kunnen voor deployment, en daarbij de basisfunctionaliteit en de performance
nog een laatste keer te testen voordat de deployment naar een volgend niveau gaat.

De meest logische plek om de testen aan te roepen is de acceptatieomgeving: deze omgeving zou vergelijkbaar moeten zijn
met productie wat voor de performance testen wel zo belangrijk is. Voor de functionele testen is de vulling van belang,
en deze wordt het best bediend door de omgeving die aangesloten is op de proefomgeving van de RvIG.

De testen kunnen ook los door ontwikkelaars worden uitgevoerd indien daar een ad hoc behoefte voor is. Voor
daadwerkelijke resultaten in de API's is het belangrijk om te beseffen dat deze nu zijn ingesteld op gegevens uit de
RvIG test dataset daar waar van toepassing.

Bij de performance test valt de aanvaardbare gemiddelde responstijd van de API's op te geven om zo een exceptie te
kunnen genereren indien deze responstijd wordt overschreden.

Indien de functionele aanroepen tot een fout leiden, leidt dat uiteraard ook tot een exceptie.

## Ondersteunde API's

De volgende BRP Bevragingen API's worden op dit moment ondersteund:

- Personen
- Bewoningen
- Volgindicaties (Update API, nog geen officiële standaard)
- Wijzigingen (Update API, nog geen officiële standaard)
- Nieuwe-ingezetenen (Amsterdamse uitbreiding op de Update API)
- TODO Verblijfplaatshistorie

## Configuratie

De programmatuur verwacht de volgende instellingen:

- INT_TEST_TOKEN: een JWT token dat voldoende autorisatie heeft om de bevraagde API's aan te spreken
- INT_TEST_BASE_URL: de basis URL waar de API's beschikbaar zijn gesteld, bijvoorbeeld https://acc.api.brp.amsterdam.nl

Je kunt deze configuratie opnemen in een .envrc opdat je eenvoudig het token kunt laten opvragen en gebruiken.

Voorbeeld .envrc:

```
export API_TENANT_ID=72fca1b1-***-****6804
export API_SCOPE="b00816f6-***-****db1a/.default"
export API_CLIENT_ID="b8ad6e3f-***-****aad4"
export API_CLIENT_SECRET="***"
export INT_TEST_TOKEN=$(curl -sX POST -H "Content-Type: application/x-www-form-urlencoded" -d "client_id=${API_CLIENT_ID}&scope=${API_SCOPE}&client_secret=${API_CLIENT_SECRET}&grant_type=client_credentials" "https://login.microsoftonline.com/${API_TENANT_ID}/oauth2/v2.0/token" | jq -r .access_token)
export INT_TEST_BASE_URL=https://acc.api.brp.amsterdam.nl
```

Uiteraard dien je hier je eigen configuratie en credentials in in te vullen.

## Aanroep

De API's die bevraagd moeten worden, dien je op te geven op de command-line. Daarnaast zijn er instellingen om de performance test aan te roepen.

```
usage: brp-integration-test [-h] [--personen] [--verblijfplaatshistorie] [--bewoning] [--volgindicaties] [--wijzigingen] [--nieuwe-ingezetenen] [-P]
                            [-d DURATION] [-u USER_COUNT] [-s SPAWN_RATE] [-R RESPONSE_TIME_LIMIT]

Test availability, health and performance of BRP API's

options:
  -h, --help            show this help message and exit
  --personen            execute BRP Bevragen API functional tests
  --verblijfplaatshistorie
                        execute BRP Verblijfplaatshistorie API functional tests
  --bewoning            execute BRP Bewoning API functional tests
  --volgindicaties      execute Update API volgindicaties functional tests
  --wijzigingen         execute Update API wijzigingen functional tests
  --nieuwe-ingezetenen  execute Update API nieuwe-ingezetenen functional tests
  -P, --performance     also execute performance tests
  -d, --duration DURATION
  -u, --user-count USER_COUNT
  -s, --spawn-rate SPAWN_RATE
  -R, --response-time-limit RESPONSE_TIME_LIMIT
                        average allowed response time limit in ms
```

# Docker

Voer uit:

- docker build -t integration-test/brp-api .
- docker run -it --rm -e INT_TEST_TOKEN -e INT_TEST_BASE_URL integration-test/brp-api --personen --performance -R 1500

## Uitvoeren

```
- git clone
- uv sync
- uv run python3 src/main.py --personen   # voorbeeld
```

# Benodigdheden

- Entra ID en service principal
- jq
- Python, indien je de code direct wilt aanroepen
- Docker, indien je gebruik wilt maken van een container

## Entra ID application roles

TBD

# Verbeterpunten

## Vereenvoudigen van definiëren van functionele tests en performance tests

Op dit moment is er nog sprake van code duplicatie als het gaat om de functionele testen en de performance testen:
deze worden apart gedefinieerd, maar hier zou hergebruik van de API aanroepen gebruikt moeten worden.

Voordeel van deze opzet is wel dat de scope van de functionele en performance testen los van elkaar gedefinieerd kunnen
worden.

## Makefile

Alle commando's voor het bouwen van docker images, het uitvoeren van docker containers kunnen beter in een Makefile landen.

# Voorbeeld van een aanroep

```
$ python3 src/main.py --bewoning --personen --nieuwe-ingezetenen --performance -R 1000 --duration 3 --user-count 3
```

```
test_simple (personen.TestPersonen.test_simple) ... ok
test_zoekvraag_bsn (personen.TestPersonen.test_zoekvraag_bsn) ... ok
test_zoekvraag_postcode_huisnummer (personen.TestPersonen.test_zoekvraag_postcode_huisnummer) ... ok
test_zoekvraag_postcode_huisnummer_en_bsn (personen.TestPersonen.test_zoekvraag_postcode_huisnummer_en_bsn) ... ok

----------------------------------------------------------------------
Ran 4 tests in 1.623s

OK
average response time (ms) [personen.PersonenUser]: 390
============================================================
test_bewoning_met_peildatum (bewoning.TestBewoning.test_bewoning_met_peildatum) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.483s

OK
average response time (ms) [bewoning.BewoningUser]: 364
============================================================
test_nieuwe_ingezetenen (nieuwe_ingezetenen.TestNieuweIngezetenen.test_nieuwe_ingezetenen) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.124s

OK
average response time (ms) [nieuwe_ingezetenen.NieuweIngezetenenUser]: 67
============================================================
```
