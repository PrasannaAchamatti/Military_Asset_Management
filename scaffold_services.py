import os

backend_src = "f:/Military_Manage/backend/src/main/java/com/mams"
ensure_dir = lambda path: os.makedirs(path, exist_ok=True)
ensure_dir(f"{backend_src}/service")

services = {
    "PurchaseService": """package com.mams.service;

import com.mams.audit.AuditAction;
import com.mams.audit.AuditService;
import com.mams.dto.PurchaseRequestDto;
import com.mams.entity.Base;
import com.mams.entity.EquipmentType;
import com.mams.entity.Purchase;
import com.mams.entity.User;
import com.mams.exception.ResourceNotFoundException;
import com.mams.repository.BaseRepository;
import com.mams.repository.EquipmentTypeRepository;
import com.mams.repository.PurchaseRepository;
import com.mams.repository.UserRepository;
import com.mams.security.UserPrincipal;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class PurchaseService {

    @Autowired private PurchaseRepository purchaseRepository;
    @Autowired private InventoryService inventoryService;
    @Autowired private AuditService auditService;
    @Autowired private BaseRepository baseRepository;
    @Autowired private EquipmentTypeRepository equipmentTypeRepository;
    @Autowired private UserRepository userRepository;

    public List<Purchase> getAllPurchases() {
        return purchaseRepository.findAll();
    }

    public List<Purchase> getPurchasesByBase(Long baseId) {
        inventoryService.validateBaseAccess(baseId);
        return purchaseRepository.findByBaseId(baseId);
    }

    @Transactional
    public Purchase createPurchase(PurchaseRequestDto dto) {
        inventoryService.validateBaseAccess(dto.getBaseId());

        Base base = baseRepository.findById(dto.getBaseId())
                .orElseThrow(() -> new ResourceNotFoundException("Base not found"));
        EquipmentType equipmentType = equipmentTypeRepository.findById(dto.getEquipmentTypeId())
                .orElseThrow(() -> new ResourceNotFoundException("Equipment Type not found"));

        UserPrincipal principal = (UserPrincipal) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        User currentUser = userRepository.findById(principal.getId()).get();

        Purchase purchase = new Purchase();
        purchase.setBase(base);
        purchase.setEquipmentType(equipmentType);
        purchase.setQuantity(dto.getQuantity());
        purchase.setPurchaseDate(dto.getPurchaseDate());
        purchase.setSupplier(dto.getSupplier());
        purchase.setReferenceNumber(dto.getReferenceNumber());
        purchase.setRemarks(dto.getRemarks());
        purchase.setCreatedBy(currentUser);

        Purchase savedPurchase = purchaseRepository.save(purchase);
        
        inventoryService.addInventory(base.getId(), equipmentType.getId(), purchase.getQuantity());
        
        auditService.logAction(AuditAction.PURCHASE_CREATED, "Purchase", savedPurchase.getId().toString(), "Added " + dto.getQuantity() + " units of " + equipmentType.getEquipmentName());

        return savedPurchase;
    }
}
""",

    "TransferService": """package com.mams.service;

import com.mams.audit.AuditAction;
import com.mams.audit.AuditService;
import com.mams.dto.TransferRequestDto;
import com.mams.entity.*;
import com.mams.exception.ResourceNotFoundException;
import com.mams.repository.BaseRepository;
import com.mams.repository.EquipmentTypeRepository;
import com.mams.repository.TransferRepository;
import com.mams.repository.UserRepository;
import com.mams.security.UserPrincipal;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class TransferService {

    @Autowired private TransferRepository transferRepository;
    @Autowired private InventoryService inventoryService;
    @Autowired private AuditService auditService;
    @Autowired private BaseRepository baseRepository;
    @Autowired private EquipmentTypeRepository equipmentTypeRepository;
    @Autowired private UserRepository userRepository;

    public List<Transfer> getAllTransfers() {
        return transferRepository.findAll();
    }

    public List<Transfer> getTransfersByBase(Long baseId) {
        inventoryService.validateBaseAccess(baseId);
        return transferRepository.findByFromBaseIdOrToBaseId(baseId, baseId);
    }

    @Transactional
    public Transfer createTransfer(TransferRequestDto dto) {
        inventoryService.validateBaseAccess(dto.getFromBaseId());

        if (dto.getFromBaseId().equals(dto.getToBaseId())) {
            throw new IllegalArgumentException("Source and destination bases cannot be the same");
        }

        Base fromBase = baseRepository.findById(dto.getFromBaseId()).orElseThrow(() -> new ResourceNotFoundException("Source Base not found"));
        Base toBase = baseRepository.findById(dto.getToBaseId()).orElseThrow(() -> new ResourceNotFoundException("Destination Base not found"));
        EquipmentType equipmentType = equipmentTypeRepository.findById(dto.getEquipmentTypeId()).orElseThrow(() -> new ResourceNotFoundException("Equipment Type not found"));

        UserPrincipal principal = (UserPrincipal) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        User currentUser = userRepository.findById(principal.getId()).get();

        // Check if sufficient inventory exists (will throw if not)
        inventoryService.reduceInventory(fromBase.getId(), equipmentType.getId(), dto.getQuantity());

        Transfer transfer = new Transfer();
        transfer.setFromBase(fromBase);
        transfer.setToBase(toBase);
        transfer.setEquipmentType(equipmentType);
        transfer.setQuantity(dto.getQuantity());
        transfer.setTransferDate(dto.getTransferDate());
        transfer.setStatus(TransferStatus.PENDING);
        transfer.setReferenceNumber(dto.getReferenceNumber());
        transfer.setRemarks(dto.getRemarks());
        transfer.setCreatedBy(currentUser);

        Transfer savedTransfer = transferRepository.save(transfer);
        
        auditService.logAction(AuditAction.TRANSFER_CREATED, "Transfer", savedTransfer.getId().toString(), "Created transfer of " + dto.getQuantity() + " units to " + toBase.getBaseName());

        return savedTransfer;
    }

    @Transactional
    public Transfer approveTransfer(Long transferId) {
        Transfer transfer = transferRepository.findById(transferId)
                .orElseThrow(() -> new ResourceNotFoundException("Transfer not found"));
        
        inventoryService.validateBaseAccess(transfer.getFromBase().getId());
        
        transfer.setStatus(TransferStatus.APPROVED);
        Transfer saved = transferRepository.save(transfer);
        
        auditService.logAction(AuditAction.TRANSFER_APPROVED, "Transfer", saved.getId().toString(), "Approved transfer");
        return saved;
    }

    @Transactional
    public Transfer completeTransfer(Long transferId) {
        Transfer transfer = transferRepository.findById(transferId)
                .orElseThrow(() -> new ResourceNotFoundException("Transfer not found"));
        
        inventoryService.validateBaseAccess(transfer.getToBase().getId());
        
        if (transfer.getStatus() != TransferStatus.APPROVED && transfer.getStatus() != TransferStatus.PENDING) {
            throw new IllegalArgumentException("Transfer is not in a valid state to be completed");
        }

        transfer.setStatus(TransferStatus.COMPLETED);
        
        inventoryService.addInventory(transfer.getToBase().getId(), transfer.getEquipmentType().getId(), transfer.getQuantity());
        
        Transfer saved = transferRepository.save(transfer);
        auditService.logAction(AuditAction.TRANSFER_COMPLETED, "Transfer", saved.getId().toString(), "Completed transfer");
        return saved;
    }
}
""",

    "AssignmentService": """package com.mams.service;

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
""",

    "ExpenditureService": """package com.mams.service;

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
"""
}

for name, content in services.items():
    with open(f"{backend_src}/service/{name}.java", "w") as f:
        f.write(content)

print("Main transactional services generated.")
