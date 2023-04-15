import atexit
import json
import os
import subprocess

from xai_components.base import InArg, InCompArg, OutArg, Component, xai_component

output_func_registered = False
output_vals = {}


def output_func():
    print(json.dumps(output_vals))


@xai_component
class XircuitOutput(Component):
    """
    This component is used to output the results of the Xircuit that
    can then be read from the calling parent Xircuit file.

    Note that things will be output as json.

    :param name: The name of the key to add to the output dict.
    :param value: The value to add to the output dict.
    """

    name: InCompArg[str]
    value: InCompArg[any]

    def execute(self, ctx) -> None:
        global output_func_registered
        global output_vals

        output_vals[self.name.value] = self.value.value

        if not output_func_registered:
            output_func_registered = True
            atexit.register(output_func)


@xai_component
class SetDictValue(Component):
    """
    This component is used to set a value in a dict.
    """
    dict: InArg[dict]
    key: InArg[str]
    value: InArg[any]

    def execute(self, ctx) -> None:
        self.dict.value[self.key.value] = self.value.value


@xai_component
class GetDictValue(Component):
    """
    This component is used to get a value from a dict.
    """
    dict: InArg[dict]
    key: InArg[str]
    value: OutArg[any]

    def execute(self, ctx) -> None:
        self.value.value = self.dict.value[self.key.value]


@xai_component
class InvokeXircuitsFile(Component):
    """
    This component is used to invoke a xircuits file.
    """
    file_name: InArg[str]
    in_args: InArg[dict]
    outputs: OutArg[dict]

    def execute(self, ctx) -> None:
        print(f"Running xircuits file: {self.file_name.value}")

        python_file = self.file_name.value.replace(".xircuits", ".py")
        compile_cmd = ["xircuits-compile", self.file_name.value, python_file]
        result = subprocess.run(
            " ".join(compile_cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
            cwd=os.getcwd()
        )
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            raise Exception(f"Error compiling xircuits file: {self.file_name.value}")

        args = []
        if self.in_args.value is not None:
            for k, v in self.in_args.value.items():
                args.append(f"--{k}={v}")

        cmd = ["python", python_file, *args]

        proc = subprocess.Popen(
            " ".join(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
            cwd=os.getcwd()
        )

        output = []
        for line in iter(proc.stdout.readline, ""):
            print(line.strip())
            output.append(line.strip())
        err = []
        for line in iter(proc.stderr.readline, ""):
            err.append(line.strip())

        proc.stdout.close()
        proc.wait()

        if proc.returncode != 0:
            print("\n".join(output))
            print("\n".join(err))
            raise Exception(f"Error running xircuits file: {self.file_name.value}")
        if len(output) > 0 and output[-1].startswith("{"):
            self.outputs.value = json.loads(output[-1])
