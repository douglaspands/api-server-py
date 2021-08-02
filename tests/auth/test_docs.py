from app.auth import docs


def test_docs_ok():
    assert docs.get_token == {
        'name': 'Get token.',
        'description': 'Get token for system access.',
        'responses': {
            400: {'description': 'Bad request.'},
            401: {'description': 'Unauthorized access.'}
        }
    }
