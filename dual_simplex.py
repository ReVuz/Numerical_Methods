import numpy as np

MAX_MODE = 'MAX'
MIN_MODE = 'MIN'


class SimplexMethod:
    def __init__(self, c, a, b, mode):  # c-obj function #b-RHS a-LHS
        # 2 variable  # number of variables #shape given the number of columns of numpy array
        self.main_variables_count = a.shape[1]
        # 4 constraints  # number of restrictions
        self.restrictions_count = a.shape[0]
        self.variables_count = self.main_variables_count + \
            self.restrictions_count  # 6  # number of variables
        self.mode = mode  # we remember the mode of operation

        # coefficients of the function
        self.c = np.concatenate([c, np.zeros((self.restrictions_count + 1))])
        # values of the function F (zj-cj)
        self.f = np.zeros((self.variables_count + 1))
        # indexes of basic variables
        self.basis = [
            i + self.main_variables_count for i in range(self.restrictions_count)]
        # (0+2,1+2,2+2,3+2)

        self.init_table(a, b)

    # initializing the table
    def init_table(self, a, b):
        # table coefficients 4x7
        self.table = np.zeros(
            (self.restrictions_count, self.variables_count + 1))
       # inserting values into table
        for i in range(self.restrictions_count):
            for j in range(self.main_variables_count):
                self.table[i][j] = a[i][j]

            for j in range(self.restrictions_count):
                # slack variable filling
                self.table[i][j + self.main_variables_count] = int(i == j)
                self.table[i][-1] = b[i]

    # getting a string with the maximum modulo negative value of b
    def get_negative_b_row(self):  # which row does our leaving variable is in?
        row = -1
        for i, a_row in enumerate(self.table):
            if a_row[-1] < 0 and (row == -1 or abs(a_row[-1]) > abs(self.table[row][-1])):
                row = i
        return row

    # getting a column with the maximum modulo element in a row
    # leaving variable col la most negative
    def get_negative_b_column(self, row):
        column = -1

        for i, aij in enumerate(self.table[row][:-1]):
            if aij < 0 and (column == -1 or abs(aij) > abs(self.table[row][column])):
                column = i

        return column

    # removing negative free coefficients
    def remove_negative_b(self):
        while True:
            row = self.get_negative_b_row()  # we are looking for a string containing negative b

            if row == -1:  # if you didn't find such a string
                return True  # then everything is fine

            # looking for a permissive column
            column = self.get_negative_b_column(row)

            if column == -1:
                return False  # failed to delete
            self.gauss(row, column)  # performing a Gaussian exception
            self.calculate_f()
            print('\nLeaving variable has been removed in row:', row + 1)
            self.print_table()

    # performing a step of the gauss method
    def gauss(self, row, column):  # column --> leaving variable row -->entering variable
        # self.table[row][column] - pivot element
        self.table[row] /= self.table[row][column]
        # self.table[row] - leaving var row
        for i in range(self.restrictions_count):
            if i != row:  # neglecting the leaving variable row
                # entering variable ooda corresponding col
                self.table[i] -= self.table[row] * self.table[i][column]

        # changing the the variable number in table based on leaving and entering variable
        self.basis[row] = column

    # calculation of F values

    def calculate_f(self):
        for i in range(self.variables_count + 1):
            self.f[i] = -self.c[i]

            for j in range(self.restrictions_count):
                self.f[i] += self.c[self.basis[j]] * self.table[j][i]

    # calculation of simplex relations for column column

    def get_relations(self, column):
        q = []

        for i in range(self.restrictions_count):
            if self.table[i][column] == 0:
                # if any value results in infinity we return it and stop
                q.append(np.inf)

            else:
                q_i = self.table[i][-1] / \
                    self.table[i][column]  # ratio calculation
                q.append(q_i if q_i >= 0 else np.inf)

        return q

    # getting a solution
    def get_solve(self):
        y = np.zeros((self.variables_count))

        # filling out the solution
        for i in range(self.restrictions_count):
            y[self.basis[i]] = self.table[i][-1]

        return y

    # decision
    def solve(self):
        print('\nIteration 0')
        self.calculate_f()
        self.print_table()

        if not self.remove_negative_b():  # if the b value is not there then it is infeasible
            print('Solution does not exist')
            return False

        iteration = 1

        while True:
            self.calculate_f()
            print('\nIteration', iteration)
            self.print_table()

            # if the plan is optimal
            if all(fi >= 0 if self.mode == MAX_MODE else fi <= 0 for fi in self.f[:-1]):
                break  # then we finish the work

            column = (np.argmin if self.mode == MAX_MODE else np.argmax)(
                self.f[:-1])  # we get the resolving column
            # we get simplex relations for the found column
            q = self.get_relations(column)

            if all(qi == np.inf for qi in q):  # if the resolving string could not be found
                # we inform you that there is no solution
                print('Solution does not exist')
                return False

            self.gauss(np.argmin(q), column)  # performing a Gaussian exception
            iteration += 1

        return True  # there is a solution

    # simplex table output
    def print_table(self):
        print('     |' + ''.join(['   y%-3d |' % (i + 1)
              for i in range(self.variables_count)]) + '    b   |')

        for i in range(self.restrictions_count):
            print('%4s |' % ('y' + str(self.basis[i] + 1)) + ''.join(
                [' %6.2f |' % aij for j, aij in enumerate(self.table[i])]))

        print('   F |' + ''.join([' %6.2f |' % aij for aij in self.f]))
        print('   y |' + ''.join([' %6.2f |' % xi for xi in self.get_solve()]))

    # coefficient output #horizontal y1,y2,y3,...
    def print_coef(self, ai, i):
        if ai == 1:
            return 'y%d' % (i + 1)

        if ai == -1:
            return '-y%d' % (i + 1)

        return '%.2fy%d' % (ai, i + 1)

    # output of the task
    def print_task(self, full=False):
        print(' + '.join(['%.2fy%d' % (ci, i + 1) for i, ci in enumerate(
            self.c[:self.main_variables_count]) if ci != 0]), '-> ', self.mode)

        for row in self.table:
            if full:
                print(' + '.join([self.print_coef(ai, i) for i, ai in enumerate(
                    row[:self.variables_count]) if ai != 0]), '=', row[-1])
            else:
                print(' + '.join([self.print_coef(ai, i) for i, ai in enumerate(
                    row[:self.main_variables_count]) if ai != 0]), '<=', row[-1])

# translation into a dual task


def make_dual(a, b, c):
    return -a.T, -c, b


ch = 'y'
while ch == 'y':
    print("\n\t\tDUAL SIMPLEX METHOD")
    print("\n1. MAXIMISE")
    print("2. MINIMISE")
    print("3. EXIT")
    print("\n")
    choice = int(input("Enter your choice : "))
    if choice == 1:
        n_eqn = int(
            input("Enter the no: of equations(except the objective function) : "))
        n_var = int(input("Enter the no: of variables : "))
        A = []
        for i in range(n_eqn):
            j = int(input("Enter the constants : "))
            A.append(j)
        c = np.array(A)
        arr = []
        for i in range(n_var):
            col = []
            for j in range(n_eqn):
                coeff = int(input("Enter the coefficients : "))
                col.append(coeff)
            arr.append(col)
        print(arr)
        a = np.array(arr)
        Z = []
        for i in range(n_var):
            k = int(input("Enter the coefficients of the objective function : "))
            Z.append(k)
        b = np.array(Z)
        a, b, c = make_dual(a, b, c)  # turned into a dual task
        simplex = SimplexMethod(c, a, b, MAX_MODE)  # turn into max mode

        print("Dual task:")
        simplex.print_task()
        simplex.solve()

    if choice == 2:
        n_eqn = int(
            input("Enter the no: of equations(except the objective function) : "))
        n_var = int(input("Enter the no: of variables : "))
        A = []
        for i in range(n_eqn):
            i = int(input("Enter the constants : "))
            A.append(i*-1)
        c = np.array(A)
        arr = []
        for i in range(n_var):
            col = []
            for j in range(n_eqn):
                coeff = int(input("Enter the coefficients : "))
                col.append(coeff*-1)
            arr.append(col)
        print(arr)
        a = np.array(arr)
        Z = []
        for i in range(n_var):
            k = int(input("Enter the coefficients of the objective function : "))
            Z.append(k)
        b = np.array(Z)
        a, b, c = make_dual(a, b, c)  # turned into a dual task
        simplex = SimplexMethod(c, a, b, MAX_MODE)  # turn into max mode

        print("Dual task:")
        simplex.print_task()
        simplex.solve()
    if choice == 3:
        print("\nThank You")
        break
    ch = input("Do you want to continue(y/n) ? : ")
'''c = np.array([1, -7, 10, -3])  # RHS
a = np.array([
    [1, -1, 1, 0],
    [1, -1, 2, -1]
])

#b = np.array([-3, -2])  # objective fn

a, b, c = make_dual(a, b, c)  # turned into a dual task
simplex = SimplexMethod(c, a, b, MAX_MODE)  # turn into max mode

print("Dual task:")
simplex.print_task()
simplex.solve()
'''
