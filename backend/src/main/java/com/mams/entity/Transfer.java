package com.mams.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "transfers")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Transfer {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "equipment_type_id", nullable = false)
    private EquipmentType equipmentType;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "from_base_id", nullable = false)
    private Base fromBase;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "to_base_id", nullable = false)
    private Base toBase;

    @Column(nullable = false)
    private int quantity;

    @Column(name = "transfer_date", nullable = false)
    private LocalDate transferDate;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private TransferStatus status;

    @Column(name = "reference_number")
    private String referenceNumber;

    private String remarks;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "created_by", nullable = false)
    private User createdBy;

    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();
}
