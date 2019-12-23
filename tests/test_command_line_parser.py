from unittest import TestCase

from bisturi import main


class CommandLineParserTestCase(TestCase):

    def test_should_validate_minimal_configuration(self):
        configs = {'source': {'host': 'localhost', 'database': 'reservafacil'}, 'dest': {
            'host': 'localhost', 'database': 'reservafacil'}}

        errors = main.do_validate_configs(configs)

        self.assertEquals(len(errors), 0)

    def test_should_not_allow_connection_configuration_without_host_or_database(self):
        configs = {'source': {}, 'dest': {}}

        errors = main.do_validate_configs(configs)

        self.assertGreaterEqual(len(errors), 1)
        self.assertEquals(errors[0], '"source.host" key not found')

        self.assertGreaterEqual(len(errors), 2)
        self.assertEquals(errors[1], '"source.database" key not found')

        self.assertGreaterEqual(len(errors), 3)
        self.assertEquals(errors[2], '"dest.host" key not found')

        self.assertGreaterEqual(len(errors), 4)
        self.assertEquals(errors[3], '"dest.database" key not found')

        self.assertEquals(len(errors), 4)

    def test_should_not_allow_configuration_without_source_or_dest(self):
        configs = {}

        errors = main.do_validate_configs(configs)

        self.assertGreaterEqual(len(errors), 1)
        self.assertEquals(errors[0], '"source" key not found')

        self.assertGreaterEqual(len(errors), 2)
        self.assertEquals(errors[1], '"dest" key not found')

        self.assertEquals(len(errors), 2)
