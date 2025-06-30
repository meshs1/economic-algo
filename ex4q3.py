from csv import DictReader
from io import StringIO
from math import sqrt

# https://he.wikipedia.org/wiki/%D7%94%D7%91%D7%97%D7%99%D7%A8%D7%95%D7%AA_%D7%9C%D7%9B%D7%A0%D7%A1%D7%AA_%D7%94%D7%A2%D7%A9%D7%A8%D7%99%D7%9D
# https://main.knesset.gov.il/about/history/pages/knessethistory.aspx?kns=20
# https://en.wikipedia.org/wiki/Huntington%E2%80%93Hill_method

data = """name,votes,dhondt
likud,985408,30
zionistunion,786313,24
jointlist,446583,13
yeshatid,371602,11
kulanu,315360,10
thejewishhome,283910,8
shas,241613,7
yisraelbeiteinu,214906,6
unitedtorahjudaism,210143,6
meretz,165529,5
"""

TOTAL_SEATS = 120


def main():
    votes = {}
    seats = {}

    with StringIO(data) as f:
        reader = DictReader(f)

        for line in reader:
            votes[line["name"]] = int(line["votes"])
            seats[line["name"]] = 0

    for i in range(TOTAL_SEATS):
        max_priority = 0
        winner = None
        for party, count in votes.items():
            current_seats = seats[party]
            denominator = max(sqrt(current_seats * (current_seats + 1)), 1)
            priority = count / denominator

            if priority > max_priority:
                max_priority = priority
                winner = party

        seats[winner] += 1

    for party, count in seats.items():
        print(f"{party}: {count} seats")


if __name__ == "__main__":
    main()
