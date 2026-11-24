package com.manchax.demo.capa4_metodos;

public interface IIterativeSolver {
    IterativeResult solveJacobi(double[][] matrixA, double[] vectorB, double tolerance, int maxIterations);
    IterativeResult solveGaussSeidel(double[][] matrixA, double[] vectorB, double tolerance, int maxIterations);
    IterativeResult solveSOR(double[][] matrixA, double[] vectorB, double tolerance, int maxIterations, double omega);
    IterativeResult solveSSOR(double[][] matrixA, double[] vectorB, double tolerance, int maxIterations, double omega);
}