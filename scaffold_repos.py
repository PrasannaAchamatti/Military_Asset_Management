import os

backend_src = "f:/Military_Manage/backend/src/main/java/com/mams"

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

ensure_dir(f"{backend_src}/repository")
repos = ["User", "Base", "EquipmentType", "Inventory", "Purchase", "Transfer", "Assignment", "Expenditure", "AuditLog"]
for repo in repos:
    content = f"""package com.mams.repository;

import com.mams.entity.{repo};
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;
import java.util.List;

@Repository
public interface {repo}Repository extends JpaRepository<{repo}, Long> {{
"""
    if repo == "User":
        content += """    Optional<User> findByUsername(String username);
    Optional<User> findByEmail(String email);
    List<User> findByBaseId(Long baseId);
"""
    elif repo == "Inventory":
        content += """    Optional<Inventory> findByBaseIdAndEquipmentTypeId(Long baseId, Long equipmentTypeId);
    List<Inventory> findByBaseId(Long baseId);
"""
    elif repo in ["Purchase", "Transfer", "Assignment", "Expenditure"]:
        if repo == "Transfer":
            content += """    List<Transfer> findByFromBaseIdOrToBaseId(Long fromBaseId, Long toBaseId);
"""
        else:
            content += f"""    List<{repo}> findByBaseId(Long baseId);
"""
    content += "}\n"
    with open(f"{backend_src}/repository/{repo}Repository.java", "w") as f:
        f.write(content)

print("Repositories generated.")
