# Sistema de Avaliação de Restaurantes com Agentes de IA

Este projeto implementa um sistema multi-agentes que processa avaliações de restaurantes para gerar pontuações automáticas. Utilizando o framework [Autogen](https://github.com/microsoft/autogen), o sistema recupera, analisa e pontua avaliações de forma eficiente, permitindo responder a consultas sobre a qualidade de restaurantes com base em avaliações textuais.

## Propósito

O objetivo é criar um sistema automatizado que possa responder a consultas sobre a qualidade de restaurantes, como "Qual é a avaliação média do Bob's?" ou "Quão bom é o restaurante Madero?". Isso é útil para recomendações automáticas e análise de sentimentos em larga escala, simulando um processo que poderia ser utilizado em sistemas de recomendação reais.

## Funcionalidades

- **Recuperação de Avaliações**: Lê e extrai avaliações de um arquivo de texto (`restaurantes.txt`), onde cada linha contém o nome do restaurante seguido por uma ou mais avaliações separadas por pontos.
- **Análise de Sentimentos**: Converte avaliações textuais em pontuações numéricas para comida e serviço, com base em uma lista pré-definida de adjetivos.
- **Cálculo de Pontuação Geral**: Usa uma fórmula específica para calcular uma pontuação final do restaurante, considerando as pontuações de comida e serviço.
- **Suporte a Consultas via Linha de Comando**: Permite que o usuário passe uma consulta como argumento ao executar o script.

## Dependências

- **Python 3.8** ou superior
- **Bibliotecas**:
  - `pyautogen`: Framework para orquestração de agentes de IA.
  - `openai`: Para utilizar o modelo `gpt-4o-mini` (ou outro modelo configurado).
- **Chave de API da OpenAI**: Necessária para acessar os modelos de linguagem.

## Instalação

1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Instale as Dependências**:
   - Crie e ative um ambiente virtual (opcional, mas recomendado):
     ```bash
     python -m venv venv
     source venv/bin/activate  # Linux/Mac
     venv\Scripts\activate     # Windows
     ```
   - Instale as bibliotecas necessárias:
     ```bash
     pip install pyautogen openai
     ```
   - Alternativamente, se houver um `requirements.txt`, use:
     ```bash
     pip install -r requirements.txt
     ```

3. **Configure a Chave de API da OpenAI**:
   - Defina a variável de ambiente `OPENAI_API_KEY`:
     - **Linux/Mac**:
       ```bash
       export OPENAI_API_KEY='sua-chave-aqui'
       ```
     - **Windows (Prompt de Comando)**:
       ```bash
       set OPENAI_API_KEY=sua-chave-aqui
       ```
   - Para configuração permanente, adicione a variável ao seu arquivo de perfil (ex.: `~/.bashrc`, `~/.zshrc`) ou use as configurações do sistema.

4. **Prepare o Arquivo `restaurantes.txt`**:
   - Certifique-se de que o arquivo `restaurantes.txt` está no mesmo diretório que `main.py`.
   - O arquivo deve seguir o formato:
     ```
     <nome_do_restaurante>. <avaliação1>. <avaliação2>. ...
     ```
   - Exemplo:
     ```
     Madero. Comida mediana, mas sem nada marcante. O atendimento é eficiente e os garçons são educados.
     Bob's. Comida mediana, atendimento ruim. Sanduíches satisfatórios, serviço mediano.
     ```

## Uso

Execute o script `main.py` passando uma consulta sobre um restaurante como argumento:

```bash
python main.py "Qual é a avaliação média do Bob's?"
```

Isso deve retornar algo como:

```
A avaliação média do Bob's é 3.790.
```

Outros exemplos de consultas:
- `"Quão bom é o restaurante Madero?"`
- `"Qual é a avaliação média do Paris 6?"`

## Estrutura do Código

O projeto é composto por um único arquivo `main.py`, que contém as seguintes funções principais:

- **`fetch_restaurant_data`**: Recupera as avaliações de um restaurante específico a partir de `restaurantes.txt`.
- **`analyze_reviews`**: Analisa as avaliações textuais e converte adjetivos em pontuações numéricas para comida e serviço, com base em uma escala pré-definida.
- **`calculate_overall_score`**: Calcula a pontuação geral do restaurante usando uma fórmula que combina as pontuações de comida e serviço.
- **`main`**: Orquestra os agentes de IA (usando Autogen) para processar a consulta do usuário, recuperar avaliações, analisá-las e calcular a pontuação final.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE). Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Para mais informações ou dúvidas, visite [meu perfil no GitHub](https://github.com/seu-usuario) ou abra uma issue no repositório.

---

**Nota**: Este README é um modelo e deve ser ajustado com as informações específicas do seu repositório, como o nome de usuário e a licença real, se aplicável.