from django.test import TestCase, RequestFactory, Client
from hive.models import Hive, HiveTimeline
from users.models import BeeUser
from .views import createhive, viewhive, graphdata, createhivescsv
from django.utils import timezone

# Create your tests here.
class CreateHiveTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = BeeUser.objects.create(username="Test")

    def test_createhive(self):
        request = self.factory.post("/Test/createhive", {"hive_name" : "Hive 1"})
        request.user = self.user
        response = createhive(request, "Test")
        hive = Hive.objects.get(hive_name="Hive 1")
        self.assertEqual(hive.user, "Test")
        
class SelectHiveTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = BeeUser.objects.create(username="Test")
        Hive.objects.create(hive_name = "Hive 1", user="Test",creation_date=timezone.now())
        
    def test_selecthive(self):
        hive = Hive.objects.get(user="Test")
        request = self.factory.get("/Test/"+str(hive.pk))
        request.user = self.user
        response = viewhive(request, "Test", hive.pk)
        self.assertEqual(response.status_code, 200)        
        
class GraphTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = BeeUser.objects.create(username="Test")
        Hive.objects.create(hive_name = "Hive 1", user="Test",creation_date=timezone.now())
        hive = Hive.objects.get(user="Test")
        date = timezone.now()
        HiveTimeline.objects.create(hive_key=hive.pk,creation_date=date,edited_date=date,timeline_date=date,queen_spotted=False,pests_disease=False,plant_life=False)
        date = date.replace(year=2016)
        HiveTimeline.objects.create(hive_key=hive.pk,creation_date=date,edited_date=date,timeline_date=date,queen_spotted=False,pests_disease=False,plant_life=False)        
        
    def test_graph(self):
        hive = Hive.objects.get(user="Test")
        request = self.factory.get("/Test/"+str(hive.pk)+"/honey_cells/graphdata")
        request.user = self.user
        response = graphdata(request, "Test", hive.pk, "honey_cells")
        self.assertEqual(response.status_code, 200)        
        
class ExportTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = BeeUser.objects.create(username="Test")
        Hive.objects.create(hive_name = "Hive 1", user="Test",creation_date=timezone.now())
        hive = Hive.objects.get(user="Test")
        date = timezone.now()
        HiveTimeline.objects.create(hive_key=hive.pk,creation_date=date,edited_date=date,timeline_date=date,queen_spotted=False,pests_disease=False,plant_life=False)
        date = date.replace(year=2016)
        HiveTimeline.objects.create(hive_key=hive.pk,creation_date=date,edited_date=date,timeline_date=date,queen_spotted=False,pests_disease=False,plant_life=False)        
        
    def test_export(self):
        request = self.factory.get("/Test/exportall")
        request.user = self.user
        response = createhivescsv(request, "Test")
        self.assertEqual(response.status_code, 200) 
        