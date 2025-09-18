
# Introducao do projeto

Este projeto apresenta a minha solução para o desafio proposto.  
O objetivo é implementar um pipeline capaz de ingerir dados brutos de novas empresas, processá-los e disponibilizar **features agregadas** em um sistema de baixa latência para consumo por diferentes serviços.

A arquitetura foi construída utilizando:
- **Airflow** para orquestração das tarefas do pipeline.  
- **Spark (PySpark)** para engenharia de features e processamento dos dados.  
- **Redis** como *feature store online*, um banco NoSQL de baixa latência que permite múltiplos serviços acessarem as mesmas features em tempo real.  
- **CI/CD** para validação do código e execução de testes automatizados.  

Além do que foi solicitado, inclui também uma pasta onde ficam armazenados os **dados processados pelo Spark** (os mesmos que estão disponíveis no Redis), garantindo reprodutibilidade e histórico do processamento.


# Passo a passo




### 1. Suba os containers:
```bash
docker compose up --build
```

### 2. Acesse os serviços:
- **Airflow Webserver**: [http://localhost:8080](http://localhost:8080)  
  - usuário: `airflow`  
  - senha: `airflow`  

###  3. Executar DAG
    - Acesse o Airflow.  
    - Habilite e rode a DAG `features_empresas`.  
    - Aguarde a execução das tasks.


# Validar/Testar
###  Verificar chaves no Redis

```bash
docker-compose exec redis redis-cli --raw --scan
```

Resultado
```
São Paulo
Belo Horizonte
Rio de Janeiro
```


###  Verificar dados de uma chaves no Redis
```bash
docker compose exec redis redis-cli --raw HGETALL "São Paulo"

```
Resultado
```
195000.0
quantidade_empresas
3
capital_social_medio
65000.0
```



# CI/CD

Pipeline de CI implementado com **GitHub Actions**:
- **Linting**: validação de estilo com `flake8/black`.  
- **Testing**: execução de testes unitários com `pytest`.  

Workflow dispara em cada **push** ou **PR**.


# Testes

Na raiz do projeto, teste local:
```bash
pytest -v
```
ou
teste dentro do container
```bash
docker compose exec airflow-webserver bash -lc "pytest -q /opt/airflow/tests"
```




# TODO

1. Criacao do arquivo make
2. Teste de integração
    - Redis
    - Spark