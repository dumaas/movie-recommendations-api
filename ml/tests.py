from django.test import TestCase
import inspect

from .registry import MLRegistry
from .movie_predictions.cosine_sim import CosineSimPredictor


class MLTests(TestCase):
    def test_rf_algorithm(self):
        input_data = {'tmdbId': 1873}  # tmdbId for 'The Dark Knight'
        my_alg = CosineSimPredictor()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        self.assertTrue('movies' in response)

    def test_registry(self):
        registry = MLRegistry()
        self.assertEqual(len(registry.endpoints), 0)
        endpoint_name = "cosine_sim_predictor"
        algorithm_object = CosineSimPredictor()
        algorithm_name = "Cosine Sim"
        algorithm_status = "production"
        algorithm_version = "0.0.1"
        algorithm_owner = "Christian Gonzalez"
        algorithm_description = "Cosine Sim with simple post-processing"
        algorithm_code = inspect.getsource(CosineSimPredictor)
        # add to registry
        registry.add_algorithm(endpoint_name, algorithm_object, algorithm_name,
                    algorithm_status, algorithm_version, algorithm_owner,
                    algorithm_description, algorithm_code)
        # there should be one endpoint available
        self.assertEqual(len(registry.endpoints), 1)
