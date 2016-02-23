from ferrisnose import AppEngineTest
from ferris3 import mail
import mock


class MailTest(AppEngineTest):

    def test_mail(self):
        with mock.patch('ferris3.mail.send') as mock_mail_send:
            mail.send(
                "test@example.com",
                "Test Email",
                "This is a test")
            mock_mail_send.assert_called_with(
                "test@example.com",
                "Test Email",
                "This is a test")
