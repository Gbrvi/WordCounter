# Distributed Word Counter com ZeroMQ 🚀

Este projeto é uma implementação de um sistema distribuído para contagem de palavras em arquivos de texto. Ele demonstra o poder do processamento paralelo utilizando **Python** e a biblioteca **ZeroMQ** (ØMQ) através do padrão de arquitetura **Router-Dealer**.

O sistema simula um comportamento estilo *MapReduce*, onde um nó mestre divide o trabalho e múltiplos nós trabalhadores processam partes do arquivo simultaneamente.

## 📋 Funcionalidades

- **Particionamento de Dados:** O servidor fragmenta automaticamente um arquivo de texto grande em pedaços menores (*chunks*).
- **Distribuição de Tarefas:** Utiliza Sockets `ROUTER` para gerenciar conexões assíncronas com múltiplos workers.
- **Processamento Paralelo:** Workers (`DEALER`) processam os dados de forma independente.
- **Agregação:** O servidor consolida os resultados parciais e exibe o total final.
- **Métricas:** Medição de tempo de I/O (disco) vs. tempo de processamento distribuído (rede/CPU).

## 🛠️ Tecnologias

- [Python 3.14]
- [PyZMQ]
- Bibliotecas nativas: `os`, `time`, `sys`

## 📦 Instalação

Certifique-se de ter o Python instalado. Em seguida, instale a dependência do ZeroMQ:

```bash
pip install pyzmq
```

## ⚙️ Arquitetura

O sistema implementa um pipeline de processamento distribuído inspirado no modelo MapReduce, dividido em três etapas críticas:


- **Split (Divisão)**: O server.py lê o arquivo de entrada (file.txt) e cria 30 arquivos temporários na pasta "/chunks".
- **Map:** O Server aguarda conexões na porta 6000
- **Conexão**: Workers se conectam e enviam um sinal READY
- **Envio:** O Server envia o conteúdo de um chunk para o Worker.
- **Reduce:** O Worker conta as palavras e devolve o valor..
- **Agrupamento:** O Server soma ao total global.
