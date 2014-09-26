from ferrisnose import AppEngineTest
from google.appengine.api import mail as gae_mail
from ferris3 import mail
import mock


class MailTest(AppEngineTest):

    def test_mail(self):
        with mock.patch('ferris3.mail.mail') as mock_mail:
            mail.send("test@example.com", "Test Email", "This is a test")
            mock_mail.send.assert_called()
