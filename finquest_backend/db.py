import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def init_db():
    db = get_db_connection()
    print("======> db connected")
    cursor = db.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        password VARCHAR(100),
        dob DATE,
        salary DECIMAL(10, 2)
    );
    """)
    db.commit()
    print("======> Users table created")
    cursor.close()

    # 2. Transactions Table
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        category ENUM('Travel', 'Shopping', 'Grocery', 'Food', 'Personal', 'Education', 'Bills', 'Other') NOT NULL,
        type ENUM('expense', 'income') NOT NULL,
        mode ENUM('upi', 'cash', 'others', 'card') NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    db.commit()
    print("======> Transactions table created")
    cursor.close()

    # 3. Profile Build Table
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profile_build (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Food DECIMAL(10, 2) DEFAULT 0,
        Travel DECIMAL(10, 2) DEFAULT 0,
        Shopping DECIMAL(10, 2) DEFAULT 0,
        Grocery DECIMAL(10, 2) DEFAULT 0,
        Personal DECIMAL(10, 2) DEFAULT 0,
        Education DECIMAL(10, 2) DEFAULT 0,
        Bills DECIMAL(10, 2) DEFAULT 0,
        Other DECIMAL(10, 2) DEFAULT 0
    );
    """)
    db.commit()
    print("======> Profile Build table created")
    cursor.close()

    # 4. Goals Table
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INT AUTO_INCREMENT PRIMARY KEY,
        amount DECIMAL(10, 2) NOT NULL,
        status ENUM('completed', 'incompleted', 'deleted') NOT NULL
    );
    """)
    db.commit()
    print("======> Goals table created")
    cursor.close()

    # 5. Available Badges Table
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS available_badges (
        badge_id INT AUTO_INCREMENT PRIMARY KEY,
        badge_image VARCHAR(255),
        badge_desc TEXT,
        badge_url VARCHAR(255),
        badge_criteria TEXT
    );
    """)
    db.commit()
    print("======> Available Badges table created")
    cursor.close()

    # 6. Issued Badges Table
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS issued_badges (
        badge_id INT PRIMARY KEY,
        id INT ,
        issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    db.commit()
    print("======> Issued Badges table created")
    cursor.close()

    # 7. Streaks Table
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS streaks (
        id INT PRIMARY KEY,
        count INT DEFAULT 0
    );
    """)
    db.commit()
    print("======> available_badges table created")
    cursor.close()

    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM available_badges;")
    count = cursor.fetchone()[0]
    cursor.close()

    if count == 0:
        cursor = db.cursor()
        cursor.execute("""
        INSERT INTO available_badges (badge_image, badge_desc, badge_url, badge_criteria) VALUES
        ('badge_streak_3.png', 'Earned for maintaining a 3-day activity streak!', 'https://yourcdn.com/badges/streak3', 'streak >= 3'),
        ('badge_streak_7.png', 'Awarded for a full week of consistent finance tracking!', 'https://yourcdn.com/badges/streak7', 'streak >= 7'),
        ('badge_first_goal.png', 'Congrats on completing your first goal!', 'https://yourcdn.com/badges/firstgoal', 'goals_completed >= 1'),
        ('badge_saver.png', 'Saved over ₹5,000 across categories. Smart spender!', 'https://yourcdn.com/badges/saver', 'total_saved >= 5000'),
        ('badge_consistent_tracker.png', 'Logged transactions for 10 days in a row!', 'https://yourcdn.com/badges/consistent', 'days_active >= 10'),
        ('badge_budget_master.png', 'Spent wisely within all budget categories this month.', 'https://yourcdn.com/badges/budgetmaster', 'all_categories_within_budget = TRUE'),
        ('badge_goal_crusher.png', 'Completed 5 financial goals. You’re unstoppable!', 'https://yourcdn.com/badges/goalcrusher', 'goals_completed >= 5'),
        ('badge_xp_level_5.png', 'Reached XP level 5. Leveling up in life!', 'https://yourcdn.com/badges/level5', 'xp_level >= 5'),
        ('badge_upi_user.png', 'Used UPI for 10 transactions. Digital native!', 'https://yourcdn.com/badges/upiuser', 'upi_transactions >= 10'),
        ('badge_first_transaction.png', 'Logged your very first transaction. Welcome aboard!', 'https://yourcdn.com/badges/firsttxn', 'transactions_count = 1');
        """)
        db.commit()
        print("======> Sample badges inserted")
        cursor.close()
    else:
        print("======> Badges already present, skipping insert")

    db.commit()
    print("======> Sample badges inserted")
    cursor.close()

    db.commit()
    print("======> Streaks table created")
    cursor.close()
    
    db.close()
