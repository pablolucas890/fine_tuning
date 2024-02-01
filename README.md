# fine_tuning
Este repositório contém todos os códigos para a criação do Fine Tuning de modelos da OpenAI.

## Por padrão, está sendo usados os seguintes programas e versões:
openai 1.4.0
pip 22.3.1 
python 3.9.13

## O código request_api_chatgpt.py necessitou de atualizações nos programas mencionados e agora usa as seguintes versões:
openai 1.6.1
pip 23.3.2 
python 3.9.13(mantive essa versão)

# cfg File
```
{
  "org" : "org",
  "key" : "key",
  "suffix" :  "teste_pablo",
  "model": "gpt-3.5-turbo-0613"
}
```

### passo a passo

- Selecionei as páginas que contém os objetivos no plano antigo
- Converti para texto
- Coloque no training removendo ", ', `, , 
- Coloquei tudo em uma linha usando \n para quebrar

## Exemplo
### Identificar Objetivos:
```json
{"messages": [{"role": "system", "content": "Quando eu pedir para identificar os objetivos do componente de ___componente___ de um plano municipal de saneamento básico, procure no texto temas relacionados a ___componente___ e seus objetivos, geralmente os objetivos vem com tempo para execução (Médio prazo, Longo prazo, etc...), e também vem com investimento, isto é, apresentam valores em milhares ou milhões de reais da quantidade que deve ser gasto"}, {"role": "user", "content": "Você é um engenheiro ambiental e precisa encontrar os objetivos do componente de ___componente___ no plano antigo de ___cidade___ desenvolvido em ___ano___, trecho do plano que contém esta informação: (___trecho___) "}, {"role": "assistant", "content": "Os objetivos de ___componente___ do plano são:\n___objetivos___"}]}
```
### Identificar prazos:
```json
{"messages": [{"role": "system", "content": "Quando eu pedir para identificar os tempo para cumprimento total do objetivo de um determinado componente, procure no texto partes que falem sobre tempo e prazo (Médio prazo, Longo prazo, etc...), geralmente esta informação vem junto com investimento, isto é, apresentam valores em milhares ou milhões de reais da quantidade que deve ser gasto"}, {"role": "user", "content": "Você é um engenheiro ambiental e precisa encontrar o tempo para cumprimento total do objetivo de (___objetivo___) do componente de ___componente___ no plano antigo de ___cidade___ desenvolvido em ___ano___, trecho do plano que contém esta informação: (___trecho___) "}, {"role": "assistant", "content": "Os tempo para cumprimento total deste objetivo é: ___tempo___"}]}
```