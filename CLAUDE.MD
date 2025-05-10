# Mobile App Architecture Summary

## Core Technology Stack

- **Backend Framework**: Flask
  - Handles business logic, data processing, and UI rendering
  - Provides database access and API endpoints
  - Runs as a local web server on the device

- **Database**: SQLite
  - Self-contained, single-file database
  - Lightweight and perfect for mobile devices
  - No separate server process required

- **Migration System**: Flask-Migrate with Alembic
  - Manages database schema evolution
  - Runs migrations automatically during app startup
  - Preserves user data when app updates with schema changes

- **UI Layer**: HTML/CSS/JavaScript via WebView
  - Web-based interface (generated in flask) displayed in a WebView
  - Same rendering across development and production environments
  - Allows browser-based debugging tools

- **Mobile Packaging**: Kivy
  - Provides cross-platform deployment to iOS and Android
  - Acts primarily as a container that launches Flask + WebView
  - Handles app lifecycle and permissions on mobile devices

## Architecture Flow

1. Kivy app launches and initializes
2. Flask server starts in a background thread
3. Kivy displays a WebView pointing to the local Flask server
4. Flask handles database operations, business logic, and UI rendering
5. User interacts with the application through the WebView interface

## Development Workflow

1. Develop and test Flask app in regular web browser
2. Use browser developer tools for debugging
3. Create migrations with Flask-Migrate during development
4. Package with Kivy for deployment to mobile devices

This architecture leverages your existing Flask knowledge while enabling deployment to mobile devices. The WebView approach provides a consistent experience across platforms and simplifies development by using familiar web technologies.


# What are we making?
we are making a CRM for a Window Washing business with bare-bones essentials.
We will use outdated technology (flask + html) without any newer frameworks
(aside from Kivy as a lite-wrapper for packaging).
The phone integration will be the simple option to copy text to send as an SMS on the phone,
but the actual sending of the SMS will be done by the user.
# Design philosophy and guidelines
We want to make an app that somebody can understand, modify etc. We want to
use SOLID principles when designing, and test, Test, TEST everything.
Tests should be written first, and then verify the test fails before moving on to writing the logic.
Use OOP where most functions are no more than 5
lines long, we break complex functions down into objects and methods. Objects that can be reused, swapped where necessary
will make maintaining this codebase easier. The goal for this codebase is to be
easy to read, no easy to maintain. We understand that designing a foolproof user experience underestimates the
ingenuity of fools. So instead we strive for a simple to use interface that does not assume, does not make things easier for the user
if it introduces black boxes of logic that are hard to follow. When making a decision, logical or otherwise, remember that
a good architect maximizes the number of decisions not made. This means if we're trying to reduce the number of if/else by using objects for controlling behavior.
For ease of querying, we are going to have the "one webpage, one table" philosophy.
Anything that needs querying an additional table should consider putting that information on the table itself.
For example, the most recent invoice for a Customer, should be also put on the Customer model; last_invoice_date, last_invoice description, last_invoice amount, last_invoice_id.
This will get updated as more invoices are added for that customer.



Essential Features
1. Customer Management

- Add new customers
- View and edit customer details
- Search and filter customers
- Basic customer history view

2. Invoice Management

- Create new invoices for customers
- Track invoice status (draft, sent, paid)
- Generate text invoices (invoices that can be copied to send as a text with their phone)
- Track payments and balances
- View invoice history by customer

Implementation Plan
1. Project Structure
```
window_wash_crm/
├── app.py
├── models.py
├── routes/
│   ├── __init__.py
│   ├── customers.py
│   └── invoices.py
├── templates/
│   ├── base.html
│   ├── customers/
│   │   ├── list.html
│   │   ├── create.html
│   │   └── view.html
│   └── invoices/
│       ├── list.html
│       ├── create.html
│       └── view.html
├── static/
│   ├── css/
│   ├── js/
│   └── img/
└── migrations/
```

