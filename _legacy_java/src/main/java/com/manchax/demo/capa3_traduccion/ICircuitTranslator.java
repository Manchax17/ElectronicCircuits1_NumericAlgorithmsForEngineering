package com.manchax.demo.capa3_traduccion;

public interface ICircuitTranslator {
    LinearSystem translateNetlist(String netlist, int nodeCount);
}