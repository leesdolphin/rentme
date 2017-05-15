from django.apps import AppConfig

class RentmeDataImporterConfig(AppConfig):

    name = 'rentme.data.importer'
    verbose_name = 'Rentme Data Importer'
    # 
    # @property
    # def models_module(self):
    #     from . import models as importer_models
    #     return importer_models
