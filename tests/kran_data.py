kran_data = [[[(4, 1), (9, 0), (14, 0)], False],  # kran data for test
             [[(3, 1), (4, 1), (9, 0), (14, 0)], True],
             [[(2, 1), (4, 1), (9, 0), (14, 0)], True],
             [[(2, 1), (3, 1), (4, 1), (9, 0), (14, 0)], True],
             [[(1, 1), (4, 1), (9, 0), (14, 0)], True],
             [[(1, 1), (3, 1), (4, 1), (9, 0), (14, 0)], True],
             [[(1, 1), (2, 1), (4, 1), (9, 0), (14, 0)], True],
             [[(1, 1), (2, 1), (3, 1), (4, 1), (9, 0), (14, 0)], True],
             [[(0, 1), (4, 1), (9, 0), (14, 0)], True],
             [[(0, 1), (3, 1), (4, 1), (9, 0), (14, 0)], True],
             [[(0, 1), (2, 1), (4, 1), (9, 0), (14, 0)], True],
             [[(0, 1), (2, 1), (3, 1), (4, 1), (9, 0), (14, 0)], True],
             [[(0, 1), (1, 1), (4, 1), (9, 0), (14, 0)], True],
             [[(0, 1), (1, 1), (3, 1), (4, 1), (9, 0), (14, 0)], True],
             [[(0, 1), (1, 1), (2, 1), (4, 1), (9, 0), (14, 0)], True],
             [[(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (9, 0), (14, 0)], True],
             [[(3, 1), (8, 0), (13, 0)], False],
             [[(2, 1), (3, 1), (8, 0), (13, 0)], True],
             [[(1, 1), (3, 1), (8, 0), (13, 0)], True],
             [[(1, 1), (2, 1), (3, 1), (8, 0), (13, 0)], True],
             [[(0, 1), (3, 1), (8, 0), (13, 0)], True],
             [[(0, 1), (2, 1), (3, 1), (8, 0), (13, 0)], True],
             [[(0, 1), (1, 1), (3, 1), (8, 0), (13, 0)], True],
             [[(0, 1), (1, 1), (2, 1), (3, 1), (8, 0), (13, 0)], True],
             [[(2, 1), (7, 0), (12, 0)], False],
             [[(1, 1), (2, 1), (7, 0), (12, 0)], True],
             [[(0, 1), (2, 1), (7, 0), (12, 0)], True],
             [[(0, 1), (1, 1), (2, 1), (7, 0), (12, 0)], True],
             [[(1, 1), (6, 0), (11, 0)], False],
             [[(0, 1), (1, 1), (6, 0), (11, 0)], True],
             [[(0, 1), (5, 0), (10, 0)], False]]


value_minutes = [[[1, 0, 0], [4, 9, 14], False],
                 [[1, 1, 0, 0], [3, 4, 9, 14], True],
                 [[1, 1, 0, 0], [2, 4, 9, 14], True],
                 [[1, 1, 1, 0, 0], [2, 3, 4, 9, 14], True],
                 [[1, 1, 0, 0], [1, 4, 9, 14], True],
                 [[1, 1, 1, 0, 0], [1, 3, 4, 9, 14], True],
                 [[1, 1, 1, 0, 0], [1, 2, 4, 9, 14], True],
                 [[1, 1, 1, 1, 0, 0], [1, 2, 3, 4, 9, 14], True],
                 [[1, 1, 0, 0], [0, 4, 9, 14], True],
                 [[1, 1, 1, 0, 0], [0, 3, 4, 9, 14], True],
                 [[1, 1, 1, 0, 0], [0, 2, 4, 9, 14], True],
                 [[1, 1, 1, 1, 0, 0], [0, 2, 3, 4, 9, 14], True],
                 [[1, 1, 1, 0, 0], [0, 1, 4, 9, 14], True],
                 [[1, 1, 1, 1, 0, 0], [0, 1, 3, 4, 9, 14], True],
                 [[1, 1, 1, 1, 0, 0], [0, 1, 2, 4, 9, 14], True],
                 [[1, 1, 1, 1, 1, 0, 0], [0, 1, 2, 3, 4, 9, 14], True],
                 [[1, 0, 0], [3, 8, 13], False],
                 [[1, 1, 0, 0], [2, 3, 8, 13], True],
                 [[1, 1, 0, 0], [1, 3, 8, 13], True],
                 [[1, 1, 1, 0, 0], [1, 2, 3, 8, 13], True],
                 [[1, 1, 0, 0], [0, 3, 8, 13], True],
                 [[1, 1, 1, 0, 0], [0, 2, 3, 8, 13], True],
                 [[1, 1, 1, 0, 0], [0, 1, 3, 8, 13], True],
                 [[1, 1, 1, 1, 0, 0], [0, 1, 2, 3, 8, 13], True],
                 [[1, 0, 0], [2, 7, 12], False],
                 [[1, 1, 0, 0], [1, 2, 7, 12], True],
                 [[1, 1, 0, 0], [0, 2, 7, 12], True],
                 [[1, 1, 1, 0, 0], [0, 1, 2, 7, 12], True],
                 [[1, 0, 0], [1, 6, 11], False],
                 [[1, 1, 0, 0], [0, 1, 6, 11], True],
                 [[1, 0, 0], [0, 5, 10], False]]






