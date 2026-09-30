package com.mams.dto;
import jakarta.validation.constraints.*;
import lombok.Data;
import java.time.LocalDate;
@Data
public class TransferRequestDto {
    @NotNull private Long equipmentTypeId;
    @NotNull private Long fromBaseId;
    @NotNull private Long toBaseId;
    @Min(1) private int quantity;
    @NotNull private LocalDate transferDate;
    private String referenceNumber;
    private String remarks;
}