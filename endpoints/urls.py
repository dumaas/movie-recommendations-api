from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import (
    EndpointViewset, MLAlgorithmViewset,
    MLAlgorithmStatusViewset, MLRequestViewset,
    PredictView
)

router = DefaultRouter(trailing_slash=False)
router.register("endpoints", EndpointViewset, basename="endpoints")
router.register("mlalgorithms", MLAlgorithmViewset, basename="mlalgorithms")
router.register("mlalgorithmstatuses", MLAlgorithmStatusViewset, basename="mlalgorithmstatuses")
router.register("mlrequests", MLRequestViewset, basename="mlrequests")

urlpatterns = [
    url("", include(router.urls)),
    url("(?P<endpoint_name>.+)/predict$", PredictView.as_view(), name="predict"),
]
