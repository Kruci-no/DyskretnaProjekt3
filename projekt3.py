import numpy as np
class Modulo_number:
    def __init__(self,p,value):
        self.p = p
        self.value = value % p
    def __eq__(self,other):
        if self.p != other.p or self.value != other.value:
            return False
        return True
    def __repr__(self):
        return str(self)
    def __hash__(self):
        return hash(str(self))
    def __add__(self,other):
        return Modulo_number(self.p,(self.value + other.value)%self.p)
    def __mul__(self,other):
        return Modulo_number(self.p,(self.value * other.value)%self.p)
    def __pow__(self,k):
        b = self.value
        pow_value = 1
        while k!=0:
            if k % 2 == 1:
                pow_value = b * pow_value
                k=k-1
            b = (b * b) % self.p
            k = k/2
        return Modulo_number(self.p,pow_value)        
    def __str__(self):
        return str(self.value) + " mod " + str( self.p)
    def is_generator(self):
        for i in range(2,self.p - 1):
            if (self.p - 1) % i == 0 and (self**i).value == 1:
                return False
        return True   
    def generate_diff_set(self):
        return {self**(i*2) for i in range((self.p-1)//2)}

def addition_array(p):
        return np.array([[Modulo_number(p,i) + Modulo_number(p,j) for j in range(p)] for i  in range(p)])
    
def generate_latine_squares(array,p):
    for i in range (1,p):
        per=[(Modulo_number(p,k)*Modulo_number(p,i)).value for k in range(p)]
        array2 = array[per,:]
        yield array2
        
def generate_rows(orth_latine_squars,p):
    for i in range(p):
        for j in range(p):
             yield np.append([i,j] ,[latine_square[i,j].value for latine_square in orth_latine_squars])
                
def generate_projective_space(matrix):
    yield {i for i in range(matrix.shape[1])}
    for i in range(matrix.shape[1]):
        for k in range(matrix.shape[1] - 1):
            line = {i}|{j + matrix.shape[1]  for j in range(matrix.shape[0]) if matrix[j][i]==k}
            yield line  
            
def is_prime(x):
    for i in range(2,int(x**(1/2))+1):
        if x%i == 0:
            return False
    return True

def set_to_code(S,n):
    string = ""
    for i in range(n):
        string = string+str(int(i in S))
    return string
    
class Robots:
    def __init__(self,N):
        self.max = N
        self.robots = []
        delta = - 3 + self.max * 4
        positive_sol = (-1+delta**(1/2))/2
        self.n = int(np.ceil(positive_sol))
        while not is_prime(self.n):
            self.n = self.n + 1
        arr = addition_array(self.n)
        orth_latine_squars = np.array([a for a in generate_latine_squares(arr,self.n) ])
        matrix = np.array([row for row in generate_rows(orth_latine_squars,self.n)])
        self.available_names = [i for i in generate_projective_space(matrix) ]

class Codes:
    def __init__(self,M,K):
        self.mess_num = M
        self.max_errors = K
        delta = - 3 + self.mess_num * 4
        positive_sol = (-1+delta**(1/2))/2
        self.n_projective= int(np.ceil(positive_sol))
        
        while not is_prime(self.n_projective ) or self.n_projective+1-1 <= self.max_errors:
            self.n_projective = self.n_projective + 1
            
        self.n_cyclic = M
        self.k = int((self.n_cyclic - 1)/2)
        self.r2 = int(self.k*(self.k-1)/(self.n_cyclic-1))
        while  (self.n_cyclic+1)%4 != 0 or self.k-self.r2<=self.max_errors or not is_prime(self.n_cyclic):
            self.n_cyclic = self.n_cyclic + 1
            self.k = int((self.n_cyclic - 1)/2)
            self.r2 = int(self.k*(self.k-1)/(self.n_cyclic-1))
        
        self.size_projective = self.n_projective**2 + self.n_projective + 1
        if self.size_projective < self.n_cyclic:
            arr = addition_array(self.n)
            orth_latine_squars = np.array([a for a in generate_latine_squares(arr,self.n_projective) ])
            matrix = np.array([row for row in generate_rows(orth_latine_squars,self.n)])
            self.set_family = [i for i in generate_projective_space(matrix) ]
            self.code_len = self.n_projective**2 + self.n_projective + 1 
        else:
            one = Modulo_number(self.n_cyclic,1)
            z = Modulo_number(self.n_cyclic,2)
            while not z.is_generator:
                z = one + z
            diff_set = z.generate_diff_set()
            self.set_family =  [{ (x + Modulo_number(self.n_cyclic,i)).value for x in diff_set} for i in range(self.n_cyclic)]
            self.code_len = self.n_cyclic
    
        self.codes=[set_to_code(S,self.code_len) for S in self.set_family]

        
if __name__=="__main__":
    N=30
    M=6
    K=3
    robots = Robots(N)
    codes = Codes(M,K)
    print("Dostępne nazwy robotów",robots.available_names[:N])
    print("Kodowania",codes.codes[:M])
    codes.size_projective