package com.mams.repository;

import com.mams.entity.Expenditure;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;
import java.util.List;

@Repository
public interface ExpenditureRepository extends JpaRepository<Expenditure, Long> {
    List<Expenditure> findByBaseId(Long baseId);
}
