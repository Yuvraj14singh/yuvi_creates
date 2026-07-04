# Yuvi Creates

A complete Django freelancing business website for a freelance web developer brand. It includes service pages, restaurant/cafe packages, portfolio, process, about, FAQ, contact enquiries, and a manual checkout/payment booking flow.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Admin

Open `http://127.0.0.1:8000/admin/` and sign in with your superuser account.

You can add/edit:
- Services
- Packages
- Portfolio projects
- Enquiries
- Payment bookings

## Payment Notes

The checkout is a demo/manual payment flow. It saves booking requests as `Pending` or `Pending Verification`; it does not process real payments, does not mark anything paid automatically, and does not include gateway keys.

Razorpay, Cashfree, or Instamojo can be integrated later by storing real keys in environment variables and updating the checkout/callback views.
