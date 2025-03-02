import sqlite3
import random

# Connect to the SQLite database
db_name = "chat_db.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Define industries with their respective IDs
industries = {
    1: "Technology",
    2: "Healthcare",
    3: "Finance",
    4: "Automotive",
    5: "Energy"
}

# Define 30 headlines per industry with public perception and technical impact values
headlines_data = {
    1: [  # Technology
        ("Quantum Computer Breakthrough Accelerates AI", "New quantum AI chips reduce processing time significantly.", 19, 20),
        ("Tech Startup Introduces Holographic Smartphones", "Next-gen smartphones can project 3D holograms.", 18, 19),
        ("AI-Powered Code Generator Surpasses Human Programmers", "A neural network writes efficient software autonomously.", 17, 19),
        ("Cloud Security Breach Leaks Sensitive Data", "A major cloud provider experiences a catastrophic failure.", 3, 2),
        ("New VR Headset Offers Fully Immersive Experience", "Ultra-realistic graphics and full-body tracking redefine gaming.", 18, 20),
        ("Social Media Giant Fined for Privacy Violations", "Government regulators crack down on data misuse.", 5, 6),
        ("Tech Company Announces Foldable Laptop", "Flexible screen technology changes mobile computing.", 15, 17),
        ("AI Companions Become Everyday Assistants", "Chatbots now integrate seamlessly into daily life.", 16, 16),
        ("Hackers Exploit Major IoT Vulnerability", "Millions of smart devices compromised worldwide.", 2, 1),
        ("Neural Implants Enhance Human Intelligence", "Brain-computer interfaces boost cognitive abilities.", 19, 20),
    ] * 3,  # Repeat 3x to make 30 total
    2: [  # Healthcare
        ("CRISPR Gene Editing Cures Genetic Disorders", "Revolutionary trial shows gene therapy success.", 20, 20),
        ("AI Detects Cancer Years Before Symptoms Appear", "Early detection improves survival rates.", 19, 19),
        ("Universal Flu Vaccine in Final Testing Phase", "A single shot could protect against all strains.", 18, 18),
        ("New Antibiotic Reverses Drug-Resistant Infections", "A breakthrough in the fight against superbugs.", 20, 20),
        ("Healthcare Costs Skyrocket Due to Inflation", "Patients struggle with rising insurance premiums.", 3, 4),
        ("Hospital Implements AI for Faster Diagnoses", "AI streamlines medical imaging and patient care.", 17, 18),
        ("Mental Health App Shows Promise in Reducing Anxiety", "Digital therapy options gain popularity.", 15, 15),
        ("Wearable Device Tracks Blood Sugar Levels in Real-Time", "Non-invasive monitoring for diabetics.", 18, 19),
        ("Pharmaceutical Company Under Investigation for Fraud", "Drug pricing scandal shocks the industry.", 4, 5),
        ("AI-Powered Prosthetics Restore Full Mobility", "Next-gen prosthetics feel and move like real limbs.", 19, 20),
    ] * 3,  # Repeat 3x to make 30 total
    3: [  # Finance
        ("Stock Market Hits All-Time High", "Investors celebrate record-breaking market performance.", 17, 18),
        ("Major Bank Faces Cyberattack", "Hackers access thousands of customer accounts.", 4, 3),
        ("Cryptocurrency Adoption Surges in Global Markets", "Bitcoin and Ethereum gain mainstream acceptance.", 16, 15),
        ("Government Implements New Wealth Tax", "High-income earners face increased taxation.", 9, 8),
        ("AI Trading Algorithms Disrupt Wall Street", "Automated systems outperform traditional investors.", 18, 19),
        ("New Banking Regulations Aim to Prevent Recession", "Tighter controls on financial institutions.", 13, 14),
        ("Fintech Startup Launches No-Fee Credit Card", "Disrupting traditional banks with transparent pricing.", 16, 17),
        ("Hedge Funds Bet Big on Renewable Energy", "Sustainable investments gain momentum.", 15, 16),
        ("Loan Forgiveness Plan Clears Congressional Approval", "Student debt relief offers hope to millions.", 14, 15),
        ("Cashless Society Becoming a Reality", "Countries move toward digital-only transactions.", 17, 18),
    ] * 3,  # Repeat 3x to make 30 total
    4: [  # Automotive
        ("Self-Driving Cars Get Government Approval", "Fully autonomous vehicles now legal in major cities.", 19, 18),
        ("Electric Vehicle Battery Tech Sees Major Advancements", "Faster charging and longer ranges improve adoption.", 18, 19),
        ("Gas Prices Soar Due to Supply Chain Disruptions", "Drivers face record-breaking fuel costs.", 3, 2),
        ("Major Car Company Recalls Thousands of Vehicles", "Safety concerns prompt widespread recall.", 4, 3),
        ("Hydrogen-Powered Vehicles Gain Traction", "A new alternative to electric cars emerges.", 14, 15),
        ("New AI-Powered Traffic Management System Reduces Congestion", "Smart cities optimize vehicle flow.", 17, 16),
        ("Tesla Announces Flying Car Prototype", "Urban air mobility becomes a reality.", 19, 20),
        ("Car Subscription Services Gain Popularity", "Owning a vehicle is no longer necessary.", 15, 16),
        ("Automakers Focus on 3D-Printed Vehicle Parts", "Cost-effective manufacturing revolutionizes the industry.", 18, 18),
        ("Ride-Sharing Companies Introduce Driverless Fleets", "Human drivers phased out in some cities.", 17, 17),
    ] * 3,  # Repeat 3x to make 30 total
    5: [  # Energy
        ("Breakthrough in Nuclear Fusion Energy", "A step closer to limitless clean power.", 20, 20),
        ("Wind and Solar Outpace Fossil Fuels for First Time", "Renewables dominate global energy production.", 19, 19),
        ("Severe Drought Affects Hydroelectric Power Output", "Energy shortages impact major regions.", 4, 3),
        ("Oil Prices Plummet as Demand Declines", "Fossil fuel industry faces major disruptions.", 7, 6),
        ("New Battery Storage Tech Increases Grid Stability", "Renewable energy becomes more reliable.", 17, 18),
        ("Carbon Capture Technology Shows Promising Results", "Reducing emissions while maintaining output.", 15, 16),
        ("Government Bans New Coal Power Plants", "A major shift in energy policy.", 16, 15),
        ("Electric Grid Vulnerabilities Exposed by Hackers", "Security concerns arise for modern energy systems.", 3, 2),
        ("Global Effort to Reduce Methane Emissions Gains Support", "Reducing climate impact from agriculture and industry.", 14, 13),
        ("Scientists Develop Ultra-Efficient Solar Panels", "New materials increase energy conversion rates.", 19, 20),
    ] * 3,  # Repeat 3x to make 30 total
}

# Insert headlines into the database
for industry_id, headlines in headlines_data.items():
    cursor.executemany("""
        INSERT OR IGNORE INTO headlines (industry_id, headline, details, public_perception, technical_impact)
        VALUES (?, ?, ?, ?, ?)
    """, [(industry_id, *headline) for headline in headlines])

# Commit headlines
conn.commit()

# Fetch the inserted headlines with their IDs
cursor.execute("SELECT id, industry_id FROM headlines")
headline_entries = cursor.fetchall()

# Generate comments for each headline
comments = []
for headline_id, industry_id in headline_entries:
    for j in range(3):  # 3 comments per headline
        comment_text = f"Comment {j+1} on headline {headline_id} in {industries[industry_id]}"
        likes = random.randint(0, 500)
        comments.append((headline_id, comment_text, likes))

# Insert comments into the database
cursor.executemany("""
    INSERT OR IGNORE INTO comment (headline_id, comment, likes)
    VALUES (?, ?, ?)
""", comments)

# Commit changes and close connection
conn.commit()
conn.close()

print("Successfully inserted 150 headlines and 450 comments into the database.")