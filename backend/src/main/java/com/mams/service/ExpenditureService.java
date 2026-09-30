package com.mams.service;

import com.mams.audit.AuditAction;
import com.mams.audit.AuditService;
import com.mams.dto.ExpenditureRequestDto;
import com.mams.entity.Expenditure;
import com.mams.entity.Base;
import com.mams.entity.EquipmentType;
import com.mams.entity.User;
import com.mams.exception.ResourceNotFoundException;
import com.mams.repository.ExpenditureRepository;
import com.mams.repository.BaseRepository;
import com.mams.repository.EquipmentTypeRepository;
import com.mams.repository.UserRepository;
import com.mams.security.UserPrincipal;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class ExpenditureService {
    @Autowired private ExpenditureRepository expenditureRepository;
    @Autowired private InventoryService inventoryService;
    @Autowired private AuditService auditService;
    @Autowired private BaseRepository baseRepository;
    @Autowired private EquipmentTypeRepository equipmentTypeRepository;
    @Autowired private UserRepository userRepository;

    public List<Expenditure> getAllExpenditures() {
        return expenditureRepository.findAll();
    }

    public List<Expenditure> getExpendituresByBase(Long baseId) {
        inventoryService.validateBaseAccess(baseId);
        return expenditureRepository.findByBaseId(baseId);
    }

    @Transactional
    public Expenditure createExpenditure(ExpenditureRequestDto dto) {
        inventoryService.validateBaseAccess(dto.getBaseId());

        Base base = baseRepository.findById(dto.getBaseId()).orElseThrow(() -> new ResourceNotFoundException("Base not found"));
        EquipmentType equipmentType = equipmentTypeRepository.findById(dto.getEquipmentTypeId()).orElseThrow(() -> new ResourceNotFoundException("Equipment Type not found"));

        inventoryService.reduceInventory(base.getId(), equipmentType.getId(), dto.getQuantity());

        UserPrincipal principal = (UserPrincipal) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        User currentUser = userRepository.findById(principal.getId()).get();

        Expenditure expenditure = new Expenditure();
        expenditure.setBase(base);
        expenditure.setEquipmentType(equipmentType);
        expenditure.setQuantity(dto.getQuantity());
        expenditure.setExpenditureType(dto.getExpenditureType());
        expenditure.setExpenditureDate(dto.getExpenditureDate());
        expenditure.setRemarks(dto.getRemarks());
        expenditure.setRecordedBy(currentUser);

        Expenditure saved = expenditureRepository.save(expenditure);
        auditService.logAction(AuditAction.EXPENDITURE_CREATED, "Expenditure", saved.getId().toString(), "Expended " + dto.getQuantity() + " units due to " + dto.getExpenditureType().name());
        
        return saved;
    }
}
