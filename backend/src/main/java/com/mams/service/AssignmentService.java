package com.mams.service;

import com.mams.audit.AuditAction;
import com.mams.audit.AuditService;
import com.mams.dto.AssignmentRequestDto;
import com.mams.entity.Assignment;
import com.mams.entity.Base;
import com.mams.entity.EquipmentType;
import com.mams.entity.User;
import com.mams.exception.ResourceNotFoundException;
import com.mams.repository.AssignmentRepository;
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
public class AssignmentService {
    @Autowired private AssignmentRepository assignmentRepository;
    @Autowired private InventoryService inventoryService;
    @Autowired private AuditService auditService;
    @Autowired private BaseRepository baseRepository;
    @Autowired private EquipmentTypeRepository equipmentTypeRepository;
    @Autowired private UserRepository userRepository;

    public List<Assignment> getAllAssignments() {
        return assignmentRepository.findAll();
    }

    public List<Assignment> getAssignmentsByBase(Long baseId) {
        inventoryService.validateBaseAccess(baseId);
        return assignmentRepository.findByBaseId(baseId);
    }

    @Transactional
    public Assignment createAssignment(AssignmentRequestDto dto) {
        inventoryService.validateBaseAccess(dto.getBaseId());

        Base base = baseRepository.findById(dto.getBaseId()).orElseThrow(() -> new ResourceNotFoundException("Base not found"));
        EquipmentType equipmentType = equipmentTypeRepository.findById(dto.getEquipmentTypeId()).orElseThrow(() -> new ResourceNotFoundException("Equipment Type not found"));

        inventoryService.reduceInventory(base.getId(), equipmentType.getId(), dto.getQuantity());

        UserPrincipal principal = (UserPrincipal) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        User currentUser = userRepository.findById(principal.getId()).get();

        Assignment assignment = new Assignment();
        assignment.setBase(base);
        assignment.setEquipmentType(equipmentType);
        assignment.setPersonnelName(dto.getPersonnelName());
        assignment.setPersonnelId(dto.getPersonnelId());
        assignment.setQuantity(dto.getQuantity());
        assignment.setAssignedDate(dto.getAssignedDate());
        assignment.setRemarks(dto.getRemarks());
        assignment.setStatus("ASSIGNED");
        assignment.setAssignedBy(currentUser);

        Assignment saved = assignmentRepository.save(assignment);
        auditService.logAction(AuditAction.ASSIGNMENT_CREATED, "Assignment", saved.getId().toString(), "Assigned " + dto.getQuantity() + " units to " + dto.getPersonnelName());
        
        return saved;
    }
}
