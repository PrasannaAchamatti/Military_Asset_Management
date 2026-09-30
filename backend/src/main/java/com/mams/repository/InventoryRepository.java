package com.mams.repository;

import com.mams.entity.Inventory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;
import java.util.List;

@Repository
public interface InventoryRepository extends JpaRepository<Inventory, Long> {
    Optional<Inventory> findByBaseIdAndEquipmentTypeId(Long baseId, Long equipmentTypeId);
    List<Inventory> findByBaseId(Long baseId);
}
