import textwrap
import re
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
        print(f"Registrando depósito na conta {conta.numero} no valor de R$ {valor}")

    def realizar_transacao(self, conta, historico_global):
        super().registrar(conta, self.valor, historico_global)
        conta.saldo += self.valor
        historico_global.adicionar_transacao(self, conta_numero=conta.numero)


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
    # Calcula o saldo com base nas transações
     return sum(transacao.valor if isinstance(transacao, Deposito) else -transacao.valor for transacao in self.transacoes)
            
           

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

    def sacar(self, valor, historico_global):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            transacao_saque = Saque(valor)
            self.transacoes.append(transacao_saque)
            transacao_saque.realizar_transacao(self, historico_global)
            print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False


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
     if transacao not in self.transacoes:  # Verifica se a transação já foi registrada
        self.transacoes.append(transacao)
        transacao.registrar(self, transacao.valor, historico_global)



class ContaCorrente(Conta):
    def __init__(self, numero, cliente, historico_global, limite=500, limite_saque=3):
        super().__init__(numero, "0001", cliente, historico_global)
        self.limite = limite
        self.limite_saque = limite_saque
        

    def sacar(self, valor, historico_global):
        # Verifica se o valor do saque excede o limite ou o número máximo de saques permitidos
        excedeu_limite = valor > self.limite
        numero_saques = len([transacao for transacao in self.historico.transacoes if isinstance(transacao, Saque)])
        excedeu_saques = numero_saques >= self.limite_saque

        if excedeu_limite or excedeu_saques:
            print("\n@@@ Operação falhou! Limite de saque excedido. @@@")
            return False

        # Calcula o saldo disponível considerando o limite
        saldo_disponivel = self.saldo + self.limite

        # Verifica se há saldo suficiente para o saque
        if valor > saldo_disponivel:
            print("\n@@@ Operação falhou! Saldo insuficiente para realizar o saque. @@@")
            return False

        # Realiza o saque
        super().sacar(valor, historico_global)
        return True

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
    cpf_pattern = re.compile(r'^\d{11}$')  # Regex para verificar se o CPF tem 11 dígitos

    cpf = input("Informe o CPF (somente número): ")

    if not cpf_pattern.match(cpf):
        print("CPF inválido. Por favor, insira um CPF válido.")
        return

    nome = input("Informe o nome completo: ")

    # Solicitar a data de nascimento até que seja fornecida corretamente
    while True:
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")

        data_nascimento_pattern = re.compile(r'^\d{2}-\d{2}-\d{4}$')

        if not data_nascimento_pattern.match(data_nascimento):
            print("Data de nascimento inválida. Por favor, insira a data no formato dd-mm-aaaa.")
        else:
            try:
                # Tentar converter a string de data para um objeto de data
                data_nascimento = datetime.strptime(data_nascimento, "%d-%m-%Y").date()
                break  # Se a conversão for bem-sucedida, sair do loop
            except ValueError:
                print("Data de nascimento inválida. Por favor, insira uma data válida no formato dd-mm-aaaa.")

    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    # Restante do código para criar o cliente
    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    criar_conta(cliente, historico_global)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")
    
    


def criar_conta(cliente, historico_global):
    numero_conta = len(cliente.contas) + 1
    conta = ContaCorrente(numero=numero_conta, cliente=cliente, historico_global=historico_global)
    cliente.contas.append(conta)
    print(f"\n=== Conta criada com sucesso! Cliente: {cliente.cpf}, Conta: {conta.numero} ===")

def exibir_extrato(conta, cpf):
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            if transacao.cliente_cpf == cpf:
                extrato += f"\n{transacao.tipo}:\n\tR$ {transacao.valor:.2f}"

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

    conta = recuperar_conta_cliente(cliente, cpf_cliente)
    if not conta:
        return

    valor_saque = float(input("Informe o valor do saque: "))
    transacao_saque = Saque(valor_saque)
    conta.sacar(valor_saque, historico_global)


def escolher_conta(clientes , cpf):
    cpf = input("Informe o CPF do cliente: ")
    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            listar_contas_por_cpf(clientes, cpf)
            num_conta = int(input("Escolha o número da conta: "))
            return recuperar_conta_cliente(cliente, num_conta)
    print("Cliente não encontrado ou sem contas.")
    return None



def obter_contas_por_cpf(clientes, cpf):
    contas_cliente = []

    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            contas_cliente.extend(cliente.contas)

    return contas_cliente



def listar_contas_por_cpf(clientes, cpf):
    contas_cliente = obter_contas_por_cpf(clientes, cpf)

    if not contas_cliente:
        print("Cliente não encontrado ou não possui contas.")
    else:
        for conta in contas_cliente:
            # Verifica se a conta pertence ao cliente com o CPF informado
            if conta.cliente.cpf == cpf:
                print(conta)




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
            conta = recuperar_conta_cliente(cliente, cpf)
            if conta:
             exibir_extrato(conta, cpf)
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

            listar_contas_por_cpf(clientes, cpf)

        elif opcao == "6":
            criar_cliente(clientes, historico_global)

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

    conta = recuperar_conta_cliente(cliente, cpf)
    if not conta:
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta.realizar_transacao(transacao, historico_global)


def recuperar_conta_cliente(cliente, cpf=None, num_conta=None):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        # Se o cliente não tem conta, perguntar se deseja criar uma
        criar_conta_opcao = input("Deseja criar uma conta para este cliente? (s/n): ")
        if criar_conta_opcao.lower() == 's':
            criar_conta(cliente, historico_global)
        else:
            return None

    # Se um número de conta foi fornecido, tenta encontrar a conta correspondente
    if num_conta is not None:
        for conta in cliente.contas:
            if conta.numero == num_conta and (cpf is None or conta.cliente.cpf == cpf):
                return conta

    # Agora permite ao cliente escolher a conta
    print("\nContas disponíveis:")
    contas_disponiveis = [conta for conta in cliente.contas if cpf is None or conta.cliente.cpf == cpf]
    for i, conta in enumerate(contas_disponiveis, 1):
        print(f"{i}. Agência: {conta.agencia}, Conta: {conta.numero}")

    while True:
        escolha_conta = input("Escolha o número da conta: ")
        try:
            indice_conta = int(escolha_conta) - 1
            conta_escolhida = contas_disponiveis[indice_conta]
            if conta_escolhida.cliente.cpf == cpf or cpf is None:
                return conta_escolhida
            else:
                print("\n@@@ Cliente não possui conta com o CPF correspondente! @@@")
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
        self.contas = []

    

if __name__ == "__main__":
    main()