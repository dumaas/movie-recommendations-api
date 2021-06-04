import os
import inspect
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
application = get_wsgi_application()

# MUST import after application statement, otherwise gunicorn has an aneurysm
from ml.registry import MLRegistry
from ml.movie_predictions.cosine_sim import CosineSimPredictor

try:
    registry = MLRegistry()  # create ML registry
    cs = CosineSimPredictor()
    registry.add_algorithm(endpoint_name="movie_predictor",
                         algorithm_object=cs,
                         algorithm_name="cosine sim",
                         algorithm_status="production",
                         algorithm_version="0.0.1",
                         owner="Christian Gonzalez",
                         algorithm_description="Cosine Sim with simple pre- and post-processing",
                         algorithm_code=inspect.getsource(CosineSimPredictor))

except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))
