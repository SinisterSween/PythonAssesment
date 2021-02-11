import re
import sys
import csv

client_list = "client_data.csv"
header1 = ("client", "available", "held", "total", "locked")
data1 = [(1, 1.5, 0.0, 1.5, "false"),
         (2, 2.0, 0.0, 2.0, "false")]

transaction_list = "transaction_data.csv"
header2 = ("type", "client", "tx", "amount")
data2 = [("deposit", 1, 1, 1.0),
         ("deposit", 2, 2, 2.0),
         ("deposit", 1, 3, 2.0),
         ("withdrawal", 1, 4, 1.5),
         ("withdrawal", 2, 5, 3.0)]
def writer(header, data, filename):
    with open (filename, "w", newline = "") as csvfile:
        transaction = csv.writer(csvfile)
        transaction.writerow(header)
        for x in data:
            transaction.writerow(x)

class Acct:
    def __init__(self, name, balance, BalanceAfterTransaction=True):
        self.name = name
        self.balance = balance
        self.startingBalance = balance
        self.BalanceAfterTransaction = BalanceAfterTransaction
        self.transactions = []
        self.locked = False
        #self.chargeback = chargeback

    def gName(self):
        return self.name

    def gBalance(self):
        return self.balance

    def sBalance(self):
        print('%s: balance is $%0.2f.' % (self.name, self.balance))
        print()

    def TransactionsList(self):
        balance = self.startingBalance
        print('   op       amount     balance')
        print('--------  ----------  ----------')
        print('                      %10.2f  (starting)' % balance)
        for transaction in self.transactions:
            [op, amount] = transaction
            if op == 'w':
                opLabel = 'withdraw'
                balance -= amount
            else:
                opLabel = 'deposit'
                balance += amount
            print('%-8s  %10.2f  %10.2f' % (opLabel, amount, balance))
        print()
    def chargeback(self):
        balance = self.startingBalance
        transactionToChargeback = input("Which Charge do you want to chargeback?")

        for transaction in self.transactions:
            [amount] = transaction
            if transactionToChargeback == '1':
                balance -= amount[0]
            print('%-8s  %10.2f  %10.2f' % ( amount, balance))
        print()


    def WD(self, amount):
        if amount > self.balance:
            print("Sorry, Insuffient Funds")
        else:
            print('%s: withdraw $%0.2f.' % (self.name, amount))
            self.balance = float('%.2f' % (self.balance - amount))
            self.transactions.append(['w', amount])
            if self.BalanceAfterTransaction:
                self.sBalance()

    def D(self, amount):
        print('%s: deposit $%0.2f.' % (self.name, amount))
        self.balance = float('%.2f' % (self.balance + amount))
        self.transactions.append(['d', amount])
        if self.BalanceAfterTransaction:
            self.sBalance()

    def TransactionProcessing(account):
        while True:
            amount = None
            op = Input().operander()
            if op == 'q':
                break
            elif op == 't':

                account.TransactionsList()
            elif op is not None:
                amount = Input().gAmount()

            if amount is None:
                pass
            elif op == 'd':
                account.D(amount)
            elif op == 'c':
                account.chargeback()
            else:
                account.WD(amount)


class Input:
    def operander(self):
        op = input('Enter d for deposit, w for withdrawal, t for transactions, c for chargeback, or q to quit: ')
        if op not in set('qdwtc-t'):
            print('Invalid operation.  Please try again.')
            op = None
        return op

    def validateAmount(self, amountStr):
        tooMuchPrecision = re.compile('.*\.\d\d\d\d.*')
        if tooMuchPrecision.match(str(amountStr)):
            raise Exception('You cannot supply fractions of a cent.')

    def gAmount(self):
        amount = None
        try:
            value = input("Please enter amount:")

            amount = float(value)
            if amount <= 0:
                raise Exception('Cannot be Negative')
            self.validateAmount(value)
        except ValueError:
            print('Invalid amount.  Please try again.')
        except Exception as e:
            print(e)
            amount = None

        return amount

#Self Testing
class Test:
    def __init__(self):
        self.numTests = 0
        self.numPass = 0

    def testBalance(self, account, expected):
        self.numTests += 1
        actual = account.gBalance()
        name = account.gName()
        if actual == expected:
            self.numPass += 1
            print('%s: OK      balance = %.2f' % (name, actual))
        else:
            print('%s: ERROR   balance = %.2f, but expected %.2f' % (name, actual, expected))

    def results(self):
        numFailed = self.numTests - self.numPass
        print()
        print('%d tests total' % self.numTests)
        if numFailed == 0:
            print('all passed')
        else:
            print('%d passed' % self.numPass)
            print('%d failed' % numFailed)
        return numFailed == 0

    def run(self):
        a1 = Acct('a1', 0, False)
        self.testBalance(a1, 0)

        a2 = Acct('a2', 100, False)
        self.testBalance(a2, 100)

        a1.D(10)
        a1.D(10)
        a1.D(10)
        a1.WD(5)
        self.testBalance(a1, 25.0)

        a2.WD(25)
        a2.WD(15)
        a2.WD(0.50)
        a2.D(15)
        self.testBalance(a2, 74.5)

        a1.WD(3.25)
        a1.D(4)
        self.testBalance(a1, 25.75)

        a2.D(1.30)
        a2.WD(11.29)
        self.testBalance(a2, 64.51)

        allPassed = self.results()
        return allPassed


class App:
    defaultBalance = 0.0

    def usage(self):
        print('usage: %s [-t|amount]' % sys.argv[0])
        print('where -t means to run test')
        print('and amount is a starting balance dollar amount')

    def parseAndValidateBalance(self, value):
        try:
            balance = float(value)
            if balance < 0:
                raise Exception('The balance cannot be negative.')
            Input().validateAmount(value)
        except ValueError:
            raise Exception('Invalid starting balance. Try something like 17.25 or 0 (the default).')
        return balance

    def getArgs(self):
        isTestFlag = False
        balance = App.defaultBalance

        if len(sys.argv) > 2:
            raise Exception('Unrecognized arguments.')
        elif len(sys.argv) == 2:
            value = sys.argv[1]
            if value == '-t':
                isTestFlag = True
            else:
                balance = self.parseAndValidateBalance(value)

        return (isTestFlag, balance)

    def processUserInputs(self, balance):
        print('Welcome to the bank.')
        account = Acct('MySavings', balance)
        account.sBalance()
        account.TransactionProcessing()

    def run(self):
        try:
            (isTestFlag, balance) = self.getArgs()
        except Exception as e:
            print(e)
            self.usage()
            sys.exit(1)

        if not isTestFlag:
            self.processUserInputs(balance)
        elif not Test().run():
            sys.exit(1)


def main():
    writer(header1, data1, client_list)
    writer(header2, data2, transaction_list)
    Test().run()
    sys.exit(0)

main()

