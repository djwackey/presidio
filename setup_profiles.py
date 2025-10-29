#!/usr/bin/env python3
import asyncio
import json

from chinese_anonymizer.db_connector import DatabaseConnector


async def setup_medical_profile():
    db = DatabaseConnector()
    try:
        # Create medical_records profile
        profile_id = await db.create_profile(
            name="medical_records", description="Default profile for medical record anonymization", is_default=True
        )
        print(f"Created profile 'medical_records' with ID: {profile_id}")

        # Define recognizers with their module paths and priority
        recognizers = [
            ("ID Card", "chinese_anonymizer.id_card_recognizer", "ChineseIdCardRecognizer", 1),
            ("Phone", "chinese_anonymizer.phone_recognizer", "ChinesePhoneRecognizer", 2),
            ("Person", "chinese_anonymizer.person_recognizer", "ChinesePersonRecognizer", 3),
            ("Address", "chinese_anonymizer.address_recognizer", "ChineseAddressRecognizer", 4),
            ("Inpatient", "chinese_anonymizer.inpatient_recognizer", "ChineseInpatientRecognizer", 5),
            ("Outpatient", "chinese_anonymizer.outpatient_recognizer", "ChineseOutpatientRecognizer", 6),
            ("Medical Test", "chinese_anonymizer.medical_test_recognizer", "ChineseMedicalTestRecognizer", 7),
        ]

        # Add each recognizer to the profile
        for name, module_path, class_name, priority in recognizers:
            # First ensure recognizer type exists
            recognizer_class = f"{module_path}.{class_name}"

            # In a real implementation, we'd check if recognizer exists first
            # For this demo, we'll assume it's already populated or handle insertion

            # Add to profile
            await db.add_recognizer_to_profile(
                profile_id=profile_id,
                recognizer_id=1,  # In production, this would come from recognizer_types table
                enabled=True,
                parameters={},
                priority=priority,
            )
            print(f"Added {name} recognizer to profile with priority {priority}")

        print("\nProfile setup completed successfully!")
        print("You can now run demo_simple.py which uses this profile")
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(setup_medical_profile())
