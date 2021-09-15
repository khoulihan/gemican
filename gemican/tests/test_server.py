import os
from shutil import rmtree
from tempfile import mkdtemp

from twisted.test import proto_helpers
from twisted.trial import unittest

from gemican.server import GeminiFactory


class TestServer(unittest.TestCase):

    def setUp(self):
        self.temp_output = mkdtemp(prefix='gemicantests.')
        print(self.temp_output)
        factory = GeminiFactory(self.temp_output)

        self.old_cwd = os.getcwd()
        os.chdir(self.temp_output)
        with open(os.path.join(self.temp_output, 'index.gmi'), 'a') as f:
            f.write((
                "# Index\n"
                "\n"
                "An example file\n"
            ))
        with open(os.path.join(self.temp_output, 'baz.gmi'), 'a') as f:
            f.write((
                "# Baz\n"
                "\n"
                "An example file\n"
            ))
        os.mkdir(os.path.join(self.temp_output, 'foo'))
        with open(os.path.join(self.temp_output, 'foo', 'index.gmi'), 'a') as f:
            f.write((
                "## Foo Index\n"
                "\n"
                "An example file\n"
            ))

        self.proto = factory.buildProtocol(("127.0.0.1", 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def tearDown(self):
        os.chdir(self.old_cwd)
        rmtree(self.temp_output)

    def test_get(self):
        # Index
        self.proto.lineReceived(b"gemini://127.0.0.1/index.gmi")
        self.assertEqual(
            self.tr.value().decode('utf-8'),
            (
                "20 text/gemini\r\n"
                "# Index\r\n"
                "\r\n"
                "An example file\r\n"
            )
        )
        self.tr.clear()

        # Implicit index
        self.proto.lineReceived(b"gemini://127.0.0.1/")
        self.assertEqual(
            self.tr.value().decode('utf-8'),
            (
                "20 text/gemini\r\n"
                "# Index\r\n"
                "\r\n"
                "An example file\r\n"
            )
        )
        self.tr.clear()

        # Nested file
        self.proto.lineReceived(b"gemini://127.0.0.1/foo/index.gmi")
        self.assertEqual(
            self.tr.value().decode('utf-8'),
            (
                "20 text/gemini\r\n"
                "## Foo Index\r\n"
                "\r\n"
                "An example file\r\n"
            )
        )
        self.tr.clear()

        # Non existent file
        self.proto.lineReceived(b"gemini://127.0.0.1/nonexistent.gmi")
        self.assertEqual(
            self.tr.value().decode('utf-8'),
            "51 The requested resource does not exist\r\n"
        )
        self.tr.clear()
