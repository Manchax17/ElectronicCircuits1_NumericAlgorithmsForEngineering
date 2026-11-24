package com.manchax.demo.capa4_metodos;

import org.springframework.stereotype.Service;
import java.util.Collections;

@Service
public class IterativeSolverImpl implements IIterativeSolver {

    @Override
    public IterativeResult solveJacobi(double[][] matrixA, double[] vectorB, double tolerance, int maxIterations) {
        // TODO: Implementar método de Jacobi en el siguiente sprint
        return new IterativeResult("Jacobi", new double[vectorB.length], 0, Collections.emptyList());
    }

    @Override
    public IterativeResult solveGaussSeidel(double[][] matrixA, double[] vectorB, double tolerance, int maxIterations) {
        // TODO: Implementar método de Gauss-Seidel en el siguiente sprint
        return new IterativeResult("Gauss-Seidel", new double[vectorB.length], 0, Collections.emptyList());
    }

    @Override
    public IterativeResult solveSOR(double[][] matrixA, double[] vectorB, double tolerance, int maxIterations, double omega) {
        // TODO: Implementar método SOR en el siguiente sprint
        return new IterativeResult("SOR", new double[vectorB.length], 0, Collections.emptyList());
    }

    @Override
    public IterativeResult solveSSOR(double[][] matrixA, double[] vectorB, double tolerance, int maxIterations, double omega) {
        // TODO: Implementar método SSOR en el siguiente sprint
        return new IterativeResult("SSOR", new double[vectorB.length], 0, Collections.emptyList());
    }
}