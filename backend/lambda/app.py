import json
import math

def lambda_handler(event, context):
    # Handle CORS preflight requests
    if event.get('httpMethod') == 'OPTIONS':
        return create_response(200, {})

    try:
        body = json.loads(event.get('body', '{}'))
        calc_type = body.get('type')
        principal = float(body.get('principal', 0))
        rate = float(body.get('rate', 0)) / 100  # Convert percentage to decimal
        time = float(body.get('time', 0))       # In years

        if calc_type == 'compound':
            n = float(body.get('compounding_frequency', 1))  # 1 = Annually, 12 = Monthly, etc.
            # Formula: A = P(1 + r/n)^(nt)
            amount = principal * math.pow((1 + rate / n), (n * time))
            interest_earned = amount - principal
            result = {
                "total_balance": round(amount, 2),
                "interest_earned": round(interest_earned, 2)
            }
            
        elif calc_type == 'emi':
            # Monthly EMI formula: [P x R x (1+R)^N] / [((1+R)^N)-1]
            monthly_rate = rate / 12
            months = time * 12
            
            if monthly_rate == 0:
                emi = principal / months
            else:
                emi = (principal * monthly_rate * math.pow(1 + monthly_rate, months)) / \
                      (math.pow(1 + monthly_rate, months) - 1)
                      
            total_payment = emi * months
            total_interest = total_payment - principal
            result = {
                "monthly_emi": round(emi, 2),
                "total_payment": round(total_payment, 2),
                "total_interest": round(total_interest, 2)
            }
        else:
            return create_response(400, {"error": "Invalid calculation type. Use 'compound' or 'emi'."})

        return create_response(200, result)

    except Exception as e:
        return create_response(500, {"error": str(e)})

def create_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST"
        },
        "body": json.dumps(body)
    }