# Projeto gRPC Distribuído — Sistema de Gerenciamento de Tarefas

Projeto desenvolvido para a disciplina de **Sistemas Distribuídos**, utilizando **gRPC** para comunicação entre múltiplas máquinas virtuais.

O sistema consiste em um servidor gRPC responsável pelo gerenciamento de tarefas e dois clientes que se comunicam remotamente com esse servidor através de uma rede privada.

## Tecnologias utilizadas

* Python 3
* gRPC
* Protocol Buffers
* VirtualBox
* Vagrant
* Linux
* Git/GitHub

---

# Arquitetura do sistema

O projeto utiliza três máquinas virtuais independentes:

```

Endereçamento das máquinas

| Máquina | Função        | IP              |
| ------- | ------------- | --------------- |
| VM 1    | Servidor gRPC | `192.168.56.10` |
| VM 2    | Cliente 1     | `192.168.56.11` |
| VM 3    | Cliente 2     | `192.168.56.12` |

O servidor utiliza a porta: 50051


Os clientes se conectam ao servidor através de: 192.168.56.10:50051

---

# Estrutura do projeto

```text
grpc-tarefas/
│
├── client/
│   └── client.py
│
├── server/
│   └── server.py
│
├── tarefas.proto
├── tarefas_pb2.py
├── tarefas_pb2_grpc.py
├── Vagrantfile
├── .gitignore
└── README.md
```

### Descrição dos arquivos

**`tarefas.proto`**

Define os serviços, mensagens e operações disponíveis no sistema gRPC.

**`tarefas_pb2.py`**

Arquivo Python gerado a partir do `.proto`, contendo as estruturas das mensagens.

**`tarefas_pb2_grpc.py`**

Arquivo Python gerado contendo o código necessário para comunicação com o serviço gRPC.

**`server/server.py`**

Implementa o servidor gRPC e as operações de gerenciamento das tarefas.

**`client/client.py`**

Implementa a interface de terminal utilizada pelos clientes.

**`Vagrantfile`**

Responsável pela criação e configuração das três máquinas virtuais.

---

# Pré-requisitos

Antes de iniciar, instale:

* VirtualBox
* Vagrant
* Git
---


# 1. Clonando o projeto

Clone o repositório:

```bash
git clone https://github.com/ViniciusLemosDev/Atividade_SD_gRPC
```

# 2. Criando as máquinas virtuais

No terminal, dentro da pasta que contém o `Vagrantfile`, execute:

```bash
vagrant up
```

O Vagrant irá criar as três máquinas:

```text
server
client1
client2
```

Para verificar:

```bash
vagrant status
```

O resultado esperado deve ser:

```text
server     running
client1    running
client2    running
```

---

# 3. Acessando as máquinas

## Servidor

```bash
vagrant ssh server
```

## Cliente 1

Abra outro terminal:

```bash
vagrant ssh client1
```

## Cliente 2

Abra um terceiro terminal:

```bash
vagrant ssh client2
```

É recomendado manter os três terminais abertos simultaneamente.

---

# 4. Acessando o projeto dentro da VM

Ao iniciar a VM, você deverá realizar os seguintes comandos:

Primeiro um cd .. pra sair do primeiro diretorio:

```bash
cd .. 
```
Depois outro cd .. pra sair do segundo diretorio

```bash
cd .. 
```

```bash
cd vagrant
```
Para entrar na pasta do projeto.

# 5. Iniciando o servidor

Na VM que vai ser o servidor e estando dentro da pasta vagrant feito no passo anterior faça o seguinte comando:

```bash
PYTHONPATH=/vagrant python3 server/server.py
```

```text
Servidor rodando na porta 50051...
```

Mantenha esse terminal aberto.

O servidor ficará aguardando requisições dos clientes.

---

# 6. Iniciando o Cliente 1

Na VM que vai ser o Cliente 1 e estando dentro da pasta vagrant feito no passo anterior faça o seguinte comando:

```bash
PYTHONPATH=/vagrant python3 client/client.py
```

O menu deverá aparecer:

```text
MENU:

1 - Criar tarefa
2 - Listar tarefa
3 - Atualizar tarefa
4 - Deletar tarefa
0 - Sair

Escolha uma opcao:
```

---

# 6. Iniciando o Cliente2

Na VM que vai ser o Cliente 2 e estando dentro da pasta vagrant feito no passo anterior faça o seguinte comando:

```bash
PYTHONPATH=/vagrant python3 client/client.py
```

O menu deverá aparecer:

```text
MENU:

1 - Criar tarefa
2 - Listar tarefa
3 - Atualizar tarefa
4 - Deletar tarefa
0 - Sair

Escolha uma opcao:
```

---


# 7. Testando a comunicação gRPC

## Criando uma tarefa

No **Cliente 1**, selecione:

```text
1 - Criar tarefa
```

Informe os dados solicitados:

```text
Titulo:
Descricao:
Status:
Data limite:
Responsavel:
```

O cliente enviará uma requisição gRPC para:

```text
192.168.56.10:50051
```

O servidor receberá a requisição e criará a tarefa.

---

# 8. Verificando a tarefa no Cliente 2

Agora, no **Cliente 2**, selecione:

```text
2 - Listar tarefa
```

A tarefa criada pelo Cliente 1 deverá aparecer.

Isso demonstra que:

```text
Cliente 1
    │
    │ CriarTarefa()
    ▼
Servidor
    │
    │ armazena tarefa
    ▼
Cliente 2
    │
    │ ListarTarefas()
    ▼
Servidor
    │
    ▼
Cliente 2 recebe a tarefa
```

Os dois clientes não armazenam suas próprias cópias independentes. O servidor é responsável pelo gerenciamento das tarefas.

---

# 9. Operações disponíveis

O sistema possui quatro operações principais:

| Opção | Operação         | RPC               |
| ----- | ---------------- | ----------------- |
| 1     | Criar tarefa     | `CriarTarefa`     |
| 2     | Listar tarefas   | `ListarTarefas`   |
| 3     | Atualizar tarefa | `AtualizarTarefa` |
| 4     | Deletar tarefa   | `DeletarTarefa`   |
| 0     | Sair             | —                 |

---


# 10. Funcionamento do servidor

As tarefas são armazenadas em memória através de um dicionário:

```python
tarefas = {}
```

Cada tarefa recebe um identificador único utilizando UUID:

```python
id_tarefa = str(uuid.uuid4())
```

A estrutura é mantida enquanto o servidor estiver em execução.

> **Importante:** atualmente as tarefas não estão sendo salvas em banco de dados. Ao desligar ou reiniciar o servidor, as tarefas armazenadas em memória serão perdidas.

---

# 11. Parando as máquinas virtuais

Quando terminar os testes, saia das VMs:

```bash
exit
```

Depois, no terminal do computador:

```bash
vagrant halt
```

Isso irá desligar as três máquinas virtuais.

Para iniciar novamente:

```bash
vagrant up
```

---

# 12. Removendo as máquinas virtuais

Caso seja necessário destruir as máquinas:

```bash
vagrant destroy
```

Para confirmar a destruição:

```text
y
```

Depois elas podem ser recriadas novamente com:

```bash
vagrant up
```

---

# 13. Problemas comuns

## `ModuleNotFoundError: No module named 'tarefas_pb2'`

Certifique-se de executar o projeto a partir da pasta correta:

```bash
cd /vagrant
```

E utilize:

```bash
PYTHONPATH=/vagrant python3 server/server.py
```

ou, no cliente:

```bash
PYTHONPATH=/vagrant python3 client/client.py
```

---

## Cliente não consegue conectar ao servidor

Verifique se o servidor está em execução.

No servidor:

```bash
ss -lntp | grep 50051
```

Também teste a rede no cliente:

```bash
ping 192.168.56.10
```

Se o `ping` funcionar e o servidor estiver escutando na porta `50051`, o cliente deverá conseguir estabelecer a conexão gRPC.

---


# 👨‍💻 Autores

**Vinicius Lemos de Carvalho**
**Gabriel Martins de Brito**
**Rafael Hernanni Medeiros Silva**

---
