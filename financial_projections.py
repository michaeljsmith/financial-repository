# TODO: Increase in rent
# TODO: Multiple investment properties
# TODO: Initial investment property
# TODO: Renovations
# TODO: Index tax brackets
# TODO: Land value increase v house value

from os import system

INITIAL_BALANCE = 150000
DURATION = 25
INFLATION = 0.03
SALARY0 = 8000
SALARY1 = 7000
SALARY_INCREASE = INFLATION
RATE = 0.07
ALTERNATIVE_YIELD = 0.06 # TODO: Split into dividends + capital growth
CAPITAL_GROWTH = 0.06 # Growth - costs (maintenance, insurance)
MAINTENANCE_FACTOR = 0.02 # Growth - costs (maintenance, insurance)
RENTAL_YIELD = 0.042 # Calculated only from single estimate
INITIAL_MONTHLY_EXPENSES = 3000 # All costs not house-related
EXPENSE_INCREASE = INFLATION
INITIAL_EXPENSE_PER_CHILD = 1000
CHILD_CARE_DURATION = 20
SCHOOL_FEE_START_AGE = 12
SCHOOL_FEE_END_AGE = 18
SCHOOL_FEE_INCREASE = INFLATION
PRIVATE_SCHOOL_FEES = 30000

MATERNITY_PERIOD = 0.5
MATERNITY_SALARY_FACTOR = 0
HOME_CARE_PERIOD = 10
HOME_CARE_SALARY_FACTOR = 0.5

FIRST_CHILD_DELAY = 5
SUBSEQUENT_CHILD_DELAY = 2

stamp_duty_brackets = [
  (0, 0.0125),
  (14000, 0.015),
  (30000, 0.0175),
  (80000, 0.035),
  (300000, 0.045),
  (1000000, 0.055)]

def stamp_duty(price):
  duty = 0
  for min, pct in reversed(stamp_duty_brackets):
    if price > min:
      amount_at_pct = price - min
      price = min
      duty += amount_at_pct * pct
  return duty

income_tax_brackets = [
  (0, 0.0),
  (18200, 0.19),
  (37000, 0.325),
  (80000, 0.37),
  (180000, 0.45)]

def income_tax(income):
  tax = 0
  for min, pct in reversed(income_tax_brackets):
    if income > min:
      amount_at_pct = income - min
      income = min
      tax += amount_at_pct * pct
  return tax

class Record(object):
  def __init__(self, title, values):
    self.title = title
    self.values = values

class Child(object):
  def __init__(self, birth):
    self.birth = birth

  def age(self):
    return time() - self.birth

_time = 0
_balance = 0
_salary = [0, 0]
_rent = 0
_principal = 0
_property = 0
_investment_property = 0
_investment_principal = 0
_desired_children = 0
_cgt_owing = 0
_children = []

_values = []

_records = []

def run(title, program):
  clear()

  take_job(0, SALARY0)
  take_job(1, SALARY1)

  program()
  wait(DURATION * 12 - _time)

  _records.append(Record(title, _values))

def clear():
  global _time
  global _balance
  global _values
  global _rent
  global _principal
  global _property
  global _investment_property
  global _investment_principal
  global _children
  global _school_fees
  global _salary
  global _desired_children
  global _cgt_owing

  _time = 0
  _balance = INITIAL_BALANCE
  _salary = [0, 0]
  _rent = 0
  _principal = 0
  _property = 0
  _investment_property = 0
  _investment_principal = 0
  _school_fees = 0
  _desired_children = 0
  _children = []
  _cgt_owing = 0
  _values = []

def report():
  _values.append(_balance + _property + _investment_property - _principal - _investment_principal - _cgt_owing)

def time():
  return _time

def pay(amount):
  global _balance
  _balance -= amount

def receive(amount):
  global _balance
  _balance += amount

def gain_property(amount):
  global _property
  _property += amount

def gain_investment_property(amount):
  global _investment_property
  _investment_property += amount

def lose_property(amount):
  global _property
  _property -= amount

def take_job(person, income):
  global _salary
  _salary[person] = income

def rent_home(price):
  global _rent
  _rent = price * RENTAL_YIELD / 12

def have_child():
  _children.append(Child(time()))

def set_desired_children(count):
  global _desired_children
  _desired_children = count

def set_school_fees(amount):
  global _school_fees
  _school_fees = amount

def wait(period):
  global _balance
  global _time
  global _principal
  global _property
  global _investment_property
  global _investment_principal
  global _salary
  global _cgt_owing

  for i in xrange(period):
    _time += 1

    if len(_children) < _desired_children:
      if len(_children):
        time_since_last_child = _children[-1].age()
        if time_since_last_child >= SUBSEQUENT_CHILD_DELAY * 12:
          have_child()
      else:
        if _time >= FIRST_CHILD_DELAY * 12:
          have_child()

    alternative_yield = _balance * ALTERNATIVE_YIELD / 12

    income_factor = [1.0, 1.0]
    if len(_children):
      time_since_last_child = _children[-1].age()
      factor = 1.0
      if time_since_last_child <= MATERNITY_PERIOD * 12:
        factor = MATERNITY_SALARY_FACTOR
      elif time_since_last_child <= HOME_CARE_PERIOD * 12:
        factor = HOME_CARE_SALARY_FACTOR

      income_factor[1] = factor

    rental_income = _investment_property * RENTAL_YIELD / 12
    investment_income = alternative_yield + rental_income
    investment_interest_due = _investment_principal * RATE / 12

    income = [s * f + investment_income / len(_salary) for s, f in zip(_salary, income_factor)]
    total_income = sum(income)
    deductions = max(0, investment_interest_due - rental_income)
    _salary = [s * (1 + (SALARY_INCREASE / 12)) for s in _salary]
    tax_payable = sum(income_tax(max(0, i - deductions) * 12) / 12 for i in income)

    total_expense_inflation = (1 + (EXPENSE_INCREASE / 12)) ** _time
    expense_per_child = INITIAL_EXPENSE_PER_CHILD * total_expense_inflation
    num_dependants = len([c for c in _children if c.age() < CHILD_CARE_DURATION * 12])
    dependant_expenses = num_dependants * expense_per_child
    expenses = INITIAL_MONTHLY_EXPENSES * total_expense_inflation

    children_at_school = len([c for c in _children if SCHOOL_FEE_START_AGE * 12 <= c.age() < SCHOOL_FEE_END_AGE * 12])
    total_school_fee_inflation = (1 + (SCHOOL_FEE_INCREASE / 12)) ** _time
    total_school_fees = children_at_school * _school_fees / 12 * total_school_fee_inflation

    disposable_income = total_income - tax_payable - expenses - _rent - dependant_expenses - total_school_fees
    _balance += disposable_income

    # TODO: reorganize all loans into a single list.
    # TODO: make minimum repayments for all loans.
    repayment = _balance
    capped_repayment = min(_principal, repayment)
    _balance -= capped_repayment
    interest_due = _principal * RATE / 12
    _principal -= capped_repayment - interest_due

    repayment = _balance
    capped_repayment = min(_investment_principal, repayment)
    _balance -= capped_repayment
    interest_due = _investment_principal * RATE / 12
    _investment_principal -= capped_repayment - interest_due

    _property += _property * (CAPITAL_GROWTH - MAINTENANCE_FACTOR) / 12
    investment_property_increase = _investment_property * (CAPITAL_GROWTH - MAINTENANCE_FACTOR) / 12
    _cgt_owing += income_tax_brackets[-1][1] * investment_property_increase # Assume cgt will eventually be levied at highest bracket.
    _investment_property += investment_property_increase

    report()

def select_private_school():
  set_school_fees(PRIVATE_SCHOOL_FEES)

def take_loan(amount):
  global _principal
  global _balance

  _principal += amount
  _balance += amount

def buy_home(price):
  total = price + stamp_duty(price)
  loan_amount = max(0, total - _balance)
  take_loan(loan_amount)
  pay(total)
  gain_property(price)

def buy_investment_property(price):
  global _investment_principal
  global _balance

  total = price + stamp_duty(price)
  loan_amount = max(0, total - _balance)
  _investment_principal += loan_amount
  _balance += loan_amount
  pay(total)
  gain_investment_property(price)

def sell_home():
  value = _property
  receive(value)
  lose_property(value)

def single_rented_house(value):
  def program():
    rent_home(value)
  return program

def single_house(value):
  def program():
    buy_home(value)
  return program

def foo():
  #set_desired_children(2)
  select_private_school()
  rent_home(1750000)
  buy_investment_property(750000)

def main():
  #run('rent house $750000', single_rented_house(750000))
  run('single house $750000', single_house(1750000))
  #run('single house $650000', single_house(650000))
  run('foo', foo)

  with open('data', 'w') as data_file:
    for t, values in enumerate(zip(*[r.values for r in _records])):
      data_file.write('\t'.join([str(t / 12.0)] + [str(v) for v in values]) + '\n')

  with open('plot.gp', 'w') as script:
    script.write('plot \\\n')
    script.write(', \\\n'.join(
      '  \'data\' using 1:' + str(i + 2) + ' title \'' + record.title + '\' with lines'
        for i, record in enumerate(_records)))

  system('gnuplot -persist plot.gp')

if __name__ == '__main__':
  main()

