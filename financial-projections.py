from os import system

DURATION = 25
SALARY = 6000
RATE = 0.07

stamp_duty_brackets = [
  (0, 0, 0.0125),
  (14000, 175, 1.5),
  (30000, 415, 1.75),
  (80000, 1290, 3.5),
  (300000, 8990, 4.5),
  (1000000, 40490, 5.5)]

def stamp_duty(price):
  for min, base, pct in reversed(stamp_duty_brackets):
    if price > min:
      return base + (price - min) * pct

class Record(object):
  def __init__(self, title, values):
    self.title = title
    self.values = values

_time = 0
_balance = 0
_income = 0
_rent = 0
_principal = 0
_repayment = 0

_values = []

_records = []

def run(title, program):
  clear()
  program()

  _records.append(Record(title, _values))

def clear():
  global _time
  global _balance
  global _income
  global _values
  global _rent
  global _principal
  global _repayment

  _time = 0
  _balance = 0
  _income = 0
  _rent = 0
  _principal = 0
  _repayment = 0
  _values = []

def report():
  _values.append(_balance - _principal)

def take_job(income):
  global _income
  _income = income

def rent_home(rent):
  global _rent
  _rent = rent

def wait(period):
  global _balance
  global _time
  global _principal

  for i in xrange(period):
    _time += 1
    _balance += _income
    _balance -= _rent

    capped_repayment = min(_balance, _repayment)
    _balance -= capped_repayment
    interest_due = _principal * RATE / 12
    _principal -= capped_repayment - interest_due

    report()

def take_loan(amount):
  global _principal
  global _balance

  _principal += amount
  _balance += amount

def set_repayments(repayment):
  global _repayment
  _repayment = repayment

def work_solidly():
  take_job(SALARY)
  rent_home(2000)
  wait(DURATION * 12)

def buy_home(price):
  global _balance
  _balance -= stamp_duty(price)
  take_loan(price)
  set_repayments(SALARY)

def single_house():
  take_job(SALARY)
  buy_home(700000)
  wait(DURATION * 12)

def main():
  run('work solidly', work_solidly)
  run('single house', single_house)

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

