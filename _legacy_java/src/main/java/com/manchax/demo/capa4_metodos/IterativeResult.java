package com.manchax.demo.capa4_metodos;

import java.util.List;

public class IterativeResult {
    private final String methodName;
    private final double[] solution;
    private final int iterations;
    private final List<Double> errorHistory;

    public IterativeResult(String methodName, double[] solution, int iterations, List<Double> errorHistory) {
        this.methodName = methodName;
        this.solution = solution;
        this.iterations = iterations;
        this.errorHistory = errorHistory;
    }

    public String getMethodName() {
        return methodName;
    }

    public double[] getSolution() {
        return solution;
    }

    public int getIterations() {
        return iterations;
    }

    public List<Double> getErrorHistory() {
        return errorHistory;
    }
}