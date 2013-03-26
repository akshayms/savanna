@tags @tag
Feature: Test of delete template with wrong param

    Scenario: User can see templates
        When User see templates
        Then Response is "200"
        And Response list of list node_templates:"[u'jt_nn.small', u'jt_nn.medium', u'jt.small', u'jt.medium', u'nn.small', u'nn.medium', u'tt_dn.small', u'tt_dn.medium']"

    Scenario: User can create template for TT+DN
        Given node_template body
        """
        {
            "node_template": {
                "name": "node-for-delete",
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

    Scenario: User can see templates, if list has two templates
        When User see templates
        Then Response is "200"
        And Response list of list node_templates:"[u'jt_nn.small', u'jt_nn.medium', u'jt.small', u'jt.medium', u'nn.small', u'nn.medium', u'tt_dn.small', u'tt_dn.medium', u'node-for-delete']"

    Scenario: User can delete template
        When User delete template with id: "0"
        Then Response is "204"

    Scenario: User can see templates, if list has two templates
        When User see templates
        Then Response is "200"
        And Response list of list node_templates:"[u'jt_nn.small', u'jt_nn.medium', u'jt.small', u'jt.medium', u'nn.small', u'nn.medium', u'tt_dn.small', u'tt_dn.medium']"

    Scenario: User can't delete template, if template already delete
        When User delete template with id: "0"
        #Then Response is "404"

    Scenario: User can't delete template, if template non exist
        When User delete template with id: "101"
        #Then Response is "404"
