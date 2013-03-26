@tags @tag
Feature: Test of create template with wrong param

    Scenario: User can see templates
        When User see templates
        Then Response is "200"
        And Response list of list node_templates:"[u'jt_nn.small', u'jt_nn.medium', u'jt.small', u'jt.medium', u'nn.small', u'nn.medium', u'tt_dn.small', u'tt_dn.medium']"

    Scenario: User can't create template DN
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-4",
                "node_type": "DN",
                "flavor_id": "m1.medium",
                "data_node": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can see templates
        When User see templates
        Then Response is "200"
        And Response list of list node_templates:"[u'jt_nn.small', u'jt_nn.medium', u'jt.small', u'jt.medium', u'nn.small', u'nn.medium', u'tt_dn.small', u'tt_dn.medium']"

    Scenario: User can't create template TT
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "TT",
                "flavor_id": "m1.medium",
                "task_tracker": {
                    "heap_size": 384,
                    "max_map_tasks": 3,
                    "max_reduce_tasks": 1,
                    "task_heap_size": 640
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can see templates, if list has two templates
        When User see templates
        Then Response is "200"
        And Response list of list node_templates:"[u'jt_nn.small', u'jt_nn.medium', u'jt.small', u'jt.medium', u'nn.small', u'nn.medium', u'tt_dn.small', u'tt_dn.medium', u'QA-node-1', u'QA-node-2', u'QA-node-3', u'QA-node-4', u'QA-node-5', u'QA-node-6']"


    Scenario: User can't create template with empty JSON
        Given node_template body
        """
        {
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong JSON
        Given node_template body
        """
        {
            "node_template": {
                "qwe": "QA-node-1",
                "qwe_qe": "TT+DN",
                "qwe_id": "m1.medium",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template without name in JSON
        Given node_template body
        """
        {
            "node_template": {
                "node_type": "TT",
                "flavor_id": "m1.medium",
                "task_tracker": {
                    "heap_size": 384,
                    "max_map_tasks": 3,
                    "max_reduce_tasks": 1,
                    "task_heap_size": 640
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template without node_type in JSON
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "flavor_id": "m1.medium",
                "task_tracker": {
                    "heap_size": 384,
                    "max_map_tasks": 3,
                    "max_reduce_tasks": 1,
                    "task_heap_size": 640
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template without flavor_id in JSON
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "TT",
                "task_tracker": {
                    "heap_size": 384,
                    "max_map_tasks": 3,
                    "max_reduce_tasks": 1,
                    "task_heap_size": 640
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template without node_param in JSON
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "TT",
                "flavor_id": "m1.medium",
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template without node_param in JSON
        Given node_template body
        """
        {
            "node_template": {
            "name": "QA-node-6",
            "node_type": "DN",
            "flavor_id": "m1.medium",
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"
#TT+DN_________________________________________________________________________

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "TT+DN",
                "flavor_id": "m1.medium",
                "job_tracker": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "TT+DN",
                "flavor_id": "m1.medium",
                "name_node": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "TT+DN",
                "flavor_id": "m1.medium",
                "task_tracker": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "TT+DN",
                "flavor_id": "m1.medium",
                "data_node": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "TT+DN",
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
        Then Response is "400"
        #And Error content:"{list}"

#JT+NN_________________________________________________________________________

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "JT+NN",
                "flavor_id": "m1.medium",
                "task_tracker": {
                    "heap_size": 384
                },
                "data_node": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "JT+NN",
                "flavor_id": "m1.medium",
                "task_tracker": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "JT+NN",
                "flavor_id": "m1.medium",
                "data_node": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "JT+NN",
                "flavor_id": "m1.medium",
                "name_node": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "JT+NN",
                "flavor_id": "m1.medium",
                "job_tracker": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"
#NN____________________________________________________________________________

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "NN",
                "flavor_id": "m1.medium",
                "task_tracker": {
                    "heap_size": 384
                },
                "data_node": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "NN",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "NN",
                "flavor_id": "m1.medium",
                "task_tracker": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "NN",
                "flavor_id": "m1.medium",
                "data_node": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "NN",
                "flavor_id": "m1.medium",
                "job_tracker": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"
#JT____________________________________________________________________________


    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "JT",
                "flavor_id": "m1.medium",
                "task_tracker": {
                    "heap_size": 384
                },
                "data_node": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "JT",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "JT",
                "flavor_id": "m1.medium",
                "task_tracker": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "JT",
                "flavor_id": "m1.medium",
                "data_node": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template if param node_type not match node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-6",
                "node_type": "JT",
                "flavor_id": "m1.medium",
                "name_node": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

#empty values__________________________________________________________________

    Scenario: User can't create template for emtpy name
        Given node_template body
        """
        {
            "node_template": {
                "name": "",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template for emtpy node_type
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-template-1",
                "node_type": "",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template for emtpy flavor_id
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-template-1",
                "node_type": "NN",
                "flavor_id": "",
                "name_node": {
                    "heap_size": 384,
                }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template for emtpy node_param
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-template-1",
                "node_type": "JT+NN",
                "flavor_id": "m1.medium",
                "job_tracker": {
                    "heap_size": 384
                },
                "name_node": {
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template for emtpy heap_size
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-template-1",
                "node_type": "JT+NN",
                "flavor_id": "m1.medium",
                "job_tracker": {
                    "heap_size": 384
                },
                "name_node": {
                    "heap_size": ""
                }
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

#wrong values__________________________________________________________________

    Scenario: User can't create template with wrong name
        Given node_template body
        """
        {
            "node_template": {
                "name": "qa_node-1",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong name
        Given node_template body
        """
        {
            "node_template": {
                "name": "qa*node-1",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong name
        Given node_template body
        """
        {
            "node_template": {
                "name": "1q",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong name
        Given node_template body
        """
        {
            "node_template": {
                "name": "qwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopqwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopqwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopqwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopqwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiopwertyuiop",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong name
        Given node_template body
        """
        {
            "node_template": {
                "name": "-q",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong node_type
        Given node_template body
        """
        {
            "node_template": {
                "name": "qanode",
                "node_type": "TT+DN+abs",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong node_type
        Given node_template body
        """
        {
            "node_template": {
                "name": "qanode",
                "node_type": "abs+TT+DN",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong node_type
        Given node_template body
        """
        {
            "node_template": {
                "name": "qanode",
                "node_type": "TT-DN",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong node_type
        Given node_template body
        """
        {
            "node_template": {
                "name": "qanode",
                "node_type": "TT+DT",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong node_type
        Given node_template body
        """
        {
            "node_template": {
               "name": "qanode",
                "node_type": "*TT+DT",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong node_type
        Given node_template body
        """
        {
            "node_template": {
                "name": "qanode",
                "node_type": "TT+DT*",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong node_type
        Given node_template body
        """
        {
            "node_template": {
                "name": "qanode",
                "node_type": "T",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong node_type
        Given node_template body
        """
        {
            "node_template": {
                "name": "qanode",
                "node_type": "123",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong node_type
        Given node_template body
        """
        {
            "node_template": {
                "name": "qanode",
                "node_type": "#$%^&*()_|}{":?><TT+DN",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong flavor_id
        Given node_template body
        """
        {
            "node_template": {
                "name": "qanode",
                "node_type": "TT+DN",
                "flavor_id": "*",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong flavor_id
        Given node_template body
        """
        {
            "node_template": {
                "name": "qanode",
                "node_type": "TT+DN",
                "flavor_id": "!@#$%^&*()_+|}{":?><",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong flavor_id
        Given node_template body
        """
        {
            "node_template": {
                "name": "qanode",
                "node_type": "TT+DN",
                "flavor_id": "not.match.flavor",
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
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong node_patam
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-1",
                "node_type": "TT+DN",
                "flavor_id": "m1.medium",
                "task_tracker": {
                    "heap_size": 12!12
                },
                "data_node": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong node_patam
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-1",
                "node_type": "TT+DN",
                "flavor_id": "m1.medium",
                "task_tracker": {
                    "heap_size": %123
                },
                "data_node": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

    Scenario: User can't create template with wrong node_patam
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-1",
                "node_type": "TT+DN",
                "flavor_id": "m1.medium",
                "task_tracker": {
                    "heap_size": qwe
                },
                "data_node": {
                    "heap_size": 384
                }
            }
        }
        """
        When User create template
        Then Response is "400"
        #And Error content:"{list}"

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

    Scenario: User can't create template with already exist name
        Given node_template body
        """
        {
            "node_template": {
                "name": "QA-node-1",
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
        Then Response is "400"



