import argparse
import numpy as np
import qiskit
from qiskit import visualization
from qiskit.circuit.library import QFT
# from qiskit.tools.jupyter.library import _generate_circuit_library_visualization


def main(args):
    num_qubits = args.qubits_size
    name='ft'

    initial_state = [1/np.sqrt(2**num_qubits)] * 2**num_qubits
    qc = qiskit.QuantumCircuit(num_qubits, name=name)
    qc.initialize(initial_state, range(num_qubits))

    qc.append(QFT(num_qubits), range(num_qubits))
    qc.measure_all()

    fig = qc.draw('mpl')
    fig.savefig('./circuit-test2.png')

    simulator = qiskit.Aer.get_backend('statevector_simulator')
    compiled_circuit = qiskit.transpile(
        qc,
        simulator,
        output_name='ft_circuit'
    )
    job = qiskit.execute(compiled_circuit, simulator)
    result = job.result()
    statevector = result.get_statevector()

    vis1 = visualization.plot_bloch_multivector(statevector)
    vis1.savefig('./bloch_multivector-2.png')


    compiled_meas_circuit = qiskit.transpile(
        qc,
        simulator,
        output_name='ft_circuit2'
    )
    job_meas = qiskit.execute(compiled_meas_circuit, simulator, shots=1024)
    result_meas = job_meas.result()
    counts = result_meas.get_counts()

    vis2 = visualization.plot_histogram(counts)
    vis2.savefig('./histogram-2.png')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='What this program is going to do.'
    )
    parser.add_argument(
        '--qubits_size', '-QS', type=int, default=4, help=''
    )
    args = parser.parse_args()

    main(args)