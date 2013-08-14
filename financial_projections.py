# TODO: Stop working after kids
# TODO: Negative gearing
# TODO: Investment properties
# TODO: Initial investment property
# TODO: Renovations
# TODO: Medicare levy
# TODO: Index tax brackets

from os import system

INITIAL_BALANCE = 150000
DURATION = 25
INFLATION = 0.03
SALARY0 = 8000
SALARY1 = 7000
SALARY_INCREASE = INFLATION
RATE = 0.07
ALTERNATIVE_YIELD = 0.06 # TODO: Split into dividends + capital growth
CAPITAL_GROWTH = 0.04 # Growth - costs (maintenance, insurance)
RENTAL_YIELD = 0.042 # Calculated only from single estimate
INITIAL_MONTHLY_EXPENSES = 3000 # All costs not house-related
EXPENSE_INCREASE = INFLATION
INITIAL_EXPENSE_PER_CHILD = 1000
CHILD_CARE_DURATION = 20
SCHOOL_FEE_START_AGE = 12
SCHOOL_FEE_END_AGE = 18
SCHOOL_FEE_INCREASE = INFLATION
PRIVATE_SCHOOL_FEES = 30000

FIRST_CHILD_DELAY = 5
SUBSEQUENT_CHILD_DELAY = 2

stamp_duty_brackets = [
  (0, 0, 0.0125),
  (14000, 175, 0.015),
  (30000, 415, 0.0175),
  (80000, 1290, 0.035),
  (300000, 8990, 0.045),
  (1000000, 40490, 0.055)]

def stamp_duty(price):
  for min, base, pct in reversed(stamp_duty_brackets):
    if price > min:
      return base + (price - min) * pct

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
_desired_children = 0
_children = []

_values = []

_records = []

def run(title, program):
  clear()
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
  global _children
  global _school_fees
  global _salary
  global _desired_children

  _time = 0
  _balance = INITIAL_BALANCE
  _salary = [0, 0]
  _rent = 0
  _principal = 0
  _property = 0
  _school_fees = 0
  _desired_children = 0
  _children = []
  _values = []

def report():
  _values.append(_balance + _property - _principal)

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
  global _salary

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

    income = [s + alternative_yield / len(_salary) for s in _salary]
    total_income = sum(income)
    _salary = [s * (1 + (SALARY_INCREASE / 12)) for s in _salary]
    tax_payable = sum(income_tax(i * 12) / 12 for i in income)

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

    repayment = _balance
    capped_repayment = min(_principal, repayment)
    _balance -= capped_repayment
    interest_due = _principal * RATE / 12
    _principal -= capped_repayment - interest_due

    _property += _property * CAPITAL_GROWTH / 12

    report()

def select_private_school():
  set_school_fees(PRIVATE_SCHOOL_FEES)

def take_loan(amount):
  global _principal
  global _balance

  _principal += amount
  _balance += amount

def single_rented_house(value):
  def program():
    take_job(0, SALARY1)
    take_job(1, SALARY1)
    rent_home(value)
  return program

def buy_home(price):
  total = price + stamp_duty(price)
  loan_amount = max(0, total - _balance)
  take_loan(loan_amount)
  pay(total)
  gain_property(price)

def sell_home():
  value = _property
  receive(value)
  lose_property(value)

def single_house(value):
  def program():
    take_job(0, SALARY0)
    take_job(1, SALARY1)
    buy_home(value)
  return program

def foo():
  set_desired_children(2)
  select_private_school()
  take_job(0, SALARY0)
  take_job(1, SALARY1)
  buy_home(750000)
  wait(5 * 12)
  sell_home()
  rent_home(750000)

def main():
  run('rent house $750000', single_rented_house(750000))
  run('single house $750000', single_house(750000))
  run('single house $650000', single_house(650000))
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

