# Telegram Digital Service Log Bot

ဤသည်မှာ ကျောင်းများအတွက် Digital Service Log စနစ်ကို အသုံးပြု၍ Python နှင့် `python-telegram-bot` library ဖြင့် ရေးသားထားသော Telegram Bot တစ်ခုဖြစ်သည်။

This is a Telegram Bot built with Python and the `python-telegram-bot` library for a school's Digital Service Log System.

## Features (လုပ်ဆောင်ချက်များ)

- **/start** command: Technician-only welcome message.
- Technician can create new service logs step by step (device name, user name, user email, service choice, parts used).
- Optional email notification mode for the user.
- **/history** command: View past service logs for technicians.
- Optional monthly Excel export email on the 1st day of every month.
- Stores all data in an SQLite database.

## Setup Instructions (တပ်ဆင်နည်း)

### 1. Clone the repository (Repository ကို ကူးယူခြင်း)

```bash
git clone <repository_url> # If applicable, otherwise assume files are already in /home/ubuntu/telegram-bot
cd /home/ubuntu/telegram-bot
```

### 2. Install dependencies (လိုအပ်သော package များ ထည့်သွင်းခြင်း)

```bash
pip install -r requirements.txt
```

### 3. Initialize the database (ဒေတာဘေ့စ် စတင်တည်ဆောက်ခြင်း)

Run the `database_setup.py` script to create the necessary SQLite tables:

```bash
python3 database_setup.py
```

This will create a `service_logs.db` file in the same directory. The app also auto-initializes the database on startup, so this step is recommended but not strictly required.

### 4. Configure the Bot Token with `.env` (`.env` ဖြင့် Bot Token ထည့်သွင်းခြင်း)

Create a `.env` file in the same folder as `main.py` and add your Telegram Bot Token and Microsoft email settings:

```env
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
BOT_RUN_MODE=polling
FREE_PLAN_MODE=false
EMAIL_DELIVERY_ENABLED=true
USER_EMAIL_REQUIRED=true
MONTHLY_REPORT_ENABLED=true
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USERNAME=YOUR_EMAIL@outlook.com
SMTP_PASSWORD=YOUR_PASSWORD_OR_APP_PASSWORD
SMTP_FROM_EMAIL=YOUR_EMAIL@outlook.com
SMTP_USE_TLS=true
APP_TIMEZONE=Asia/Yangon
MONTHLY_REPORT_RECIPIENT_EMAIL=YOUR_REPORT_EMAIL@example.com
MONTHLY_REPORT_SEND_HOUR=9
MONTHLY_REPORT_SEND_MINUTE=0
WEBHOOK_BASE_URL=
WEBHOOK_PATH=/telegram/webhook
WEBHOOK_SECRET_TOKEN=
HEALTHCHECK_PATH=/healthz
DROP_PENDING_UPDATES=false
```

You can copy the format from `.env.example`.

### 5. Run the Bot (Bot ကို စတင်ခြင်း)

```bash
python3 main.py
```

Your bot should now be running and accessible via Telegram.

## Quick Start with a New Telegram Bot (Telegram Bot အသစ်နှင့် ချိတ်ဆက်နည်း)

1. Open Telegram and chat with `@BotFather`
2. Send `/newbot`
3. Enter a display name for your bot
4. Enter a unique bot username ending with `bot`
5. Copy the token given by BotFather
6. Create a `.env` file in this project folder
7. Add these settings:

```env
BOT_TOKEN=PASTE_YOUR_NEW_TOKEN_HERE
BOT_RUN_MODE=polling
FREE_PLAN_MODE=false
EMAIL_DELIVERY_ENABLED=true
USER_EMAIL_REQUIRED=true
MONTHLY_REPORT_ENABLED=true
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USERNAME=YOUR_EMAIL@outlook.com
SMTP_PASSWORD=YOUR_PASSWORD_OR_APP_PASSWORD
SMTP_FROM_EMAIL=YOUR_EMAIL@outlook.com
SMTP_USE_TLS=true
APP_TIMEZONE=Asia/Yangon
MONTHLY_REPORT_RECIPIENT_EMAIL=YOUR_REPORT_EMAIL@example.com
MONTHLY_REPORT_SEND_HOUR=9
MONTHLY_REPORT_SEND_MINUTE=0
WEBHOOK_BASE_URL=
WEBHOOK_PATH=/telegram/webhook
WEBHOOK_SECRET_TOKEN=
HEALTHCHECK_PATH=/healthz
DROP_PENDING_UPDATES=false
```

8. Run the database setup:

```bash
python3 database_setup.py
```

9. Run the bot:

```bash
python3 main.py
```

## Usage (အသုံးပြုပုံ)

### For Technicians (နည်းပညာရှင်များအတွက်)

1. Start the bot: Send `/start`
2. Create new log: Send `/newlog`
3. Follow prompts to enter: Device Name, User Name, User Email, Service Type, Parts Used.
   - **User Email**: Required only when email delivery is enabled.
   - **Service Type choices**: `Body Service`, `Windows Service`, `Device Clean`, `Software Installation`, `Small Repairs`

## Microsoft Mail Notes

- Use `smtp.office365.com` with port `587` and `SMTP_USE_TLS=true`.
- `SMTP_USERNAME` and `SMTP_FROM_EMAIL` should usually be the same Microsoft email address.
- Do not leave placeholder values like `yourname@outlook.com` or `your_real_password_or_app_password` in `.env`.
- If login fails after this, SMTP AUTH may be disabled on the mailbox or tenant side in Microsoft 365.
- If MFA is enabled on the account, you may need an app password or an SMTP-enabled account policy depending on your Microsoft setup.

## Monthly Auto Report

- The bot auto-generates an Excel export and emails it on the 1st day of every month.
- Set `MONTHLY_REPORT_RECIPIENT_EMAIL` to the email that should receive the file.
- Default schedule is `09:00` in `Asia/Yangon`. You can change it with `MONTHLY_REPORT_SEND_HOUR`, `MONTHLY_REPORT_SEND_MINUTE`, and `APP_TIMEZONE`.
- The bot must be running for the scheduler to send the report automatically.

## Lite Mode For Render Free

Render free web services are useful for testing, but they have important limits:

- No persistent disk
- Outbound SMTP on port `587` is not supported
- The service can spin down when idle

Because of those limits, this project includes a lightweight deployment mode:

- `FREE_PLAN_MODE=true`
- `EMAIL_DELIVERY_ENABLED=false`
- `USER_EMAIL_REQUIRED=false`
- `MONTHLY_REPORT_ENABLED=false`

In lite mode:

- The bot still accepts `/newlog`, `/history`, and `/export`
- User email collection is skipped
- Service logs are saved locally only
- Email notifications are disabled
- Monthly auto-email reports are disabled
- SQLite data can be lost whenever the free service restarts or redeploys

## Database Schema (ဒေတာဘေ့စ် ပုံစံ)

### `service_logs` table

| Column Name           | Type      | Description                                   |
|-----------------------|-----------|-----------------------------------------------|
| `id`                  | INTEGER   | Primary Key, Auto-incrementing                |
| `technician_name`     | TEXT      | Name of the technician                        |
| `device_id`           | TEXT      | Device name of the serviced item              |
| `user_name`           | TEXT      | Name of the user (e.g., teacher)              |
| `user_email`         | TEXT      | Email address of the user                     |
| `service_done`        | TEXT      | Description of service performed              |
| `parts_used`          | TEXT      | Parts used for the service                    |
| `status`              | TEXT      | Current status (e.g., 'Email Sent', 'Email Failed')        |
| `created_at`          | TIMESTAMP | Timestamp of log creation                     |
| `user_chat_id`        | INTEGER   | Telegram Chat ID of the user                  |
| `technician_chat_id`  | INTEGER   | Telegram Chat ID of the technician            |
| `confirmation_message_id` | INTEGER | Legacy Telegram message ID field              |
| `delivery_method`    | TEXT      | Delivery channel (`telegram` or `email`)      |

### `confirmations` table

| Column Name           | Type      | Description                                   |
|-----------------------|-----------|-----------------------------------------------|
| `id`                  | INTEGER   | Primary Key, Auto-incrementing                |
| `service_log_id`      | INTEGER   | Foreign Key referencing `service_logs.id`     |
| `user_id`             | INTEGER   | Telegram User ID of the confirmer             |
| `user_telegram_name`  | TEXT      | Full name of the Telegram user who confirmed  |
| `confirmed_at`        | TIMESTAMP | Timestamp of confirmation                     |

## Render Deployment

This project can now run on Render as a `Web Service`.

- Local development can stay on `BOT_RUN_MODE=polling`.
- Render should use `BOT_RUN_MODE=webhook`.
- In webhook mode, the app starts an HTTP server, exposes a health endpoint, and registers a Telegram webhook automatically.
- The included Blueprint is tuned for Render's `free` instance type.

### Render-ready files in this repo

- Repo root `render.yaml`
- Repo root `.python-version`
- Shared runtime/storage config in `config.py`

### What was added for Render

- SQLite database path is now configurable.
- Export directory is now configurable.
- Data defaults to a local `data/` folder.
- Database initialization now runs automatically at startup.
- A webhook-based Render web service Blueprint was added.
- A `/healthz` endpoint was added for Render health checks.
- The app can auto-use Render's `RENDER_EXTERNAL_URL` as the Telegram webhook base URL.
- Lite mode disables SMTP-dependent and always-on-only features by default.

### Blueprint deploy steps

1. Push the full project to GitHub, GitLab, or Bitbucket.
2. In Render, open `New > Blueprint`.
3. Connect the repository that contains this `render.yaml`.
4. Deploy the Blueprint and let Render create the web service.
5. Fill in these secret environment variables in Render:
   - `BOT_TOKEN`
   - `WEBHOOK_SECRET_TOKEN`

### How webhook mode works on Render

- Render automatically provides `RENDER_EXTERNAL_URL` for web services.
- The app uses that value to register this Telegram webhook:

```text
https://your-service.onrender.com/telegram/webhook
```

- Render health checks call:

```text
/healthz
```

- If you use a custom domain for the bot, set `WEBHOOK_BASE_URL=https://your-domain.example` so Telegram uses your custom URL instead of the default `onrender.com` domain.

### Default environment values used by the Blueprint

- `BOT_RUN_MODE=webhook`
- `FREE_PLAN_MODE=true`
- `EMAIL_DELIVERY_ENABLED=false`
- `USER_EMAIL_REQUIRED=false`
- `MONTHLY_REPORT_ENABLED=false`
- `APP_TIMEZONE=Asia/Yangon`
- `MONTHLY_REPORT_SEND_HOUR=9`
- `MONTHLY_REPORT_SEND_MINUTE=0`
- `WEBHOOK_PATH=/telegram/webhook`
- `HEALTHCHECK_PATH=/healthz`
- `DROP_PENDING_UPDATES=false`
- `DATA_DIR=./data`

### If you deploy manually instead of using Blueprint

Use these settings in Render:

- Service type: `Web Service`
- Runtime: `Python`
- Root Directory: `telegram-bot`
- Build Command: `pip install -r requirements.txt`
- Start Command: `python main.py`
- Health Check Path: `/healthz`
- Plan: `free`

### Current deployment limitations

- This bot is designed for a single running instance because it uses SQLite.
- On Render free, data can be lost when the service restarts or redeploys.
- Email notifications and monthly auto-email reports are disabled in the included free-plan Blueprint.
- Free services can spin down on idle, so the first Telegram message after idle might be delayed.
- If you switch between polling and webhook deployments, let the new deployment fully start so it can register the correct Telegram delivery mode.
