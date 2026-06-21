import asyncio
import smtplib
import unittest
from unittest.mock import patch

import scripts.send_log_email as email_mod
from routers.email_config import update_yaml_field


class FakeSMTP:
    login_calls = []

    def __init__(self, server, port, timeout=30):
        self.server = server
        self.port = port
        self.timeout = timeout

    def starttls(self):
        return None

    def login(self, username, password):
        self.__class__.login_calls.append((username, password))

    def send_message(self, message):
        self.message = message

    def quit(self):
        return None


class SendEmailAuthUsernameTests(unittest.TestCase):
    def setUp(self):
        FakeSMTP.login_calls = []

    def run_send_email_with_config(self, email_config):
        config = {"email": email_config}
        with patch.object(email_mod.smtplib, "SMTP", FakeSMTP), patch.object(email_mod, "load_config", lambda: config):
            return asyncio.run(email_mod.send_email("test", "body"))

    def test_uses_configured_auth_username_when_present(self):
        result = self.run_send_email_with_config(
            {
                "smtp_server": "smtp.example.test",
                "smtp_port": 587,
                "sender": "from@example.com",
                "auth_username": "smtp-auth-user",
                "password": "secret",
                "receiver": "to@example.com",
            }
        )

        self.assertEqual(result["status"], "success")
        self.assertEqual(FakeSMTP.login_calls, [("smtp-auth-user", "secret")])

    def test_falls_back_to_sender_for_qq_style_config(self):
        result = self.run_send_email_with_config(
            {
                "smtp_server": "smtp.qq.com",
                "smtp_port": 587,
                "sender": "user@qq.com",
                "password": "authorization-code",
                "receiver": "to@example.com",
            }
        )

        self.assertEqual(result["status"], "success")
        self.assertEqual(FakeSMTP.login_calls, [("user@qq.com", "authorization-code")])


class EmailConfigYamlUpdateTests(unittest.TestCase):
    def test_inserts_missing_nested_email_field(self):
        content = """email:\n  smtp_server: smtp.qq.com\n  smtp_port: 587\n  sender: \"user@qq.com\"\n  password: \"secret\"\n  receiver: \"to@example.com\"\n\nlog_folder: logs\n"""

        updated = update_yaml_field(content, ["email", "auth_username"], '"smtp-auth-user"')

        self.assertIn('  auth_username: "smtp-auth-user"', updated)
        self.assertLess(updated.index("  auth_username:"), updated.index("log_folder:"))


if __name__ == "__main__":
    unittest.main()
