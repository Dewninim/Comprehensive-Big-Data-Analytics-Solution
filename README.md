# **Comprehensive-Big-Data-Analytics-Solution** 📊

## **1. Data Collection** 📥
### **Dataset Overview**
The dataset consists of **55,500 patient records** with the following key attributes:
- **Patient Information**: Name, Age, Gender, Blood Type
- **Medical Details**: Medical Condition, Date of Admission, Discharge Date, Medication, Test Results
- **Healthcare Providers**: Doctor, Hospital, Insurance Provider
- **Billing & Administration**: Billing Amount, Room Number, Admission Type

### **Project Use Case**
#### **Problem:**
- High patient readmission rates and increasing healthcare costs due to a lack of predictive insights into patient outcomes and resource allocation.
- Difficulty in predicting patient outcomes based on factors like test results, admission type, and medical condition.

#### **Solution:**
- Implement a **big data analytics solution** using **machine learning** to **predict patient readmissions**, identify **high-risk patients**, and **optimize healthcare resources**.
- Use predictive modeling to anticipate patient outcomes and suggest cost-effective strategies without compromising patient care quality.
- Analyze trends and patterns to improve decision-making in **hospital resource allocation**.

---

## **2. Data Storage with AWS S3, EMR, and PySpark** 🗄️📂

### **Setup AWS S3 for Data Storage**
1. Navigate to **AWS S3 Console**.
2. Create an S3 bucket (e.g., `bigdata-group13`).
3. Upload the necessary files:
   - **Dataset**: `s3://bigdata-group13/dataset/input/healthcare_dataset.csv`
   - **PySpark script**: `s3://bigdata-group13/scripts/process_data.py`

### **Configure VPC for EMR**
1. Open **AWS VPC Console**.
2. Create a **new VPC** if not already available.
3. Set up **public and private subnets**.
4. Ensure **Internet Gateway** is attached for public access.
5. Configure a **security group** to allow SSH (port 22) and required access.

### **Launch EMR Cluster with S3 and VPC Integration**
1. Open **AWS EMR Console** and click **Create Cluster**.
2. Select:
   - **Cluster Type**: Hadoop and Spark enabled.
   - **VPC**: Select the configured VPC.
   - **Security Group**: Ensure SSH access is enabled.
   - **Bootstrap Actions**: None required.
3. Launch the cluster and wait until it reaches the **Waiting** state.

### **Connect to EMR Master Node via SSH**
1. Copy the **Master Node Public DNS** from the EMR console.
2. Open **Terminal / Putty** and use:
   ```bash
   ssh -i your-key.pem hadoop@<MasterPublicDNS>
   ```

### **Copy Dataset from S3 to HDFS**
```bash
hadoop fs -mkdir /input
hadoop fs -cp s3a://bigdata-group13/dataset/input/healthcare_dataset.csv /input/
```

### **Run PySpark Script on EMR**
1. Copy the script from S3 to the EMR master node:
   ```bash
   aws s3 cp s3://bigdata-group13/scripts/process_data.py .
   ```
2. Execute the PySpark job:
   ```bash
   spark-submit process_data.py
   ```

### **Store Processed Data in S3**
- Processed data is saved to:
  ```
  s3://bigdata-group13/dataset/output/
  ```
- Verify in the **AWS S3 Console**.

### **Shut Down EMR to Avoid Costs**
```bash
aws emr terminate-clusters --cluster-ids <your-cluster-id>
```

---

## **3. Data Processing** 🔄
### **Steps Taken:**
- **Data Cleaning**:
  - Removed missing values and duplicates.
  - Standardized column names.
  - Transformed the `age` column into `age_group`.
- **Aggregation and Transformation**:
  - Calculated summary statistics.
  - Saved the cleaned dataset as `processed_healthcare_data.csv`.

---

## **4. Data Analysis** 💯🚀🎯
- **Schema Verification**:
  ```python
  df.printSchema()
  df.show(25)
  ```
- **Handling Missing Data**:
  ```python
  from pyspark.sql.functions import col, sum
  df.select([sum(col(c).isNull().cast("int")).alias(c) for c in df.columns]).show()
  ```
- **Feature Engineering**:
  ```python
  from pyspark.sql.functions import mean, upper
  df = df.fillna({"Billing_amount": df.select(mean("Billing_amount")).collect()[0][0]})
  df = df.withColumn("Name", upper(col("Name")))
  ```
- **Basic Statistics & Distribution**:
  ```python
  df.describe().show()
  ```
- **Aggregation and Grouping**:
  ```python
  df.groupBy("medical_condition").count().show()
  ```
- **Correlation Analysis**:
  ```python
  from pyspark.ml.stat import Correlation
  from pyspark.ml.feature import VectorAssembler
  assembler = VectorAssembler(inputCols=["age", "billing_amount"], outputCol="features")
  df_vector = assembler.transform(df).select("features")
  correlation_matrix = Correlation.corr(df_vector, "features").collect()[0][0]
  print(correlation_matrix.toArray())
  ```

---

## **5. Data Visualization** 📈

- **Visualizations Include:**
  - Age distribution histogram.
  - Billing amount by medical condition (bar chart).
  - Age vs. Billing Amount (scatter plot).

---

## **6. Deployment on AWS** 👨‍💻

### **Launch an AWS EC2 Instance**  

- **Go to AWS EC2 Console** → [EC2 Dashboard](https://console.aws.amazon.com/ec2)  
- Click **"Launch Instance"**  
- **Choose an AMI**: Select **Ubuntu 22.04 LTS **  
- **Instance Type**: Select **t2.micro**   
- **Create Key Pair**:
  - **Key Name**: `healthcare`
  - **Format**: `.pem`  
  - Click **Create & Download**  
- **Configure Security Group**:
  - **Allow SSH (22):** Your IP  
  - **Allow Custom TCP (8888):** Anywhere (0.0.0.0/0)  
- **Launch the Instance** and wait until it's running.  

---

### **Connect to EC2 via SSH**  

- Move & Set Permissions for Key Pair  
```sh
mv ~/Downloads/healthcare.pem ~/.ssh/
chmod 400 ~/.ssh/healthcare.pem
```

- SSH Into the Instance  
```sh
ssh -i "~/.ssh/healthcare.pem" ubuntu@<your-ec2-public-ip>
```
Replace `<your-ec2-public-ip>` with your instance’s **public IPv4 address**.

---

### **Install Jupyter Notebook**  

```sh
sudo apt update -y
sudo apt install python3-pip -y
pip3 install jupyter
```

---

### **Configure Jupyter for Remote Access**  

```sh
jupyter notebook --generate-config
echo "c.NotebookApp.ip = '0.0.0.0'" >> ~/.jupyter/jupyter_notebook_config.py
```

---

### **Upload `healthcare.ipynb` to EC2**  

- From your **local machine**, run:  
```sh
scp -i "~/.ssh/healthcare.pem" healthcare.ipynb ubuntu@<your-ec2-public-ip>:/home/ubuntu/
```

---

### **Start Jupyter Notebook**  

```sh
jupyter notebook --port=8888 --no-browser --allow-root
```

- Access Jupyter from browser:  
```sh
http://<your-ec2-public-ip>:8888/tree
```
- Use the **token** shown in the terminal to log in.

- For JupyterLab:
```sh
http://<your-ec2-public-ip>:8888/lab
```

---

### **Keep Jupyter Running After Logout**  

- Install & Use `screen`  
```sh
sudo apt install screen -y
screen -S jupyter
jupyter notebook --port=8888 --no-browser --allow-root
```






