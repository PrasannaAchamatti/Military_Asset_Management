package com.mams.controller;

import com.mams.dto.EquipmentTypeDto;
import com.mams.entity.EquipmentType;
import com.mams.service.EquipmentTypeService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/equipment-types")
public class EquipmentTypeController {
    @Autowired private EquipmentTypeService equipmentTypeService;

    @GetMapping
    public List<EquipmentType> getAll() {
        return equipmentTypeService.getAllEquipmentTypes();
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public EquipmentType create(@Valid @RequestBody EquipmentTypeDto dto) {
        return equipmentTypeService.createEquipmentType(dto);
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public EquipmentType update(@PathVariable Long id, @Valid @RequestBody EquipmentTypeDto dto) {
        return equipmentTypeService.updateEquipmentType(id, dto);
    }
}
