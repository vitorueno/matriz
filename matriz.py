from math import sqrt
from random import randint
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
        self.rota = [x for x in range(self.l)]

    @classmethod
    def from_list(self, lista):
        objeto = self.__new__(self)
        objeto.m = lista
        objeto.l = len(lista)
        objeto.c = len(lista[0])
        objeto.isGauss = False
        objeto.isJordan = False
        objeto.L = None
        objeto.U = None
        objeto.rota = [x for x in range(objeto.l)]
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

    def trocar_linha(self, i1, i2):
        tmp = [0 for x in range(self.c)]
        for j in range(self.c):
            tmp[j] = self.m[i1][j]
            self.m[i1][j] = self.m[i2][j]
            self.m[i2][j] = tmp[j]

        tmp2 = self.rota[i1]
        self.rota[i1] = self.rota[i2]
        self.rota[i2] = tmp2

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

    def gauss_pivoteamento_parcial(self):
        if self.isGauss:
            raise Exception('Matriz já passou pela eliminação de Gauss')

        for i in range(self.l-1):
            pivo = self.m[i][i]
            for k in range(i+1, self.l):
                if abs(self.m[k][i]) > pivo:
                    self.trocar_linha(i, k)
                    pivo = self.m[i][i]

                fator = self.m[k][i]
                self.subtrair_linha(k, i, pivo, fator)

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


def main():
    A = Matriz.from_list([
        [2, 4, 3, 1],
        [1, 2, -2, 11],
        [4, 4, 3, 3]
    ])

    print(A.rota)
    A.gauss_pivoteamento_parcial()

    print(A)
    print(A.rota)


if __name__ == "__main__":
    main()
