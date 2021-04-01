import math
import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument("-c1", "--type", choices=["diff", "annuity"],
                    help="You need to choose only one option.")
parser.add_argument("-c2", "--principal", type=int,
                    help="Please input number.")
parser.add_argument("-c3", "--periods", type=int,
                    help="Please input number.")
parser.add_argument("-c4", "--interest", type=float,
                    help="Please input number.")
parser.add_argument("-c5", "--payment", type=int,
                    help="Please input number.")

args = parser.parse_args()

payment_type = args.type
loan_principal = args.principal
loan_interest = args.interest
loan_payment = args.payment
loan_period = args.periods


def diff_pay(principal, periods, interest):
    monthly_payment = []
    for i in range(periods):
        month = i + 1
        result = ((principal / periods) + (
                interest * (principal - ((principal * (month - 1)) / periods))))
        rounded_result = math.ceil(result)
        monthly_payment.append(rounded_result)
        print('Month ' + str(month) + ': payment is ' + str(rounded_result))
    return monthly_payment


def annuity_pay(principal, periods, interest):
    result = principal * (interest * math.pow(1 + interest, periods)) / (
            (math.pow(1 + interest, periods)) - 1)
    rounded_result = math.ceil(result)
    print("Your monthly payment = " + str(rounded_result) + "!")
    return rounded_result


def calc_principal(payment, periods, interest):
    result = payment / ((interest * (math.pow(1 + interest, periods))) / (
            (math.pow(1 + interest, periods)) - 1))
    rounded_result = math.floor(result)
    print('Your loan principal = ' + str(rounded_result) + "!")
    return rounded_result


def n_months_repay_loan(principal, payment, interest):
    result = math.ceil(
        math.log(payment / (payment - interest * principal), 1 + interest))
    years = math.floor(result / 12)
    months = result % 12
    if years == 0 and months == 1:
        print("It will take " + str(months) + "month to repay this loan!")
    elif years == 0 and months > 1:
        print("It will take " + str(months) + 'months to repay this loan!')
    elif years == 1 and months == 1:
        print("It will take " + str(years) + " year " + str(months) + " month to repay this loan!")
    elif years == 1 and months > 1:
        print("It will take " + str(years) + " year " + str(months) + " months to repay this loan!")
    elif years > 1 and months == 1:
        print("It will take " + str(years) + " years " + str(months) + " month to repay this loan!")
    else:
        print("It will take " + str(years) + " years " + str(months) + " months to repay this loan!")
    return result


def over_pay_annuity(period, payment, principal):
    result = (period * payment - principal)
    rounded_result = math.ceil(result)
    print("Overpayment = " + str(rounded_result))


def over_pay_diff(period, payment, principal):
    result = 0
    for i in range(period):
        result += payment[i]
    rounded_result = math.ceil(result)
    final_overpayment = rounded_result - principal
    print("Overpayment = " + str(final_overpayment))


def error_message():
    print('Incorrect parameters')


def positive(value):
    if value < 0:
        print('Incorrect parameters')
        sys.exit()


# check if none of the value negative
if args.principal is not None:
    positive(args.principal)

if args.interest is not None:
    positive(args.interest)

if args.payment is not None:
    positive(args.payment)

if args.periods is not None:
    positive(args.periods)

# calculate float interest
if args.interest is not None:
    loan_interest /= 1200

# error messages
if args.type is None:
    error_message()

if args.type == "diff" and args.payment is not None:
    error_message()

if args.type == "annuity" and args.interest is None:
    error_message()

#  calculating differentiated payments (--type=diff --principal=500000 --periods=8 --interest=7.8)
if payment_type == 'diff':
    diff_payment = diff_pay(loan_principal, loan_period, loan_interest)
    over_pay_diff(loan_period, diff_payment, loan_principal)
# calculate the annuity payment (--type=annuity --principal=1000000 --periods=60 --interest=10)
elif payment_type == 'annuity' and args.payment is None:
    annuity_payment = annuity_pay(loan_principal, loan_period, loan_interest)
    over_pay_annuity(loan_period, annuity_payment, loan_principal)
else:
    # calculate the principal (--type=annuity --payment=8722 --periods=120 --interest=5.6)
    if payment_type == 'annuity' and args.payment is not None and args.periods is not None and args.interest is not None:
        principal_payment = calc_principal(loan_payment, loan_period, loan_interest)
        over_pay_annuity(loan_period, loan_payment, principal_payment)
    # calculate how long it will take to repay a loan (--type=annuity --principal=500000 --payment=23000 --interest=7.8)
    elif payment_type == 'annuity' and args.principal is not None and args.payment is not None and args.interest is not None:
        number_of_months = n_months_repay_loan(loan_principal, loan_payment, loan_interest)
        over_pay_annuity(number_of_months, loan_payment, loan_principal)
