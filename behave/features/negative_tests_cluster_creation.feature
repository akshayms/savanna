@tags @tag
Feature: Negative tests for cluster section

    Scenario: User can create cluster with name "QA-cluster"
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt_nn.medium": 1,
                    "tt_dn.small": 1
                },
                "name": "QA-cluster",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When User create cluster
        Then  Response is "202"

    Scenario: User can not create cluster with name "QA-cluster" that already exists
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                 {"
                    jt_nn.medium": 1,
                    "tt_dn.small": 1
                 },
                 "name": "QA-cluster",
                 "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can delete cluster with name "QA-cluster" by ID
        When User delete cluster with id: "0"
        Then  Response is "204"

    Scenario: User can not create cluster with blank cluster name
        Given cluster data
        """
        {
            "cluster":
             {
                "node_templates":
                {
                    "jt_nn.medium": 1,
                    "tt_dn.small": 1
                },
                "name": "",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
             }
        }
        """
        When User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster with invalid characters in cluster name
        Given cluster data
        """
        {
            "cluster":
             {
                "node_templates":
                 {
                    "jt_nn.medium": 1,
                    "tt_dn.small": 1
                 },
                 "name": "QA_*&cluster",
                 "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
             }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster with space in cluster name
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt_nn.medium": 1,
                    "tt_dn.small": 1
                },
                "name": "QA cluster",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster with blank base image ID
        Given cluster data
        """
        {
            "cluster":
             {
                "node_templates":
                {
                    "jt_nn.medium": 1,
                    "tt_dn.small": 1
                },
                "name": "QA-cluster-1",
                "base_image_id": ""
             }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster with wrong base image ID #This cluster create #No validation
        #Given cluster data
        #"""
        #{"cluster": {"node_templates": {"jt_nn.medium": 1, "tt_dn.small": 1}, "name": "QA-cluster-2", "base_image_id": "abc"}}
        #"""
        #When  User create cluster
        #Then  Response is "400"

    Scenario: User can not create cluster with negative parameter in number of JT and NN
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                 {
                    "jt_nn.medium": -1,
                    "tt_dn.small": 1
                 },
                 "name": "QA-cluster-3",
                 "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster with negative parameter in number of TT and DN
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt_nn.medium": 1,
                    "tt_dn.small": -1
                },
                "name": "QA-cluster-4",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster with characters in number of JT and NN
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt_nn.medium": abc,
                    "tt_dn.small": 1
                },
                "name": "QA-cluster-5",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster with characters in number of TT and DN
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt_nn.medium": 1,
                    "tt_dn.small": abc
                }, "name": "QA-cluster-6",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster with nonexistent JT and NN
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "abc": 1,
                    "tt_dn.small": 1
                },
                "name": "QA-cluster-7",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster with nonexistent TT and DN
        Given cluster data
        """
        {
            "cluster":
             {
                "node_templates":
                {
                    "jt_nn.medium": 1,
                    "abc": 1
                },
                "name": "QA-cluster-8",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
             }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster with empty value for JT and NN
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "": 1,
                    "tt_dn.small": 1
                },
                "name": "QA-cluster-9",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster with empty value for TT and DN
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {   "jt_nn.medium": 1,
                    "": 1
                },
                "name": "QA-cluster-10",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster without number of JT and NN
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt_nn.medium": ,
                    "tt_dn.small": 1
                },
                "name": "QA-cluster-11",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster without number of TT and DN
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt_nn.medium": 1,
                    "tt_dn.small":
                },
                "name": "QA-cluster-12",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster without JT and NN
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "tt_dn.small": 1
                },
                "name": "QA-cluster-13",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster without (JT, NN) and (TT, DN)
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates": {},
                "name": "QA-cluster-14",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster without node template
        Given cluster data
        """
        {
            "cluster":
            {
                "name": "QA-cluster-15",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster without cluster name
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt_nn.medium": 1,
                    "tt_dn.small": 1
                }, "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster without base image ID
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt_nn.medium": 1,
                    "tt_dn.small": 1
                },
                "name": "QA-cluster-16"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

#-----------------------------------------------------------------------------------------------------------------------

    Scenario: User can not create cluster with negative parameter in number of JT
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                 {
                    "jt.medium": -1,
                    "nn.medium": 1,
                    "tt_dn.small": 1
                 },
                 "name": "QA-cluster-31",
                 "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster with negative parameter in number of NN
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                 {
                    "jt.medium": 1,
                    "nn.medium": -1,
                    "tt_dn.small": 1
                 },
                 "name": "QA-cluster-32",
                 "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster with characters in number of JT
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt.medium": abc,
                    "nn.medium": 1,
                    "tt_dn.small": 1
                },
                "name": "QA-cluster-51",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster with characters in number of NN
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt.medium": 1,
                    "nn.medium": abc,
                    "tt_dn.small": 1
                },
                "name": "QA-cluster-52",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster with nonexistent JT
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "abc": 1,
                    "nn.medium": 1,
                    "tt_dn.small": 1
                },
                "name": "QA-cluster-71",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster with nonexistent NN
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt.medium": 1,
                    "abc": 1,
                    "tt_dn.small": 1
                },
                "name": "QA-cluster-72",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster with empty value for JT
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "": 1,
                    "nn.medium": 1,
                    "tt_dn.small": 1
                },
                "name": "QA-cluster-91",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster with empty value for NN
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt.medium": 1,
                    "": 1,
                    "tt_dn.small": 1
                },
                "name": "QA-cluster-92",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster without number of JT
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt.medium": ,
                    "nn.medium": 1,
                    "tt_dn.small": 1
                },
                "name": "QA-cluster-111",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster without number of NN
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt.medium": 1,
                    "nn.medium": ,
                    "tt_dn.small": 1
                },
                "name": "QA-cluster-112",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster without JT
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "nn.medium": 1,
                    "tt_dn.small": 1
                },
                "name": "QA-cluster-131",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

    Scenario: User can not create cluster without NN
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt.medium": 1,
                    "tt_dn.small": 1
                },
                "name": "QA-cluster-132",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When  User create cluster
        Then  Response is "400"

#-----------------------------------------------------------------------------------------------------------------------

