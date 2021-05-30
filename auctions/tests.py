from django.test import TestCase
from auctions.models import Listing, User, Category
from datetime import datetime, timezone

# Create your tests here.


class ListingTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            username = "marcos",
            password = "pbkdf2_sha256$216000$Q6Hx5oddOBdX$cHmPBCiyBymUuwd8JLlbQxnlpX8kv2N34fdINuqgAZM=",
            email = "marcos@wadahome.com",
        )

        Category.objects.create (
            description = "Kitchen test"
        )
        cat1 = Category.objects.get(id=1)
        user1 = User.objects.all().first()
        print(user1.email)
        for i in range(1,10):
            Listing.objects.create(
                active = True, 
                owner = user1, 
                creationDate = datetime.now(timezone.utc), 
                title="teste"+str(i), 
                description="Teste +str(i)", 
                category = cat1,
                currentPrice = 1, 
                initialPrice = 0.5)

    def testDate(self):
        start=datetime(2021,2,23,8,15,0,500000,tzinfo=timezone.utc)
        end=datetime(2021,2,25,8,15,0,500000,tzinfo=timezone.utc)
        for i in Listing.objects.filter(creationDate__range=(start, end)):
            print (i.creationDate)
        self.assertEqual(True, True)
        self.assertEqual(False, False)