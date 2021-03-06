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


value_minutes = [[[1, 0, 0], [10, 5, 0], False],
                 [[1, 1, 0, 0], [11, 10, 5, 0], True],
                 [[1, 1, 0, 0], [12, 10, 5, 0], True],
                 [[1, 1, 1, 0, 0], [12, 11, 10, 5, 0], True],
                 [[1, 1, 0, 0], [13, 10, 5, 0], True],
                 [[1, 1, 1, 0, 0], [13, 11, 10, 5, 0], True],
                 [[1, 1, 1, 0, 0], [13, 12, 10, 5, 0], True],
                 [[1, 1, 1, 1, 0, 0], [13, 12, 11, 10, 5, 0], True],
                 [[1, 1, 0, 0], [14, 10, 5, 0], True],
                 [[1, 1, 1, 0, 0], [14, 11, 10, 5, 0], True],
                 [[1, 1, 1, 0, 0], [14, 12, 10, 5, 0], True],
                 [[1, 1, 1, 1, 0, 0], [14, 12, 11, 10, 5, 0], True],
                 [[1, 1, 1, 0, 0], [14, 13, 10, 5, 0], True],
                 [[1, 1, 1, 1, 0, 0], [14, 13, 11, 10, 5, 0], True],
                 [[1, 1, 1, 1, 0, 0], [14, 13, 12, 10, 5, 0], True],
                 [[1, 1, 1, 1, 1, 0, 0], [14, 13, 12, 11, 10, 5, 0], True],
                 [[1, 0, 0], [11, 6, 1], False],
                 [[1, 1, 0, 0], [12, 11, 6, 1], True],
                 [[1, 1, 0, 0], [13, 11, 6, 1], True],
                 [[1, 1, 1, 0, 0], [13, 12, 11, 6, 1], True],
                 [[1, 1, 0, 0], [14, 11, 6, 1], True],
                 [[1, 1, 1, 0, 0], [14, 12, 11, 6, 1], True],
                 [[1, 1, 1, 0, 0], [14, 13, 11, 6, 1], True],
                 [[1, 1, 1, 1, 0, 0], [14, 13, 12, 11, 6, 1], True],
                 [[1, 0, 0], [12, 7, 2], False],
                 [[1, 1, 0, 0], [13, 12, 7, 2], True],
                 [[1, 1, 0, 0], [14, 12, 7, 2], True],
                 [[1, 1, 1, 0, 0], [14, 13, 12, 7, 2], True],
                 [[1, 0, 0], [13, 8, 3], False],
                 [[1, 1, 0, 0], [14, 13, 8, 3], True],
                 [[1, 0, 0], [14, 9, 4], False],
                 [[1, 1, 1, 1, 1, 1, 1, 1, 1], [
                     14, 12, 10, 8, 6, 4, 3, 1, 0], False],
                 [[1, 1, 1, 1], [11, 9, 6, 2], False],
                 [[1, 1, 1], [11, 7, 3], False],
                 [[1, 1, 1, 1], [14, 9, 5, 0], False],
                 [[1, 1, 1], [14, 9, 4], False],
                 [[1, 0, 1, 1], [14, 9, 4, 0], False],
                 [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
                  False],
                 [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [14, 13, 12, 11, 10, 9, 8, 7, 5, 4, 2, 1, 0],
                  False],
                 [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
                  False],
                 [[1, 1, 1, 1, 1, 1, 1, 1, 1], [
                     14, 12, 11, 9, 8, 6, 4, 1, 0], False],
                 [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
                  False],
                 [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [
                     14, 12, 11, 10, 9, 8, 7, 6, 1, 0], False],
                 [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [13, 10, 9, 7, 6, 5, 4, 3, 2, 1, 0],
                  False],
                 [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [13, 12, 11, 10, 9, 8, 7, 5, 4, 3, 2, 1, 0],
                  False],
                 [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [14, 13, 12, 11, 9, 8, 6, 5, 4, 3, 2, 1, 0],
                  False],
                 [[1, 1, 1, 1, 1, 1, 1, 1, 1], [
                     13, 12, 11, 10, 7, 5, 3, 2, 0], False],
                 [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [14, 13, 11, 10, 8, 7, 5, 4, 3, 2, 1, 0],
                  False],
                 [[1, 1], [12, 10], True],
                 [[1], [12], False],
                 [[1, 0], [14, 9], False],
                 [[1, 1], [13, 10], True],
                 [[1, 1, 1, 1], [14, 13, 12, 11], True],
                 [[0, 1], [14, 10], False],
                 [[1, 1, 0], [14, 11, 9], True],
                 [[1, 1, 1, 1, 1, 1], [14, 13, 12, 11, 10, 9], True],
                 [[1, 1], [1, 0], False],
                 [[1], [0], False],
                 [[1, 1, 1], [4, 2, 0], False],
                 [[1], [1], False],
                 [[1], [2], False],
                 [[1], [3], False],
                 [[0], [4], False],
                 [[0], [3], False],
                 [[0], [2], False],
                 [[0], [1], False],
                 [[0], [0], False],
                 [[1, 0], [9, 4], False],
                 [[1, 0], [8, 3], False],
                 [[1, 0], [7, 2], False],
                 [[1, 0], [6, 1], False],
                 [[1, 0], [5, 0], False],
                 [[1], [4], False],
                 [[1, 0], [10, 5], False],
                 [[1, 0], [9, 4], False],
                 [[1, 0], [8, 3], False],
                 [[1, 0], [7, 2], False],
                 [[1, 0], [6, 1], False],
                 [[1], [5], False],
                 [[1, 0], [11, 6], False],
                 [[1, 0], [10, 5], False],
                 [[0, 1, 0], [14, 9, 4], False],
                 [[0, 1, 0], [13, 8, 3], False],
                 [[0, 1, 0], [12, 7, 2], False],
                 [[0, 1], [11, 6], False],
                 [[1, 0], [10, 5], False],
                 [[0, 1, 0], [14, 9, 4], False],
                 [[0, 1, 0], [13, 8, 3], False],
                 [[0, 1, 0], [12, 7, 2], False],
                 [[0, 1, 0], [11, 6, 1], False],
                 [[0, 1], [10, 5], False],
                 [[1], [1], False],
                 [[1], [2], False],
                 [[1], [3], False],
                 [[1], [4], False],
                 [[1], [5], False],
                 [[1], [6], False],
                 [[1], [7], False],
                 [[1], [8], False],
                 [[1], [9], False],
                 [[], [], False]]
