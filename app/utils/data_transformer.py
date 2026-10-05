from fastapi_test.app.models.models import CachedData


def transformer_function(data):
    new_data = data["list_1"] + data["list_2"]
    return new_data
