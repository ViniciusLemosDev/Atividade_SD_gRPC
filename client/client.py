import grpc

import tarefas_pb2
import tarefas_pb2_grpc

channel = grpc.insecure_channel("192.168.56.10:50051")

stub = tarefas_pb2_grpc.TaskServiceStub(channel)

def mostrar_menu():
    print("\n MENU:")
    print("1 - Criar tarefa")
    print("2 - Listar tarefa")
    print("3 - Atualizar tarefa")
    print("4 - Deletar tarefa")
    print("0 - Sair")

def criar_tarefa(stub):
    titulo = input("TItulo: ")
    descricao = input("Descricao: ")
    status = input("Status: ")
    data_limite = input("Data limite: ")
    responsavel = input("Responsavel: ")

    request = tarefas_pb2.CriarTarefaRequest(
        titulo=titulo,
        descricao=descricao,
        status=status,
        data_limite=data_limite,
        responsaveis=[responsavel]
    )

    resposta = stub.CriarTarefa(request)

    print("\nTarefa criada com sucesso!")
    print(resposta)

def listar_tarefas(stub):
    request = tarefas_pb2.ListarTarefasRequest()

    resposta = stub.ListarTarefas(request)

    print("\nTAREFAS:")

    for tarefa in resposta.tarefas:
        print(f"\nID: {tarefa.id}")
        print(f"Titulo: {tarefa.titulo}")
        print(f"Descricao: {tarefa.descricao}")
        print(f"Status: {tarefa.status}")
        print(f"Data limite: {tarefa.data_limite}")
        print(f"Responsaveis: {', '.join(tarefa.responsaveis)}")

        input("\n Aperte enter para visualizar a proxima tarefa.")
        
    input("\nAperte enter para voltar para o Menu")

def atualizar_tarefa(stub):
    id_tarefa = input("ID da tarefa que deseja atualizar: ")

    titulo = input("Novo título: ")
    descricao = input("Nova descrição: ")
    status = input("Novo status: ")
    data_limite = input("Nova data limite: ")
    responsavel = input("Novo responsável: ")

    request = tarefas_pb2.AtualizarTarefaRequest(
        id=id_tarefa,
        titulo=titulo,
        descricao=descricao,
        status=status,
        data_limite=data_limite,
        responsaveis=[responsavel]
    )

    resposta = stub.AtualizarTarefa(request)

    print("\nTarefa atualizada com sucesso!")
    print(resposta)

def deletar_tarefa(stub):
    id_tarefa = input("ID da tarefa que deseja deletar: ")

    request = tarefas_pb2.DeletarTarefaRequest(
        id=id_tarefa
    )

    resposta = stub.DeletarTarefa(request)

    print(f"\n{resposta.mensagem}")

while True:
    mostrar_menu()

    opcao = input("Escolha uma opcao: ")

    match opcao:
        case "1":
            criar_tarefa(stub)

        case "2":
            listar_tarefas(stub)

        case "3":
            atualizar_tarefa(stub)

        case "4":
            deletar_tarefa(stub)

        case "0":
            print("Encerrando...")
            break

        case _:
            print("Pode nao PAE, digita uma opcao valida.")


