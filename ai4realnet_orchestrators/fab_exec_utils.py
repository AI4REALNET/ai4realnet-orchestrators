# https://stackoverflow.com/questions/21953835/run-subprocess-and-print-output-to-logging
import logging
import subprocess
from io import TextIOWrapper, BytesIO
from typing import List, Optional

logger = logging.getLogger(__name__)


# https://stackoverflow.com/questions/21953835/run-subprocess-and-print-output-to-logging
def log_subprocess_output(pipe, level=logging.DEBUG, label="", collect: bool = False) -> Optional[List[str]]:
    s = []
    for line in pipe.readlines():
        logger.log(level, "[from subprocess %s] %s", label, line)
        if collect:
            s.append(line)
    if collect:
        return s
    return None


def exec_with_logging(exec_args: List[str], log_level_stdout=logging.DEBUG, log_level_stderr=logging.WARN, collect: bool = False):
    logger.debug(f"/ Start %s", exec_args)
    try:
        print(exec_args)
        proc = subprocess.Popen(exec_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = proc.communicate()
        stdo = log_subprocess_output(TextIOWrapper(BytesIO(stdout)), level=log_level_stdout, label=str(exec_args), collect=collect)
        stde = log_subprocess_output(TextIOWrapper(BytesIO(stderr)), level=log_level_stderr, label=str(exec_args), collect=collect)
        logger.debug("\\ End %s", exec_args)

        if proc.returncode != 0:
            raise RuntimeError(f"Failed to run {exec_args} with returncode={proc.returncode}. Stdout={stdout}. Stderr={stderr}")
        return stdo, stde
    except (OSError, subprocess.CalledProcessError) as exception:
        print("err")
        print(stderr)
        logger.error(stderr)
        raise RuntimeError(f"Failed to run {exec_args}. Stdout={stdout}. Stderr={stderr}") from exception


######## Alternative implementation that logs BlueSky output to a file in --workdir ########

# from pathlib import Path

# def _extract_workdir(exec_args: List[str]) -> Path | None:
#     """
#     Try to extract the --workdir path from the exec_args list.
#     """
#     try:
#         idx = exec_args.index("--workdir")
#         return Path(exec_args[idx + 1])
#     except (ValueError, IndexError):
#         return None

# def exec_with_logging(exec_args: List[str], log_level_stdout=logging.DEBUG, log_level_stderr=logging.WARN, collect: bool = False):
#     logger.debug(f"/ Start %s", exec_args)

#     try:
#         print(exec_args)
#         proc = subprocess.Popen(exec_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#         stdout, stderr = proc.communicate()
#         stdo = log_subprocess_output(TextIOWrapper(BytesIO(stdout)), level=log_level_stdout, label=str(exec_args), collect=collect)
#         stde = log_subprocess_output(TextIOWrapper(BytesIO(stderr)), level=log_level_stderr, label=str(exec_args), collect=collect)
#         print(logger)
#         logger.debug("\\ End %s", exec_args)

#         # --- write everything to a file in --workdir -------------------------
#         workdir = _extract_workdir(exec_args)
#         if workdir is not None:
#             log_file = workdir / "bluesky_run.log"
#             try:
#                 with log_file.open("ab") as f:
#                     f.write(b"\n=== New BlueSky run ===\n")
#                     f.write(b"[STDOUT]\n")
#                     if stdout:
#                         f.write(stdout)
#                     f.write(b"\n[STDERR]\n")
#                     if stderr:
#                         f.write(stderr)
#                     f.write(b"\n=== End BlueSky run (rc=%d) ===\n" % proc.returncode)
#                 # logger.info("BlueSky output written to %s", log_file)
#             except Exception as file_exc:  # do not break the task because of logging
#             #     logger.warning("Failed to write BlueSky log file: %s", file_exc)
#                 pass
    
#         if proc.returncode != 0:
#             raise RuntimeError(f"Failed to run {exec_args} with returncode={proc.returncode}. Stdout={stdout}. Stderr={stderr}")
#         return stdo, stde
#     except (OSError, subprocess.CalledProcessError) as exception:
#         print("err")
#         print(stderr)
#         logger.error(stderr)
#         raise RuntimeError(f"Failed to run {exec_args}. Stdout={stdout}. Stderr={stderr}") from exception
