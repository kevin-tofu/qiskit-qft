import argparse
import numpy as np
import qiskit
from qiskit import visualization


def qft_general(qc, num_qubits):
    for j in range(num_qubits):
        qc.h(j)
        for k in range(j+1, num_qubits):
            qc.cp(2 * np.pi / 2**(k-j+1), k, j)
    for j in range(num_qubits//2):
        qc.swap(j, num_qubits-j-1)
    return qc


def main(args):

    # initialize circuit
    name='ft'
    num_qubits = args.qubits_size
    qc = qiskit.QuantumCircuit(num_qubits, name=name)
    signal = np.ones(2**num_qubits).tolist()
    signal = np.array(signal) / np.linalg.norm(signal)
    qc.initialize(signal, range(num_qubits))

    # define circuit
    ft_circuit = qft_general(qc, num_qubits)
    print(ft_circuit, len(ft_circuit))
    fig = ft_circuit.draw('mpl')
    fig.savefig('./circuit-test1.png')

    # simulate circuit
    simulator = qiskit.Aer.get_backend('statevector_simulator')
    compiled_circuit = qiskit.transpile(
        ft_circuit,
        simulator,
        output_name='ft_circuit'
    )
    job = qiskit.execute(compiled_circuit, simulator)
    result = job.result()

    statevector = result.get_statevector()
    vis1 = visualization.plot_bloch_multivector(statevector)
    vis1.savefig('./bloch_multivector-1.png')

    # measure state vector
    ft_circuit.measure_all()
    compiled_meas_circuit = qiskit.transpile(
        ft_circuit,
        simulator,
        output_name='ft_circuit_m'
    )
    job_meas = qiskit.execute(compiled_meas_circuit, simulator, shots=1024)
    result_meas = job_meas.result()
    counts = result_meas.get_counts()
    vis2 = visualization.plot_histogram(counts)
    vis2.savefig('./histogram-1.png')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='What this program is going to do.'
    )
    parser.add_argument(
        '--qubits_size', '-QS', type=int, default=4, help=''
    )
    args = parser.parse_args()

    main(args)