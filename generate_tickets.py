import json
import random

issues = [
    {"problem": "Unable to activate international roaming", 
     "solution": "Reset network settings and enable data roaming. Verify roaming is enabled on account.", 
     "category": "roaming"},
    
    {"problem": "Error code 5412 after SIM swap", 
     "solution": "Error 5412 indicates authentication failure. Restart device and wait 10 minutes.", 
     "category": "technical"},
    
    {"problem": "Incorrect international charges", 
     "solution": "Review call logs. Submit billing adjustment if confirmed.", 
     "category": "billing"},
    
    {"problem": "Voicemail not working after upgrade", 
     "solution": "Reset voicemail password by dialing *611.", 
     "category": "technical"},
    
    {"problem": "Cannot receive SMS codes", 
     "solution": "Check if SMS blocking is enabled.", 
     "category": "technical"},
    
    {"problem": "Slow data speeds in area", 
     "solution": "Check network maintenance. Create ticket with location and speed test.", 
     "category": "network"},
    
    {"problem": "Account locked due to payment failure", 
     "solution": "Verify payment method. Account unlock takes 2-4 hours.", 
     "category": "billing"},
    
    {"problem": "eSIM activation failing", 
     "solution": "Ensure iOS is updated. Restart and retry QR code.", 
     "category": "technical"},
    
    {"problem": "Port-in request stuck", 
     "solution": "Verify account number from old carrier. Port takes 2-24 hours.", 
     "category": "porting"},
    
    {"problem": "Device won't connect to 5G", 
     "solution": "Verify device supports 5G bands. Toggle airplane mode.", 
     "category": "network"},
]

tickets = []
for i in range(100):
    issue = random.choice(issues)
    ticket = {
        "id": f"ticket_{i}",
        "text": f"Issue: {issue['problem']} | Solution: {issue['solution']}",
        "category": issue["category"]
    }
    tickets.append(ticket)

with open('tickets.json', 'w') as f:
    json.dump(tickets, f, indent=2)

print(f"✓ Generated {len(tickets)} tickets")