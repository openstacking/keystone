# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import uuid


class ShadowUsersCoreTests(object):
    def test_shadow_federated_user(self):
        user = self.identity_api.shadow_federated_user(
            self.federated_user['idp_id'],
            self.federated_user['protocol_id'],
            self.federated_user['unique_id'],
            self.federated_user['display_name'])
        self.assertIsNotNone(user['id'])
        self.assertEqual(5, len(user.keys()))
        self.assertIsNotNone(user['name'])
        self.assertIsNone(user['password_expires_at'])
        self.assertIsNotNone(user['domain_id'])
        # NOTE(breton): below, attribute `enabled` is explicitly tested to be
        # equal True. assertTrue should not be used, because it converts
        # the passed value to bool().
        self.assertEqual(True, user['enabled'])

    def test_shadow_existing_federated_user(self):

        # introduce the user to keystone for the first time
        shadow_user1 = self.identity_api.shadow_federated_user(
            self.federated_user['idp_id'],
            self.federated_user['protocol_id'],
            self.federated_user['unique_id'],
            self.federated_user['display_name'])
        self.assertEqual(self.federated_user['display_name'],
                         shadow_user1['name'])

        # shadow the user again, with another name to invalidate the cache
        # internally, this operation causes request to the driver. It should
        # not fail.
        self.federated_user['display_name'] = uuid.uuid4().hex
        shadow_user2 = self.identity_api.shadow_federated_user(
            self.federated_user['idp_id'],
            self.federated_user['protocol_id'],
            self.federated_user['unique_id'],
            self.federated_user['display_name'])
        self.assertEqual(self.federated_user['display_name'],
                         shadow_user2['name'])
        self.assertNotEqual(shadow_user1['name'], shadow_user2['name'])

        # The shadowed users still share the same unique ID.
        self.assertEqual(shadow_user1['id'], shadow_user2['id'])