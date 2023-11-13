menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
extrato = ""
numero_saque = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "s":
        if numero_saque >= LIMITE_SAQUES:
            print("Operação falhou! Você já excedeu o limite de saques.")
        else:
            valor = float(input("Informe o valor do saque: "))
            if valor <= 0:
                print("Operação falhou! O valor informado é inválido.")
            elif valor > saldo:
                print("Operação falhou! Você não tem saldo suficiente.")
            else:
                saldo -= valor
                extrato += f"Saque: R$ {valor:.2f}\n"
                numero_saque += 1

    elif opcao == "e":
        print("\n======================== EXTRATO ========================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"Saldo: R$ {saldo:.2f}")
        print("===========================================================")

    elif opcao == "q":
        print("Saindo...")
        break
    else:
        print("Operação inválida! Por favor, informe a opção novamente da operação desejada.")
