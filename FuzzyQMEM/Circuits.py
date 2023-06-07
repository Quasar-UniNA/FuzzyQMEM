from qiskit import QuantumCircuit, QuantumRegister
from qiskit.ignis.mitigation.measurement import complete_meas_cal


import math

class Circuit():
    def __init__(self, name, draw_circuit=False):
        self.circuit = None
        self.name = name
        self.draw_circuit= draw_circuit

    def createCircuit(self):
        pass

    def getOptimalDistribution(self, num_shots):
        pass



class BasisStateCircuit(Circuit):
    def __init__(self, state_label, num_qubits, draw_circuit=False):
        Circuit.__init__(self, state_label, draw_circuit)
        self.state_label=state_label
        self.num_qubits=num_qubits
        self.index=None

    def createCircuit(self):
        qr = QuantumRegister(self.num_qubits)
        meas_calibs, state_labels = complete_meas_cal(qr=qr, circlabel='state')
        self.index=state_labels.index(self.state_label)
        self.circuit = meas_calibs[self.index]
        if self.draw_circuit:
            print(self.circuit.draw(output="latex_source", fold=300))

    def getOptimalDistribution(self, num_shots):
        result = [0]*2**self.num_qubits
        result[self.index] = num_shots
        return result


class BellStateCircuit2Q(Circuit):
    def __init__(self, draw_circuit=False):
        Circuit.__init__(self, "Bell_States", draw_circuit)

    def createCircuit(self):
        self.circuit = QuantumCircuit(2,2)
        self.circuit.h(0)
        self.circuit.cx(0,1)
        self.circuit.measure(self.circuit.qregs[0],self.circuit.cregs[0])
        if self.draw_circuit:
            print(self.circuit.draw(output="latex_source", fold=300))

    def getOptimalDistribution(self, num_shots):
        return [num_shots / 2, 0, 0, num_shots / 2]



class RandomCircuit1(Circuit):
    def __init__(self, draw_circuit=False):
        Circuit.__init__(self, "Random_1", draw_circuit)

    def createCircuit(self):
        self.circuit = QuantumCircuit(2,2)
        self.circuit.rx(math.pi/2,0)
        self.circuit.ry(math.pi/2,1)
        self.circuit.cx(0,1)
        self.circuit.rx(math.pi / 8,0)
        self.circuit.measure(self.circuit.qregs[0],self.circuit.cregs[0])
        if self.draw_circuit:
            print(self.circuit.draw(output="latex_source", fold=300))

    def getOptimalDistribution(self, num_shots):
        return [num_shots * 15.43291 / 100, num_shots * 34.56709 / 100, num_shots * 15.43291 / 100,
                num_shots * 34.56709 / 100]


class RandomCircuit2(Circuit):
    def __init__(self, draw_circuit=False):
        Circuit.__init__(self, "Random_2", draw_circuit)

    def createCircuit(self):
        self.circuit = QuantumCircuit(2,2)
        self.circuit.ry(math.pi/4,0)
        self.circuit.rx(math.pi/3,0 )
        self.circuit.cx(0,1)
        self.circuit.measure(self.circuit.qregs[0],self.circuit.cregs[0])
        if self.draw_circuit:
            print(self.circuit.draw(output="latex_source", fold=300))

    def getOptimalDistribution(self, num_shots):
        return [num_shots * 67.67767 / 100, 0, 0, num_shots * 32.32233 / 100]



class RandomCircuit3(Circuit):
    def __init__(self, draw_circuit=False):
        Circuit.__init__(self, "Random_3", draw_circuit)

    def createCircuit(self):
        self.circuit = QuantumCircuit(2,2)
        self.circuit.h(0)
        self.circuit.rx(math.pi/4,1)
        self.circuit.x(1)
        self.circuit.measure(self.circuit.qregs[0],self.circuit.cregs[0])
        if self.draw_circuit:
            print(self.circuit.draw(output="latex_source", fold=300))

    def getOptimalDistribution(self, num_shots):
        return [num_shots * 7.32233 / 100, num_shots * 7.32233 / 100, num_shots * 42.67767 / 100,
                num_shots * 42.67767 / 100]


class RandomCircuit4(Circuit):
    def __init__(self, draw_circuit=False):
        Circuit.__init__(self, "Random_4", draw_circuit)

    def createCircuit(self):
        self.circuit = QuantumCircuit(2,2)
        self.circuit.rx(math.pi/4,0)
        self.circuit.ry(math.pi/8,0)
        self.circuit.x(0)
        self.circuit.h(1)
        self.circuit.measure(self.circuit.qregs[0],self.circuit.cregs[0])
        # print(qc)
        if self.draw_circuit:
            print(self.circuit.draw(output="latex_source", fold=300))

    def getOptimalDistribution(self, num_shots):
        return [num_shots * 8.66796 / 100, num_shots * 41.33204 / 100, num_shots * 8.66796 / 100,
                num_shots * 41.33204 / 100]


