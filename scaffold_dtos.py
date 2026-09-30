import os

backend_src = "f:/Military_Manage/backend/src/main/java/com/mams"
ensure_dir = lambda path: os.makedirs(path, exist_ok=True)
ensure_dir(f"{backend_src}/dto")

dtos = {
    "PurchaseRequestDto": """package com.mams.dto;
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
}""",
    "TransferRequestDto": """package com.mams.dto;
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
}""",
    "AssignmentRequestDto": """package com.mams.dto;
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
}""",
    "ExpenditureRequestDto": """package com.mams.dto;
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
}""",
    "BaseDto": """package com.mams.dto;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;
@Data
public class BaseDto {
    private Long id;
    @NotBlank private String baseCode;
    @NotBlank private String baseName;
    private String location;
    private boolean active;
}""",
    "EquipmentTypeDto": """package com.mams.dto;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;
@Data
public class EquipmentTypeDto {
    private Long id;
    @NotBlank private String equipmentCode;
    @NotBlank private String equipmentName;
    @NotBlank private String category;
    private String description;
    @NotBlank private String unit;
    private boolean active;
}""",
    "DashboardStatsDto": """package com.mams.dto;
import lombok.Data;
@Data
public class DashboardStatsDto {
    private long openingBalance;
    private long purchases;
    private long transferIn;
    private long transferOut;
    private long assigned;
    private long expended;
    private long netMovement;
    private long closingBalance;
}"""
}

for name, content in dtos.items():
    with open(f"{backend_src}/dto/{name}.java", "w") as f:
        f.write(content)

print("DTOs generated successfully.")
