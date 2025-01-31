# PayCrew 👥💰

Build AI crews that can handle payment operations using natural language with CrewAI and Payman. PayCrew creates specialized AI agents that work together to process financial transactions securely and efficiently.

## The Crew 🤖

PayCrew consists of five specialized agents working together:

1. **Data Generator** 📊
   - Generates realistic mock financial data for testing
   - Creates valid bank account and routing numbers
   - Ensures data follows standard formats

2. **Payee Manager** 👥
   - Manages payment destinations
   - Searches for existing payees
   - Creates new payment destinations
   - Tools: SearchPayeesTool, AddPayeeTool

3. **Balance Checker** 💰
   - Monitors account balances
   - Verifies sufficient funds
   - Maintains accurate balance records
   - Tools: GetBalanceTool

4. **Accounts Payable** 💸
   - Processes outgoing payments
   - Verifies payment details
   - Executes transfers securely
   - Tools: SendPaymentTool

5. **Accounts Receivable** 📥
   - Handles incoming payments
   - Generates payment requests
   - Creates checkout links
   - Tools: AskForMoneyTool

## Quick Start 🚀

1. Get your API keys:
   - Get your Payman API key from [app.paymanai.com](https://app.paymanai.com)
   - Get your OpenAI API key from [platform.openai.com](https://platform.openai.com)

2. Clone and setup:
```bash
# Clone the repository
git clone https://github.com/paymanai/paycrew.git
cd paycrew

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. Configure environment:
```bash
# Create .env file with your API keys
OPENAI_API_KEY=your_openai_api_key
PAYMAN_API_SECRET=your_payman_api_secret
PAYMAN_ENVIRONMENT=sandbox
```

4. Run a test payment:
```python
python payment_crew.py
```

## How It Works 🔄

1. **Data Generation**
   - Data Generator creates mock bank details when needed
   - Ensures realistic test data for development

2. **Payee Verification**
   - Payee Manager searches for existing payee
   - Creates new payee if not found using generated data
   - Returns payment destination ID

3. **Balance Check**
   - Balance Checker verifies sufficient funds
   - Ensures transaction can proceed

4. **Payment Processing**
   - Accounts Payable processes the payment
   - Uses verified payee and balance information
   - Returns payment confirmation

## Security 🔒

- Never commit your `.env` file
- Keep API keys secure
- Use sandbox environment for testing
- Always verify payment details
- Follow security best practices

## Development 🛠️

### Project Structure
```
paycrew/
├── payment_crew.py     # Main crew implementation
├── tools.py           # CrewAI tool wrappers
├── requirements.txt   # Project dependencies
├── .env              # API keys (not in repo)
└── README.md         # Documentation
```

### Adding New Features
1. Create new tools in `tools.py`
2. Add new agents to `payment_crew.py`
3. Update task workflows as needed
4. Test thoroughly in sandbox

## Contributing 🤝

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License 📄

MIT

## Support 💬

- Documentation: [docs.paymanai.com](https://docs.paymanai.com)
- Issues: [GitHub Issues](https://github.com/paymanai/paycrew/issues)
- Email: support@paymanai.com
