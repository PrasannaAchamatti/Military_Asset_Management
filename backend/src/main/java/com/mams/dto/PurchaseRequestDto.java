package com.mams.dto;
import jakarta.validation.constraints.*;
import lombok.Data;
import java.time.LocalDate;
@Data
public class PurchaseRequestDto {
    @NotNull private Long baseId;
    @NotNull private Long equipmentTypeId;
    @Min(1) private int quantity;
    @NotNull private LocalDate purchaseDate;
    private String supplier;
    private String referenceNumber;
    private String remarks;
}