# Copyright 2013 IBM Corp.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from nova.api.openstack.compute import plugins
from nova.api.openstack.compute.plugins.v3 import access_ips
from nova.api.openstack.compute.plugins.v3 import servers
from nova.api.openstack import wsgi
from nova.compute import api as compute_api
from nova import db
from nova import exception
from nova.objects import instance as instance_obj
from nova.openstack.common import jsonutils
from nova import test
from nova.tests.api.openstack import fakes
from nova.tests.image import fake


class AccessIPsExtTest(test.NoDBTestCase):
    def setUp(self):
        super(AccessIPsExtTest, self).setUp()
        self.access_ips_ext = access_ips.AccessIPs(None)

    def _test(self, func):
        server_dict = {access_ips.AccessIPs.v4_key: '1.1.1.1',
                       access_ips.AccessIPs.v6_key: 'fe80::'}
        create_kwargs = {}
        func(server_dict, create_kwargs)
        self.assertEqual(create_kwargs, {'access_ip_v4': '1.1.1.1',
                                         'access_ip_v6': 'fe80::'})

    def _test_with_ipv4_only(self, func):
        server_dict = {access_ips.AccessIPs.v4_key: '1.1.1.1'}
        create_kwargs = {}
        func(server_dict, create_kwargs)
        self.assertEqual(create_kwargs, {'access_ip_v4': '1.1.1.1'})

    def _test_with_ipv6_only(self, func):
        server_dict = {access_ips.AccessIPs.v6_key: 'fe80::'}
        create_kwargs = {}
        func(server_dict, create_kwargs)
        self.assertEqual(create_kwargs, {'access_ip_v6': 'fe80::'})

    def _test_without_ipv4_and_ipv6(self, func):
        server_dict = {}
        create_kwargs = {}
        func(server_dict, create_kwargs)
        self.assertEqual(create_kwargs, {})

    def _test_with_ipv4_null(self, func):
        server_dict = {access_ips.AccessIPs.v4_key: None}
        create_kwargs = {}
        func(server_dict, create_kwargs)
        self.assertEqual(create_kwargs, {'access_ip_v4': None})

    def _test_with_ipv6_null(self, func):
        server_dict = {access_ips.AccessIPs.v6_key: None}
        create_kwargs = {}
        func(server_dict, create_kwargs)
        self.assertEqual(create_kwargs, {'access_ip_v6': None})

    def _test_with_ipv4_blank(self, func):
        server_dict = {access_ips.AccessIPs.v4_key: ''}
        create_kwargs = {}
        func(server_dict, create_kwargs)
        self.assertEqual(create_kwargs, {'access_ip_v4': None})

    def _test_with_ipv6_blank(self, func):
        server_dict = {access_ips.AccessIPs.v6_key: ''}
        create_kwargs = {}
        func(server_dict, create_kwargs)
        self.assertEqual(create_kwargs, {'access_ip_v6': None})

    def test_server_create(self):
        self._test(self.access_ips_ext.server_create)

    def test_server_create_with_ipv4_only(self):
        self._test_with_ipv4_only(self.access_ips_ext.server_create)

    def test_server_create_with_ipv6_only(self):
        self._test_with_ipv6_only(self.access_ips_ext.server_create)

    def test_server_create_without_ipv4_and_ipv6(self):
        self._test_without_ipv4_and_ipv6(self.access_ips_ext.server_create)

    def test_server_create_with_ipv4_null(self):
        self._test_with_ipv4_null(self.access_ips_ext.server_create)

    def test_server_create_with_ipv6_null(self):
        self._test_with_ipv6_null(self.access_ips_ext.server_create)

    def test_server_create_with_ipv4_blank(self):
        self._test_with_ipv4_blank(self.access_ips_ext.server_create)

    def test_server_create_with_ipv6_blank(self):
        self._test_with_ipv6_blank(self.access_ips_ext.server_create)

    def test_server_update(self):
        self._test(self.access_ips_ext.server_update)

    def test_server_update_with_ipv4_only(self):
        self._test_with_ipv4_only(self.access_ips_ext.server_update)

    def test_server_update_with_ipv6_only(self):
        self._test_with_ipv6_only(self.access_ips_ext.server_update)

    def test_server_update_without_ipv4_and_ipv6(self):
        self._test_without_ipv4_and_ipv6(self.access_ips_ext.server_update)

    def test_server_update_with_ipv4_null(self):
        self._test_with_ipv4_null(self.access_ips_ext.server_update)

    def test_server_update_with_ipv6_null(self):
        self._test_with_ipv6_null(self.access_ips_ext.server_update)

    def test_server_update_with_ipv4_blank(self):
        self._test_with_ipv4_blank(self.access_ips_ext.server_update)

    def test_server_update_with_ipv6_blank(self):
        self._test_with_ipv6_blank(self.access_ips_ext.server_update)

    def test_server_rebuild(self):
        self._test(self.access_ips_ext.server_rebuild)

    def test_server_rebuild_with_ipv4_only(self):
        self._test_with_ipv4_only(self.access_ips_ext.server_rebuild)

    def test_server_rebuild_with_ipv6_only(self):
        self._test_with_ipv6_only(self.access_ips_ext.server_rebuild)

    def test_server_rebuild_without_ipv4_and_ipv6(self):
        self._test_without_ipv4_and_ipv6(self.access_ips_ext.server_rebuild)

    def test_server_rebuild_with_ipv4_null(self):
        self._test_with_ipv4_null(self.access_ips_ext.server_rebuild)

    def test_server_rebuild_with_ipv6_null(self):
        self._test_with_ipv6_null(self.access_ips_ext.server_rebuild)

    def test_server_rebuild_with_ipv4_blank(self):
        self._test_with_ipv4_blank(self.access_ips_ext.server_rebuild)

    def test_server_rebuild_with_ipv6_blank(self):
        self._test_with_ipv6_blank(self.access_ips_ext.server_rebuild)


class AccessIPsExtAPIValidationTest(test.TestCase):
    def setUp(self):
        super(AccessIPsExtAPIValidationTest, self).setUp()

        def fake_save(context, **kwargs):
            pass

        def fake_rebuild(*args, **kwargs):
            pass

        ext_info = plugins.LoadedExtensionInfo()
        self.controller = servers.ServersController(extension_info=ext_info)
        fake.stub_out_image_service(self.stubs)
        self.stubs.Set(db, 'instance_get_by_uuid', fakes.fake_instance_get())
        self.stubs.Set(instance_obj.Instance, 'save', fake_save)
        self.stubs.Set(compute_api.API, 'rebuild', fake_rebuild)

    def _test_create(self, params):
        body = {
            'server': {
                'name': 'server_test',
                'imageRef': '76fa36fc-c930-4bf3-8c8a-ea2a2420deb6',
                'flavorRef': 'http://localhost/123/flavors/3',
            },
        }
        body['server'].update(params)

        req = fakes.HTTPRequestV3.blank('/servers')
        req.method = 'POST'
        req.headers['content-type'] = 'application/json'
        req.body = jsonutils.dumps(body)
        self.controller.create(req, body=body)

    def _test_update(self, params):
        body = {
            'server': {
            },
        }
        body['server'].update(params)

        req = fakes.HTTPRequestV3.blank('/servers')
        req.method = 'PUT'
        req.headers['content-type'] = 'application/json'
        req.body = jsonutils.dumps(body)
        self.controller.update(req, fakes.FAKE_UUID, body=body)

    def _test_rebuild(self, params):
        body = {
            'rebuild': {
                'imageRef': '76fa36fc-c930-4bf3-8c8a-ea2a2420deb6',
            },
        }
        body['rebuild'].update(params)
        req = fakes.HTTPRequestV3.blank('/servers')
        req.method = 'PUT'
        req.headers['content-type'] = 'application/json'
        req.body = jsonutils.dumps(body)
        self.controller._action_rebuild(req, fakes.FAKE_UUID, body=body)

    def test_create_server_with_access_ipv4(self):
        params = {access_ips.AccessIPs.v4_key: '192.168.0.10'}
        self._test_create(params)

    def test_create_server_with_invalid_access_ipv4(self):
        params = {access_ips.AccessIPs.v4_key: '1.1.1.1.1.1'}
        self.assertRaises(exception.ValidationError, self._test_create, params)

    def test_create_server_with_access_ipv6(self):
        params = {access_ips.AccessIPs.v6_key: '2001:db8::9abc'}
        self._test_create(params)

    def test_create_server_with_invalid_access_ipv6(self):
        params = {access_ips.AccessIPs.v6_key: 'fe80:::::::'}
        self.assertRaises(exception.ValidationError, self._test_create, params)

    def test_update_server_with_access_ipv4(self):
        params = {access_ips.AccessIPs.v4_key: '192.168.0.10'}
        self._test_update(params)

    def test_update_server_with_invalid_access_ipv4(self):
        params = {access_ips.AccessIPs.v4_key: '1.1.1.1.1.1'}
        self.assertRaises(exception.ValidationError, self._test_update, params)

    def test_update_server_with_access_ipv6(self):
        params = {access_ips.AccessIPs.v6_key: '2001:db8::9abc'}
        self._test_update(params)

    def test_update_server_with_invalid_access_ipv6(self):
        params = {access_ips.AccessIPs.v6_key: 'fe80:::::::'}
        self.assertRaises(exception.ValidationError, self._test_update, params)

    def test_rebuild_server_with_access_ipv4(self):
        params = {access_ips.AccessIPs.v4_key: '192.168.0.10'}
        self._test_rebuild(params)

    def test_rebuild_server_with_invalid_access_ipv4(self):
        params = {access_ips.AccessIPs.v4_key: '1.1.1.1.1.1'}
        self.assertRaises(exception.ValidationError, self._test_rebuild,
                          params)

    def test_rebuild_server_with_access_ipv6(self):
        params = {access_ips.AccessIPs.v6_key: '2001:db8::9abc'}
        self._test_rebuild(params)

    def test_rebuild_server_with_invalid_access_ipv6(self):
        params = {access_ips.AccessIPs.v6_key: 'fe80:::::::'}
        self.assertRaises(exception.ValidationError, self._test_rebuild,
                          params)


class AccessIPsControllerTest(test.NoDBTestCase):
    def setUp(self):
        super(AccessIPsControllerTest, self).setUp()
        self.controller = access_ips.AccessIPsController()

    def _test_with_access_ips(self, func, kwargs={'id': 'fake'}):
        req = wsgi.Request({'nova.context':
                    fakes.FakeRequestContext('fake_user', 'fake',
                                             is_admin=True)})
        instance = {'uuid': 'fake',
                    'access_ip_v4': '1.1.1.1',
                    'access_ip_v6': 'fe80::'}
        req.cache_db_instance(instance)
        resp_obj = wsgi.ResponseObject(
            {"server": {'id': 'fake'}})
        func(req, resp_obj, **kwargs)
        self.assertEqual(resp_obj.obj['server'][access_ips.AccessIPs.v4_key],
                         '1.1.1.1')
        self.assertEqual(resp_obj.obj['server'][access_ips.AccessIPs.v6_key],
                         'fe80::')

    def _test_without_access_ips(self, func, kwargs={'id': 'fake'}):
        req = wsgi.Request({'nova.context':
                    fakes.FakeRequestContext('fake_user', 'fake',
                                             is_admin=True)})
        instance = {'uuid': 'fake',
                    'access_ip_v4': None,
                    'access_ip_v6': None}
        req.cache_db_instance(instance)
        resp_obj = wsgi.ResponseObject(
            {"server": {'id': 'fake'}})
        func(req, resp_obj, **kwargs)
        self.assertEqual(resp_obj.obj['server'][access_ips.AccessIPs.v4_key],
                         '')
        self.assertEqual(resp_obj.obj['server'][access_ips.AccessIPs.v6_key],
                         '')

    def test_create(self):
        self._test_with_access_ips(self.controller.create, {'body': {}})

    def test_create_without_access_ips(self):
        self._test_with_access_ips(self.controller.create, {'body': {}})

    def test_show(self):
        self._test_with_access_ips(self.controller.show)

    def test_show_without_access_ips(self):
        self._test_without_access_ips(self.controller.show)

    def test_detail(self):
        req = wsgi.Request({'nova.context':
                    fakes.FakeRequestContext('fake_user', 'fake',
                                             is_admin=True)})
        instance1 = {'uuid': 'fake1',
                     'access_ip_v4': '1.1.1.1',
                     'access_ip_v6': 'fe80::'}
        instance2 = {'uuid': 'fake2',
                     'access_ip_v4': '1.1.1.2',
                     'access_ip_v6': 'fe81::'}
        req.cache_db_instance(instance1)
        req.cache_db_instance(instance2)
        resp_obj = wsgi.ResponseObject(
            {"servers": [{'id': 'fake1'}, {'id': 'fake2'}]})
        self.controller.detail(req, resp_obj)
        self.assertEqual(
            resp_obj.obj['servers'][0][access_ips.AccessIPs.v4_key],
            '1.1.1.1')
        self.assertEqual(
            resp_obj.obj['servers'][0][access_ips.AccessIPs.v6_key],
            'fe80::')
        self.assertEqual(
            resp_obj.obj['servers'][1][access_ips.AccessIPs.v4_key],
            '1.1.1.2')
        self.assertEqual(
            resp_obj.obj['servers'][1][access_ips.AccessIPs.v6_key],
            'fe81::')

    def test_detail_without_access_ips(self):
        req = wsgi.Request({'nova.context':
                    fakes.FakeRequestContext('fake_user', 'fake',
                                             is_admin=True)})
        instance1 = {'uuid': 'fake1',
                     'access_ip_v4': None,
                     'access_ip_v6': None}
        instance2 = {'uuid': 'fake2',
                     'access_ip_v4': None,
                     'access_ip_v6': None}
        req.cache_db_instance(instance1)
        req.cache_db_instance(instance2)
        resp_obj = wsgi.ResponseObject(
            {"servers": [{'id': 'fake1'}, {'id': 'fake2'}]})
        self.controller.detail(req, resp_obj)
        self.assertEqual(
            resp_obj.obj['servers'][0][access_ips.AccessIPs.v4_key], '')
        self.assertEqual(
            resp_obj.obj['servers'][0][access_ips.AccessIPs.v6_key], '')
        self.assertEqual(
            resp_obj.obj['servers'][1][access_ips.AccessIPs.v4_key], '')
        self.assertEqual(
            resp_obj.obj['servers'][1][access_ips.AccessIPs.v6_key], '')

    def test_update(self):
        self._test_with_access_ips(self.controller.update, {'id': 'fake',
                                                            'body': {}})

    def test_update_without_access_ips(self):
        self._test_without_access_ips(self.controller.update, {'id': 'fake',
                                                               'body': {}})

    def test_rebuild(self):
        self._test_with_access_ips(self.controller.rebuild, {'id': 'fake',
                                                             'body': {}})

    def test_rebuild_without_access_ips(self):
        self._test_without_access_ips(self.controller.rebuild, {'id': 'fake',
                                                                'body': {}})
