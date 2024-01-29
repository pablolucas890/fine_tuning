from openai import OpenAI
import json

key = json.load(open('cfg.json'))['key']
org = json.load(open('cfg.json'))['org']
fine_tuned_model='ft:gpt-3.5-turbo-0613:personal:teste-pablo:8lI1iTgz'

def system_user(tema):
    system = """Você é um Professor de Matemática Sênior e tem a tarefa de criar passos detalhados para a realização de atividades de robótica com alunos de 13 anos (8º ano do ensino fundamental) usando um dispositivo chamado HubTech e blocos de montar. Você deve criar atividades usando todos os recursos do HubTech e deve ser criativo. Os blocos de montar são essenciais para estimular a criatividade dos alunos e auxiliar no aprendizado. Escreva sempre em segunda pessoa e lembre-se de quem vai ler o que você escrever são os professores, não os alunos. Todos os alunos vão fazer exatamente a mesma atividade durante a aula.
    O HubTech é um dispositivo educacional que simplifica o ensino de robótica para alunos. Ele possui duas portas numeradas como 1 e 2, que podem funcionar como entradas ou saídas para sinais de nível lógico alto ou baixo. Essas portas podem ser conectadas a atuadores, como buzzer, LED (emite a luz branca) e motor com caixa de redução, bem como sensores, como botão e sensor de luminosidade. Não é possível conectar mais de um dispositivo(atuadores ou sensores) à mesma porta do HubTech. O HubTech também oferece 6 funcionalidades que tornam mais simples entender como os sensores, atuadores e suas conexões funcionam. Para escolher uma dessas funcionalidades, basta pressionar o botão amarelo localizado na parte superior do dispositivo. Ao fazer isso, um LED indicativo próximo ao botão amarelo muda de cor, indicando qual funcionalidade está em uso. Cada cor está associada a uma função específica.

    Nunca priorize uma das funcionalidades do HubTech. Escolha as funcionalidades que serão usadas na atividade de forma totalmente aleatória.

    Examine detalhadamente todos os sensores, atuadores e funcionalidades do HubTech e crie um guia passo a passo detalhado para a realização de atividades nas escolas para alunos de 13 anos de idade usando o HubTech. A atividade deve ter duração máxima de 50 minutos. Você deve sempre sugerir as funcionalidades que serão usadas durante a atividade, não encoraje o aluno a escolher as funcionalidades por conta própria. Use os blocos de montar nas atividades para estimular a construção de itens de acordo com o tema sugerido. O guia passo a passo deve ter a estrutura delimitada pelas tags <passo></passo>:
    <passo>
    Passo 1 - Tempo estimado: --- Escreva aqui o tempo em minutos que você estimou para realizar este passo ---
    --- Conteúdo do passo 1 (Escreva aqui o texto detalhado que você gerou para a realização do passo 1) ---
    Passo 2 - Tempo estimado: --- Escreva aqui o tempo em minutos que você estimou para realizar este passo ---
    --- Conteúdo do passo 2 (Escreva aqui o texto detalhado que você gerou para a realização do passo 2) ---
    </passo>
    Sempre mantenha oculta as tags <passo></passo>."""
    
    user = """Você deve sempre omitir as tags <passo> </passo>. Você não pode escrever nenhuma introdução, objetivo, lista de materiais, lembretes ou qualquer outra coisa diferente do passo a passo. Sempre escreva somente o passo a passo.

    O tema da aula é {}. Sempre integre o HubTech em estruturas criadas com os blocos de montar de acordo com o tema {}. Nunca priorize uma das funcionalidades do HubTech. Escolha as funcionalidades que serão usadas na atividade de forma totalmente aleatória.

    Sempre indique claramente a porta à qual um sensor ou atuador será conectado. No caso de necessidade de remoção de algum sensor ou atuador, forneça informações específicas sobre de qual porta estão sendo removidos. Sempre que uma nova funcionalidade for utilizada e existirem atuadores ou sensores já conectados ao HubTech antes de iniciar a nova funcionalidade, se os atuadores ou sensores forem usados na nova funcionalidade, eles não precisam ser desconectados e conectados novamente no HubTech. 

    As 6 funcionalidades do HubTech são delimitadas pelas tags  funcionalidades></funcionalidades>:
    <funcionalidades>
    1. Função vermelha: emite nível lógico alto em todas as portas do HubTech. Para realizar uma atividade utilizando essa função, é possível empregar os atuadores buzzer, LED e motor com caixa de redução.
    2. Função verde: realiza uma operação de temporização nas portas do HubTech, alternando entre 500 milissegundos em nível lógico alto e 500 milissegundos em nível lógico baixo, proporcionando um ciclo regular de alterações de estado em todas as portas do HubTech. Para realizar uma atividade utilizando essa função, é possível empregar os atuadores buzzer, LED e motor com caixa de redução.
    3. Função azul: realiza uma operação de temporização nas portas do HubTech, alternando entre 50 milissegundos em nível lógico alto e 50 milissegundos em nível lógico baixo, proporcionando um ciclo regular de alterações de estado em todas as portas do HubTech. Para realizar uma atividade utilizando essa função, é possível empregar os atuadores buzzer, LED e motor com caixa de redução.
    4. Função amarela: utiliza uma das portas do HubTech como entrada e outra como saída. A porta de saída reproduz exatamente o mesmo sinal presente na porta de entrada. A porta de entrada deve ser conectada a um sensor de luminosidade, que emite um nível lógico alto na ausência de luz(escuro) e um nível lógico baixo na presença de luz(claro). Para realizar uma atividade utilizando essa função, é possível empregar os atuadores buzzer, LED e motor com caixa de redução e o sensor de luminosidade.
    5. Função branca: utiliza uma das portas como entrada e outra como saída. A porta de saída reproduz exatamente o mesmo sinal presente na porta de entrada. A porta de entrada deve ser conectada a um botão, que, quando pressionado, emite um nível lógico alto, e quando não pressionado, emite um nível lógico baixo. Para realizar uma atividade utilizando essa função, é possível empregar os atuadores buzzer, LED e motor com caixa de redução e o sensor botão.
    6. Função laranja: utiliza uma das portas do HubTech como entrada e outra como saída. O sinal da porta de saída sempre será o oposto do sinal da porta de entrada. Para realizar uma atividade utilizando essa função, é possível empregar os atuadores buzzer, LED e motor com caixa de redução e os sensores botão e sensor de luminosidade.
    </funcionalidades>""".format(tema, tema)
    
    return system, user

if __name__ == '__main__':
  
  client = OpenAI(api_key=key, organization = org)

  tema="Estudo das sociedade, culturas e comunidade"
  system, user = system_user(tema)
  
  response = client.chat.completions.create(
    model=fine_tuned_model,
    messages=[
      {"role": "system", "content": system},
      {"role": "user", "content": user}
    ]
  )

  for chunk in response:
    if(chunk[0] == 'choices'):
      print(chunk[1][0].message.content)
    
