import numpy as np

match = -3
blank = 5
sub = 1
gap = '-'
d=3

class dist_value:
    def __init__(self, value, prev_dist_index: tuple[int,int] = None):
        self.value = value
        self.prev_dist_index = prev_dist_index

    def set_pointer(self, dist):
        self.prev_dist_index = dist

    def __str__(self):
        return f"{self.value}"

def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if(type(matrix[i][j]) == int):
                print(matrix[i][j], " ", end="")
            else:
                print(matrix[i][j].value, " ", end="")
            
        print("\n") 

    return None   

def print_dict(band_dict):
    for key, value in band_dict.items():
        print(key, value.value)



def calculate_dist(diag: int, up: int, side: int, seq1: str, seq2: str, 
                row_index, col_index) -> tuple[int, tuple[int, int]]:
    dist = None
    if(side!=None):
        side = side+blank
    if(up!= None):
        up = up+blank
    index = None
    if seq1[row_index] == seq2[col_index]:
        diag = diag+match
    else:
        diag = diag +sub
    dist = diag
    index = [row_index-1, col_index-1]
    if(up == None) or (side==None):
        if(up==None) and (side < diag):
            dist = side
            index = [row_index, col_index-1]
        elif(side == None) and (up < diag):
            dist = diag
            index = [row_index-1, col_index]
    else:
        if (side < diag) and (side < up):
            dist = side
            index = [row_index, col_index-1]
        elif (up < side) and (up < diag):
            dist = up
            index = [row_index-1, col_index]

    if (up < diag):
        dist = up
        index = [row_index-1, col_index]

    
    return dist, index

def intit_basecase(matrix, d_row, d_col, band: bool):
    for i in range(1,d_col):
        if(band):
            matrix[(0,i)] = dist_value(matrix.get((0, i-1)).value + blank )
          #  matrix.update({(0,i): dist_value(matrix.get([0, i-1]).value + blank)})
            matrix.get(tuple([0,i])).prev_dist_index = [0,i-1]
        else:
            matrix[0][i] = dist_value(matrix[0][i-1].value + blank)
            matrix[0][i].prev_dist_index = [0,i-1]
    for i in range(1,d_row):
        if(band):
            matrix[(i,0)] = dist_value(matrix.get((i-1,0)).value + blank)
            #matrix.update({tuple([i,0]): dist_value(matrix.get([i-1, 0]).value + blank)})
            matrix.get(tuple([i,0])).prev_dist_index = [i-1,0] 
        else:
            matrix[i][0] = dist_value(matrix[i-1][0].value + blank)
            matrix[i][0].prev_dist_index = [i-1,0]
       # print("i: ", i, " prev_dist_val ", matrix[i][0].prev_dist_val)
    
    return None

#think about setting up calc distance differently and using dict for original method
def fill_matrix_test(matrix, d, bandwidth, seq1, seq2, band: bool):
    b = 1
    for i in range(b,d+2):
        for j in range(b,d+2):
            #dist, index = calculate_dist(matrix.get((i-1,j-1)).value, matrix.get((i-1,j)).value, 
            #matrix.get((i,j-1)).value, seq1, seq2, i, j)
            matrix[(i,j)] = dist_value(dist)
            matrix.get((i,j)).prev_dist_index = index
            if(d_col != len(seq1)):
                d_col = d_col+1
            if(d_col+1 == bandwidth):
                b_col = b_col+1
            print("val: ", matrix.get((i,j)).value)
            dist, index = calculate_dist(matrix[i-1][j-1].value,matrix[i-1][j].value,
            matrix[i][j-1].value, seq1, seq2, i,j)
            matrix[i][j] = dist_value(dist)
            matrix[i][j].prev_dist_index = index
            dist2, index2 = calculate_dist(matrix[j-1]) 

def fill_matrix(matrix, d_row, d_col, bandwidth, seq1, seq2, b_col, band: bool):
    for i in range(1,d_row):
        for j in range(b_col,d_col):
            #print("i: ", i, " j: ", j)
            if(band):
                print("i: ",i, " j: ", j)
                if(matrix.get((i,j-1))== None):
                    dist,index = calculate_dist(matrix.get((i-1,j-1)), matrix.get((i-1,j)).value, None,
                     seq1, seq2, i, j)
                elif(matrix.get((i-1,j))==None):
                    print("diag: ",matrix.get((i-1,j-1)))
                    print("side: ",matrix.get((i,j-1)))
                    dist, index = calculate_dist(matrix.get((i-1,j-1)).value, None, matrix.get((i,j-1)).value,
                    seq1, seq2, i, j)
                else:
                    dist, index = calculate_dist(matrix.get((i-1,j-1)).value, matrix.get((i-1,j)).value, 
                matrix.get((i,j-1)).value, seq1, seq2, i, j)
                matrix[(i,j)] = dist_value(dist)
                matrix.get((i,j)).prev_dist_index = index
                if(d_col != len(seq1)):
                    d_col = d_col+1
                if(d_col+1 == bandwidth):
                    b_col = b_col+1
                print("val: ", matrix.get((i,j)).value)
            else:
                dist, index = calculate_dist(matrix[i-1][j-1].value,matrix[i-1][j].value,
                matrix[i][j-1].value, seq1, seq2, i,j)
                matrix[i][j] = dist_value(dist)
                matrix[i][j].prev_dist_index = index

    return None

def normal_edit(seq1: str, seq2: str):
   # seq1 = gap + seq1
   # seq2 = gap + seq2
    d_row = len(seq1)
    d_col = len(seq2)
    matrix = [[0 for _ in range(len(seq2))] for _ in range(len(seq1))] 
    matrix[0][0] = dist_value(0)
    intit_basecase(matrix, len(seq1), len(seq2), False)
    fill_matrix(matrix, len(seq1), len(seq2), 0, seq1, seq2,1, False)
    dist = matrix[d_row-1][d_col-1]
    print_matrix(matrix)
    return dist, matrix

#could just have a dictionary with the dist value and 'index'
def banded_edit(seq1: str, seq2: str, d, bandwidth):
    dist = 0
    band_dict = dict()
    band_dict.update({tuple([0,0]): dist_value(0)})
    intit_basecase(band_dict,d+1,d+1, True)
    print_dict(band_dict)
    fill_matrix(band_dict, d+1, d+1, 0, seq1, seq2,1, True)
    print_dict(band_dict)
    return dist, band_dict

#need to consider gaps in this function
# also need to check indexing for string
def get_alignment(matrix,seq1,seq2):
    #i = 0
    alg_mat = []
    align1 = ''
    align2 = ''
    alg_mat.append([len(seq1)-1,len(seq2)-1])
    i = len(seq1)-1
    j = len(seq2)-1
    while(1):
        prev = matrix[i][j].prev_dist_index
        if(prev == [0,0]) or (prev == None):
            break
        alg_mat.append(prev)
        i = prev[0]
        j = prev[1]
        #index = matrix[]
    alg_mat.reverse()
    prev_i = -1
    prev_j = -1
    for val in alg_mat:
        if(val[0] == prev_i):
            align1 = align1 + gap
        else:
            align1 = align1 + seq1[val[0]]
        if(val[1] == prev_j):
            align2 = align2 + gap
        else:
            align2 = align2 + seq2[val[1]]
        prev_i = val[0]
        prev_j = val[1]
    return align1, align2

# for right now it is str1 on row, str2 on col
'''here is my design experience lol, so for normal obviously want to create a matrix with back pointers
if we are moving to the right, or down it will cost 5
a match will be moving diagonal with a cost of -3
a substitution will also be a diagonal move with cost of 1
whichever string is bigger goes on top, smaller one goes on bottom, we need the first 
value to be blank on both strings
the 'backpointers' of the data structure should be the indexes not the distance value
seq1_len = len(seq1)
    seq2_len = len(seq2)
    if(seq1_len > seq2_len):
        matrix = np.empty(seq2_len, seq1_len)
    else:
        matrix = np.empty(seq1_len, seq2_len)
'''
'''
banded algorithm
list[[0,0],[0,1],[0,2],[0,3],[1,0],[1,1],[1,2],[1,3],[1,4],
[2,0],[2,1],[2,2],[2,3],[2,4],[2,5],[3,0],[3,1],[3,2],[3,3],
[3,4],[3,5],[3,6],[4,1],[4,2],[4,3],[4,4],[4,7],[5,2],[5,3],
[5,4],[5,5],[5,6],[5,7],[6,3],[6,4],[6,5],[6,6],[6,7],[7,4]
[7,5],[7,6],[7,7]]
use dict which keeps track of what 'index' each value is at
'''

def align(
        seq1: str,
        seq2: str,
        match_award=-3,
        indel_penalty=5,
        sub_penalty=1,
        banded_width=-1,
        gap='-'
) -> tuple[float, str | None, str | None]:
    match = match_award
    blank = indel_penalty
    sub = sub_penalty 
    gap = gap
    seq1 = gap + seq1
    seq2 = gap + seq2
    if(banded_width == -1):
        dist, matrix = normal_edit(seq1, seq2)
    
    else:
        dist, matrix = banded_edit(seq1, seq2,d, banded_width)
    alignment1, alignment2 = get_alignment(matrix,seq1,seq2)
  

    return dist.value, alignment1, alignment2
    """
        Align seq1 against seq2 using Needleman-Wunsch
        Put seq1 on left (j) and seq2 on top (i)
        => matrix[i][j]
        :param seq1: the first sequence to align; should be on the "left" of the matrix
        :param seq2: the second sequence to align; should be on the "top" of the matrix
        :param match_award: how many points to award a match
        :param indel_penalty: how many points to award a gap in either sequence
        :param sub_penalty: how many points to award a substitution
        :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
        :param gap: the character to use to represent gaps in the alignment strings
        :return: alignment cost, alignment 1, alignment 2
    """

def main():
    str1 = "hey"
    str2 = "he"
    dist2, a2, b2 = align("ACAATCC", "AGCATGC")
    #dist2, a2, b2 = align("ATGCATGC", "ATGGTGC")
    print(a2)
    print(b2)
    print(dist2)
    dist, a, b = align("ACAATCC", "AGCATGC", banded_width=3)
    print(a)
    print(b)
    print(dist)
   
  
   # normal_edit(str1, str2)



if __name__ == "__main__":
    main()
