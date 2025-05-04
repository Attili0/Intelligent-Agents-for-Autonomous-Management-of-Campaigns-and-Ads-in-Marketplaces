from typing import Dict, List
from autogen import ConversableAgent
import sys
import os
import re
import math

def fetch_restaurant_data(restaurant_name: str) -> Dict[str, List[str]]:
    """Recupera avaliações de um restaurante a partir de restaurantes.txt."""
    reviews = {}
    try:
        with open("restaurantes.txt", "r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    # Divide a linha no primeiro ponto para separar o nome do restaurante
                    parts = line.split(".", 1)
                    if len(parts) == 2:
                        name, review_text = parts
                        name = name.strip()
                        # Divide o texto restante em avaliações separadas
                        review_sentences = [s.strip() for s in review_text.split(".") if s.strip()]
                        if name not in reviews:
                            reviews[name] = []
                        reviews[name].extend(review_sentences)
    except FileNotFoundError:
        return {"error": "Arquivo restaurantes.txt não encontrado."}

    if restaurant_name in reviews:
        return {restaurant_name: reviews[restaurant_name]}
    return {"error": f"Restaurante {restaurant_name} não encontrado."}

def calculate_overall_score(restaurant_name: str, food_scores: List[int], customer_service_scores: List[int]) -> Dict[str, float]:
    """Calcula a pontuação geral do restaurante com base nas pontuações de comida e serviço."""
    if not food_scores or not customer_service_scores or len(food_scores) != len(customer_service_scores):
        return {restaurant_name: 0.000}
    
    N = len(food_scores)
    total = sum(math.sqrt(f * f * s) for f, s in zip(food_scores, customer_service_scores))
    score = total * (1 / (N * math.sqrt(125))) * 10
    return {restaurant_name: round(score, 3)}

def analyze_reviews(reviews: List[str]) -> tuple:
    """Converte avaliações em pontuações de comida e serviço."""
    score_map = {
        "horrível": 1, "nojento": 1, "terrível": 1,
        "ruim": 2, "desagradável": 2, "ofensivo": 2,
        "mediano": 3, "sem graça": 3, "irrelevante": 3,
        "bom": 4, "agradável": 4, "satisfatório": 4,
        "incrível": 5, "impressionante": 5, "surpreendente": 5
    }
    
    food_scores = []
    customer_service_scores = []
    
    for review in reviews:
        sentences = re.split(r"[.,;!?]\s*", review.lower())
        food_score = 3  # Default to 3
        service_score = 3  # Default to 3
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            is_food = any(word in sentence for word in ["comida", "prato", "sabor", "qualidade", "ingredientes"])
            is_service = any(word in sentence for word in ["atendimento", "serviço", "garçom", "equipe", "funcionário"])
            
            for adj, score in score_map.items():
                if adj in sentence:
                    if is_food:
                        food_score = score
                    if is_service:
                        service_score = score
        
        food_scores.append(food_score)
        customer_service_scores.append(service_score)
    
    return food_scores, customer_service_scores

def get_data_fetch_agent_prompt(restaurant_query: str) -> str:
    """Gera o prompt para o agente de busca de dados."""
    return f"Por favor, obtenha as avaliações do restaurante {restaurant_query} chamando a função fetch_restaurant_data."

def main(user_query: str):
    entrypoint_agent_system_message = "Você é um assistente útil que processa consultas de usuários sobre avaliações de restaurantes e coordena outros agentes para fornecer uma resposta."
    llm_config = {
        "config_list": [{
            "model": "gpt-4o-mini",
            "api_key": os.environ.get("OPENAI_API_KEY")
        }]
    }
    
    # Agente principal de entrada
    entrypoint_agent = ConversableAgent(
        "entrypoint_agent", 
        system_message=entrypoint_agent_system_message, 
        llm_config=llm_config
    )
    entrypoint_agent.register_for_llm(name="fetch_restaurant_data", description="Obtém as avaliações de um restaurante específico.")(fetch_restaurant_data)
    entrypoint_agent.register_for_execution(name="fetch_restaurant_data")(fetch_restaurant_data)

    # Agente de busca de dados
    data_fetch_agent = ConversableAgent(
        "data_fetch_agent",
        system_message="Você é responsável por buscar avaliações de restaurantes com base na consulta do usuário.",
        llm_config=llm_config
    )
    data_fetch_agent.register_for_llm(name="fetch_restaurant_data", description="Obtém as avaliações de um restaurante específico.")(fetch_restaurant_data)
    data_fetch_agent.register_for_execution(name="fetch_restaurant_data")(fetch_restaurant_data)
    
    # Agente de análise de avaliações
    review_analysis_agent = ConversableAgent(
        "review_analysis_agent",
        system_message="Você analisa avaliações de restaurantes e converte elas em pontuações numéricas para comida e serviço.",
        llm_config=llm_config
    )
    
    # Agente de cálculo de pontuação
    score_agent = ConversableAgent(
        "score_agent",
        system_message="Você calcula a pontuação geral de um restaurante com base nas pontuações de comida e serviço e fornece uma resposta amigável ao usuário.",
        llm_config=llm_config
    )
    score_agent.register_for_llm(name="calculate_overall_score", description="Calcula a pontuação geral de um restaurante.")(calculate_overall_score)
    score_agent.register_for_execution(name="calculate_overall_score")(calculate_overall_score)
    
    # Extrair o nome do restaurante da consulta
    patterns = [
        r"Quão bom é o restaurante (.*?)\?",
        r"Qual é a avaliação média do (.*?)\?"
    ]
    restaurant_name = None
    for pattern in patterns:
        match = re.search(pattern, user_query, re.IGNORECASE)
        if match:
            restaurant_name = match.group(1).strip()
            break
    
    if not restaurant_name:
        print("Nome do restaurante não identificado na consulta.")
        return
    
    # Fluxo de conversação
    chat_results = entrypoint_agent.initiate_chats([
        {
            "recipient": data_fetch_agent,
            "message": get_data_fetch_agent_prompt(restaurant_name),
            "max_turns": 1,
            "summary_method": "last_msg"
        },
        {
            "recipient": review_analysis_agent,
            "message": lambda context: f"Analise as seguintes avaliações do {restaurant_name}: {context['chat_history'][0]['content']}",
            "max_turns": 1,
            "summary_method": "last_msg"
        },
        {
            "recipient": score_agent,
            "message": lambda context: f"Calcule a pontuação geral do {restaurant_name} com base nas pontuações de comida e serviço: {context['chat_history'][1]['content']}",
            "max_turns": 1,
            "summary_method": "last_msg"
        }
    ])
    
    # Processar resultados
    reviews_dict = fetch_restaurant_data(restaurant_name)
    if "error" in reviews_dict:
        print(reviews_dict["error"])
        return
    
    reviews = reviews_dict[restaurant_name]
    food_scores, service_scores = analyze_reviews(reviews)
    score_dict = calculate_overall_score(restaurant_name, food_scores, service_scores)
    score = score_dict[restaurant_name]
    
    print(f"A avaliação média do {restaurant_name} é {score:.3f}.")

if __name__ == "__main__":
    assert len(sys.argv) > 1, "Certifique-se de incluir uma consulta para algum restaurante ao executar a função main."
    main(sys.argv[1])