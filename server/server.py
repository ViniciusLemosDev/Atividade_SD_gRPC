import grpc
from concurrent import futures
import uuid

import tarefas_pb2
import tarefas_pb2_grpc

tarefas = {}

server = grpc.server(
    futures.ThreadPoolExecutor(max_workers=10)
)

class TaskService(tarefas_pb2_grpc.TaskServiceServicer):

    def CriarTarefa(self, request, context):
        id_tarefa = str(uuid.uuid4())

        tarefa = tarefas_pb2.Tarefa(
            id=id_tarefa,
            titulo=request.titulo,
            descricao=request.descricao,
            status=request.status,
            data_limite=request.data_limite,
            responsaveis=request.responsaveis
        )

        tarefas[id_tarefa] = tarefa

        return tarefa

    def ListarTarefas(self, request, context):
        lista_tarefas = []

        for tarefa in tarefas.values():
            lista_tarefas.append(tarefa)

        return tarefas_pb2.ListarTarefasResponse(
            tarefas=lista_tarefas
        )

    def AtualizarTarefa(self, request, context):

        if request.id not in tarefas:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Tarefa não encontrada")
            return tarefas_pb2.Tarefa()

        tarefa = tarefas[request.id]

        tarefa.titulo = request.titulo
        tarefa.descricao = request.descricao
        tarefa.status = request.status
        tarefa.data_limite = request.data_limite
        tarefa.responsaveis[:] = request.responsaveis

        return tarefa

    def DeletarTarefa(self, request, context):

        if request.id not in tarefas:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Tarefa não encontrada")
            return tarefas_pb2.DeletarTarefaResponse()

        del tarefas[request.id]

        return tarefas_pb2.DeletarTarefaResponse(
            sucesso=True,
            mensagem="Tarefa deletada com sucesso"
        )
        
tarefas_pb2_grpc.add_TaskServiceServicer_to_server(
    TaskService(),
    server
)

server.add_insecure_port("[::]:50051")

server.start()
print("Servidor rodando na porta 50051...")

server.wait_for_termination()