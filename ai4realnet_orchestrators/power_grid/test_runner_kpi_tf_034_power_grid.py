from ai4realnet_orchestrators.power_grid.power_grid_test_runner import PowerGridTestRunner
from grid2evaluate.agent_runnner import AgentRunner
from grid2evaluate.topological_action_complexity_kpi import TopologicalActionComplexityKpi
from pathlib import Path
import os


class TestRunner_KPI_TF_034_Power_Grid(PowerGridTestRunner):

  def run_scenario(self, scenario_id: str, submission_id: str):
    # here you would implement the logic to run the test for the scenario:
    scenario_data = PowerGridTestRunner.load_scenario_data(scenario_id)
    input_directory=Path(scenario_data['scenario_base_path'], self.submission_data[scenario_id]['scenario_name'])
    record_directory=Path(scenario_data['scenario_recorder_path'], self.submission_data[scenario_id]['scenario_name'])

    if not os.path.exists(record_directory):
        os.makedirs(record_directory)

    agent_runner = AgentRunner()
    agent_runner.run(input_directory, record_directory)

    kpi = TopologicalActionComplexityKpi()
    kpi_result = kpi.evaluate(record_directory)
    avg_topology = kpi_result[2]
    primary_kpi_value = avg_topology

    return {
      "primary": primary_kpi_value
    }

