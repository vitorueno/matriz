from matriz import *
import unittest


class Matriz_Teste(unittest.TestCase):
    def test_init(self):
        m1 = Matriz(1, 2)
        self.assertEqual(m1.l, 1)
        self.assertEqual(m1.c, 2)
        self.assertEqual(m1.m, [[0, 0]])

        m2 = Matriz(0, 0)
        self.assertEqual(m2.l, 0)
        self.assertEqual(m2.c, 0)
        self.assertEqual(m2.m, [])

        m3 = Matriz(-2, -3)
        self.assertEqual(m3.l, 2)
        self.assertEqual(m3.c, 3)
        self.assertEqual(m3.m, [[0, 0, 0], [0, 0, 0]])

        m4 = Matriz(3, 1)
        self.assertEqual(m4.l, 3)
        self.assertEqual(m4.c, 1)
        self.assertEqual(m4.m, [[0], [0], [0]])

    def test_from_list(self):
        m1 = Matriz.from_list([[1, 2, 3], [4, 5, 6]])
        self.assertEqual(m1.l, 2)
        self.assertEqual(m1.c, 3)
        self.assertEqual(m1.m, [[1, 2, 3], [4, 5, 6]])

        m2 = Matriz.from_list([[1, 2, 3]])
        self.assertEqual(m2.l, 1)
        self.assertEqual(m2.c, 3)
        self.assertEqual(m2.m, [[1, 2, 3]])

        m3 = Matriz.from_list([[1], [2], [3]])
        self.assertEqual(m3.l, 3)
        self.assertEqual(m3.c, 1)
        self.assertEqual(m3.m, [[1], [2], [3]])

    def test_gauss(self):
        m1 = Matriz.from_list([
            [2, 3, 1, 0, 9],
            [3, 1, 2, 1, 9],
            [2, 1, 3, 4, 15],
            [1, 2, 4, 3, 15]])

        m1.gauss()

        self.assertEqual(m1.m, [[2, 3, 1, 0, 9],
                                [0, -7, 1, 2, -9],
                                [0, 0, -12, -24, -60],
                                [0, 0, 0, 56, 112]])

    def test_LU(self):
        m1 = Matriz.from_list([
            [2, 4, 3, 5],
            [-4, -7, -5, -8],
            [6, 8, 2, 9],
            [4, 9, -2, 14]])
        m2 = deepcopy(m1)

        m1.gauss()

        result = m1.L * m1.U

        self.assertEqual(result.m, m2.m)

    def test_jordan(self):
        m1 = Matriz.from_list([[2, 3, 1, 0, 9],
                               [0, -7, 1, 2, -9],
                               [0, 0, -24, -48, -120],
                               [0, 0, 0, -1344, -2688]])

        m1.jordan()

        self.assertEqual(m1.m, [[1.0, 0, 0, 0, 1.0],
                                [0, 1.0, 0, 0, 2.0],
                                [0, 0, 1.0, 0, 1.0],
                                [0, 0, 0, 1.0, 2.0]])

    def test_soma_escalar(self):
        m1 = Matriz.from_list([[1, 2], [3, 4]])
        mResult = m1 + 1
        self.assertEqual(m1.m, [[2, 3], [4, 5]])
        self.assertEqual(m1.m, mResult.m)

        m1 = Matriz.from_list([[1, 2], [3, 4]])
        1 + m1
        self.assertEqual(m1.m, [[2, 3], [4, 5]])

    def test_soma_matriz(self):
        m1 = Matriz.from_list([[1, 2], [3, 4]])
        m2 = Matriz.from_list([[1, 2], [3, 4]])
        mResult = m1 + m2

        self.assertEqual(m1.m, [[2, 4], [6, 8]])
        self.assertEqual(m1.m, mResult.m)

        mResult = m2 + m1
        self.assertEqual(m2.m, [[3, 6], [9, 12]])
        self.assertEqual(m2.m, mResult.m)

    def test_sub_escalar(self):
        m1 = Matriz.from_list([[1, 2], [3, 4]])
        mResult = m1 - 1
        self.assertEqual(m1.m, [[0, 1], [2, 3]])
        self.assertEqual(m1.m, mResult.m)

        m1 = Matriz.from_list([[1, 2], [3, 4]])
        1 - m1

        self.assertEqual(m1.m, [[0, -1], [-2, -3]])

    def test_sub_matriz(self):
        m1 = Matriz.from_list([[5, 10], [15, 20]])
        m2 = Matriz.from_list([[1, 2], [3, 4]])
        mResult = m1 - m2

        self.assertEqual(m1.m, [[4, 8], [12, 16]])
        self.assertEqual(m1.m, mResult.m)

        mResult = m2 - m1
        self.assertEqual(m2.m, [[-3, -6], [-9, -12]])
        self.assertEqual(m2.m, mResult.m)

    def test_mul_escalar(self):
        m1 = Matriz.from_list([[1, 2], [3, 4]])
        mResult = m1 * 2

        self.assertEqual(m1.m, [[2, 4], [6, 8]])
        self.assertEqual(mResult.m, [[2, 4], [6, 8]])

        m1 = Matriz.from_list([[1, 2], [3, 4]])
        2 * m1
        self.assertEqual(m1.m, [[2, 4], [6, 8]])

    def test_mul_matriz(self):
        m1 = Matriz.from_list([[2, 3], [1, 0], [4, 5]])
        m2 = Matriz.from_list([[3, 1], [2, 4]])
        m3 = m1 * m2

        self.assertEqual(m3.l, 3)
        self.assertEqual(m3.c, 2)
        self.assertEqual(m3.m, [[12, 14], [3, 1], [22, 24]])
        self.assertEqual(m1.m, [[2, 3], [1, 0], [4, 5]])
        self.assertEqual(m2.m, [[3, 1], [2, 4]])

    def test_div_escalar(self):
        m1 = Matriz.from_list([[2, 4], [8, 16]])
        mResult = m1 / 2
        mResult *= 2
        self.assertEqual(m1.m, [[1, 2], [4, 8]])
        self.assertEqual(mResult.m, [[2, 4], [8, 16]])

        m1 = Matriz.from_list([[2, 4], [5, 10]])

        100 / m1

        self.assertEqual(m1.m, [[50, 25], [20, 10]])

    def test_retro_sub(self):
        m1 = Matriz.from_list([[1.0, 0, 0, 0, 1.0],
                              [0, 1.0, 0, 0, 2.0],
                              [0, 0, 1.0, 0, 1.0],
                              [0, 0, 0, 1.0, 2.0]])

        result = m1.retrosubstituicao()

        self.assertEqual(result.m, [[1.0], [2.0], [1.0], [2.0]])

    def test_substituicao_direta(self):
        m1 = Matriz.from_list([
            [2, 0, 0, 0, 6],
            [2, 4, 0, 0, 22],
            [1, 2, 3, 0, 29],
            [4, 2, 1, 5, 31]
        ])

        result = m1.substituicao_direta()

        self.assertEqual(result.m, [[3], [4], [6], [1]])

    def test_identidade(self):
        m1 = Matriz.identidade(3)

        self.assertEqual(m1.m, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def test_cholesky(self):
        A = Matriz.from_list([
            [4, 12, -16],
            [12, 37, -43],
            [-16, -43, 98]
        ])

        G, Gt = A.cholesky()

        self.assertEqual((G * Gt).m, A.m)

    def test_gauss_pivoteamento_parcial(self):
        A = Matriz.from_list([
            [2, 4, 3, 1],
            [1, 2, -2, 11],
            [4, 4, 3, 3]
        ])

        A.gauss_pivoteamento_parcial()

        self.assertEqual(A.m, [[4, 4, 3, 3],
                               [0, 8, 6, -2],
                               [0, 0, -56, 168]])

        self.assertEqual(A.rota, [2, 0, 1])


if __name__ == '__main__':
    unittest.main()
