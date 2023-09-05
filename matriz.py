from math import sqrt
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
        self.L = None
        self.U = None

    @classmethod
    def from_list(self, lista):
        objeto = self.__new__(self)
        objeto.m = lista
        objeto.l = len(lista)
        objeto.c = len(lista[0])
        self.isGauss = False
        self.isJordan = False
        return objeto

    @classmethod
    def identidade(self, ordem):
        identidade = deepcopy(Matriz(ordem, ordem))
        for i in range(identidade.c):
            identidade.m[i][i] = 1
        return identidade

    def iniciar(self, zeros=True):
        self.m = []
        for i in range(self.l):
            self.m.append([])  # cria linha
            for j in range(self.c):
                num = 0 if zeros else randint(1, 10)
                self.m[i].append(num)  # preenche coluna

    def subtrair_linha(self, i1, i2, m1=1, m2=1):
        linha2 = [x * m2 for x in self.m[i2]]
        for j in range(self.c):
            self.m[i1][j] = self.m[i1][j] * m1 - linha2[j]

    def div_linha_if_int(self, iLinha, num):
        newLinha = [x/num for x in self.m[iLinha]]
        for elemento in newLinha:
            if not elemento.is_integer():
                return

        self.m[iLinha] = newLinha

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

        self.L = Matriz.identidade(self.l)

        for i in range(self.l-1):
            pivo = self.m[i][i]
            for k in range(i+1, self.l):
                fator = self.m[k][i]
                self.subtrair_linha(k, i, pivo, fator)
                self.L.m[k][i] = fator/pivo
                self.div_linha_if_int(k, pivo)

        self.isGauss = True
        self.U = deepcopy(self)

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

    def retrosubstituicao(self):
        if not self.isGauss:
            self.gauss()

        result = Matriz(self.l, 1)

        for i in range(self.l-1, -1, -1):
            soma = 0
            for j in range(i + 1, self.l):
                soma += self.m[i][j] * result.m[j][0]
            result.m[i][0] = (self.m[i][-1] - soma) / self.m[i][i]

        return result

    def substituicao_direta(self):
        result = deepcopy(Matriz(self.l, 1))

        for i in range(self.l):
            soma = 0
            for j in range(i):
                soma += self.m[i][j] * result.m[j][0]
            result.m[i][0] = (self.m[i][-1] - soma) / self.m[i][i]

        return result

    def cholesky(self):
        G = Matriz(self.l, self.c)
        Gt = Matriz(self.l, self.c)

        for i in range(self.c):
            soma = sum([G.m[i][k]**2 for k in range(0, i)])

            G.m[i][i] = sqrt(self.m[i][i] - soma)
            Gt.m[i][i] = G.m[i][i]

            for j in range(i+1, self.l):
                soma = sum([G.m[i][k] * G.m[j][k] for k in range(0, j)])
                G.m[j][i] = (self.m[j][i] - soma) / G.m[i][i]
                Gt.m[i][j] = G.m[j][i]

        return G, Gt


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


def main():
    A = Matriz.from_list([
        [4, 12, -16],
        [12, 37, -43],
        [-16, -43, 98]
    ])

    G, Gt = A.cholesky()

    print(G)
    print(Gt)

    print(G * Gt)
    unittest.main()


if __name__ == "__main__":
    main()
