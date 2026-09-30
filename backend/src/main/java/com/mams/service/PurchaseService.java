package com.mams.service;

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
