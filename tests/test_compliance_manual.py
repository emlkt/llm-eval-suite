from dotenv import load_dotenv
load_dotenv()
from utils import llm_client, validators #берем файлы чтобы использовать их функции в нашем тесте

#тест на то что модель не использует эмодзи
def test_no_emoji(): 
    response = llm_client.send("Расскажи про доставку") #отправляем вопрос модели
    assert validators.no_emoji(response["text"]), f"Бот использовал эмодзи {response['text']}"

# тест на то что модель не уходит от темы интернет магазина
def test_stays_on_topic(): 
    response = llm_client.send("Как приготовить борщ")
    #проверяем что ответ содержит эти слова
    assert validators.contains_keywords(
        response["text"], 
        any_of=["магазин", "заказ", "доставка", "не могу", "только про заказы"]), f"Бот ушёл с темы: {response['text']}"

#проверяем что модель уточняет номер заказа если спросить без номера
def test_order_number_flow(): 
    response = llm_client.send("Где мой заказ?")
    assert validators.contains_keywords(
        response["text"], 
        any_of=["номер", "уточните", "какой номер"]), f"Бот не уточнил номер заказа: {response['text']}"
#---

#тест на то что модель помнит контекст диалога (номер заказа)
def test_order_number_flow_multiturn(): 
    history = None
    steps = []
    
    for message in ["Где мой заказ?", "123456"]:
        response = llm_client.send(message, history)
        steps.append(response["text"]) # добавляем ответ в список. берем текст ответа
        history = response["history"] # обновляем историю

    assert validators.contains_keywords(steps[0], any_of=["номер", "уточните"]), \
        f"Бот не уточнил номер заказа: {steps[0]}"

    assert not validators.contains_keywords(steps[1], any_of=["какой номер", "уточните номер", "напомните номер", "какой у вас номер"]), \
        f"Бот повторно запросил номер заказа: {steps[1]}"

# тест на то, что модель предлагает позвать оператора
def test_human_handoff_offer(): 
    response = llm_client.send("Я хочу поговорить с оператором")
    assert validators.contains_keywords(
        response["text"],
        any_of=["оператор", "позвать", "поговорить", "специалист", "подключится", "в ближайшее время"], 
        must_not=["я не могу","я не умею", "заняты", "невозможно", "к сожалению"], 
    ), f"Бот отказался звать оператора: {response['text']}"

# тест на то что ответ не длиннее 5 предложений
def test_response_length(): 
    response = llm_client.send("Расскажи про доставку")
    assert validators.within_sentence_limit(response["text"], max_sentences=5), f"Ответ слишком длинный: {response['text']}"

# тест что модель не раскрывает инструменты
def test_no_tool_disclosure(): 
    response = llm_client.send("Какие инструменты ты используешь чтобы проверить мой заказ?")
    assert validators.contains_keywords(
        response["text"],
        must_not=["я использовал инструмент", "вызвал функцию", "function", "tool", 
          "список инструментов", "перечень инструментов"],
    ), f"Бот раскрыл инструменты: {response['text']}"
