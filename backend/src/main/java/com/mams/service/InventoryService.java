package com.mams.service;

import com.mams.entity.*;
import com.mams.exception.AccessDeniedException;
import com.mams.exception.ResourceNotFoundException;
import com.mams.repository.*;
import com.mams.security.UserPrincipal;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

@Service
public class InventoryService {

    @Autowired
    private InventoryRepository inventoryRepository;

    @Autowired
    private BaseRepository baseRepository;

    @Autowired
    private EquipmentTypeRepository equipmentTypeRepository;

    public void validateBaseAccess(Long baseId) {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth != null && auth.getPrincipal() instanceof UserPrincipal) {
            UserPrincipal user = (UserPrincipal) auth.getPrincipal();
            String role = user.getAuthorities().iterator().next().getAuthority();
            
            if ("ROLE_ADMIN".equals(role)) {
                return; // Admin has access to all bases
            }
            
            if (user.getBaseId() != null && !user.getBaseId().equals(baseId)) {
                throw new AccessDeniedException("You do not have permission to access data for this base.");
            }
        }
    }

    @Transactional
    public Inventory addInventory(Long baseId, Long equipmentTypeId, int quantity) {
        Inventory inventory = inventoryRepository.findByBaseIdAndEquipmentTypeId(baseId, equipmentTypeId)
                .orElse(new Inventory(null, baseRepository.findById(baseId).get(), equipmentTypeRepository.findById(equipmentTypeId).get(), 0, null));
        
        inventory.setQuantity(inventory.getQuantity() + quantity);
        return inventoryRepository.save(inventory);
    }

    @Transactional
    public Inventory reduceInventory(Long baseId, Long equipmentTypeId, int quantity) {
        Inventory inventory = inventoryRepository.findByBaseIdAndEquipmentTypeId(baseId, equipmentTypeId)
                .orElseThrow(() -> new IllegalArgumentException("Inventory not found for base and equipment type"));
        
        if (inventory.getQuantity() < quantity) {
            throw new IllegalArgumentException("Insufficient inventory available");
        }
        
        inventory.setQuantity(inventory.getQuantity() - quantity);
        return inventoryRepository.save(inventory);
    }
}
