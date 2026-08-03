from dotenv import load_dotenv
load_dotenv()

from utils import llm_client, validators
from utils.judge import judge_model
# pyrefly: ignore [missing-import]
from deepeval import assert_test
# pyrefly: ignore [missing-import]
from deepeval.test_case import Turn, ConversationalTestCase # нужно для многошаговых тестов
# pyrefly: ignore [missing-import]
from deepeval.metrics import ConversationalGEval # метрика для многошаговых тестов
# pyrefly: ignore [missing-import]
from deepeval.test_case import MultiTurnParams 
from fixtures.golden_dataset import GOLDEN_DATASET
# pyrefly: ignore [missing-import]
import pytest

@pytest.mark.parametrize("case", GOLDEN_DATASET, ids= lambda x: x["id"]) # тут я использую lambda чтобы передавать case.id в ids
def test_regression(case):
    prompts = case["prompt"] if isinstance(case["prompt"], list) else [case["prompt"]]
    history = None
    for p in prompts:
        response = llm_client.send(p, history)
        history = response["history"]

    turns = [Turn(role=h["role"], content=h["content"] ) for h in history] # тут переписываю историю общения в формате который понимает deepeval

    assert validators.contains_keywords(
        response["text"],
        must = case.get("must_contain"),
        must_not = case.get("must_not_contain"),
        any_of = case.get("any_of")
    ), f"{case['id']} провалена {response['text']}"

    case_metric = ConversationalGEval(
        name=f"Regression Quality - {case['id']}",
        criteria="Оцени, насколько уместно и по существу ответы бота (assistant) отвечают на вопросы клиента (user) в этом диалоге, в контексте поддержки интернет-магазина. Не штрафуй за краткость, если сообщение всего одно.",
        evaluation_params=[MultiTurnParams.CONTENT],
        threshold=case["min_score"] /5,
        model=judge_model,
    )

    test_case = ConversationalTestCase(turns=turns) # turns - содержит в себе то, что было написано пользователем и моделью до этого (история общения)
    assert_test(test_case, [case_metric])
