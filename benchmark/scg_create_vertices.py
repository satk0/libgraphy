import sys

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import csgraph_from_dense

n = int(sys.argv[1])

sparse_matrix = csr_matrix((n,n), dtype=np.int8).toarray()
graph = csgraph_from_dense(sparse_matrix)
