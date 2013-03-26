@tags @tag
Feature: Test of template section

    Scenario: User can see templates
        When User see templates
        Then Response is "200"
        And Response list of list node_templates:"[u'jt_nn.small', u'jt_nn.medium', u'jt.small', u'jt.medium', u'nn.small', u'nn.medium', u'tt_dn.small', u'tt_dn.medium']"

    Scenario: User can create template for TT+DN
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-1",
                "node_type": "TT+DN",
                "flavor_id": "m1.medium",
                "task_tracker": {
                    "heap_size": 384,
                    "max_map_tasks": 3,
                    "max_reduce_tasks": 1,
                    "task_heap_size": 640
                },
                "data_node": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "202"

    Scenario: User can see templates
        When User see templates
        Then Response is "200"
        And Response list of list node_templates:"[u'jt_nn.small', u'jt_nn.medium', u'jt.small', u'jt.medium', u'nn.small', u'nn.medium', u'tt_dn.small', u'tt_dn.medium', u'QA-node-1']"

    Scenario: User can create template JT+NN
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-2",
                "node_type": "JT+NN",
                "flavor_id": "m1.medium",
                "job_tracker": {
                    "heap_size": 384
                },
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
        And Response list of list node_templates:"[u'jt_nn.small', u'jt_nn.medium', u'jt.small', u'jt.medium', u'nn.small', u'nn.medium', u'tt_dn.small', u'tt_dn.medium', u'QA-node-1', u'QA-node-2']"

    Scenario: User can create template NN
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-3",
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
        And Response list of list node_templates:"[u'jt_nn.small', u'jt_nn.medium', u'jt.small', u'jt.medium', u'nn.small', u'nn.medium', u'tt_dn.small', u'tt_dn.medium', u'QA-node-1', u'QA-node-2', u'QA-node-3']"

    Scenario: User can create template JT
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-4",
                "node_type": "JT",
                "flavor_id": "m1.medium",
                "job_tracker": {
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
        And Response list of list node_templates:"[u'jt_nn.small', u'jt_nn.medium', u'jt.small', u'jt.medium', u'nn.small', u'nn.medium', u'tt_dn.small', u'tt_dn.medium', u'QA-node-1', u'QA-node-2', u'QA-node-3', u'QA-node-4']"

    Scenario: User can get template by id
        When User get template with id: "0"
        Then Response is "200"
        #And Response for list node_template by id is:"{u'name': u'QA-node-1', u'task_tracker': {u'heap_size': u'384'}, u'data_node': {u'heap_size': u'384'}, u'node_type': {u'processes': [u'task_tracker', u'data_node'], u'name': u'TT+DN'}, u'flavor_id': u'm1.medium'}"

    Scenario: User can delete template
        When User delete template with id: "0"
        Then Response is "204"

    Scenario: User can get templates
         When User see templates
         Then Response is "200"
         And Response list of list node_templates:"[u'jt_nn.small', u'jt_nn.medium', u'jt.small', u'jt.medium', u'nn.small', u'nn.medium', u'tt_dn.small', u'tt_dn.medium', u'QA-node-2', u'QA-node-3', u'QA-node-4']"

    Scenario: User can delete template
        When User delete template with id: "3"
        Then Response is "204"

    Scenario: User can get templates
         When User see templates
         Then Response is "200"
         And Response list of list node_templates:"[u'jt_nn.small', u'jt_nn.medium', u'jt.small', u'jt.medium', u'nn.small', u'nn.medium', u'tt_dn.small', u'tt_dn.medium', u'QA-node-2', u'QA-node-3']"

    Scenario: User can delete template
        When User delete template with id: "1"
        Then Response is "204"

    Scenario: User can get templates
         When User see templates
         Then Response is "200"
         And Response list of list node_templates:"[u'jt_nn.small', u'jt_nn.medium', u'jt.small', u'jt.medium', u'nn.small', u'nn.medium', u'tt_dn.small', u'tt_dn.medium', u'QA-node-3']"

    Scenario: User can delete template
        When User delete template with id: "2"
        Then Response is "204"

    Scenario: User can get templates
         When User see templates
         Then Response is "200"
         And Response list of list node_templates:"[u'jt_nn.small', u'jt_nn.medium', u'jt.small', u'jt.medium', u'nn.small', u'nn.medium', u'tt_dn.small', u'tt_dn.medium']"
