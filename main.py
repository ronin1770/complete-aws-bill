import boto3
from datetime import datetime, timedelta

def validate_dates(start_date, end_date):
    today = datetime.today()
    earliest_allowed = today - timedelta(days=450)  # Approx 15 months
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    if start < earliest_allowed:
        raise ValueError(f"Start date {start_date} is too old! Earliest allowed is {earliest_allowed.date()}.")

    if end > today:
        raise ValueError(f"End date {end_date} is in the future!")

def get_usage_costs(start_date, end_date):
    ce = boto3.client('ce')

    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[
            {'Type': 'DIMENSION', 'Key': 'SERVICE'},
            {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}
        ],
        Filter={
            "Not": {
                "Dimensions": {
                    "Key": "RECORD_TYPE",
                    "Values": ["Credit"]
                }
            }
        }
    )

    service_costs = {}
    for group in response['ResultsByTime'][0]['Groups']:
        service_name = group['Keys'][0]
        usage_type = group['Keys'][1]
        amount = float(group['Metrics']['UnblendedCost']['Amount'])

        if amount != 0:
            if service_name not in service_costs:
                service_costs[service_name] = []
            service_costs[service_name].append((usage_type, amount))

    return service_costs

def get_credits(start_date, end_date):
    ce = boto3.client('ce')

    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        Filter={
            "Dimensions": {
                "Key": "RECORD_TYPE",
                "Values": ["Credit"]
            }
        }
    )

    credits_total = float(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
    return credits_total

def print_cost_report(service_costs, credits_total):
    net_spend = 0

    for service, usage_list in service_costs.items():
        total_cost = sum(amount for _, amount in usage_list)
        net_spend += total_cost

        print(f"\n--- {service} --- (Total: ${total_cost:.2f})")
        for usage_type, cost in sorted(usage_list, key=lambda x: x[1], reverse=True):
            print(f"    {usage_type}: ${cost:.2f}")

    # Credits section
    if credits_total != 0:
        print(f"\n--- Credits Applied ---")
        print(f"   Total Credits: ${abs(credits_total):.2f}")
        net_spend += credits_total  # credits are negative

    print(f"\n=== Net Spend after Credits: ${net_spend:.2f} ===")

if __name__ == "__main__":
    start = '2025-03-01'
    end = '2025-03-31'

    validate_dates(start, end)

    service_costs = get_usage_costs(start, end)
    credits_total = get_credits(start, end)

    print_cost_report(service_costs, credits_total)
