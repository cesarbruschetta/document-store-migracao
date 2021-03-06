import unittest
import os
from unittest.mock import patch, ANY

from documentstore_migracao.main.migrate_articlemeta import migrate_articlemeta_parser
from . import SAMPLES_PATH


class TestMigrateProcess(unittest.TestCase):
    @patch("documentstore_migracao.processing.extracted.extract_all_data")
    def test_command_extrate(self, mk_extract_all_data):

        migrate_articlemeta_parser(
            ["extract", os.path.join(SAMPLES_PATH, "documents_pids.txt")]
        )
        mk_extract_all_data.assert_called_once_with(
            ["S0021-25712009000400001\n", "S0021-25712009000400002"]
        )

    @patch("documentstore_migracao.processing.conversion.convert_article_ALLxml")
    def test_command_conversion(self, mk_convert_article_ALLxml):

        migrate_articlemeta_parser(["convert"])
        mk_convert_article_ALLxml.assert_called_once_with()

    @patch("documentstore_migracao.processing.conversion.convert_article_xml")
    def test_command_conversion_arg_pathFile(self, mk_convert_article_xml):

        migrate_articlemeta_parser(["convert", "--file", "/tmp/example.xml"])
        mk_convert_article_xml.assert_called_once_with("/tmp/example.xml")

    @patch("documentstore_migracao.processing.validation.validate_article_ALLxml")
    def test_command_validation(self, mk_validate_article_ALLxml):

        migrate_articlemeta_parser(["validate"])
        mk_validate_article_ALLxml.assert_called_once_with(False, False)

    @patch("documentstore_migracao.processing.validation.validate_article_xml")
    def test_command_validation_arg_validateFile(self, mk_validate_article_xml):

        migrate_articlemeta_parser(["validate", "--file", "/tmp/example.xml"])
        mk_validate_article_xml.assert_called_once_with("/tmp/example.xml")

    @patch("documentstore_migracao.processing.packing.pack_article_ALLxml")
    def test_command_pack_sps(self, mk_pack_article_ALLxml):

        migrate_articlemeta_parser(["pack"])
        mk_pack_article_ALLxml.assert_called_once_with()

    @patch("documentstore_migracao.processing.packing.pack_article_xml")
    def test_command_pack_sps_arg_pathFile(self, mk_pack_article_xml):

        migrate_articlemeta_parser(["pack", "--file", "/tmp/example.xml"])
        mk_pack_article_xml.assert_called_once_with("/tmp/example.xml")

    @patch("documentstore_migracao.processing.inserting.import_documents_to_kernel")
    def test_command_import(self, mk_import_documents_to_kernel):

        migrate_articlemeta_parser(
            [
                "import",
                "--uri",
                "mongodb://user:password@mongodb-host/?authSource=admin",
                "--db",
                "document-store",
                "--minio_host",
                "localhost:9000",
                "--minio_access_key",
                "minio",
                "--minio_secret_key",
                "minio123",
                "--output",
                "/tmp/docs.json"
            ]
        )
        mk_import_documents_to_kernel.assert_called_once_with(
            session_db=ANY, storage=ANY, folder=ANY, output_path=ANY
        )

    @patch("documentstore_migracao.processing.inserting.register_documents_in_documents_bundle")
    def test_command_link_documents_issues(self, mk_register_documents_in_documents_bundle):

        migrate_articlemeta_parser(
            [
                "link_documents_issues",
                "--uri",
                "mongodb://user:password@mongodb-host/?authSource=admin",
                "--db",
                "document-store",
                "/tmp/docs.json",
                "/tmp/jornal.json",
            ]
        )
        mk_register_documents_in_documents_bundle.assert_called_once_with(
            session_db=ANY, file_documents=ANY, file_journals=ANY
        )

    def test_not_arg(self):

        with self.assertRaises(SystemExit) as cm:
            migrate_articlemeta_parser([])
            self.assertEqual("Vc deve escolher algum parametro", str(cm.exception))
