import xacc
import ast

from xacc import Benchmark
from pelix.ipopo.decorators import ComponentFactory, Property, Requires, Provides, \
Validate, Invalidate, Instantiate

import qv_benchmark_helper

@ComponentFactory("qv_benchmark_factory") # Manipulates the class and sets its (unique) factory name
@Provides("benchmark") # Indicate that the components will provide a service
@Property("_benchmark", "benchmark", "qv")
@Property("_name", "name", "qv")
@Instantiate("qv_benchmark_instance") # Tell iPOPO to instantiate a component instance as soon as the file is loaded
class QPT(Benchmark):

    def __init__(self):
        self.circuit_name = None
        self.qv = None
        self.nq = None
        self.qpu = None
        self.qubit_map = []

    def execute(self, inputParams):
        xacc_opts = inputParams['XACC']
        acc_name = xacc_opts['accelerator']

        if 'verbose' in xacc_opts and xacc_opts['verbose']:
            xacc.set_verbose(True)

        if 'Benchmark' not in inputParams:
            xacc.error('Invalid benchmark input - must have Benchmark description')

        if 'Circuit' not in inputParams:
            xacc.error('Invalid benchmark input - must have circuit description')

        self.qpu = xacc.getAccelerator(acc_name, xacc_opts)
        if 'Decorators' in inputParams:
            if 'readout_error' in inputParams['Decorators']:
                qpu = xacc.getAcceleratorDecorator('ro-error', qpu)


        provider = xacc.getIRProvider('quantum')

        if 'source' in inputParams['Circuit']:
            # here assume this is xasm always
            src = inputParams['Circuit']['source']
            xacc.qasm(src)
            # get the name of the circuit
            circuit_name = None
            for l in src.split('\n'):
                if '.circuit' in l:
                    circuit_name = l.split(' ')[1]
            self.circuit_name = circuit_name
            ansatz = xacc.getCompiled(circuit_name)

        opts = {'circuit':ansatz, 'accelerator':self.qpu}
        if 'qubit-map' in inputParams['Circuit']:
            raw_qbit_map = inputParams['Circuit']['qubit-map']
            if not isinstance(raw_qbit_map, list):
                raw_qbit_map = ast.literal_eval(raw_qbit_map)
            self.qubit_map = raw_qbit_map
            opts['qubit-map'] = self.qubit_map

        self.qv = xacc.getAlgorithm('qv', opts)

        self.nq = ansatz.nLogicalBits()

        buffer = xacc.qalloc(ansatz.nLogicalBits())

        self.qv.execute(buffer)
        return buffer


    def analyze(self, buffer, inputParams):
        pass

