package com.mams.dto;
import jakarta.validation.constraints.*;
import lombok.Data;
import com.mams.entity.ExpenditureType;
import java.time.LocalDate;
@Data
public class ExpenditureRequestDto {
    @NotNull private Long baseId;
    @NotNull private Long equipmentTypeId;
    @Min(1) private int quantity;
    @NotNull private ExpenditureType expenditureType;
    @NotNull private LocalDate expenditureDate;
    private String remarks;
}