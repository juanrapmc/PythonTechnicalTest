from rest_framework.test import APISimpleTestCase, APITestCase, APIClient
from rest_framework.exceptions import ValidationError, APIException
from unittest import TestCase, mock
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


class TestBondsModel(DTestCase):

    @mock.patch("bonds.models.getLeiLegalName")
    def setUp(self, m_getLegalName):
        self.User = get_user_model()
        user = self.User.objects.create(username="test", password="test")
        self.bond_data = {
            "isin": "ISIN",
            "size": 123,
            "currency": "GBP",
            "maturity": "2020-01-01",
            "lei": "TESTLEI",
            "user": user
        }
        user2 = self.User.objects.create(username="test2", password="test2")
        m_getLegalName.return_value = "TEST VAL1"
        Bond.objects.create(**self.bond_data)
        self.bond_data["user"] = user2
        m_getLegalName.return_value = "TEST VAL2"
        Bond.objects.create(**self.bond_data)

    @mock.patch("bonds.models.getLeiLegalName")
    def test_bondCreate(self, m_getLegalName):
        m_getLegalName.return_value = "TEST VAL"
        self.assertEqual("TESTVAL", Bond.objects.create(**self.bond_data).legal_name)

    @mock.patch("bonds.models.getLeiLegalName")
    def test_bondCreateNoLegalName(self, m_getLegalName):
        m_getLegalName.return_value = None
        self.assertRaises(ValidationError, Bond.objects.create)

    def test_bondUser1GetOwnData(self):
        user = self.User.objects.get(username="test")
        bond = Bond.objects.all().filter(user=user)
        self.assertEqual(1, len(bond))
        self.assertEqual("TESTVAL1", bond[0].legal_name)


class TestBondsAPI(APITestCase):

    def setUp(self):
        self.User = get_user_model()
        self.User.objects.create(username="test", password="test")

    def test_unauthenticated(self):
        resp = self.client.get('/bonds/')
        self.assertEqual(resp.status_code, 403)

    def test_authenticated(self):
        client = APIClient()
        user = self.User.objects.get(username="test")
        client.force_authenticate(user=user)
        resp = client.get("/bonds/")
        self.assertEqual(resp.status_code, 200)
