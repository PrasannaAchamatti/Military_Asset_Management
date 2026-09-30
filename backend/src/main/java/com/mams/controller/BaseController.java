package com.mams.controller;

import com.mams.dto.BaseDto;
import com.mams.entity.Base;
import com.mams.service.BaseService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/bases")
public class BaseController {
    @Autowired private BaseService baseService;

    @GetMapping
    public List<Base> getAllBases() {
        return baseService.getAllBases();
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public Base createBase(@Valid @RequestBody BaseDto dto) {
        return baseService.createBase(dto);
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public Base updateBase(@PathVariable Long id, @Valid @RequestBody BaseDto dto) {
        return baseService.updateBase(id, dto);
    }
}
