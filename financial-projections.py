from os import system

duration = 25

class Record(object):
  def __init__(self, title, values):
    self.title = title
    self.values = values

_time = 0
_balance = 0
_income = 0
_rent = 0

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

  _time = 0
  _balance = 0
  _income = 0
  _rent = 0
  _values = []

def report():
  _values.append(_balance)

def take_job(income):
  global _income
  _income = income

def wait(period):
  global _balance
  global _income
  global _time

  for i in xrange(period):
    _time += 1
    _balance += _income
    _balance -= _rent
    report()

def work_solidly():
  take_job(7000)
  wait(duration * 12)

def main():
  run('work solidly', work_solidly)

  with open('data', 'w') as data_file:
    for t, values in enumerate(zip(*[r.values for r in _records])):
      data_file.write('\t'.join([str(t / 12.0)] + [str(v) for v in values]) + '\n')

  with open('plot.gp', 'w') as script:
    script.write('plot \\\n')
    for i, record in enumerate(_records):
      script.write('  \'data\' using 1:' + str(i + 2) + ' title \'' + record.title + '\' with lines\n')

  system('gnuplot -persist plot.gp')

if __name__ == '__main__':
  main()

