usuarios = [
    # {
    #     "cpf": "12345678900",
    #     "nome": "João Silva",
    #     "data_nascimento": "01/01/1990",
    #     "endereco": "Rua A, 123 - Bairro - Cidade X/UF"
    # },
    # {
    #     "cpf": "98765432100",
    #     "nome": "Maria Oliveira",
    #     "data_nascimento": "15/05/1985",
    #     "endereco": "Avenida B, 456 - Bairro - Cidade Y/UF"
    # }
]
contas = [
    # {"numero_conta": 1, "cpf": "12345678900", "saldo": 0, "extrato": "", "numero_saques": 0},
    # {"numero_conta": 2, "cpf": "98765432100", "saldo": 0, "extrato": "", "numero_saques": 0}
    
]
limite_saques = 3
limite_saque = 500
agencia = "0001"
contador_numero_conta = 0
menu_principal = """\n
[c] Cadastrar usuário
[a] Abrir conta
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
=> """

def cadastrar_usuario(usuarios, cpf, nome, data_nascimento, endereco):
    # """Cadastra um novo usuário se o CPF não estiver em uso."""
    if any(u.get("cpf") == cpf for u in usuarios):
        print("Usuário com este CPF já cadastrado.")
    else:
        usuarios.append({
            "cpf": cpf,
            "nome": nome,
            "data_nascimento": data_nascimento,
            "endereco": endereco
        })
        print("Usuário cadastrado com sucesso.")

def criar_conta(usuarios, contas, numero_conta, cpf):
    # """Cria uma nova conta vinculada a um usuário existente."""
    global contador_numero_conta
    if not any(u.get("cpf") == cpf for u in usuarios):
        print("Usuário não encontrado. Não é possível criar a conta.")
        return

    else:
        contador_numero_conta += 1
        contas.append({
            "numero_conta": contador_numero_conta,
            "cpf": cpf,
            "saldo": 0,
            "extrato": "",
            "numero_saques": 0
        })
       
        print(f"Conta criada com sucesso! Número da conta: {contador_numero_conta}")

def fazer_deposito(saldo, valor, /):
    # """Adiciona o valor ao saldo e retorna o novo saldo."""
    if valor > 0:
        saldo += valor
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
    else:
        print("O valor do depósito deve ser positivo.")
    return saldo

def fazer_saque(*, saldo, valor, limite, numero_saques, limite_saques):
    # """Realiza um saque se as condições forem atendidas e retorna o novo saldo e número de saques."""
    if valor > saldo:
        print("Saldo insuficiente para o saque.")
    elif valor > limite:
        print("O valor do saque excede o limite permitido.")
    elif numero_saques >= limite_saques:
        print("Número máximo de saques diários atingido.")
    elif valor > 0:
        saldo -= valor
        numero_saques += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
    else:
        print("O valor do saque deve ser positivo.")
    return saldo, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    # """Exibe o extrato das transações e o saldo atual."""
    print("\n================ EXTRATO ================")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        print(extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")




def main():
    global numero_conta
    while True:
        opcao = input(menu_principal).lower()

        if opcao == 'c':
            cpf = input("Informe o CPF (somente números): ")
            nome = input("Informe o nome completo: ")
            data_nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ")
            endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
            cadastrar_usuario(usuarios, cpf, nome, data_nascimento, endereco)

        elif opcao == 'a':
            cpf = input("Informe o CPF do usuário para vincular a conta: ")
            criar_conta(usuarios, contas, contador_numero_conta, cpf)
            

        elif opcao == 'd':
            numero = int(input("Informe o número da conta: "))
            conta = next((conta for conta in contas if conta["numero_conta"] == numero), None)
            if conta:
                valor = float(input("Informe o valor do depósito: "))
                conta["saldo"] = fazer_deposito(conta["saldo"], valor)
                if valor > 0:
                    conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"
            else:
                print("Conta não encontrada.")

        elif opcao == 's':
            numero = int(input("Informe o número da conta: "))
            conta = next((conta for conta in contas if conta["numero_conta"] == numero), None)
            if conta:
                valor = float(input("Informe o valor do saque: "))
                conta["saldo"], conta["numero_saques"] = fazer_saque(
                    saldo=conta["saldo"],
                    valor=valor,
                    limite=limite_saque,
                    numero_saques=conta["numero_saques"],
                    limite_saques=limite_saques
                )
                if valor > 0 and valor <= conta["saldo"]:
                    conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
            else:
                print("Conta não encontrada.")

        elif opcao == 'e':
            numero = int(input("Informe o número da conta: "))
            conta = next((conta for conta in contas if conta["numero_conta"] == numero), None)
            if conta:
                exibir_extrato(conta["saldo"], extrato = conta["extrato"])
            else:         
                print("Conta não encontrada.")

        elif opcao == 'q':
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()