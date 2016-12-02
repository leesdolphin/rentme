



def default_model_builder(name, response):
    this_module = default_model_builder.__module__
    model_class = getattr(this_module, name)
    return model_class.build_from_response(response,
                                           model_builder=default_model_builder)


class ModelRegistry():

    def __init__(self):
        self.models = {}
        self.model_instances = {}

    def register(self, name):
        pass
