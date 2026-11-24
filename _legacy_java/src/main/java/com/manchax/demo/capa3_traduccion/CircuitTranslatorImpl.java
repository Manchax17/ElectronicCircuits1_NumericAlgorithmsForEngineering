package com.manchax.demo.capa3_traduccion;

import org.springframework.stereotype.Service;

@Service
public class CircuitTranslatorImpl implements ICircuitTranslator {

    @Override
    public LinearSystem translateNetlist(String netlist, int nodeCount) {
        // TODO: Implementar algoritmo de estampado nodal en el siguiente sprint
        double[][] emptyMatrix = new double[nodeCount][nodeCount];
        double[] emptyVector = new double[nodeCount];
        return new LinearSystem(emptyMatrix, emptyVector);
    }
}