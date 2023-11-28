import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Transacao(ABC):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    @classmethod
    def registrar(cls, conta, valor, historico):
        # Lógica de registro comum a todas as transações
        print("Registrando transação genérica")


class Deposito(Transacao):
    @classmethod
    def registrar(cls, conta, valor, historico):
        super(Deposito, cls).registrar(conta, valor, historico)
        # Lógica de registro específica para depósito
        print(f"Registrando depósito na conta {conta.numero} no valor de {valor}")

    def realizar_transacao(self, conta, historico_global):
        super().registrar(conta, self.valor, historico_global)
        conta.saldo += self.valor
        historico_global.adicionar_transacao(self)

class Saque(Transacao):
    @classmethod
    def registrar(cls, conta, valor, historico):
        super(Saque, cls).registrar(conta, valor, historico)
        # Lógica de registro específica para saque
        print(f"Registrando saque na conta {conta.numero} no valor de {valor}")

    def realizar_transacao(self, conta, historico_global):
        super().registrar(conta, self.valor, historico_global)
        conta.saldo -= self.valor  # Atualiza o saldo ao realizar um saque
        historico_global.adicionar_transacao(self)




class Conta:
    def __init__(self, numero, agencia, cliente, historico, saldo=0.0):
        self._saldo = saldo
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = historico
        self.transacoes = []
    
    def __str__(self):
        return f"Conta {self.numero} - Saldo: R$ {self.saldo:.2f}"
    
    @property
    def saldo(self):
        # Calcular o saldo com base nas transações
        return sum(transacao.valor for transacao in self.transacoes)

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @saldo.setter
    def saldo(self, novo_saldo):
        self._saldo = novo_saldo


    def depositar(self, valor, historico_global):
        transacao = Deposito(valor)
        self.transacoes.append(transacao)
        transacao.realizar_transacao(self, historico_global)
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        self._saldo += valor

    def exibir_saldo(self):
        saldo_atualizado = sum(transacao.valor for transacao in self.transacoes)
        print(f"Saldo:\nR$ {saldo_atualizado:.2f}")

    def realizar_transacao(self, transacao, historico_global):
        self.transacoes.append(transacao)
        transacao.registrar(self, transacao.valor, historico_global)

class ContaConrrente(Conta):
     def __init__(self, numero , cliente ,limite = 500 ,limite_saque=3):
         
         super().__init__(numero , cliente)
         self.limite = limite
         self.limite_saque = limite_saque
     def sacar (self , valor ):
         numero_saques = len([transacao for transacao in self.historico.transacao if transacao
                             ["tipo"]== Saque.__name__ ])
         
         excedeu_limite = valor > self._limite
         excedeu_saques = numero_saques >= self._limite_saques
          
         if excedeu_limite:
             print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
             
         elif excedeu_saques:   
             print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
         else:
             return super().sacar(valor)   
         return False 
     
     def __str__(self):
          return f"""\
              Agência:\t{self.agencia}
               C/C:\t\t{self.numero}
                Titular:\t{self.cliente.nome}
                """
              
             

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

    def menu(self):
        menu = """\n
        ================ MENU ================
            [1]\tDepositar
            [2]\tSacar
            [3]\tExtrato
            [4]\tNova conta
            [5]\tListar contas
            [6]\tNovo usuário
            [7]\tSair
        ============> """
        opcao = input(textwrap.dedent(menu))
        while not opcao.isdigit() or not 1 <= int(opcao) <= 7:
            print("Opção inválida. Por favor, escolha uma opção de 1 a 7.")
            opcao = input("=> ")
        return opcao


def criar_cliente(clientes, historico_global):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    criar_conta(cliente, historico_global)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(cliente, historico_global):
    numero_conta = len(cliente.contas) + 1
    conta = Conta(saldo=0, numero=numero_conta, agencia=0,
                  cliente=cliente, historico=historico_global)
    cliente.contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")


def escolher_conta(clientes):
    listar_contas(clientes)
    numero_conta = input("Escolha o número da conta: ")
    for cliente in clientes:
        for conta in cliente.contas:
            if conta.numero == int(numero_conta):
                return conta
    print("\n@@@ Conta não encontrada! @@@")
    return None


def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def filtrar_cliente(cpf, clientes):
    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            return cliente
    return None


def sacar(clientes, historico_global):
    cpf_cliente = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf_cliente, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    valor_saque = float(input("Informe o valor do saque: "))
    transacao_saque = Saque(valor_saque)
    conta.sacar(valor_saque, historico_global)


def escolher_conta(clientes):
    cpf = input("Informe o CPF do cliente: ")
    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            listar_contas(cliente)
            num_conta = int(input("Escolha o número da conta: "))
            return recuperar_conta_cliente(cliente, num_conta)
    print("Cliente não encontrado ou sem contas.")
    return None


def listar_contas(cliente):
    if isinstance(cliente, PessoaFisica):
        for conta in cliente.contas:
            print(conta)
    else:
        print("Cliente não é do tipo PessoaFisica ou não possui contas.")


def main():
    historico_global = Historico()
    clientes = []

    while True:
        opcao = historico_global.menu()

        if opcao == "1":
            depositar(clientes, historico_global)

        elif opcao == "2":
            sacar(clientes, historico_global)

        elif opcao == "3":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue
            conta = recuperar_conta_cliente(cliente)
            if conta:
                exibir_extrato(conta)
            else:
                print("\n@@@ Cliente não possui conta! @@@")

        elif opcao == "4":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            criar_conta(cliente, historico_global)

        elif opcao == "5":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            listar_contas(cliente)

        elif opcao == "6":
            criar_cliente(clientes, historico_global)
            print("\n=== Cliente criado com sucesso! ===")

        elif opcao == "7":
            break

        else:
            print(
                "Operação inválida, por favor selecione novamente a operação desejada."
            )


def depositar(clientes, historico_global):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    conta.realizar_transacao(transacao, historico_global)


def recuperar_conta_cliente(cliente, num_conta=None):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        # Se o cliente não tem conta, perguntar se deseja criar uma
        criar_conta_opcao = input(
            "Deseja criar uma conta para este cliente? (s/n): ")
        if criar_conta_opcao.lower() == 's':
            criar_conta(cliente, historico_global)
        else:
            return None

    # Se um número de conta foi fornecido, tenta encontrar a conta correspondente
    if num_conta is not None:
        for conta in cliente.contas:
            if conta.numero == num_conta:
                return conta

    # Agora permite ao cliente escolher a conta
    print("\nContas disponíveis:")
    for i, conta in enumerate(cliente.contas, 1):
        print(f"{i}. Agência: {conta.agencia}, Conta: {conta.numero}")

    escolha_conta = input("Escolha o número da conta: ")
    try:
        indice_conta = int(escolha_conta) - 1
        return cliente.contas[indice_conta]
    except (ValueError, IndexError):
        print("\n@@@ Escolha inválida! @@@")
        return None


class Cliente:
    def __init__(self, endereco, contas=None):
        self.endereco = endereco
        self.contas = contas if contas is not None else []

    def exibir_contas(self):
        if self.contas:
            print("Contas:")
            for conta in self.contas:
                print(f"- Agência: {conta.agencia}, Conta: {conta.numero}")
        else:
            print("O cliente não possui contas.")


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco, contas=[]):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.contas = contas


if __name__ == "__main__":
    main()