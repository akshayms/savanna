@tags @tag
Feature: Test of get template with wrong param

    Scenario: User can see templates
        When User see templates
        Then Response is "200"
        And Response list of list node_templates:"[u'jt_nn.small', u'jt_nn.medium', u'jt.small', u'jt.medium', u'nn.small', u'nn.medium', u'tt_dn.small', u'tt_dn.medium']"

    Scenario: User can create template for TT+DN
        Given node_template body
        """
        {
            "node_template": {
                "name": "node-for-get",
                "node_type": "NN",
                "flavor_id": "m1.medium",
                "name_node": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "202"

    Scenario: User can see templates, if list has two templates
        When User see templates
        Then Response is "200"
        And Response list of list node_templates:"[u'jt_nn.small', u'jt_nn.medium', u'jt.small', u'jt.medium', u'nn.small', u'nn.medium', u'tt_dn.small', u'tt_dn.medium', u'node-for-get']"

    Scenario: User can get template by id
        When User get template with id: "0"
        Then Response is "200"
        And Response for list node_template by id is:"{u'name_node': {u'heap_size': u'384'}, u'node_type': {u'processes': [u'name_node'], u'name': u'NN'}, u'flavor_id': u'm1.medium', u'name': u'node-for-get'}"

    Scenario: I can delete node_template by id
        When User delete template with id: "0"
        Then Response is "204"

    Scenario: User can't get template by id, if node is deleted
        When User get template with id: "0"
        Then Response is "404"

    Scenario: User can get template by id, if node is not exist
        When User get template with id: "0"
        Then Response is "404"
