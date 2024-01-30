'''Algoritmo capaz de calcular o desempenho de um ou mais candidatos no Vestibular UEM'''


from dataclasses import dataclass

@dataclass
class Prova:
    Código: int
    Redação: float
    Respostas: list

@dataclass
class Desempenho:
    Código: int
    Nota: float

def somatorio_alternativas(s:int)->list[int]:
    '''Recebe um valor s, calcula e retorna quais alternativas da questão
    compõe o valor s.
        Exemplos:
        >>> somatorio_alternativas(31)
        [1, 2, 4, 8, 16]'''
    corretas = []
    alternativa = 1
    while(s > 0):
        if(s % 2 == 1):
            corretas.append(alternativa)
        s = s // 2
        alternativa = alternativa * 2

    return corretas

def qualificados(provas:list[Prova], qlf:list)->list[Prova]:
    if len(provas) == 0:
        return qlf
    else:
        if(provas[0].Redação != 0.0):
            qlf.append(provas[0])
            return qualificados(provas[1:], qlf)
        else:
            return qualificados(provas[1:], qlf)

def calc_desempenho(classificados: list[Prova], gab: list)->list:
    desempenhos = []
    for i in range(len(classificados)):
        desempenhos_cand = []
        for j in range(len(gab)):
            nota_cand = []
            alternativas_candidato = somatorio_alternativas(classificados[i].Respostas[j])
            alternativas_gabarito = somatorio_alternativas(gab[j])
            if(len(alternativas_candidato) > len(alternativas_gabarito)):
                desempenhos_cand.append(0)
            else:
                marcou_a_mais = verifica_questao(alternativas_candidato, alternativas_gabarito)
                if(marcou_a_mais == True):
                    desempenhos_cand.append(0)
                else:
                    valor_alternativa = 6/len(alternativas_gabarito)
                    parcial = len(alternativas_candidato) * valor_alternativa
                    desempenhos_cand.append(parcial)
        total_candidato = soma_vetor(desempenhos_cand)
        desempenhos.append(total_candidato)
    return desempenhos

def verifica_questao(lista_respostas, lista_gabarito: list)->bool:
    if(len(lista_respostas) == 0):
        return False
    else:
        if(lista_respostas[0] in lista_gabarito):
            return verifica_questao(lista_respostas[1:], lista_gabarito)
        else:
            return True

def soma_vetor(array:list)->float:
    soma = 0
    for i in range(len(array)):
        soma += array[i]
    return soma

def resultados_finais(provas:list[Prova], desempenhos:list)->list[Desempenho]:
    result:list[Desempenho] = []
    for i in range(len(provas)):
        cdg_candidato = provas[i].Código
        nota_candidato = desempenhos[i] + provas[i].Redação
        candidato = Desempenho(cdg_candidato, nota_candidato)
        result.append(candidato)
    
    return result

def ordena_notas(lista: list[Desempenho])->list[Desempenho]:
    cdg_aux: Desempenho.Código
    nota_aux: Desempenho.Nota


    for i in range(len(lista)):
        for j in range(i+1, len(lista)):
            if(lista[j].Nota > lista[i].Nota):
                cdg_aux = lista[j].Código
                nota_aux = lista[j].Nota
                lista[j].Código = lista[i].Código
                lista[j].Nota = lista[i].Nota
                lista[i].Código = cdg_aux
                lista[i].Nota = nota_aux
    
    return lista


def main():
    print("\n\t----- INSERÇÃO DO GABARITO -----\n")
    n = int(input("Insira o tamanho da lista de respostas/gabarito: "))
    gabarito = []
    for i in range(n):
        elem = int(input(f"Insira o gabarito da questão {i+1}: "))
        gabarito.append(elem)
    print("GABARITO:", gabarito)

    print("\n\n\t ----- INSERÇÃO DAS PROVAS -----\n")
    resp = True
    provas = []
    while(resp == True):
        cod = int(input("Insira o código do candidato: "))
        red = float(input("Insira a nota de redação: "))
        resps= []
        for i in range(n):
            alt = int(input(f"Insira a resposta da questão {i+1}: "))
            resps.append(alt)
        test = Prova(cod,red,resps)
        provas.append(test)

        resposta = input("Deseja adicionar mais uma prova? (S/N) ")
        resposta = resposta.upper()
        if(resposta != 'S'):
            resp = False

    classificados:list[Prova] = []
    classificados = qualificados(provas, classificados)
    resultados_parciais:list[Desempenho] = calc_desempenho(classificados, gabarito)
    resultado = resultados_finais(classificados, resultados_parciais)
    ordenado = ordena_notas(resultado)
    print("\n\n\t ----- DESEMPENHOS -----\n")
    print("CÓDIGO \t\t\t NOTA")
    print("", "-"*30,)
    for i in range(len(ordenado)):
        print(ordenado[i].Código, "\t\t\t", ordenado[i].Nota)
        

