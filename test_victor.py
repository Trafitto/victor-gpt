from victor import Victor
from constants import OPEN_API_CHAT_URL

mocked_json_response = {'id': 'test-id', 'object': 'chat.completion', 'created': 1684881956, 'model': 'gpt-3.5-turbo-0301', 'usage': {'prompt_tokens': 362, 'completion_tokens': 184, 'total_tokens': 546
                                                                                                                                      }, 'choices': [
    {'message': {'role': 'assistant', 'content': 'test'
                 }, 'finish_reason': 'stop', 'index': 0
     }
]
}


def test_victor(requests_mock, no_threshold=0):
    victor = Victor()

    requests_mock.post(OPEN_API_CHAT_URL, json=mocked_json_response)
    # disable decorator
    response = victor.tells.__wrapped__(
        victor, message="Posso farti una domanda a caso?")
    assert response == 'test'
