package com.mams.config;

import com.mams.entity.*;
import com.mams.repository.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import java.util.Arrays;
import java.util.List;

@Component
public class DataSeeder implements CommandLineRunner {

    @Autowired private UserRepository userRepository;
    @Autowired private BaseRepository baseRepository;
    @Autowired private EquipmentTypeRepository equipmentTypeRepository;
    @Autowired private PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) throws Exception {
        if (baseRepository.count() == 0) {
            seedBases();
        }
        if (equipmentTypeRepository.count() == 0) {
            seedEquipmentTypes();
        }
        if (userRepository.count() == 0) {
            seedUsers();
        }
    }

    private void seedBases() {
        List<Base> bases = Arrays.asList(
            new Base(null, "B-001", "Alpha Base", "North Region", true, null),
            new Base(null, "B-002", "Bravo Base", "South Region", true, null),
            new Base(null, "B-003", "Charlie Base", "East Region", true, null),
            new Base(null, "B-004", "Delta Base", "West Region", true, null),
            new Base(null, "B-005", "Echo Base", "Central Region", true, null)
        );
        baseRepository.saveAll(bases);
    }

    private void seedEquipmentTypes() {
        List<EquipmentType> equipmentTypes = Arrays.asList(
            new EquipmentType(null, "EQ-001", "Military Vehicle", "Vehicles", "Standard transport vehicle", "unit", true, null),
            new EquipmentType(null, "EQ-002", "Transport Truck", "Vehicles", "Heavy logistics truck", "unit", true, null),
            new EquipmentType(null, "EQ-003", "Armored Vehicle", "Vehicles", "Light armored vehicle", "unit", true, null),
            new EquipmentType(null, "EQ-004", "Communication Radio", "Communication Equipment", "Long range radio", "set", true, null),
            new EquipmentType(null, "EQ-005", "Protective Gear", "Protective Equipment", "Standard body armor", "set", true, null),
            new EquipmentType(null, "EQ-006", "Medical Kit", "Medical Equipment", "Field medical kit", "box", true, null),
            new EquipmentType(null, "EQ-007", "Training Equipment", "Other", "Training dummy", "unit", true, null)
        );
        equipmentTypeRepository.saveAll(equipmentTypes);
    }

    private void seedUsers() {
        Base alphaBase = baseRepository.findAll().get(0);

        User admin = new User();
        admin.setUsername("admin");
        admin.setFullName("System Administrator");
        admin.setEmail("admin@mams.local");
        admin.setPasswordHash(passwordEncoder.encode("password"));
        admin.setRole(Role.ADMIN);
        admin.setActive(true);

        User commander = new User();
        commander.setUsername("commander");
        commander.setFullName("Alpha Base Commander");
        commander.setEmail("commander@mams.local");
        commander.setPasswordHash(passwordEncoder.encode("password"));
        commander.setRole(Role.BASE_COMMANDER);
        commander.setBase(alphaBase);
        commander.setActive(true);

        User logistics = new User();
        logistics.setUsername("logistics");
        logistics.setFullName("Logistics Officer");
        logistics.setEmail("logistics@mams.local");
        logistics.setPasswordHash(passwordEncoder.encode("password"));
        logistics.setRole(Role.LOGISTICS_OFFICER);
        logistics.setActive(true);

        userRepository.saveAll(Arrays.asList(admin, commander, logistics));
    }
}
