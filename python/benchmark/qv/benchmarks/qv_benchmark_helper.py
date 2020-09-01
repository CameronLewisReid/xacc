import numpy as np
import xacc

def qv_circuits(qubit_lists=None, ntrials=1,
                qr=None, cr=None):
    """
    Return a list of square quantum volume circuits (depth=width)

    The qubit_lists is specified as a list of qubit lists. For each
    set of qubits, circuits the depth as the number of qubits in the list
    are generated

    Args:
        qubit_lists (list): list of list of qubits to apply qv circuits to. Assume
            the list is ordered in increasing number of qubits
        ntrials (int): number of random iterations
        qr (QuantumRegister): quantum register to act on (if None one is created)
        cr (ClassicalRegister): classical register to measure to (if None one is created)

    Returns:
        tuple: A tuple of the type (``circuits``, ``circuits_nomeas``) wheere:
            ``circuits`` is a list of lists of circuits for the qv sequences
            (separate list for each trial) and `` circuitss_nomeas`` is the
            same circuits but with no measurements for the ideal simulation
    """

    circuits = [[] for e in range(ntrials)]
    circuits_nomeas = [[] for e in range(ntrials)]

    # get the largest qubit number out of all the lists (for setting the
    # register)

    depth_list = [len(qubit_list) for qubit_list in qubit_lists]

    # go through for each trial
    for trial in range(ntrials):

        # go through for each depth in the depth list
        for depthidx, depth in enumerate(depth_list):

            n_q_max = np.max(qubit_lists[depthidx])

            provider = xacc.getIRProvider('quantum')

            qr = xacc.qalloc(int(n_q_max+1))
            qr2 = xacc.qalloc(int(depth))
            #cr = qiskit.ClassicalRegister(int(depth), 'cr')

            qc = provider.createComposite('qv_depth_%d_trial_%d' % (depth, trial))
            qc2 = provider.createComposite('qv_depth_%d_trial_%d' % (depth, trial))

            # build the circuit
            for _ in range(depth):
                # Generate uniformly random permutation Pj of [0...n-1]
                perm = np.random.permutation(depth)
                # For each pair p in Pj, generate Haar random SU(4)
                for k in range(int(np.floor(depth/2))):
                    unitary = random_unitary(4)
                    pair = int(perm[2*k]), int(perm[2*k+1])
                    haar = provider.createInstruction(unitary, [qr[qubit_lists[depthidx][pair[0]]],
                                        qr[qubit_lists[depthidx][pair[1]]]])
                    qc.addInstructions([haar])
                    qc2.addInstructions([haar])

            # append an id to all the qubits in the ideal circuits
            # to prevent a truncation error in the statevector
            # simulators
            #qc2.u1(0, qr2)

            circuits_nomeas[trial].append(qc2)

            # add measurement
            for qind, qubit in enumerate(qubit_lists[depthidx]):
                qc.measure(qr[qubit], cr[qind])

            circuits[trial].append(qc)

    return circuits, circuits_nomeas




def random_unitary(dims, seed=None):
    """Return a random unitary Operator.

    The operator is sampled from the unitary Haar measure.

    Args:
        dims (int or tuple): the input dimensions of the Operator.
        seed (int or np.random.Generator): Optional. Set a fixed seed or
                                           generator for RNG.

    Returns:
        Operator: a unitary operator.
    """
    if seed is None:
        random_state = np.random.default_rng()
    elif isinstance(seed, np.random.Generator):
        random_state = seed
    else:
        random_state = default_rng(seed)

    dim = np.product(dims)
    mat = stats.unitary_group.rvs(dim, random_state=random_state)
    return Operator(mat, input_dims=dims, output_dims=dims)

#### EXAMPLE ####

# qubit_lists: list of list of qubit subsets to generate QV circuits
qubit_lists = [[0,1,3],[0,1,3,5],[0,1,3,5,7],[0,1,3,5,7,10]]
# ntrials: Number of random circuits to create for each subset
ntrials = 50

circuits, circuits_nomeas = qv_circuits()

for program in circuits:
    buffer = xacc.qalloc(3)
    qpu = xacc.getAccelerator('ibm:ibmq_valencia', {'shots':8192})
    qpu.execute(buffer, program)
    results = buffer.getMeasurementCounts()
    fidelities = buffer['1q-gate-fidelities']

    print(results)