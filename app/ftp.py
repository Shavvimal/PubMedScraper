import logging
from ftplib import FTP
import re
import os


class FtpDownloader:
    """
    Downloads the files through FTP
    """
    def __init__(self, host, ftp_path, user_id=None, pwd=None, reg_ex=".*"):
        self.ftp_path = ftp_path
        self.reg_ex = reg_ex
        self.pwd = pwd
        self.user_id = user_id
        self.host = host
        self.ftp_client = None

    @property
    def logger(self):
        return logging.getLogger(__name__)

    @property
    def ftp_client(self):
        self.__ftp_client__ = self.__ftp_client__ or FTP(self.host)
        return self.__ftp_client__

    @ftp_client.setter
    def ftp_client(self, value):
        self.__ftp_client__ = value

    def iterate(self, local_path):
        ftp = None
        re_obj = re.compile(self.reg_ex)
        # Make the local path and ignore if exists..
        os.makedirs(local_path, exist_ok=True)
        try:
            ftp = self.ftp_client
            # login
            if self.user_id is None:
                ftp.login()
            else:
                ftp.login(self.user_id, self.pwd)

            ftp.cwd(self.ftp_path)
            file_names = ftp.nlst()

            for filename in filter(lambda f: re_obj.match(f) is not None, file_names):
                self.logger.info("Downloading {} ..".format(filename))
                yield self._download_file(ftp, filename, local_path)


        finally:
            if ftp is not None: ftp.quit()

    def __call__(self, local_path):
        return list(self.iterate(local_path))

    @staticmethod
    def _download_file(ftp_connection, remote_file, local_path):
        local_filename = os.path.join(local_path, remote_file)
        with open(local_filename, 'wb') as f:
            ftp_connection.retrbinary('RETR ' + remote_file, f.write)

        return local_filename


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_comm/
    ftp_downloader = FtpDownloader(
        host="ftp.ncbi.nlm.nih.gov",
        ftp_path="/pub/pmc/oa_bulk/oa_comm/xml/",
        # Regex for .tar.gz files like oa_comm_xml.incr.2024-01-29.tar.gz
        reg_ex="oa_comm_xml.incr.*.tar.gz"
    )
    ftp_downloader("./pubmed-tar")
    # Should download ~52 tar.gz files
    print("Downloaded the files..")
