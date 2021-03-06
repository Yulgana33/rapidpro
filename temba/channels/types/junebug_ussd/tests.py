from __future__ import unicode_literals, absolute_import


from django.urls import reverse
from temba.tests import TembaTest
from ...models import Channel


class JunebugTypeTest(TembaTest):

    def test_claim(self):
        Channel.objects.all().delete()
        self.login(self.admin)

        url = reverse('channels.claim_junebug_ussd')

        # check that claim page URL appears on claim list page
        response = self.client.get(reverse('channels.channel_claim'))
        self.assertContains(response, url)

        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

        post_data = {
            "country": "ZA",
            "number": "+273454325324",
            "url": "http://example.com/messages.json",
            "username": "foo",
            "password": "bar",
            "secret": "secret-word"
        }

        response = self.client.post(url, post_data)

        channel = Channel.objects.get()
        self.assertEquals(channel.channel_type, 'JNU')
        self.assertEquals(channel.role, Channel.ROLE_USSD)
        self.assertEqual(channel.secret, "secret-word")
