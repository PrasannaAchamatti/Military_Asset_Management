package com.mams.dto;
import jakarta.validation.constraints.*;
import lombok.Data;
import java.time.LocalDate;
@Data
public class AssignmentRequestDto {
    @NotNull private Long baseId;
    @NotNull private Long equipmentTypeId;
    @NotBlank private String personnelName;
    @NotBlank private String personnelId;
    @Min(1) private int quantity;
    @NotNull private LocalDate assignedDate;
    private String remarks;
}