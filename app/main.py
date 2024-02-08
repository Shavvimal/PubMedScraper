import logging
import os

from ftp import FtpDownloader
from ftp_downloader_post_process import FtpDownloaderPostProcess
from parser import PubMedXMLParser
from pg import PGDatabase

from dotenv import load_dotenv

load_dotenv()


class PubMedFTPSQLOrchestrator:
    def __init__(self, host, ftp_path, user_id=None, pwd=None, reg_ex=".*", local_path="./data"):
        self.local_path = local_path
        self.ftp_path = ftp_path
        self.reg_ex = reg_ex
        self.pwd = pwd
        self.user_id = user_id
        self.host = host
        # Parser
        self.parser = PubMedXMLParser()
        # Database
        self.db = PGDatabase()

    def run(self):
        # Download the files
        downloader_ftp = FtpDownloader(
            host=self.host,
            ftp_path=self.ftp_path,
            # Regex for .tar.gz files like oa_comm_xml.incr.2024-01-29.tar.gz
            reg_ex=self.reg_ex)
        # Wrap the downloader_ftp with a post-processing decorator to upload parse and send to DB
        downloader = FtpDownloaderPostProcess(downloader_ftp, lambda x: self.post_processor(x))
        list(downloader.iterate(local_path=self.local_path))

    def post_processor(self, f):
        logger = logging.getLogger(__name__)
        # Run post processing
        data_dicts = self.parser.extract_parse(f)
        # Send to DB
        self.db.post_papers(data_dicts)
        print(f"Saved {len(data_dicts)} to DB...")
        # Clean up
        os.remove(f)
        logger.info("Parsed and deleted local copy...")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_comm/
    orchestrator = PubMedFTPSQLOrchestrator(
        host="ftp.ncbi.nlm.nih.gov",
        ftp_path="/pub/pmc/oa_bulk/oa_comm/xml/",
        # Regex for .tar.gz files like oa_comm_xml.incr.2024-01-29.tar.gz
        # reg_ex=".*oa_comm_xml.incr.2023-12-19.tar.gz")
        reg_ex="oa_comm_xml.incr.*.tar.gz"
    )
    orchestrator.run()
