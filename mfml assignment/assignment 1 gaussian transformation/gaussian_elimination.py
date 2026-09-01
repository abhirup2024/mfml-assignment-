import copy 

def print_matrix(matrix,label=""):
    if label:
        print("\n"+label)
    for row in matrix:
        print(["{:.6f}".format(value) for value in row])

def check_dimensions(A,b):
    if len(A)==0:
        raise ValueError("Coefficient matrix cannot be empty!\n")
    if len(A[0])==0:
        raise ValueError("the coefficient matrix must have atleast one column\n")

    columns = len(A[0])

    for row in A:
        if len(row) != columns:
            raise ValueError("Invalid matrix dimensions , all rows must have the same length")

    if len(A) != len(b):
        raise ValueError("Error ! the number of equations must match the length of RHS vector")

def forward_elimination(A,b,tolerance=1e-10):
    check_dimensions(A,b)

    rows = len(A)
    columns = len(A[0])

    aug = [list(A[i]) + [b[i]] for i in range(rows)]

    print_matrix(aug,"Augumented matrix [A|b]:")

    pivot_columns=[]
    current_row = 0

    for col in range(columns):
        if current_row>=rows:
            break

        max_row = current_row

        for r in range(current_row+1, rows):
            if(abs(aug[r][col])>abs(aug[max_row][col])):
                max_row=r

        if abs(aug[max_row][col])<tolerance:
            continue

        if max_row != current_row:
            aug[max_row],aug[current_row] = aug[current_row],aug[max_row]

        for r in range(current_row+1,rows):
            if abs(aug[r][col])>tolerance:
                factor = aug[r][col]/aug[current_row][col]

                for j in range(col,columns+1):
                    aug[r][j] -= factor*aug[current_row][j]

        pivot_columns.append(col)
        current_row +=1

    print_matrix(aug,"matrix after forward elimination")

    return aug,pivot_columns

def check_inconsistent(aug, num_variables, tolerance=1e-10):

    for row in aug:

        all_zero = True

        # Check coefficients
        for j in range(num_variables):

            if abs(row[j]) >= tolerance:
                all_zero = False
                break

        # If coefficients are all zero but RHS is not zero
        if all_zero and abs(row[num_variables]) >= tolerance:
            return True

    return False

def back_substitution(aug,pivot_columns, num_variables, tolerance=1e-10):

    x=[0.0]*num_variables

    for i in range(len(pivot_columns)-1, -1, -1):
        pivot_col = pivot_columns[i]
        pivot= aug[i][pivot_col]

        if abs(pivot)<tolerance:
            raise ValueError("zero point encountered during back substitution")

        value = aug[i][num_variables]

        for j in range(pivot_col+1, num_variables):
            value -= aug[i][j]*x[j]

        x[pivot_col]= value/pivot
    return x

def rank_calculation(aug, num_variables, tolerance=1e-10):
    rank=0

    for row in aug:
        nonzero_coeff = False

        for j in range(num_variables):
            if abs(row[j])>=tolerance:
                nonzero_coeff=True
                break

        if nonzero_coeff:
            rank+=1

    return rank

def verify_soln(A,b,x, tolerance=1e-10):
    print("\nsolution verification :")

    correct= True

    for i in range(len(A)):
        lhs=0.0

        for j in range(len(x)):
            lhs += A[i][j]*x[j]

        difference= abs(lhs -b[i])

        if difference<=tolerance:
            result="pass"
        else:
            result="fail"
            correct=False

        print("equation ",i+1," LHS = ",lhs," RHS = ",b[i]," result = ",result)

    if correct:
        print("verification passed ! ")
    else:
        print("verification failed ! ")

def gaussian_elimination(A,b):
    original_A= copy.deepcopy(A)
    original_b= list(b)

    try:
        check_dimensions(original_A,original_b)

        rows= len(original_A)
        variables= len(original_A[0])

        if rows > variables:
            print("\nSystem type: OVERDETERMINED")

        elif rows < variables:
            print("\nSystem type: UNDERDETERMINED")

        else:
            print("\nSystem type: DETERMINED")

        print("\nGaussian Elimination")

        print_matrix(original_A,"the coefficient matrix A")
        print("\nRHS vector")
        print(original_b)

        aug,pivot_columns = forward_elimination(copy.deepcopy(original_A),original_b)

        if check_inconsistent(aug, variables):

            print("\nResult:")
            print("The system is INCONSISTENT.")
            print("Therefore, there is NO SOLUTION.")

            return None

        rank = rank_calculation(aug, variables)

        print("\nrank of coefficient matrix =",rank)
        print("\nnumber of variables =",variables)
        print("\nnumber of rows =",rows)

        if rank== variables:
            x=back_substitution(aug,pivot_columns,variables)
            print("\nResult: UNIQUE solution ")

            for i in range(variables):
                print("x",i+1,"=",x[i])

            verify_soln(original_A,original_b,x)

            return x
        
        else:
            x=back_substitution(aug,pivot_columns,variables)

            print("\nResult: the system of equations has INFINITELY MANY solutions ")
            print("the system has :",variables-rank," free variables ")

            for i in range(variables):
                print("x",i+1," = ",x[i])

            verify_soln(original_A,original_b,x)
            return x

    except ValueError as e:
        print("\nError :",e)
        return None

def main():
    print("gaussian elimination ")

    rows=int(input("enter the number of equations :"))
    variables= int(input("enter the number of variables(unknowns) :"))

    print("\nenter the coefficient matrix A (if an equations is 3x+4y-5z=8 , enter the coefficient of the variables x,y,z respectively as \n3\n4'\n-5  )")

    A=[]

    for i in range(rows):
        row=[]

        for j in range(variables):
            value = float(input("enter A["+str(i+1)+"]["+str(j+1)+"]:"))
            row.append(value)

        A.append(row)

    print("enter the RHS vector 'b' (suppose the system of equations : 3x+4y=5 , 7x-11y=-13 ; enter \n5\n-13  )")
    b=[]
    for i in range(rows):
        value = float(input(f"enter b[{i+1}] :"))
        b.append(value)

    gaussian_elimination(A,b)

main()