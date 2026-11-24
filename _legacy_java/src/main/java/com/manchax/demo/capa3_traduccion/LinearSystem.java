package com.manchax.demo.capa3_traduccion;

public class LinearSystem {
    private final double[][] matrixA;
    private final double[] vectorB;

    public LinearSystem(double[][] matrixA, double[] vectorB) {
        this.matrixA = matrixA;
        this.vectorB = vectorB;
    }

    public double[][] getMatrixA() {
        return matrixA;
    }

    public double[] getVectorB() {
        return vectorB;
    }
}