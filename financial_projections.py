# TODO: Increase in rent
# TODO: More accurate maintenance costs
# TODO: Startup
# TODO: Renovations
# TODO: Index tax brackets
# TODO: Land value increase v house value
# TODO: Pay cgt on sale to allow compensating deductions
# TODO: Superannuation

from os import system

INITIAL_BALANCE = 150000
DURATION = 25
INFLATION = 0.03
SALARY0 = 10000
SALARY1 = 7000
SALARY_INCREASE = INFLATION
RATE = 0.07
ALTERNATIVE_YIELD = 0.06 # TODO: Split into dividends + capital growth
CAPITAL_GROWTH = 0.06
MAINTENANCE_FACTOR = 0.02 # TODO: More accurate measure
RENTAL_YIELD = 0.042 # Calculated only from single estimate
INITIAL_MONTHLY_EXPENSES = 3000 # All costs not house-related
EXPENSE_INCREASE = INFLATION
INITIAL_EXPENSE_PER_CHILD = 1000
CHILD_CARE_DURATION = 20
SCHOOL_FEE_START_AGE = 12
SCHOOL_FEE_END_AGE = 18
SCHOOL_FEE_INCREASE = INFLATION
PRIVATE_SCHOOL_FEES = 30000

DEFAULT_LOAN_DURATION = 25

INITIAL_PROPERTY_VALUE = 200000
INITIAL_PROPERTY_PRINCIPAL = 100000

MATERNITY_PERIOD = 0.5
MATERNITY_SALARY_FACTOR = 0
HOME_CARE_PERIOD = 10
HOME_CARE_SALARY_FACTOR = 0.5

FIRST_CHILD_DELAY = 3
SUBSEQUENT_CHILD_DELAY = 2

def minimum_repayments(amount, duration):
  return (RATE / 12) / (1 - (1 + RATE / 12) ** (-duration)) * amount

def bracket_total(amount, brackets):
  due = 0
  for min, pct in reversed(brackets):
    if amount > min:
      amount_at_pct = amount - min
      amount = min
      due += amount_at_pct * pct
  return due

stamp_duty_brackets = [
  (0, 0.0125),
  (14000, 0.015),
  (30000, 0.0175),
  (80000, 0.035),
  (300000, 0.045),
  (1000000, 0.055)]

def stamp_duty(price):
  return bracket_total(price, stamp_duty_brackets)

income_tax_brackets = [
  (0, 0.0),
  (18200, 0.19),
  (37000, 0.325),
  (80000, 0.37),
  (180000, 0.45)]

def income_tax(income):
  return bracket_total(income, income_tax_brackets)

class Record(object):
  def __init__(self, title, values):
    self.title = title
    self.values = values

class Child(object):
  def __init__(self, birth):
    self.birth = birth

  def age(self):
    return time() - self.birth

class Property(object):
  OCCUPY = 1
  INVESTMENT = 2

  def __init__(self, use, value, principal, minimum_repayment):
    self.use = use
    self.value = value
    self.principal = principal
    self.minimum_repayment = minimum_repayment

    self.total_increase = 0
    self.total_rent = 0
    self.total_cgt = 0
    self.total_negative_gearing = 0
    self.total_interest_paid = 0
    self.total_maintenance = 0

  def cgt(self):
    if self.use == Property.INVESTMENT:
      return 1.0
    return 0.0

  def rent(self):
    if self.use == Property.INVESTMENT:
      return 1.0
    return 0.0

  def negative_gearing(self):
    if self.use == Property.INVESTMENT:
      return 1.0
    return 0.0

_time = 0
_balance = 0
_salary = [0, 0]
_rent = 0
_properties = []
_desired_children = 0
_cgt_owing = 0
_children = []

_values = []

_records = []

def register_initial_property():
  global _properties
  _properties.append(
      Property(Property.INVESTMENT, INITIAL_PROPERTY_VALUE, INITIAL_PROPERTY_PRINCIPAL,
               minimum_repayments(INITIAL_PROPERTY_VALUE, DEFAULT_LOAN_DURATION * 12)))

def run(title, program):
  clear()

  take_job(0, SALARY0)
  take_job(1, SALARY1)

  program()
  wait(DURATION * 12 - _time)

  print

  print title
  print 'balance', round(_balance)
  print 'property value: ', round(sum(p.value for p in _properties))
  print 'principal: ', round(sum(p.principal for p in _properties))
  print 'cgt owing: ', round(_cgt_owing)

  for i, p in enumerate(_properties):
    print '  property %d:' % (i,)
    print '    value: %d: ' % (p.value,)
    print '    principal %d: ' % (p.principal,)
    print '    total capital gain: %d' % (p.total_increase,)
    print '    total rent earned: %d' % (p.total_rent,)
    print '    total cgt payable: %d' % (p.total_cgt,)
    print '    total negative gearing deduction: %d' % (p.total_negative_gearing,)
    print '    total maintenance: %d' % (p.total_maintenance,)
    print '    total interest paid: %d' % (p.total_interest_paid,)

  _records.append(Record(title, _values))

def clear():
  global _time
  global _balance
  global _values
  global _rent
  global _children
  global _school_fees
  global _properties
  global _salary
  global _desired_children
  global _cgt_owing

  _time = 0
  _balance = INITIAL_BALANCE
  _salary = [0, 0]
  _rent = 0
  _properties = []
  _school_fees = 0
  _desired_children = 0
  _children = []
  _cgt_owing = 0
  _values = []

def report():
  property = sum(p.value for p in _properties)
  principal = sum(p.principal for p in _properties)
  #_values.append(_balance + property - principal - _cgt_owing)
  _values.append(_balance)

def time():
  return _time

def pay(amount):
  global _balance
  _balance -= amount

def receive(amount):
  global _balance
  _balance += amount

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
  global _properties
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

    income_factor = [1.0, 1.0]
    if len(_children):
      time_since_last_child = _children[-1].age()
      factor = 1.0
      if time_since_last_child <= MATERNITY_PERIOD * 12:
        factor = MATERNITY_SALARY_FACTOR
      elif time_since_last_child <= HOME_CARE_PERIOD * 12:
        factor = HOME_CARE_SALARY_FACTOR

      income_factor[1] = factor

    deductions = 0
    investment_income = 0
    # Assume that we have allocated all money to offset accounts to avoid interest, and any left over is in some other investment.
    invested_money = _balance
    for p in _properties:
      rental_income = p.value * p.rent() * RENTAL_YIELD / 12
      p.total_rent += rental_income
      # TODO: Subtract maintenance/interest
      investment_income += rental_income

      offset_portion = min(invested_money, p.principal)
      invested_money -= offset_portion
      interest_due = (p.principal - offset_portion) * RATE / 12
      maintenance = p.value * MAINTENANCE_FACTOR / 12
      negative_gearing_deduction = p.negative_gearing() * max(0, interest_due + maintenance - rental_income)
      p.total_negative_gearing += negative_gearing_deduction
      deductions += negative_gearing_deduction

      repayment = min(p.principal, p.minimum_repayment)
      _balance -= repayment

      maintenance = p.value * MAINTENANCE_FACTOR / 12
      p.total_maintenance += maintenance
      _balance -= maintenance
      p.total_interest_paid += interest_due
      p.principal -= repayment - interest_due

      property_increase = p.value * CAPITAL_GROWTH / 12
      cgt = p.cgt() * income_tax_brackets[-1][1] * property_increase # Assume cgt will eventually be levied at highest bracket.
      p.total_cgt += cgt
      _cgt_owing += cgt
      p.value += property_increase
      p.total_increase += property_increase

    alternative_yield = invested_money * ALTERNATIVE_YIELD / 12

    investment_income += alternative_yield

    income = [s * f + investment_income / len(_salary) for s, f in zip(_salary, income_factor)]
    total_income = sum(income)
    _salary = [s * (1 + (SALARY_INCREASE / 12)) for s in _salary]
    tax_payable = sum(income_tax(max(0, i - deductions / len(_salary)) * 12) / 12 for i in income)

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

    report()

def select_private_school():
  set_school_fees(PRIVATE_SCHOOL_FEES)

def buy_property(use, price):
  global _properties
  global _balance

  total = price + stamp_duty(price)
  # TODO: deposit
  #loan_amount = max(0, total - _balance)
  loan_amount = total
  _balance += loan_amount
  _properties.append(Property(use, price, loan_amount, minimum_repayments(loan_amount, DEFAULT_LOAN_DURATION * 12)))
  pay(total)

  # Sort occupied properties first so that we prefer to pay off
  # non-negative-geared loans.
  _properties.sort(key=lambda p: p.use)

def sell_property(property_index):
  global _balance

  p = _properties.pop(property_index)
  # TODO: sale expenses
  proceeds = p.value - p.principal
  # CGT was paid as we went.
  _balance += proceeds

PLOT_SIZE = (640, 480)
SCREEN_WIDTH = 2000

_plot_position = (0, 0)

def plot_runs(run_defs):
  global _records
  global _plot_position
  _records = []

  for title, run_def in run_defs:
    run(title, run_def)

  with open('data', 'w') as data_file:
    for t, values in enumerate(zip(*[r.values for r in _records])):
      data_file.write('\t'.join([str(t / 12.0)] + [str(v) for v in values]) + '\n')

  with open('plot.gp', 'w') as script:
    script.write('set terminal x11 size %d,%d position %d,%d\n' % (PLOT_SIZE[0], PLOT_SIZE[1], _plot_position[0], _plot_position[1]))
    script.write('plot \\\n')
    script.write(', \\\n'.join(
      '  \'data\' using 1:' + str(i + 2) + ' title \'' + record.title + '\' with lines'
        for i, record in enumerate(_records)))

  system('gnuplot -persist plot.gp')

  _plot_position = _plot_position[0] + PLOT_SIZE[0], _plot_position[1]
  if _plot_position[0] + PLOT_SIZE[0] > SCREEN_WIDTH:
    _plot_position = 0, _plot_position[1] + PLOT_SIZE[1]

def compare_single_house_prices():
  def single_house(value):
    def program():
      set_desired_children(2)
      select_private_school()
      buy_property(Property.OCCUPY, value)
    return program

  plot_runs([
    ('single house $750000', single_house(750000)),
    ('single house $650000', single_house(650000))])

def compare_initial_property():
  def with_property():
    register_initial_property()
    set_desired_children(2)
    select_private_school()
    buy_property(Property.OCCUPY, 650000)

  def sell():
    register_initial_property()
    sell_property(0)
    set_desired_children(2)
    select_private_school()
    buy_property(Property.OCCUPY, 650000)

  def without_property():
    set_desired_children(2)
    select_private_school()
    buy_property(Property.OCCUPY, 650000)

  plot_runs([
    ('sell initial_property', sell),
    ('with initial property', with_property),
    ('without initial property', without_property)])

def main():
  compare_initial_property()
  #compare_single_house_prices()

if __name__ == '__main__':
  main()

