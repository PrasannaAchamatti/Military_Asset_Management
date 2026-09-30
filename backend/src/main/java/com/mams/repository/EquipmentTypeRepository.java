package com.mams.repository;

import com.mams.entity.EquipmentType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;
import java.util.List;

@Repository
public interface EquipmentTypeRepository extends JpaRepository<EquipmentType, Long> {
}
