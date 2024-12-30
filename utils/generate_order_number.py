import random
import string
from datetime import datetime

def generate_order_number():
    # Get the current date in YYYY-MM-DD format
    date_str = datetime.now().strftime('%Y%m%d')
    
    # Generate a random alphanumeric string of length 6
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    # Combine the date and the random string to form the order number
    order_number = f"{date_str}-{random_str}"
    return order_number
