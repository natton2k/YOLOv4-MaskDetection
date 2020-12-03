package com.bangmaple.com.bangmaple.controllers;

import com.bangmaple.repository.ThermalDataRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class ThermalDataController {

    @Autowired
    private ThermalDataRepository thermalDataRepository;

    @GetMapping
    public ResponseEntity getAll() {
        return ResponseEntity.ok(thermalDataRepository.findAll());
    }

    @GetMapping
    @RequestMapping("/latest")
    public ResponseEntity getLatest() {
        List list = thermalDataRepository.findAll();
        return ResponseEntity.ok(list.get(list.size()-1));
    }

}
