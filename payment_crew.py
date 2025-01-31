from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from tools import (
    SendPaymentTool,
    SearchPayeesTool,
    AddPayeeTool,
    AskForMoneyTool,
    GetBalanceTool
)

# Load environment variables
load_dotenv()

# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0
)

# Create specialized agents
balance_checker = Agent(
    role='Balance Checker',
    goal='Monitor and verify account balances for all transactions',
    backstory="""You are a meticulous financial controller who specializes in 
    balance verification and monitoring. You ensure sufficient funds are available 
    for all transactions and maintain accurate balance records.""",
    verbose=True,
    allow_delegation=True,
    tools=[GetBalanceTool()],
    llm=llm
)

payee_manager = Agent(
    role='Payee Manager',
    goal='Manage and verify all payment destinations',
    backstory="""You are an expert in payment destination management, responsible 
    for maintaining accurate records of all payees. You verify existing payees 
    and set up new payment destinations when needed.""",
    verbose=True,
    allow_delegation=True,
    tools=[SearchPayeesTool(), AddPayeeTool()],
    llm=llm
)

accounts_payable = Agent(
    role='Accounts Payable Specialist',
    goal='Process outgoing payments efficiently and securely',
    backstory="""You are a skilled accounts payable specialist who ensures all 
    outgoing payments are processed correctly. You verify payment details and 
    execute transfers with precision.""",
    verbose=True,
    allow_delegation=True,
    tools=[SendPaymentTool()],
    llm=llm
)

accounts_receivable = Agent(
    role='Accounts Receivable Specialist',
    goal='Manage incoming payments and payment requests',
    backstory="""You are an experienced accounts receivable specialist who handles 
    all incoming payments and payment requests. You generate payment links and 
    track incoming funds.""",
    verbose=True,
    allow_delegation=True,
    tools=[AskForMoneyTool()],
    llm=llm
)

# Add this after the other agents
data_generator = Agent(
    role='Data Generator',
    goal='Generate mock financial data and parameters when needed',
    backstory="""You are a financial data specialist who creates realistic mock 
    data for testing and development purposes. You generate plausible bank account 
    numbers, routing numbers, and other financial parameters while following 
    standard formats and conventions.""",
    verbose=True,
    allow_delegation=True,
    tools=[],  # This agent doesn't need tools, it just generates data
    llm=llm
)

# Create tasks
def create_payment_tasks(payment_details):
    generate_mock_data = Task(
        description=f"""Generate mock bank account details for the recipient:
        {payment_details}
        Create and return a dictionary with these fields:
        - routing_number: A valid 9-digit ABA routing number
        - account_number: A plausible 10-12 digit account number
        - account_type: "checking" or "savings"
        - account_holder_name: Use the recipient's name from payment_details
        
        Format the response as a Python dictionary.""",
        agent=data_generator,
        expected_output="mock_bank_details"
    )

    verify_payee = Task(
        description=f"""Using the mock bank details from the previous task, create a payment destination:
        {payment_details}
        1. Search for existing payee using recipient email or name
        2. If not found, create new US_ACH payee using the mock bank details provided
        3. Return the payment_destination_id""",
        agent=payee_manager,
        expected_output="payment_destination_id"
    )

    check_balance = Task(
        description=f"""Check if there are sufficient funds for you to send money to the recipient:
        {payment_details}
        1. Get current balance
        2. Verify amount is available
        3. Return confirmation""",
        agent=balance_checker,
        expected_output="balance_check_confirmation"
    )

    process_payment = Task(
        description=f"""Process the payment using verified details:
        {payment_details}
        1. Use payment_destination_id from verify_payee task
        2. Confirm balance check from check_balance task
        3. Execute payment
        4. Return confirmation""",
        agent=accounts_payable,
        expected_output="payment_confirmation"
    )

    return [generate_mock_data, verify_payee, check_balance, process_payment]

# Create the crew
def create_payment_crew(payment_details):
    payment_crew = Crew(
        agents=[data_generator, payee_manager, balance_checker, accounts_payable, accounts_receivable],
        tasks=create_payment_tasks(payment_details),
        verbose=True
    )
    return payment_crew

# Example usage
if __name__ == "__main__":
    # Example payment details
    payment_details = {
        "amount_decimal": 100.00,
        "recipient_name": "John Doe",
        "recipient_email": "john@example.com",
        "memo": "Test payment"
    }
    
    # Create and run the crew
    crew = create_payment_crew(payment_details)
    result = crew.kickoff()
    print("\nCrew Results:", result) 