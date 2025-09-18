
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
















.
├─ airflow/
│  ├─ dags/                # DAGs do Airflow
│  ├─ plugins/             # (opcional) hooks/operators/sensors custom
│  └─ logs/                # logs compartilhados webserver/scheduler
├─ data/                   # dados de entrada/saída (montado no container)
│  └─ raw/                 # fontes brutas (ex.: CSVs)
│  └─ processed/           # artefatos intermediários/exports
├─ spark_processing/       # código de transformação/feature engineering
│  ├─ __init__.py
│  ├─ feature_engineering.py
│  └─ utils.py
├─ connections/            # conexões/clients (redis, db), SEM segredos
│  ├─ __init__.py
│  └─ redis_client.py
├─ tests/
│  ├─ unit/                # testes unitários puros (sem serviços externos)
│  └─ integration/         # integração leve (mocks/fixtures)
├─ configs/                # yaml/json com params (schemas, paths, env)
│  └─ settings.yaml
├─ infra/                  # docker, compose, CI, scripts de setup
│  ├─ Dockerfile
│  └─ docker-compose.yml
├─ .github/workflows/      # CI (lint + tests)
├─ requirements.txt
├─ README.md
└─ .gitignore






docker compose down

# start

1. 
docker compose up --build

2. 
http://localhost:8080/home

usuario: airflow
senha: airflow

3. start dag



# teste unitarios
docker compose exec airflow-webserver bash -lc "pytest -q /opt/airflow/tests"

ou 

pytest -q tests




# visualizacao dos dados no redis
docker-compose exec redis redis-cli --scan

resultado
"Rio de Janeiro"
"S\xc3\xa3o Paulo"
"Belo Horizonte"






python -m venv venv 
call venv\Scripts\activate

pytest -q tests









teste unitario
- teste de cada funcao

