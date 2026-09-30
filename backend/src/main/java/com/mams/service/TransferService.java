package com.mams.service;

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
