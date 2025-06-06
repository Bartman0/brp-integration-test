import argparse

from personen import Personen
from verblijfplaatshistorie import Verblijfplaatshistorie
from bewoning import Bewoning
from volgindicatie import Volgindicaties
from wijzigingen import Wijzigingen
from nieuwe_ingezetenen import NieuweIngezetenen


def main():
    parser = argparse.ArgumentParser(
        prog="brp-integration-test",
        description="Test availability, health and performance of BRP API's",
    )
    parser.add_argument("--personen", action="store_true")  # on/off flag
    parser.add_argument("--verblijfplaatshistorie", action="store_true")  # on/off flag
    parser.add_argument("--bewoning", action="store_true")  # on/off flag
    parser.add_argument("--volgindicaties", action="store_true")  # on/off flag
    parser.add_argument("--wijzigingen", action="store_true")  # on/off flag
    parser.add_argument("--nieuwe-ingezetenen", action="store_true")  # on/off flag
    parser.add_argument("-P", "--performance", action="store_true")  # on/off flag
    parser.add_argument("-d", "--duration", type=int, default=5)  # on/off flag
    parser.add_argument("-u", "--user_count", type=int, default=10)  # on/off flag
    parser.add_argument("-s", "--spawn_rate", type=int, default=20)  # on/off flag

    args = parser.parse_args()

    if args.personen:
        personen = Personen(
            args.performance, args.duration, args.user_count, args.spawn_rate
        )
        personen.run()
    if args.verblijfplaatshistorie:
        verblijfplaatshistorie = Verblijfplaatshistorie(args.performance, args.duration)
        verblijfplaatshistorie.run()
    if args.bewoning:
        bewoning = Bewoning(args.performance, args.duration)
        bewoning.run()
    if args.volgindicaties:
        volgindicaties = Volgindicaties(args.performance, args.duration)
        volgindicaties.run()
    if args.wijzigingen:
        wijzigingen = Wijzigingen(args.performance, args.duration)
        wijzigingen.run()
    if args.nieuwe_ingezetenen:
        nieuwe_ingezetenen = NieuweIngezetenen(args.performance, args.duration)
        nieuwe_ingezetenen.run()


if __name__ == "__main__":
    main()
