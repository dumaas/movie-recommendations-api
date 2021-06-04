from django.db import models


class Endpoint(models.Model):
  '''
  Represents the ML API endpoint

  Attributes:
      name: the name of the endpoint, used in the API url,
      owner: the string with owner name,
      created_at: the data of endpoint creation
  '''
  name = models.CharField(max_length=200)
  owner = models.CharField(max_length=200)
  created_at = models.DateTimeField(auto_now_add=True, blank=True)

  def __str__(self):
    return self.name


class MLAlgorithm(models.Model):
  '''
  Represents the ML algorithm object

  Attributes:
      name: The name of the algorithm.
      description: The short description of how the algorithm works.
      code: The code of the algorithm.
      version: The version of the algorithm similar to software versioning.
      owner: The name of the owner.
      created_at: The date when MLAlgorithm was added.
      parent_endpoint: The reference to the Endpoint.
  '''
  name = models.CharField(max_length=200)
  description = models.CharField(max_length=1000)
  code = models.CharField(max_length=50000)
  version = models.CharField(max_length=200)
  owner = models.CharField(max_length=200)
  created_at = models.DateTimeField(auto_now_add=True, blank=True)
  parent_endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)

  def __str__(self):
    return self.name


class MLAlgorithmStatus(models.Model):
  '''
  Represent status of the MLAlgorithm which can change during the time.

    Attributes:
        status: The status of algorithm in the endpoint. Can be: testing, staging, production, ab_testing.
        active: The boolean flag which point to currently active status.
        created_by: The name of creator.
        created_at: The date of status creation.
        parent_mlalgorithm: The reference to corresponding MLAlgorithm.
  '''
  status = models.CharField(max_length=200)
  active = models.BooleanField()
  created_by = models.CharField(max_length=200)
  created_at = models.DateTimeField(auto_now_add=True, blank=True)
  parent_mlalgorithm = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE, related_name="status")

  def __str__(self):
    return self.parent_mlalgorithm + " status: " + self.status


class MLRequest(models.Model):
  '''
  Keeps information about all requests to ML algorithms.

    Attributes:
        input_data: The input data to ML algorithm in JSON format.
        full_response: The response of the ML algorithm.
        response: The response of the ML algorithm in JSON format.
        feedback: The feedback about the response in JSON format.
        created_at: The date when request was created.
        parent_mlalgorithm: The reference to MLAlgorithm used to compute response.
  '''
  input_data = models.CharField(max_length=10000)
  full_response = models.CharField(max_length=10000)
  response = models.CharField(max_length=10000)
  feedback = models.CharField(max_length=10000, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True, blank=True)
  parent_mlalgorithm = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE)

  def __str__(self):
    return "Request for " + self.parent_mlalgorithm
