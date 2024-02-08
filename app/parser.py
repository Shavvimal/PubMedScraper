from bs4 import BeautifulSoup
import tarfile
from models import PubMedModel

class PubMedXMLParser:
    """
    Extracts Nested XML Files from .tar.gz and parses them
    """

    def __init__(self):
        pass

    def parse_xml(self, xml_content) -> PubMedModel:
        soup = BeautifulSoup(xml_content, "html.parser")

        # Safely extracting data with checks for None
        pmid_element = soup.select_one('[pub-id-type="pmid"]')
        title_element = soup.select_one("article-title")
        abstract_element = soup.select_one("abstract")
        sec_elements = soup.select("body sec")
        author_elements = soup.select('[contrib-type="author"]')

        pmid = pmid_element.text.strip() if pmid_element else "N/A"
        title = title_element.text.strip() if title_element else "N/A"
        abstract = abstract_element.text.strip() if abstract_element else "N/A"
        full_text = "\n".join(sec.get_text(strip=True, separator=" ") for sec in sec_elements)
        authors = ", ".join(a.get_text(strip=True, separator=" ") for a in author_elements)

        data = {"pmid": pmid, "title": title, "abstract": abstract, "full_text": full_text, "authors": authors}
        # Return a Pydantic Model
        return PubMedModel(**data)

    def extract(self, tar_path):
        """
        Extracts all nested XML files from the .tar.gz file
        """
        files = []
        with tarfile.open(tar_path, "r:gz") as tar:
            for member in tar.getmembers():
                if member.isfile() and member.name.endswith(".xml"):
                    f = tar.extractfile(member)
                    if f:
                        files.append(f.read())  # Read and store file content directly
        return files

    def extract_parse(self, tar_path) -> list[PubMedModel]:
        """
        Extracts all nested XML files from the .tar.gz file and parses them into dictionaries. Returns a list of dictionaries.
        """
        xml_files_content = self.extract(tar_path)
        parsed_data = [self.parse_xml(content) for content in xml_files_content]
        return parsed_data


if __name__ == '__main__':
    parser = PubMedXMLParser()
    # data = parser.parse_xml("./test_data/PMC8578926.xml")
    # print(data)
    data_dicts = parser.extract_parse("./test_data/oa_comm_xml.incr.2023-12-19.tar.gz")
    print(data_dicts)
