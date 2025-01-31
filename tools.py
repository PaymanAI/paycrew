from crewai.tools import BaseTool
from pydantic import Field
from typing import Optional, Dict, Any, List
from typing_extensions import Literal

from langchain_payman_tool import (
    SendPaymentTool as LangchainSendPaymentTool,
    SearchPayeesTool as LangchainSearchPayeesTool,
    AddPayeeTool as LangchainAddPayeeTool,
    AskForMoneyTool as LangchainAskForMoneyTool,
    GetBalanceTool as LangchainGetBalanceTool
)

class SendPaymentTool(BaseTool):
    name: str = "send_payment"
    description: str = "Send funds from an agent's wallet to a payee"
    tool: LangchainSendPaymentTool = Field(default_factory=LangchainSendPaymentTool)

    def _run(self, 
            amount_decimal: float,
            payment_destination_id: Optional[str] = None,
            payment_destination: Optional[Dict[str, Any]] = None,
            customer_id: Optional[str] = None,
            customer_email: Optional[str] = None,
            customer_name: Optional[str] = None,
            memo: Optional[str] = None) -> str:
        return self.tool._run(
            amount_decimal=amount_decimal,
            payment_destination_id=payment_destination_id,
            payment_destination=payment_destination,
            customer_id=customer_id,
            customer_email=customer_email,
            customer_name=customer_name,
            memo=memo
        )

class SearchPayeesTool(BaseTool):
    name: str = "search_payees"
    description: str = "Search for existing payment destinations (payees)"
    tool: LangchainSearchPayeesTool = Field(default_factory=LangchainSearchPayeesTool)

    def _run(self,
            name: Optional[str] = None,
            contact_email: Optional[str] = None,
            type: Optional[str] = None) -> str:
        return self.tool._run(
            name=name,
            contact_email=contact_email,
            type=type
        )

class AddPayeeTool(BaseTool):
    name: str = "add_payee"
    description: str = """Add a new payee (payment destination). For US_ACH type, you must provide:
        - type: 'US_ACH'
        - account_holder_name: The name on the bank account
        - account_number: The bank account number
        - routing_number: The bank routing number
        - account_type: Either 'checking' or 'savings'"""
    tool: LangchainAddPayeeTool = Field(default_factory=LangchainAddPayeeTool)

    def _run(self,
            type: Literal["CRYPTO_ADDRESS", "US_ACH"],
            name: Optional[str] = None,
            routing_number: Optional[str] = None,
            account_number: Optional[str] = None,
            account_type: Optional[str] = None,
            account_holder_name: Optional[str] = None,
            contact_details: Optional[Dict[str, Any]] = None,
            **kwargs) -> str:
        try:
            # For US_ACH, ensure required fields are passed directly
            if type == "US_ACH":
                return self.tool._run(
                    type=type,
                    name=name,
                    routing_number=routing_number,
                    account_number=account_number,
                    account_type=account_type,
                    account_holder_name=account_holder_name,
                    contact_details=contact_details
                )
            # For other types, pass through as normal
            return self.tool._run(
                type=type,
                name=name,
                contact_details=contact_details,
                **kwargs
            )
        except Exception as e:
            return f"Error in add_payee: {str(e)}"

class AskForMoneyTool(BaseTool):
    name: str = "ask_for_money"
    description: str = "Generate a checkout link to request money from a customer"
    tool: LangchainAskForMoneyTool = Field(default_factory=LangchainAskForMoneyTool)

    def _run(self,
            amount_decimal: float,
            customer_id: str,
            customer_email: Optional[str] = None,
            customer_name: Optional[str] = None,
            memo: Optional[str] = None) -> str:
        return self.tool._run(
            amount_decimal=amount_decimal,
            customer_id=customer_id,
            customer_email=customer_email,
            customer_name=customer_name,
            memo=memo
        )

class GetBalanceTool(BaseTool):
    name: str = "get_balance"
    description: str = "Get the spendable balance for either the agent or a specific customer"
    tool: LangchainGetBalanceTool = Field(default_factory=LangchainGetBalanceTool)

    def _run(self,
            customer_id: Optional[str] = None,
            currency: str = "USD") -> str:
        return self.tool._run(
            customer_id=customer_id,
            currency=currency
        ) 