package com.manchax.demo.capa2_control;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/circuitos")
public class CircuitController {

    @GetMapping("/estado")
    public String verificarEstado() {
        return "Capa 2 (Controlador REST) operativa y lista para recibir circuitos.";
    }
}