# Desafio DIO - Python com GitHub Copilot
# Programa simples para verificar se um número é par ou ímpar

def verificar_par_ou_impar(numero):
    if numero % 2 == 0:
        return "Par"
    else:
        return "Ímpar"


numero = int(input("Digite um número: "))
resultado = verificar_par_ou_impar(numero)

print(f"O número {numero} é {resultado}.")