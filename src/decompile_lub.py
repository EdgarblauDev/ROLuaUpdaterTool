from os import path
from shutil import which
from subprocess import Popen

UNLUAC_PATH = path.normpath('.\\tools\\unluac.jar')


class JavaNotFoundException(Exception):
    """JavaNotFoundException

    :requires: Java installed - Tested with OpenJDK 11.
    """
    pass


def decompile_lub(file: str, output_file: str) -> str:
    """Decompiles a LUB file using unluac

    :requires: Java installed - Tested with OpenJDK 11.
    """

    try:
        # recreate the file path
        file = path.normpath(file)

        # check if the user have Java Installed (method could be tricky)
        is_installed = which("java")
        if is_installed is None:
            raise JavaNotFoundException(
                'Java is not installed. Install OpenJDK 11 at least.')

        # check if the file exists
        if not path.isfile(file):
            raise FileNotFoundError(file)

        output = None

        # call the subprocess to execute the utility to decompile the file
        with Popen(f"java -jar {UNLUAC_PATH} {file} > {output_file} --rawstring", shell=True) as util_exec:
            output = util_exec.wait()

        # check if the output is 0 (no errors)
        if output == 0:
            return output_file

        return None

    except Exception:
        return None
