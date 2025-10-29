-- Database schema for medical data de-identification system
-- Created with Claude Code

-- Table for storing recognizer type definitions
CREATE TABLE `recognizer_types` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(50) NOT NULL,
  `module_path` VARCHAR(255) NOT NULL,
  `class_name` VARCHAR(100) NOT NULL,
  `description` TEXT,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `unique_recognizer` (`module_path`, `class_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table for storing anonymizer profiles
CREATE TABLE `anonymizer_profiles` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(50) NOT NULL,
  `description` TEXT,
  `is_default` BOOLEAN DEFAULT 0,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `unique_profile_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Junction table for profile-recognizer relationships
CREATE TABLE `profile_recognizer_settings` (
  `profile_id` INT NOT NULL,
  `recognizer_id` INT NOT NULL,
  `enabled` BOOLEAN DEFAULT 1,
  `parameters` JSON,
  `priority` INT NOT NULL DEFAULT 1,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`profile_id`, `recognizer_id`),
  FOREIGN KEY (`profile_id`) REFERENCES `anonymizer_profiles`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`recognizer_id`) REFERENCES `recognizer_types`(`id`) ON DELETE CASCADE,
  INDEX `idx_priority` (`priority`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert default recognizer types
INSERT INTO `recognizer_types` (
  name, module_path, class_name, description
) VALUES
('ID Card', 'chinese_anonymizer.id_card_recognizer', 'ChineseIdCardRecognizer', 'Chinese ID card number recognition'),
('Phone', 'chinese_anonymizer.phone_recognizer', 'ChinesePhoneRecognizer', 'Chinese phone number recognition'),
('Person', 'chinese_anonymizer.person_recognizer', 'ChinesePersonRecognizer', 'Chinese person name recognition'),
('Address', 'chinese_anonymizer.address_recognizer', 'ChineseAddressRecognizer', 'Chinese address recognition'),
('Inpatient', 'chinese_anonymizer.inpatient_recognizer', 'ChineseInpatientRecognizer', 'Inpatient medical record recognition'),
('Outpatient', 'chinese_anonymizer.outpatient_recognizer', 'ChineseOutpatientRecognizer', 'Outpatient medical record recognition'),
('Medical Test', 'chinese_anonymizer.medical_test_recognizer', 'ChineseMedicalTestRecognizer', 'Medical test result recognition');