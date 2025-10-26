"""
PayPal Payment Service - Coaching Session Payments
Handles one-time payments for single sessions and 3-session packages using PayPal Orders API v2.
Supports USD and CAD currencies with billing agreement for automatic penalty charging.
"""

import os
import logging
import requests
from typing import Optional, Dict
from datetime import datetime
import base64
import sys

# Python 3.7 compatibility - Literal was added in 3.8
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    try:
        from typing_extensions import Literal
    except ImportError:
        # Fallback for Python 3.7 without typing_extensions
        Literal = str  # type: ignore

logger = logging.getLogger(__name__)


class PayPalPaymentService:
    """Service for processing coaching session payments via PayPal Orders API v2"""

    # Pricing configuration
    PRICES = {
        'single_session': {
            'USD': '150.00',
            'CAD': '150.00'
        },
        'three_pack': {
            'USD': '500.00',
            'CAD': '500.00'
        }
    }

    def __init__(self):
        self.client_id = os.getenv('PAYPAL_CLIENT_ID')
        self.client_secret = os.getenv('PAYPAL_CLIENT_SECRET')
        self.mode = os.getenv('PAYPAL_MODE', 'sandbox')  # 'sandbox' or 'live'

        # Set API base URL based on mode
        if self.mode == 'live':
            self.base_url = 'https://api-m.paypal.com'
        else:
            self.base_url = 'https://api-m.sandbox.paypal.com'

        self.access_token = None
        self.token_expires_at = None

        self._initialize_service()

    def _initialize_service(self):
        """Initialize PayPal API and get access token"""
        if not self.client_id or not self.client_secret:
            logger.warning("PayPal credentials not set. Payment processing will be mocked.")
            return

        # Get initial access token
        self._get_access_token()
        logger.info(f"PayPal payment service initialized successfully ({self.mode} mode)")

    def _get_access_token(self) -> Optional[str]:
        """Get OAuth2 access token from PayPal"""
        if not self.client_id or not self.client_secret:
            return None

        # Check if token is still valid
        if self.access_token and self.token_expires_at:
            if datetime.utcnow() < self.token_expires_at:
                return self.access_token

        try:
            # Encode credentials for Basic Auth
            credentials = f"{self.client_id}:{self.client_secret}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()

            headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            data = {'grant_type': 'client_credentials'}

            response = requests.post(
                f'{self.base_url}/v1/oauth2/token',
                headers=headers,
                data=data,
                timeout=10
            )

            response.raise_for_status()
            token_data = response.json()

            self.access_token = token_data['access_token']
            # Token expires in seconds, calculate expiry time
            expires_in = token_data.get('expires_in', 3600)
            from datetime import timedelta
            self.token_expires_at = datetime.utcnow() + timedelta(seconds=expires_in - 60)  # 60s buffer

            logger.info("PayPal access token obtained successfully")
            return self.access_token

        except requests.RequestException as e:
            logger.error(f"Failed to get PayPal access token: {e}")
            return None

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for PayPal API requests"""
        token = self._get_access_token()
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

    def create_order(
        self,
        session_type: Literal['single_session', 'three_pack'],
        currency: Literal['USD', 'CAD'],
        user_id: str,
        user_email: str,
        metadata: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        Create a PayPal Order for coaching session purchase

        Args:
            session_type: 'single_session' or 'three_pack'
            currency: 'USD' or 'CAD'
            user_id: User's ID from database
            user_email: User's email for receipt
            metadata: Additional metadata to attach

        Returns:
            Dict with order_id and approval_url, or None if failed
        """
        if not self.access_token:
            # Mock mode for development
            mock_order_id = f"ORDER_MOCK_{session_type}_{currency}"
            mock_approval_url = f"https://paypal.com/checkoutnow?token={mock_order_id}"
            logger.warning(f"PayPal not initialized. Returning mock order: {mock_order_id}")
            return {
                'order_id': mock_order_id,
                'approval_url': mock_approval_url,
                'amount': self.PRICES[session_type][currency],
                'currency': currency
            }

        try:
            amount = self.PRICES[session_type][currency]

            # Prepare custom_id for metadata
            import json
            custom_data = {
                'user_id': user_id,
                'session_type': session_type
            }
            if metadata:
                custom_data.update(metadata)

            # Create order payload (PayPal Orders API v2)
            order_payload = {
                'intent': 'CAPTURE',
                'purchase_units': [{
                    'amount': {
                        'currency_code': currency,
                        'value': amount
                    },
                    'description': f'Coaching Session - {session_type.replace("_", " ").title()}',
                    'custom_id': json.dumps(custom_data)  # Store metadata
                }],
                'application_context': {
                    'brand_name': 'WIMD Coaching',
                    'landing_page': 'BILLING',
                    'user_action': 'PAY_NOW',
                    'return_url': os.getenv('PAYPAL_RETURN_URL', 'https://whatismydelta.com/booking/success'),
                    'cancel_url': os.getenv('PAYPAL_CANCEL_URL', 'https://whatismydelta.com/booking/cancel')
                },
                # Enable vault for future charges (50% penalty)
                'payment_source': {
                    'paypal': {
                        'experience_context': {
                            'payment_method_preference': 'IMMEDIATE_PAYMENT_REQUIRED',
                            'brand_name': 'WIMD Coaching',
                            'user_action': 'PAY_NOW'
                        },
                        'attributes': {
                            'vault': {
                                'store_in_vault': 'ON_SUCCESS',
                                'usage_type': 'MERCHANT',
                                'customer_type': 'CONSUMER'
                            }
                        }
                    }
                }
            }

            response = requests.post(
                f'{self.base_url}/v2/checkout/orders',
                headers=self._get_headers(),
                json=order_payload,
                timeout=10
            )

            response.raise_for_status()
            order = response.json()

            # Extract approval URL
            approval_url = None
            for link in order.get('links', []):
                if link.get('rel') == 'approve':
                    approval_url = link.get('href')
                    break

            logger.info(f"Created PayPal Order {order['id']} for {session_type} ({currency})")

            return {
                'order_id': order['id'],
                'approval_url': approval_url,
                'amount': amount,
                'currency': currency,
                'status': order.get('status')
            }

        except requests.RequestException as e:
            logger.error(f"PayPal API error creating order: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error creating PayPal order: {e}")
            return None

    def capture_order(self, order_id: str) -> Optional[Dict]:
        """
        Capture (complete) a PayPal order after user approval

        Args:
            order_id: PayPal Order ID

        Returns:
            Dict with capture details, or None if failed
        """
        if not self.access_token:
            logger.warning(f"PayPal not initialized. Mock capturing order {order_id}")
            return {
                'order_id': order_id,
                'status': 'COMPLETED',
                'capture_id': f'CAPTURE_MOCK_{order_id}'
            }

        try:
            response = requests.post(
                f'{self.base_url}/v2/checkout/orders/{order_id}/capture',
                headers=self._get_headers(),
                timeout=10
            )

            response.raise_for_status()
            capture_data = response.json()

            # Extract capture ID
            capture_id = None
            if capture_data.get('purchase_units'):
                payments = capture_data['purchase_units'][0].get('payments', {})
                captures = payments.get('captures', [])
                if captures:
                    capture_id = captures[0].get('id')

            logger.info(f"Captured PayPal Order {order_id}, capture ID: {capture_id}")

            return {
                'order_id': order_id,
                'status': capture_data.get('status'),
                'capture_id': capture_id,
                'payer_email': capture_data.get('payer', {}).get('email_address')
            }

        except requests.RequestException as e:
            logger.error(f"PayPal API error capturing order {order_id}: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error capturing order: {e}")
            return None

    def get_order(self, order_id: str) -> Optional[Dict]:
        """
        Retrieve order details

        Args:
            order_id: PayPal Order ID

        Returns:
            Dict with order details, or None if not found
        """
        if not self.access_token:
            logger.warning(f"PayPal not initialized. Mock retrieving order {order_id}")
            return {
                'id': order_id,
                'status': 'COMPLETED'
            }

        try:
            response = requests.get(
                f'{self.base_url}/v2/checkout/orders/{order_id}',
                headers=self._get_headers(),
                timeout=10
            )

            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            logger.error(f"PayPal API error retrieving order {order_id}: {e}")
            return None

    def charge_via_billing_agreement(
        self,
        billing_agreement_id: str,
        amount: str,
        currency: str,
        description: str,
        user_id: str,
        appointment_id: str
    ) -> Optional[str]:
        """
        Charge using existing billing agreement (for 50% cancellation fee)

        Args:
            billing_agreement_id: Billing Agreement ID from original payment
            amount: Amount to charge (e.g., "75.00" for 50% of $150)
            currency: Currency code
            description: Charge description
            user_id: User's ID
            appointment_id: Appointment being charged for

        Returns:
            Payment ID if successful, None if failed
        """
        if not self.access_token:
            mock_payment_id = f"PAY_MOCK_FEE_{appointment_id}"
            logger.warning(f"PayPal not initialized. Returning mock payment: {mock_payment_id}")
            return mock_payment_id

        try:
            # Create payment using billing agreement
            import json
            payment_payload = {
                'intent': 'sale',
                'payer': {
                    'payment_method': 'paypal',
                    'funding_instruments': [{
                        'billing_agreement_token': billing_agreement_id
                    }]
                },
                'transactions': [{
                    'amount': {
                        'total': amount,
                        'currency': currency
                    },
                    'description': description,
                    'custom': json.dumps({
                        'user_id': user_id,
                        'appointment_id': appointment_id,
                        'type': 'cancellation_fee'
                    })
                }]
            }

            response = requests.post(
                f'{self.base_url}/v1/payments/payment',
                headers=self._get_headers(),
                json=payment_payload,
                timeout=10
            )

            response.raise_for_status()
            payment = response.json()

            logger.info(f"Charged cancellation fee via billing agreement: {payment.get('id')}")
            return payment.get('id')

        except requests.RequestException as e:
            logger.error(f"PayPal API error charging via billing agreement: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error charging via billing agreement: {e}")
            return None

    def refund_capture(
        self,
        capture_id: str,
        amount: Optional[str] = None,
        currency: Optional[str] = None
    ) -> Optional[str]:
        """
        Refund a captured payment (full or partial)

        Args:
            capture_id: Capture ID to refund
            amount: Amount to refund (None = full refund)
            currency: Currency code (required if amount specified)

        Returns:
            Refund ID if successful, None if failed
        """
        if not self.access_token:
            mock_refund_id = f"REFUND_MOCK_{capture_id}"
            logger.warning(f"PayPal not initialized. Returning mock refund: {mock_refund_id}")
            return mock_refund_id

        try:
            refund_payload = {}

            if amount and currency:
                refund_payload['amount'] = {
                    'value': amount,
                    'currency_code': currency
                }

            response = requests.post(
                f'{self.base_url}/v2/payments/captures/{capture_id}/refund',
                headers=self._get_headers(),
                json=refund_payload if refund_payload else None,
                timeout=10
            )

            response.raise_for_status()
            refund = response.json()

            refund_type = "partial" if amount else "full"
            logger.info(f"Created {refund_type} refund {refund['id']} for capture {capture_id}")

            return refund['id']

        except requests.RequestException as e:
            logger.error(f"PayPal API error creating refund: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error creating refund: {e}")
            return None


# Singleton instance
_paypal_service = None

def get_paypal_service() -> PayPalPaymentService:
    """Get or create singleton PayPalPaymentService instance"""
    global _paypal_service
    if _paypal_service is None:
        _paypal_service = PayPalPaymentService()
    return _paypal_service
