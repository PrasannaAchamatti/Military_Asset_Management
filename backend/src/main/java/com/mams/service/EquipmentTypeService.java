package com.mams.service;

import com.mams.audit.AuditAction;
import com.mams.audit.AuditService;
import com.mams.dto.EquipmentTypeDto;
import com.mams.entity.EquipmentType;
import com.mams.exception.ResourceNotFoundException;
import com.mams.repository.EquipmentTypeRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class EquipmentTypeService {
    @Autowired private EquipmentTypeRepository equipmentTypeRepository;
    @Autowired private AuditService auditService;

    public List<EquipmentType> getAllEquipmentTypes() {
        return equipmentTypeRepository.findAll();
    }

    public EquipmentType createEquipmentType(EquipmentTypeDto dto) {
        EquipmentType eq = new EquipmentType();
        eq.setEquipmentCode(dto.getEquipmentCode());
        eq.setEquipmentName(dto.getEquipmentName());
        eq.setCategory(dto.getCategory());
        eq.setDescription(dto.getDescription());
        eq.setUnit(dto.getUnit());
        eq.setActive(dto.isActive());
        
        EquipmentType saved = equipmentTypeRepository.save(eq);
        auditService.logAction(AuditAction.EQUIPMENT_CREATED, "EquipmentType", saved.getId().toString(), "Created equipment: " + eq.getEquipmentName());
        return saved;
    }

    public EquipmentType updateEquipmentType(Long id, EquipmentTypeDto dto) {
        EquipmentType eq = equipmentTypeRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Equipment Type not found"));
        eq.setEquipmentCode(dto.getEquipmentCode());
        eq.setEquipmentName(dto.getEquipmentName());
        eq.setCategory(dto.getCategory());
        eq.setDescription(dto.getDescription());
        eq.setUnit(dto.getUnit());
        eq.setActive(dto.isActive());
        
        EquipmentType saved = equipmentTypeRepository.save(eq);
        auditService.logAction(AuditAction.EQUIPMENT_UPDATED, "EquipmentType", saved.getId().toString(), "Updated equipment: " + eq.getEquipmentName());
        return saved;
    }
}
