package com.manchax.demo.capa5_servicios;

import com.manchax.demo.capa4_metodos.IterativeResult;
import org.springframework.stereotype.Service;
import java.util.Collections;
import java.util.List;

@Service
public class ResultComparisonServiceImpl implements IResultComparisonService {

    @Override
    public List<IterativeResult> compareAllMethods(double[][] matrixA, double[] vectorB, double tolerance, int maxIterations, double omega) {
        // TODO: Orquestar los 4 métodos y consolidar métricas comparativas
        return Collections.emptyList();
    }
}