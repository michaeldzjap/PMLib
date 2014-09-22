from sparse_diff_matr import laplacian_matrix_2d

mat = laplacian_matrix_2d(4,4,'LeftSimplySupportedRightSimplySupportedTopClampedBottomSimplySupported')
print mat.todense()
