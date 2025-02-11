import sys
import json

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import csgraph_from_dense

edges = json.loads(sys.argv[1])

n = 50

sparse_matrix = csr_matrix((n,n), dtype=np.int8).toarray()
for e in edges:
    sparse_matrix[e[0], e[1]] = e[2]

graph = csgraph_from_dense(sparse_matrix)

