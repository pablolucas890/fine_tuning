# fine_tuning
Este repositório contém todos os códigos para a criação do Fine Tuning de modelos da OpenAI.

## Developement

- Install `python3-openpyxl`
  - sudo ap install `python3-openpyxl`
- Create cfg file at `~/` with:
  ```js
  {
    "org" : "org",
    "key" : "key",
    "suffix" :  "suffix",
    "base_model_to_fine_tune": "gpt-3.5-turbo-0613",
    "model_to_conversation": "ft:gpt-3.5-turbo-0613:personal:teste-pablo:8xFa0aLd",
    "excel_file_path": "data/pmsb_funasa_model.xlsx",
    "tokens_limit": 4096
  }
  ```
- Install python packages
  - `pip3 install -r requirements.txt`

## Training

### To predictive objectives
```json
{"messages": [{"role": "system", "content": "Quando for solicitado para identificar os objetivos do componente de ___componente___ de um plano municipal de saneamento básico, procure no texto temas relacionados a ___componente___ e seus objetivos, geralmente os objetivos vem com tempo para execução (Médio prazo, Longo prazo, etc...), e também vem com investimento, isto é, apresentam valores em milhares ou milhões de reais da quantidade que deve ser gasto"}, {"role": "user", "content": "Você é um engenheiro ambiental e precisa encontrar os objetivos do componente de ___componente___ no plano antigo de ___cidade___ desenvolvido em ___ano___, trecho do plano que contém esta informação: (___trecho___) "}, {"role": "assistant", "content": "___objetivos___"}]}
```
### To predictive deadlines
```json
{"messages": [{"role": "system", "content": "Quando for solicitado para identificar o prazo para cumprimento total do objetivo de um determinado componente, procure no texto partes que falem sobre tempo e prazo (Médio prazo, Longo prazo, etc...), geralmente esta informação vem junto com investimento, isto é, apresentam valores em milhares ou milhões de reais da quantidade que deve ser gasto"}, {"role": "user", "content": "Você é um engenheiro ambiental e precisa encontrar o tempo para cumprimento total do objetivo de (___objetivo___) do componente de ___componente___ no plano antigo de ___cidade___ desenvolvido em ___ano___, trecho do plano que contém esta informação: (___trecho___) "}, {"role": "assistant", "content": "___tempo___"}]}
```
### To predictive actions
```json
{"messages": [{"role": "system", "content": "Quando for solicitado para identificar as ações a serem realizadas a partir de um objetivo de um determinado componente, procure no texto partes que falem sobre ações e que de alguma forma estejam relacionadas ao objetivo que lhe for entregue"}, {"role": "user", "content": "Você é um engenheiro ambiental e precisa encontrar as acções a serem realizadas no objetivo de (___objetivo___) do componente de ___componente___ no plano antigo de ___cidade___ desenvolvido em ___ano___, trecho do plano que contém esta informação: (___trecho___) "}, {"role": "assistant", "content": "___acoes___"}]}
```
### To predictive investiments
```json
{"messages": [{"role": "system", "content": "Quando for solicitado para identificar o investimento previsto para realização de um objetivo de um determinado componente, procure no texto partes que falem sobre investimento, isto é, valores em milhares ou milhões de reais referentes a quantidade que deve ser gasto"}, {"role": "user", "content": "Você é um engenheiro ambiental e precisa encontrar o prazo para cumprimento do objetivo de (___objetivo___) do componente de ___componente___ no plano antigo de ___cidade___ desenvolvido em ___ano___, trecho do plano que contém esta informação: (___trecho___) "}, {"role": "assistant", "content": "___investimento___"}]}
```