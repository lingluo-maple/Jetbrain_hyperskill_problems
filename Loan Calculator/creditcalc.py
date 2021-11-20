import math
import argparse
import sys


# write your code here

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", choices=["annuity", "diff"], required=True)
    parser.add_argument("--payment")
    parser.add_argument("--principal")
    parser.add_argument("--periods")
    parser.add_argument("--interest", required=True)
    args = parser.parse_args()
    if len(sys.argv) < 5:
        print("Incorrect parameters")
    mode = args.type
    if args.payment:
        payment = float(args.payment)
    else:
        payment = None
    if args.principal:
        principal = float(args.principal)
    else:
        principal = None
    if args.periods:
        periods = float(args.periods)
    else:
        periods = None
    interest = float(args.interest)
    if mode == "diff" and payment:
        print("Incorrect parameters")
        return
    if principal and payment and periods:
        print("Incorrect parameters")
        return
    run(mode, payment, principal, periods, interest)


def run(mode, payment=None, principal=None, periods=None, interest=None):
    P = principal
    n = periods
    i = (interest / 100) / 12.0
    if mode == "annuity":
        if principal and payment:
            x = payment / (payment - i * P)
            n = math.log(x, 1 + i)
            if n > int(n):
                n = int(n) + 1
            else:
                n = int(n)
            months_to_years(n)
            print(f"Overpayment = {payment * n - P}")
        elif principal and not payment:
            x = i * pow(1 + i, n)
            y = pow(1 + i, n) - 1
            payment = principal * (x / y)
            if payment > int(payment):
                payment = int(payment) + 1
            else:
                payment = int(payment)
            print(f"Your monthly payment = {payment}")
        elif not principal:
            x = i * pow(1 + i, n)
            y = pow(1 + i, n) - 1
            P = payment / (x / y)
            print(f"Your loan principal = {P}")

    if mode == "diff":
        count = 0
        for m in range(1, int(n) + 1):
            x = (P * (m - 1)) / n
            d = (P / n) + i * (P - x)
            if d > int(d):
                d = int(d) + 1
            else:
                d = int(d)
            print(f"Month {m}: payment is {d}")
            count = count + d
        count = int(round(count - P, 0))
        print(f"Overpayment = {count}")


def months_to_years(months: int):
    if months >= 12:
        year = months // 12
        months = months % 12
    else:
        year = 0
    if months == 0:
        send_month = ""
    elif months == 1:
        send_month = "1 month "
    else:
        send_month = f"{months} months "

    if year == 1:
        send_year = "1 year "
    elif year > 1:
        send_year = f"{year} years "
    else:
        send_year = ""

    if year and months:
        and_ = "and "
    else:
        and_ = ""
    msg = f"It will take {send_year}{and_}{send_month}to repay this loan!"
    print(msg)


if __name__ == '__main__':
    try:
        main()
    except:
        print("Incorrect parameters")
