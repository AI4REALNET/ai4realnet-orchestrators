# based on https://github.com/codalab/codabench/blob/develop/compute_worker/compute_worker.py
import logging
import os
import ssl
from typing import List

from celery import Celery

from ai4realnet_orchestrators.orchestrator import Orchestrator
from ai4realnet_orchestrators.energy.energy_runner import EnergyTestRunner

logger = logging.getLogger(__name__)

app = Celery(
  broker=os.environ.get('BROKER_URL'),
  backend=os.environ.get('BACKEND_URL'),
  queue=os.environ.get("BENCHMARK_ID"),
  broker_use_ssl={
    'keyfile': os.environ.get("RABBITMQ_KEYFILE"),
    'certfile': os.environ.get("RABBITMQ_CERTFILE"),
    'ca_certs': os.environ.get("RABBITMQ_CA_CERTS"),
    'cert_reqs': ssl.CERT_REQUIRED
  }
)

your_orchestrator = Orchestrator(
  test_runners={
    "871f3eef-2bf4-4c04-ae6e-b6992581736a": EnergyTestRunner(
      test_id="871f3eef-2bf4-4c04-ae6e-b6992581736a", scenario_ids=['a11501c4-a28f-4b57-8d29-e62c9db35bc9', 'd25f9677-3131-4d03-91c1-82624ca94cc6', '6c7b4616-43df-4858-84a1-630c89c04897']
    ),
  }
)


# https://docs.celeryq.dev/en/stable/userguide/tasks.html#bound-tasks: A task being bound means the first argument to the task will always be the task instance (self).
# https://docs.celeryq.dev/en/stable/userguide/tasks.html#names: Every task must have a unique name.
@app.task(name=os.environ.get("BENCHMARK_ID"), bind=True)
def orchestrator(self, submission_data_url: str, tests: List[str] = None, **kwargs):
  submission_id = self.request.id
  benchmark_id = orchestrator.name
  logger.info(
    f"Queue/task {benchmark_id} received submission {submission_id} with submission_data_url={submission_data_url} for tests={tests}"
  )
  return your_orchestrator.run(
    submission_id=submission_id,
    submission_data_url=submission_data_url,
    tests=tests,
  )
