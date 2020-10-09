from rest_framework.test import APISimpleTestCase
from unittest import TestCase, mock
from unittest.mock import patch
from bonds.utils import getLeiLegalName
from django.test import TestCase as DTestCase
from bonds.models import Bond
from django.contrib.auth import get_user_model


class HelloWorld(APISimpleTestCase):
    def test_root(self):
        resp = self.client.get("/")
        assert resp.status_code == 200


class TestUtils(TestCase):

    @mock.patch("bonds.utils.requests.get")
    def test_getLeiLegalNameSuccess(self, m_get):
        m_get.return_value = mock.Mock(ok=True)
        m_get.return_value.json.return_value = [
            {
                "LEI": { "$": "R0MUWSFPU8MPRO8K5P83" },
                "Entity": { "LegalName": { "@xml:lang": "fr", "$": "BNP PARIBAS" } },
            }
        ]
        self.assertEqual("BNP PARIBAS", getLeiLegalName("R0MUWSFPU8MPRO8K5P83"))

    @mock.patch("bonds.utils.requests.get")
    def test_getLiLegalNameNotExists(self, m_get):
        m_get.return_value = mock.Mock(ok=True)
        m_get.return_value.json.return_value = []
        self.assertEqual(None, getLeiLegalName("R0MUWSFPU8MPRO8K5P80"))

    @mock.patch("bonds.utils.requests.get")
    def tes_getLeiLegalNameNotOk(self, m_get):
        m_get.return_value - mock.Mock(ok=False)
        self.assertEqual(None, getLeiLegalName(""))


class TestBonds(DTestCase):

    def setUp(self):
        self.User = get_user_model()
        self.User.objects.create(username="test", password="test")

    @mock.patch("bonds.models.getLeiLegalName")
    def test_bondCreate(self, m_getLegalName):
        m_getLegalName.return_value = "TEST VAL"
        user = self.User.objects.get(username="test")
        bond = Bond.objects.create(
            isin="ISIN",
            size=123,
            currency="GBP",
            maturity="2020-01-01",
            lei="TESTLEI",
            user=user
        )
        self.assertEqual("TESTVAL", bond.legal_name)
