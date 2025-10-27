from ai4realnet_orchestrators.power_grid.power_grid_test_runner import PowerGridTestRunner
from grid2evaluate.assistant_alert_accuracy_kpi import AssistantAlertAccuracyKpi
from pathlib import Path

class TestRunner_KPI_AF_008_Power_Grid(PowerGridTestRunner):

  def run_scenario(self, scenario_id: str, submission_id: str):
    # here you would implement the logic to run the test for the scenario:
    scenario_data = PowerGridTestRunner.load_scenario_data(scenario_id)
    input_directory=Path(scenario_data['scenario_base_path'], self.submission_data[scenario_id]['scenario_name'])

    return self.getResult(input_directory)

  def getResult(self, input_directory: Path):
    kpi = AssistantAlertAccuracyKpi()
    kpi_result = kpi.evaluate(input_directory)

    primary_kpi_value = 33 #dummy value

    return {
      "primary": primary_kpi_value
    }
