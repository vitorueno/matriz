from random import randint
import unittest
from copy import deepcopy


class Matriz:
    def __init__(self, linha: int, coluna: int):
        self.l = abs(linha)
        self.c = abs(coluna)
        self.iniciar()
        self.isGauss = False
        self.isJordan = False

    @classmethod
    def from_list(self, lista):
        objeto = self.__new__(self)
        objeto.m = lista
        objeto.l = len(lista)
        objeto.c = len(lista[0])
        self.isGauss = False
        self.isJordan = False
        return objeto

    def iniciar(self, zeros=True):
        self.m = []
        for i in range(self.l):
            self.m.append([])  # cria linha
            for j in range(self.c):
                num = 0 if zeros else randint(1, 10)
                self.m[i].append(num)  # preenche coluna

    def subtrair_linha(self, indiceLinha1, indiceLinha2, multLinha1=1, multLinha2=1):
        linha2 = [x * multLinha2 for x in self.m[indiceLinha2]]
        for j in range(self.c):
            self.m[indiceLinha1][j] = self.m[indiceLinha1][j] * \
                multLinha1 - linha2[j]

    def __str__(self):
        matriz_string = ''

        for i in range(self.l):
            for j in range(self.c):
                matriz_string += f'{self.m[i][j]} '

            matriz_string += '\n'

        return matriz_string

    def __add__(self, outro):
        for i in range(self.l):
            for j in range(self.c):
                if isinstance(outro, int) or isinstance(outro, float):
                    self.m[i][j] += outro
                elif isinstance(outro, Matriz):
                    self.m[i][j] += outro.m[i][j]
        return deepcopy(self)

    def __radd__(self, outro):
        if isinstance(outro, int) or isinstance(outro, float):
            return self.__add__(outro)

    def __sub__(self, outro):
        for i in range(self.l):
            for j in range(self.c):
                if isinstance(outro, int) or isinstance(outro, float):
                    self.m[i][j] -= outro
                elif isinstance(outro, Matriz):
                    self.m[i][j] -= outro.m[i][j]
                else:
                    raise Exception('Tipo não suportado')

        return deepcopy(self)

    def __rsub__(self, outro):
        if isinstance(outro, int) or isinstance(outro, float):
            self * -1
            return self.__add__(outro)

    def __mul__(self, outro):
        if isinstance(outro, int) or isinstance(outro, float):
            for i in range(self.l):
                for j in range(self.c):
                    self.m[i][j] *= outro

            return deepcopy(self)

        elif isinstance(outro, Matriz):
            if self.c != outro.l:
                raise Exception('Operação inválida: a quantidade de colunas da matriz a' +
                                'esquerda deve ser igual a quantidade de linhas da matriz a direita' +
                                f'mas {self.c} != {outro.l}')

            n = Matriz(self.l, outro.c)  # nova matriz

            for i in range(self.l):
                for j in range(outro.c):
                    soma = 0
                    for k in range(self.c):  # índice auxiliar
                        soma += self.m[i][k] * outro.m[k][j]

                    n.m[i][j] = soma

            return n

        else:
            raise Exception('Tipo não suportado')

    def __rmul__(self, outro):
        if isinstance(outro, int) or isinstance(outro, float):
            return self.__mul__(outro)

    def __truediv__(self, outro):
        if not (isinstance(outro, int) or isinstance(outro, float)):
            raise Exception('Tipo não permitido para operação')

        for i in range(self.l):
            for j in range(self.c):
                self.m[i][j] /= outro

        return deepcopy(self)

    def __rtruediv__(self, outro):
        if isinstance(outro, int) or isinstance(outro, float):
            for i in range(self.l):
                for j in range(self.c):
                    self.m[i][j] = 1/self.m[i][j]
            return self.__mul__(outro)

    def gauss(self):
        if self.isGauss:
            raise Exception('Matriz já passou pela eliminação de Gauss')

        for i in range(self.l-1):
            pivo = self.m[i][i]
            for k in range(i+1, self.l):
                primeiro = self.m[k][i]
                self.subtrair_linha(k, i, pivo, primeiro)

        self.isGauss = True

    def jordan(self):
        if self.isJordan:
            raise Exception('Matriz já passou pela elimanação de gauss Jordan')

        if not self.isGauss:
            self.gauss()

        for i in range(self.l-1, -1, -1):
            pivo = self.m[i][i]
            for j in range(i-1, -1, -1):
                primeiro = self.m[j][i]
                self.subtrair_linha(j, i, pivo, primeiro)

            self.m[i][i] /= pivo
            self.m[i][self.c-1] /= pivo

        self.isJordan = True


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
                                [0, 0, -24, -48, -120],
                                [0, 0, 0, -1344, -2688]])

    def test_gauss_jordan(self):
        m1 = Matriz.from_list([
            [2, 3, 1, 0, 9],
            [3, 1, 2, 1, 9],
            [2, 1, 3, 4, 15],
            [1, 2, 4, 3, 15]])

        m1.gauss()
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


def main():
    # m1 = Matriz.from_list([[1, 2], [3, 4]])
    # m2 = Matriz.from_list([[1, 2], [3, 4]])
    # m1 + m2

    # print(m2)
    # m1 = Matriz.from_list([
    #     [2, 3, 1, 0, 9],
    #     [3, 1, 2, 1, 9],
    #     [2, 1, 3, 4, 15],
    #     [1, 2, 4, 3, 15]])

    # m1.gauss()

    # m1.jordan()

    # print(m1)

    unittest.main()


if __name__ == "__main__":
    main()
