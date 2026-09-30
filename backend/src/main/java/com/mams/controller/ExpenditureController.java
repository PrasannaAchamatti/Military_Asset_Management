package com.mams.controller;

import com.mams.dto.ExpenditureRequestDto;
import com.mams.entity.Expenditure;
import com.mams.service.ExpenditureService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/expenditures")
public class ExpenditureController {
    @Autowired private ExpenditureService expenditureService;

    @GetMapping
    public List<Expenditure> getAll(@RequestParam(required = false) Long baseId) {
        if (baseId != null) {
            return expenditureService.getExpendituresByBase(baseId);
        }
        return expenditureService.getAllExpenditures();
    }

    @PostMapping
    public Expenditure create(@Valid @RequestBody ExpenditureRequestDto dto) {
        return expenditureService.createExpenditure(dto);
    }
}
