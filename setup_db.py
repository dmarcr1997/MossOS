# setup_database.py
import sqlite3  # Import sqlite3 for database operations
import os  # Import os for file path verification
import PyPDF2  # Import PyPDF2 for PDF text extraction

# Connect to SQLite database
conn = sqlite3.connect('research_papers.db')  # Create/connect to research_papers.db
cursor = conn.cursor()  # Create cursor for executing queries

# Create papers table to store paper metadata
cursor.execute('''
    CREATE TABLE IF NOT EXISTS papers
    (id INTEGER PRIMARY KEY, title TEXT, authors TEXT, file_path TEXT, module TEXT)
''')

# Create progress table to track user progress
cursor.execute('''
    CREATE TABLE IF NOT EXISTS progress
    (id INTEGER PRIMARY KEY, module TEXT, completed BOOLEAN, score REAL, project TEXT)
''')

# Create paper_content table to store extracted PDF text
cursor.execute('''
    CREATE TABLE IF NOT EXISTS paper_content
    (id INTEGER PRIMARY KEY, paper_id INTEGER, content TEXT, FOREIGN KEY(paper_id) REFERENCES papers(id))
''')

# List of 36 papers with title, authors, file_path, and module
papers = [
    ('Mechatronics: A Study on Its Scientific Constitution', 'Rocha, A. P., et al.', 'papers/mechatronics_study.pdf', 'Module 1: Fundamentals of Mechatronics'),
    ('Zeptonewton and Attotesla per Centimeter Metrology with Coupled Oscillators', 'Bouche, I., et al.', 'papers/zeptonewton_metrology.pdf', 'Module 1: Fundamentals of Mechatronics'),
    ('Embedded Systems in Mechatronics: Real-Time Applications', 'Unknown Authors', 'papers/embedded_systems_mechatronics.pdf', 'Module 2: Embedded Systems'),
    ('Smart Materials for Mechatronic Applications', 'Unknown Authors', 'papers/smart_materials_mechatronics.pdf', 'Module 7: Bionic Materials'),
    ('Energy-Efficient Mechatronic Systems', 'Unknown Authors', 'papers/energy_efficient_mechatronics.pdf', 'Module 1: Fundamentals of Mechatronics'),
    ('Advanced Control Algorithms for Robotic Exoskeletons', 'Unknown Authors', 'papers/exoskeleton_control_algorithms.pdf', 'Module 3: Control Systems'),
    ('Control Strategies for Bionic Limbs: A Review', 'Unknown Authors', 'papers/bionic_limbs_control.pdf', 'Module 4: Introduction to Bionics'),
    ('Review of Robotic Prostheses Manufactured with 3D Printing', 'Salazar, M., et al.', 'papers/3d_printed_prostheses.pdf', 'Module 4: Introduction to Bionics'),
    ('Robotic Prostheses: Design for Accessibility', 'Unknown Authors', 'papers/prostheses_design_accessibility.pdf', 'Module 4: Introduction to Bionics'),
    ('Neural Interfaces for Bionic Systems: Current Trends and Future Challenges', 'Unknown Authors', 'papers/neural_interfaces_bionics.pdf', 'Module 5: Neural Interfaces'),
    ('Human-Machine Interfaces for Bionic Systems', 'Unknown Authors', 'papers/human_machine_interfaces.pdf', 'Module 5: Neural Interfaces'),
    ('Neural Control of Bionic Limbs: Current Trends', 'Unknown Authors', 'papers/neural_control_bionic_limbs.pdf', 'Module 5: Neural Interfaces'),
    ('Bioinspired Robotics: From Nature to Engineering', 'Wang, J., et al.', 'papers/bioinspired_robotics.pdf', 'Module 6: Advanced Robotics'),
    ('Soft Robotics for Medical Applications', 'Unknown Authors', 'papers/soft_robotics_medical.pdf', 'Module 6: Advanced Robotics'),
    ('Haptics in Robotics: Design and Implementation', 'Unknown Authors', 'papers/haptics_robotics_design.pdf', 'Module 6: Advanced Robotics'),
    ('Advanced Materials for Soft Robotics: Fabrication and Applications', 'Unknown Authors', 'papers/soft_robotics_materials.pdf', 'Module 7: Bionic Materials'),
    ('Soft Actuators for Bionic Applications: Materials and Mechanisms', 'Unknown Authors', 'papers/soft_actuators_bionics.pdf', 'Module 7: Bionic Materials'),
    ('Bionic Skin: Sensors and Materials', 'Unknown Authors', 'papers/bionic_skin_sensors.pdf', 'Module 7: Bionic Materials'),
    ('Wearable Robotics for Rehabilitation: Design and Control', 'Unknown Authors', 'papers/wearable_robotics_rehab.pdf', 'Module 8: Wearable Robotics'),
    ('Exoskeletons for Industrial Applications', 'Unknown Authors', 'papers/exoskeletons_industrial.pdf', 'Module 8: Wearable Robotics'),
    ('Soft Exoskeletons: Materials and Control', 'Unknown Authors', 'papers/soft_exoskeletons_control.pdf', 'Module 8: Wearable Robotics'),
    ('Machine Learning in Mechatronics: Predictive Maintenance Applications', 'Unknown Authors', 'papers/ml_mechatronics_maintenance.pdf', 'Module 9: Machine Learning for Mechatronics'),
    ('Machine Learning for Bionic Control Systems', 'Unknown Authors', 'papers/ml_bionic_control.pdf', 'Module 9: Machine Learning for Mechatronics'),
    ('AI in Mechatronics: Applications and Challenges', 'Unknown Authors', 'papers/ai_mechatronics_applications.pdf', 'Module 9: Machine Learning for Mechatronics'),
    ('Bionic Vision Systems: Progress and Challenges', 'Unknown Authors', 'papers/bionic_vision_systems.pdf', 'Module 10: Advanced Bionic Systems'),
    ('Bionic Hearing Systems: Advances in Cochlear Implants', 'Unknown Authors', 'papers/bionic_hearing_systems.pdf', 'Module 10: Advanced Bionic Systems'),
    ('Bionic Systems for Space Exploration', 'Unknown Authors', 'papers/bionic_systems_space.pdf', 'Module 10: Advanced Bionic Systems'),
    ('Ethics of Bionic Systems: Balancing Innovation and Responsibility', 'Unknown Authors', 'papers/bionics_ethics.pdf', 'Module 11: Ethics and Regulation'),
    ('Regulatory Challenges for Bionic Devices: Global Perspectives', 'Unknown Authors', 'papers/bionic_regulatory_challenges.pdf', 'Module 11: Ethics and Regulation'),
    ('Regulatory Frameworks for Bionic Innovations', 'Unknown Authors', 'papers/bionic_regulatory_frameworks.pdf', 'Module 11: Ethics and Regulation'),
    ('Capstone Project: Designing a Bionic Hand', 'Tejada, J. C., et al.', 'papers/bionic_hand_design.pdf', 'Module 12: Capstone Project'),
    ('3D Printing of Bionic Structures: Design and Fabrication', 'Unknown Authors', 'papers/3d_printing_bionic_structures.pdf', 'Module 12: Capstone Project'),
    ('Biohybrid Systems: Integrating Biology and Robotics', 'Unknown Authors', 'papers/biohybrid_systems.pdf', 'Module 12: Capstone Project'),
    ('Bionic Sensors: Design and Applications', 'Unknown Authors', 'papers/bionic_sensors_design.pdf', 'Module 3: Control Systems'),
    ('Haptic Feedback in Bionic Prostheses: Current Advances', 'Unknown Authors', 'papers/haptic_feedback_prostheses.pdf', 'Module 3: Control Systems'),
    ('Energy Harvesting for Wearable Mechatronic Systems', 'Unknown Authors', 'papers/energy_harvesting_mechatronics.pdf', 'Module 2: Embedded Systems'),
]

# Insert papers into the database
cursor.executemany('INSERT OR REPLACE INTO papers (title, authors, file_path, module) VALUES (?, ?, ?, ?)', papers)

# Extract text from PDFs and store in paper_content table
for i, (_, _, file_path, _) in enumerate(papers, 1):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                content = ""
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        content += text + "\n"
                # Truncate content to avoid LLM context limit (e.g., 2048 tokens)
                content = content[:10000]  # Adjust based on LLM capacity
                cursor.execute('INSERT OR REPLACE INTO paper_content (paper_id, content) VALUES (?, ?)', (i, content))
                print(f"Extracted content for {file_path}")
        else:
            print(f"Warning: {file_path} not found")
            cursor.execute('INSERT OR REPLACE INTO paper_content (paper_id, content) VALUES (?, ?)', (i, ""))
    except Exception as e:
        print(f"Error extracting {file_path}: {str(e)}")
        cursor.execute('INSERT OR REPLACE INTO paper_content (paper_id, content) VALUES (?, ?)', (i, ""))

# Insert sample progress entry
cursor.execute('INSERT OR REPLACE INTO progress (module, completed, score, project) VALUES (?, ?, ?, ?)',
               ('Module 1: Fundamentals of Mechatronics', False, 0.0, ''))

# Commit changes and close connection
conn.commit()
conn.close()

# Verify file paths
for _, _, file_path, _ in papers:
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} does not exist. Ensure the PDF is in the papers directory.")