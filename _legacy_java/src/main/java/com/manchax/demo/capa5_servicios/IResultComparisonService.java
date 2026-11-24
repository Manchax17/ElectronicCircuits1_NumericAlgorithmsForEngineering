package com.manchax.demo.capa5_servicios;

import com.manchax.demo.capa4_metodos.IterativeResult;
import java.util.List;

public interface IResultComparisonService {
    List<IterativeResult> compareAllMethods(double[][] matrixA, double[] vectorB, double tolerance, int maxIterations, double omega);
}