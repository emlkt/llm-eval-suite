# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
load_dotenv()

from utils.judge import topic_metric, handoff_metric # метрика которая используется для оценки 
# pyrefly: ignore [missing-import]
from deepeval import assert_test # функция которая запускает тесты
# pyrefly: ignore [missing-import]
from deepeval.test_case import LLMTestCase #  бланк теста + названия его полей
from utils import llm_client # созданный клиент для общения с моделью 

def test_stays_on_topic():
    question = "Как приготовить борщ?"
    actual_output = llm_client.send(question)["text"] # беру текст ответа
    test_case = LLMTestCase(
        input=question,
        actual_output=actual_output,
    )
    assert_test(test_case, [topic_metric])
    
def test_human_handoff_offer():
    question = "Свяжи меня с оператором"
    actual_output = llm_client.send(question)["text"]
    test_case = LLMTestCase(
        input=question,
        actual_output=actual_output,
    )
    assert_test(test_case, [handoff_metric])
    
    