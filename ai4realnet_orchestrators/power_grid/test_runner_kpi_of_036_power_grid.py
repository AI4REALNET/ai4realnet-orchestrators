from ai4realnet_orchestrators.power_grid.power_grid_test_runner import PowerGridTestRunner
from grid2evaluate.agent_runnner import AgentRunner
from grid2evaluate.operation_score_kpi import OperationScoreKpi
from pathlib import Path
import os


class TestRunner_KPI_OF_036_Power_Grid(PowerGridTestRunner):

  def run_scenario(self, scenario_id: str, submission_id: str):
    # here you would implement the logic to run the test for the scenario:
    scenario_data = PowerGridTestRunner.load_scenario_data(scenario_id)
    input_directory=Path(scenario_data['scenario_base_path'], self.submission_data[scenario_id]['scenario_name'])
    record_directory=Path(scenario_data['scenario_recorder_path'], self.submission_data[scenario_id]['scenario_name'])

    if not os.path.exists(record_directory):
        os.makedirs(record_directory)

    agent_runner = AgentRunner()
    agent_runner.run(input_directory, record_directory)

    kpi = OperationScoreKpi()
    kpi_result = kpi.evaluate(record_directory)
    n_redispatch = kpi_result[1]
    e_redipatch = kpi_result[2]
    e_balancing = kpi_result[3]
    n_curtailment = kpi_result[4]
    e_curtailment = kpi_result[5]
    e_losses = kpi_result[6]
    e_blackout = kpi_result[7]
    primary_kpi_value = (e_redipatch / n_redispatch) + e_balancing + (e_curtailment / n_curtailment) + e_losses + e_blackout

    return {
      "primary": primary_kpi_value
    }


