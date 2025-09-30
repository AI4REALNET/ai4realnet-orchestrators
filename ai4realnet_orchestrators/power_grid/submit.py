import json
import os
from uuid import UUID

from ai4realnet_orchestrators.power_grid.test_runner_kpi_cf_012_power_grid import TestRunner_KPI_CF_012_Power_Grid
from fab_clientlib import DefaultApi, ApiClient, Configuration, SubmissionsPostRequest, ResultsSubmissionsSubmissionIdTestsTestIdsPostRequest, \
  ResultsSubmissionsSubmissionIdTestsTestIdsPostRequestDataInner
from fab_oauth_utils import backend_application_flow


def _get_fab():
  FAB_API_URL = os.environ.get("FAB_API_URL", "https://ai4realnet-int.flatland.cloud:8000")
  CLIENT_ID = os.environ.get("CLIENT_ID", 'ai4realnet-client-credentials')
  CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
  TOKEN_URL = os.environ.get("TOKEN_URL", "https://keycloak.flatland.cloud/realms/flatland/protocol/openid-connect/token")
  token = backend_application_flow(CLIENT_ID, CLIENT_SECRET, TOKEN_URL)
  print(token)
  fab = DefaultApi(ApiClient(configuration=Configuration(host=FAB_API_URL, access_token=token["access_token"])))
  return fab


# https://stackoverflow.com/questions/36588126/uuid-is-not-json-serializable
class UUIDEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, UUID):
      # if the obj is uuid, we simply return the value of uuid
      return obj.hex
    return json.JSONEncoder.default(self, obj)


def _pretty_print(submissions):
  print(json.dumps(submissions.to_dict(), indent=4, cls=UUIDEncoder))


if __name__ == '__main__':
  submission_name = "something"
  fab = _get_fab()
  _pretty_print(fab.health_live_get())
  # test_runner = _get_test_runner(test)
  test_runner = TestRunner_KPI_CF_012_Power_Grid(
    test_id="ab91af79-ffc3-4da7-916a-6574609dc1b6", scenario_ids=['75d20248-740b-4d84-86e7-1de89f10fc1e'], benchmark_id="4b0be731-8371-4e4e-a673-b630187b0bb8"
  )
  benchmark_id = test_runner.benchmark_id
  test_id = test_runner.test_id

  submitted = fab.submissions_post(
    SubmissionsPostRequest(
      benchmark_id=benchmark_id,
      name=submission_name,
      # TODO use versioned dependency instead of latest
      submission_data_url="ghcr.io/flatland-association/flatland-baselines:latest",
      test_ids=[test_id])
  )

  _pretty_print(submitted)

  submission_id = submitted.body.id

  fab.results_submissions_submission_id_tests_test_ids_post(
    submission_id=submission_id,
    test_ids=[test_id],
    results_submissions_submission_id_tests_test_ids_post_request=ResultsSubmissionsSubmissionIdTestsTestIdsPostRequest(
      data=[
        ResultsSubmissionsSubmissionIdTestsTestIdsPostRequestDataInner(
          scenario_id=scenario_id,
          scores=test_runner.run_scenario(scenario_id, submission_id),
        )
        for scenario_id in test_runner.scenario_ids
      ]
    ),
  )

  fab.results_submissions_submission_ids_get(submission_ids=[submission_id])
  results = fab.results_submissions_submission_ids_get([submission_id])
  print(results)
