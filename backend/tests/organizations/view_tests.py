"""Tests for organization endpoints."""


import json
import unittest

import harness


class OrganizationTest(harness.TestHarness):
    """Tests for organization endpoints."""

    @harness.with_sess(user_id=1)
    def test_crud(self):
        """Basic CRUD tests."""
        # create a user
        resp = self.post_json("/v1/users/", {"name": "snakes"})
        self.assertEqual(json.loads(resp.data), {
            'avatar_url': None,
            'id': 1,
            'organizations': [],
            'url': '/v1/users/1',
            'name': 'snakes'})

        # no quest yet, so 404
        resp = self.app.get("/v1/organizations/1")
        self.assertEqual(resp.status_code, 404)

        # create an org
        resp = self.post_json(
                "/v1/organizations/",
                {"name": "hotel", "description": "cat hotel house"})
        self.assertEqual(resp.status_code, 200)

        # and get it back
        resp = self.app.get("/v1/organizations/1")
        self.assertEqual(json.loads(resp.data), {
            "description": "cat hotel house",
            "icon_url": None,
            "id": 1,
            "members": [],
            "name": "hotel",
            "url": "/v1/organizations/1",
            "user_id": 1})

        # edit
        resp = self.put_json('/v1/organizations/1', {
            'icon_url': 'rubber'})
        self.assertEqual(resp.status_code, 200)

        # and get it back
        resp = self.app.get("/v1/organizations/1")
        self.assertEqual(json.loads(resp.data), {
            "description": "cat hotel house",
            "icon_url": 'rubber',
            "id": 1,
            "members": [],
            "name": "hotel",
            "url": "/v1/organizations/1",
            "user_id": 1})

        # delete
        resp = self.app.delete("/v1/organizations/1")
        self.assertEqual(resp.status_code, 200)

        # and it's gone
        resp = self.app.get("/v1/organizations/1")
        self.assertEqual(resp.status_code, 404)

        resp = self.put_json('/v1/organizations/1', {'name': 'no!'})
        self.assertEqual(resp.status_code, 404)

        resp = self.app.delete("/v1/organizations/1")
        self.assertEqual(resp.status_code, 404)

    @harness.with_sess(user_id=1)
    def test_links(self):
        """Test linking users and organizations together."""

        # create the resources
        resp = self.post_json("/v1/users/", {"name": "snakes"})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json("/v1/users/", {"name": "rakes"})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                "/v1/organizations/",
                {"name": "mouse", "description": "nip"})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                "/v1/organizations/",
                {"name": "blouse", "description": "blip"})
        self.assertEqual(resp.status_code, 200)

        # no links yet
        resp = self.app.get("/v1/organizations/1")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data)['members'], [])

        resp = self.app.get("/v1/organizations/2")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data)['members'], [])

        # create some links
        resp = self.app.put("/v1/organizations/1/users/1")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.put("/v1/organizations/1/users/2")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.put("/v1/organizations/2/users/2")
        self.assertEqual(resp.status_code, 200)

        # see the links on the organizations
        resp = self.app.get("/v1/organizations/1")
        self.assertEqual(json.loads(resp.data)['members'], [
            {"id": 1, "name": "snakes",
                "url": "/v1/users/1", "avatar_url": None},
            {"id": 2, "name": "rakes",
                "url": "/v1/users/2", "avatar_url": None}])

        resp = self.app.get("/v1/organizations/2")
        self.assertEqual(json.loads(resp.data)['members'], [
            {"id": 2, "name": "rakes",
                "url": "/v1/users/2", "avatar_url": None}])

        # and on the users
        resp = self.app.get("/v1/users/1")
        self.assertEqual(json.loads(resp.data)['organizations'], [
            {'id': 1, 'name': 'mouse', 'icon_url': None,
                'url': '/v1/organizations/1'}])

        resp = self.app.get("/v1/users/2")
        self.assertEqual(json.loads(resp.data)['organizations'], [
            {'id': 1, 'name': 'mouse', 'icon_url': None,
                'url': '/v1/organizations/1'},
            {'id': 2, 'name': 'blouse', 'icon_url': None,
                'url': '/v1/organizations/2'}])

        # check idempotency
        resp = self.app.put("/v1/organizations/1/users/1")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/v1/organizations/1")
        self.assertEqual(json.loads(resp.data)['members'], [
            {"id": 1, "name": "snakes",
                "url": "/v1/users/1", "avatar_url": None},
            {"id": 2, "name": "rakes",
                "url": "/v1/users/2", "avatar_url": None}])

        resp = self.app.get("/v1/organizations/2")
        self.assertEqual(json.loads(resp.data)['members'], [
            {"id": 2, "name": "rakes",
                "url": "/v1/users/2", "avatar_url": None}])

        # delete a link
        resp = self.app.delete("/v1/organizations/1/users/2")
        self.assertEqual(resp.status_code, 200)

        # and it's gone
        resp = self.app.get("/v1/organizations/1")
        self.assertEqual(json.loads(resp.data)['members'], [
            {"id": 1, "name": "snakes",
                "url": "/v1/users/1", "avatar_url": None}])

        resp = self.app.get("/v1/organizations/2")
        self.assertEqual(json.loads(resp.data)['members'], [
            {"id": 2, "name": "rakes",
                "url": "/v1/users/2", "avatar_url": None}])


if __name__ == '__main__':
    unittest.main()
