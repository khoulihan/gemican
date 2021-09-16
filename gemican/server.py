import argparse
import logging
import sys
from pathlib import Path

from OpenSSL import crypto

from magic import from_file as magic_from_file

from twisted.internet import protocol, reactor, ssl
from twisted.internet.error import SSLError
from twisted.protocols.basic import LineReceiver
from twisted.python import log

from gemican.log import init as init_logging

from .utils import urlparse


logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Gemican Development Server',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "port",
        default=1966,
        type=int,
        nargs="?",
        help="Port to Listen On"
    )
    parser.add_argument(
        "server",
        default="",
        nargs="?",
        help="Interface to Listen On"
    )
    parser.add_argument(
        '--cert',
        default="./cert.pem",
        nargs="?",
        help=(
            'Path to certificate file. '
            'Relative to current directory'
        )
    )
    parser.add_argument(
        '--key',
        default="./key.pem",
        nargs="?",
        help=(
            'Path to certificate key file. '
            'Relative to current directory'
        )
    )
    parser.add_argument(
        '--path',
        default=".",
        help=(
            'Path to gemican source directory to serve. '
            'Relative to current directory'
        )
    )
    return parser.parse_args()


def load_file_content(filepath):
    with open(filepath, 'r') as f:
        return f.read()


def load_certificate(keyfile, certfile):
    """
    Load an x509 certificate from private and public PEM files.
    """
    keydata = load_file_content(keyfile)
    certdata = load_file_content(certfile)

    key = ssl.KeyPair.load(keydata, format=crypto.FILETYPE_PEM)
    cert = ssl.Certificate.loadPEM(certdata)
    certificate = ssl.PrivateCertificate.fromCertificateAndKeyPair(cert, key)

    return certificate


class GeminiProtocol(LineReceiver):

    MAX_LENGTH = 1024

    def _return_status(self, status, meta):
        self.sendLine("{} {}".format(status, meta).encode('utf-8'))
        self.transport.loseConnection()

    def _return_success(self, requested):
        if requested.suffix in ('.gmi', '.gemini'):
            mimetype = 'text/gemini'
        else:
            mimetype = magic_from_file(str(requested), mime=True)
        self.sendLine("{} {}".format(20, mimetype).encode('utf-8'))
        if mimetype.startswith('text/'):
            with open(requested, 'r') as f:
                for line in f:
                    self.sendLine(line.rstrip('\r\n').encode('utf-8'))
        else:
            with open(requested, 'rb') as f:
                self.transport.write(f.read())
        self.transport.loseConnection()

    def lineReceived(self, line):
        line = line.decode('utf-8')
        # logger does not work once the reactor is running
        print(line)

        try:
            req = urlparse(line, 'gemini')
        except ValueError:
            print("Invalid URL")
            self._return_status(50, "Invalid URL")
            return

        path = req.path
        if path.endswith('/'):
            path = f'{path}index.gmi'
        requested = Path(self.factory.base_path).resolve() / path.lstrip('/')

        if not requested.is_file():
            print("Not found")
            self._return_status(51, "The requested resource does not exist")
            return

        self._return_success(requested)


class GeminiFactory(protocol.Factory):

    protocol = GeminiProtocol

    def __init__(self, base_path):
        self.base_path = base_path


class GeminiServer():

    def __init__(self, base_path, bind, port, keyfile, certfile):
        self.base_path = base_path
        self.bind = bind
        self.port = port
        self.keyfile = keyfile
        self.certfile = certfile

    def serve_forever(self):
        log.startLogging(sys.stdout)
        certificate = load_certificate(self.keyfile, self.certfile)
        # TODO: bind does not get used here...
        reactor.listenSSL(
            self.port,
            GeminiFactory(self.base_path),
            certificate.options(),
        )
        reactor.run()

    def close(self):
        pass


if __name__ == '__main__':
    init_logging(level=logging.INFO)
    logger.warning(
        "'python -m gemican.server' is deprecated.\nThe "
        "Gemican development server should be run via "
        "'gemican --listen' or 'gemican -l'.\nThis can be combined "
        "with regeneration as 'gemican -lr'.\nRerun 'gemican-"
        "quickstart' to get new Makefile and tasks.py files."
    )
    args = parse_arguments()

    geminid = GeminiServer(
        args.path,
        args.server,
        args.port,
        args.key,
        args.cert,
    )

    logger.info(
        "Serving at port %s, server %s.",
        args.port, args.server
    )
    try:
        geminid.serve_forever()
    except SSLError as e:
        logger.error(
            "Couldn't open certificate file %s or key file %s",
            args.cert, args.key
        )
        logger.error(
            "Could not listen on port %s, server %s.",
            args.port, args.server
        )
        sys.exit(getattr(e, 'exitcode', 1))
    except KeyboardInterrupt:
        logger.info("Shutting down server.")
        geminid.close()
