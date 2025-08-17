# **Daily Transactions ETL Pipeline**

This project sets up an **Airflow DAG** that:

1. Runs **daily**
2. Reads transactions data from a **local CSV** (simulating S3 ingestion)
3. Performs **data cleaning + aggregation** in Python
4. Loads the transformed results into a **MySQL database**



## **1. Prerequisites**

* Python **3.8+**
* Pip or Conda environment
* MySQL installed locally on Windows
* Airflow installed locally

---

## **2. Python Environment Setup**

1. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install required Python libraries:

   ```bash
   pip install apache-airflow pandas mysql-connector-python
   ```

---

## **3. Apache Airflow Setup (Local)**

1. Initialize Airflow home:

   ```bash
   mkdir %USERPROFILE%\airflow
   setx AIRFLOW_HOME %USERPROFILE%\airflow
   ```

2. Initialize Airflow metadata DB:

   ```bash
   airflow db init
   ```

3. Create a user account:

   ```bash
   airflow users create \
      --username admin \
      --firstname First \
      --lastname Last \
      --role Admin \
      --email admin@example.com \
      --password admin
   ```

4. Start Airflow services:

   ```bash
   airflow webserver -p 8080
   airflow scheduler
   ```

5. Place the DAG file (`dag.py`) in:

   ```
   %USERPROFILE%\airflow\dags\
   ```

---

## **4. MySQL Setup on Windows**

1. **Install MySQL**

   * Download from [MySQL Installer](https://dev.mysql.com/downloads/installer/)
   * During setup:

     * Choose **Server Only** or **Developer Default**
     * Set username = `root`
     * Set password = your choice (e.g., `password123`)

2. **Verify Installation**

   ```bash
   mysql -u root -p
   ```

3. **Create Database**

   ```sql
   CREATE DATABASE testdb;
   USE testdb;
   ```

4. **Create Tables (if not auto-created by script)**

   ```sql
   CREATE TABLE transactions (
       id INT AUTO_INCREMENT PRIMARY KEY,
       date DATE,
       bank_id VARCHAR(255),
       customer_id VARCHAR(255),
       amount DOUBLE
   );

   CREATE TABLE daily_transactions (
       id INT AUTO_INCREMENT PRIMARY KEY,
       date DATE,
       bank_id VARCHAR(255),
       total_amount DOUBLE
   );
   ```

---

## **5. CSV Input**

Sample CSV file (`transactions.csv`) should be placed in `data/` folder:

```csv
date,bank_id,amount,customer_id
2025-08-15,HDFC,1000,CUST1
2025-08-15,ICICI,2000,CUST2
2025-08-15,HDFC,500,CUST3
2025-08-16,SBI,1200,CUST1
2025-08-16,ICICI,700,CUST2
```

---

## **6. Run the DAG**

1. Start Airflow webserver + scheduler

   ```bash
   airflow webserver -p 8080
   airflow scheduler
   ```

2. Open Airflow UI: [http://localhost:8080](http://localhost:8080)

3. Enable the DAG: **`daily_transactions_dag`**

---

## **7. Analytics Queries**

Run the following queries in MySQL for insights:

* **Top 5 banks by volume in last 7 days**

  ```sql
  SELECT bank_id, SUM(total_amount) AS total_volume
  FROM daily_transactions
  WHERE date >= CURDATE() - INTERVAL 7 DAY
  GROUP BY bank_id
  ORDER BY total_volume DESC
  LIMIT 5;
  ```

* **Average transaction per customer for a given month**

  ```sql
  SELECT customer_id, AVG(amount) AS avg_transaction_value
  FROM transactions
  WHERE DATE_FORMAT(date, '%Y-%m') = '2025-08'
  GROUP BY customer_id;
  ```# EFT-Corporation
EFT Corporation
