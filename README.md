# Complete AWS Bill

A lightweight Python tool that fetches and analyzes AWS billing data, including **usage costs** and **credit utilization**, using the **Boto3 Cost Explorer API**.

- 🏷️ Grouped by **Service** and **Usage Type**
- 💵 Shows **Credits applied** separately
- 📈 Calculates **Net Spend** after Credits
- 🕵️ Useful for spotting **billing leaks** and **optimizing costs**
- 🌎 Open-source and easy to extend!

---

## 🚀 Features

- Fetch AWS billing details for a **custom date range** (start and end dates).
- Breaks down **costs by Service** and **Usage Type**.
- Separately fetches and **applies Credits** (e.g., promotional, support, EDP).
- Provides **net spend** calculation after credits.
- Python 3.x compatible.
- Lightweight and dependency-free (only needs `boto3`).

---

## ⚙️ Requirements

- Python 3.7+
- AWS credentials configured (via environment variables, AWS CLI, or `boto3` profiles).

Install boto3 if you haven't:

```bash
pip install boto3
```

```bash
pip install -r requirements.txt
```

Make sure your IAM role or user has **Cost Explorer permissions**:
- `ce:GetCostAndUsage`

---

## 🛠️ Usage

1. Clone the repository:

```bash
git clone https://github.com/yourusername/aws-cost-analyzer.git
cd aws-cost-analyzer
```

2. Configure your AWS credentials (if not already set up):

```bash
aws configure
```

3. Run the script:

```bash
python aws_cost_analyzer.py
```

You can modify the `start_date` and `end_date` inside the script, or extend it to accept them as command-line arguments.

---

## 🧩 Example Output

```plaintext
--- Amazon Elastic Compute Cloud - Compute --- (Total: $325.76)
    USE1-EBS:VolumeUsage.gp2: $123.45
    USE1-NATGateway-Hours: $67.89

--- Amazon S3 --- (Total: $45.12)
    USE1-Requests-Tier1: $15.12

--- Credits Applied ---
   Total Credits: $23.33

=== Net Spend after Credits: $347.55 ===
```

---

## 📚 How It Works

- **Step 1:** Query AWS Cost Explorer for usage costs (excluding credits).
- **Step 2:** Query AWS Cost Explorer separately for credits.
- **Step 3:** Merge the two datasets.
- **Step 4:** Print a detailed cost breakdown and net spend.

---

## 📈 Future Improvements

- Export reports to CSV/Excel
- Add support for daily or hourly granularity
- Compare two months side-by-side
- Slack/Email alert for anomalies
- Generate visual charts 📊

---

## 🤝 Contributing

Pull requests are welcome!  
If you find bugs, have feature requests, or just want to make it better — feel free to open an issue or PR.

---

## 🪪 License

MIT License.  
Feel free to use, modify, and distribute.

If you like my work, please subscribe to my Instagram Channel @motivation_nitrous (https://www.instagram.com/motivation_nitrous/)
