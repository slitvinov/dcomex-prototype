from xml.dom.minidom import parse
import os
import subprocess

script_dir = os.path.abspath(os.path.dirname(__file__))

def write_config_file(xcoords, ycoords,
                      parameters: list,
                      filename: str):

    theta1, theta2 = parameters

    with open(filename, "w") as f:
        print("""<MSolve4Korali version="1.0">
	<Mesh>
		<LengthX>1</LengthX>
		<LengthY>1</LengthY>
		<ElementsX>10</ElementsX>
		<ElementsY>10</ElementsY>
	</Mesh>
	<Physics type="Thermal">
		<CommonThickness>1</CommonThickness>
		<Density>1</Density>
		<SpecialHeatCoefficient>1</SpecialHeatCoefficient>
		<Conductivity>1</Conductivity>
		<TemperatureAtBoundaries>0</TemperatureAtBoundaries>
		<HeatSourceMagnitude>10</HeatSourceMagnitude>
		<HeatSourceSpread>0.01</HeatSourceSpread>
	</Physics>
	<Output>""", file=f)

        for x, y in zip(xcoords, ycoords):
            print(f'        <Temperature X="{x}" Y="{y}"/>', file=f)

        print(f"""	</Output>
	<Parameters>
		<Theta1>{theta1}</Theta1>
		<Theta2>{theta2}</Theta2>
	</Parameters>
</MSolve4Korali>""", file=f)


def parse_results(filename: str):
    document = parse(filename)
    x = []
    y = []
    T = []
    for node in document.getElementsByTagName("Temperature"):
        x.append(float(node.getAttribute("X")))
        y.append(float(node.getAttribute("Y")))
        T.append(float(node.childNodes[0].nodeValue))
    return x, y, T



def run_msolve_mock(xcoords, ycoords,
                    generation: int,
                    sample_id: int,
                    parameters: list):

    basedir = os.getcwd()
    run_dir = os.path.join(basedir,
                           f"gen_{str(generation).zfill(6)}",
                           f"sample_{str(sample_id).zfill(6)}")

    os.makedirs(run_dir, exist_ok=True)
    os.chdir(run_dir)

    input_file  = os.path.join(run_dir, "config.xml")
    output_file = os.path.join(run_dir, "result.xml")
    stdout_file = open(os.path.join(run_dir, "stdout.txt"), "w")
    stderr_file = open(os.path.join(run_dir, "stderr.txt"), "w")

    write_config_file(xcoords, ycoords, parameters, input_file)

    subprocess.call(['python3', os.path.join(script_dir, 'msolve_mock.py'),
                     '--input-file', input_file,
                     '--output-file', output_file],
                    stdout=stdout_file, stderr=stderr_file)

    x, y, T = parse_results(output_file)

    os.chdir(basedir)
    return x, y, T



def run_msolve(xcoords, ycoords,
               generation: int,
               sample_id: int,
               parameters: list):

    basedir = os.getcwd()
    run_dir = os.path.join(basedir,
                           f"gen_{str(generation).zfill(6)}",
                           f"sample_{str(sample_id).zfill(6)}")

    os.makedirs(run_dir, exist_ok=True)
    os.chdir(run_dir)

    input_file  = os.path.join(run_dir, "config.xml")
    output_file = os.path.join(run_dir, "result.xml")
    stdout_file = open(os.path.join(run_dir, "stdout.txt"), "w")
    stderr_file = open(os.path.join(run_dir, "stderr.txt"), "w")

    write_config_file(xcoords, ycoords, parameters, input_file)

    msolve_path = os.path.join(script_dir, '..', 'msolve', 'MSolveApp',
                               'ISAAR.MSolve.MSolve4Korali', 'bin', 'Debug', 'net6.0',
                               'ISAAR.MSolve.MSolve4Korali')

    subprocess.call([msolve_path, input_file, output_file],
                    stdout=stdout_file, stderr=stderr_file)

    x, y, T = parse_results(output_file)

    os.chdir(basedir)
    return x, y, T
