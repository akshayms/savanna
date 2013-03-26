@tags @tag
Feature: Negative tests for get cluster

    Scenario: User can create cluster with name "cluster-QA"
        Given cluster data
        """
        {"cluster": {"node_templates": {"jt_nn.medium": 1, "tt_dn.small": 1}, "name": "cluster-QA", "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"}}
        """
        When User create cluster
        Then  Response is "202"

    Scenario: User can delete cluster with name "cluster-QA" by ID
        When User delete cluster with id: "0"
        Then  Response is "204"

    Scenario: User can not get deleted cluster with name "cluster-QA" by ID #No validation
        #When User get cluster with id: "0"
        #Then  Response is "400"

    Scenario: User can get clusters, if all cluster is delete
        When  User see clusters
        Then  Response is "200"
        And Response list of list clusters:"[]"