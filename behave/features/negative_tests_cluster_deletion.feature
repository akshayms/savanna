@tags @tag
Feature: Negative tests for cluster deletion

    Scenario: User can create cluster with name "cluster-QA"
        Given cluster data
        """
        {"cluster": {"node_templates": {"jt_nn.medium": 1, "tt_dn.small": 1}, "name": "cluster-QA", "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"}}
        """
        When User create cluster
        Then  Response is "202"

    Scenario: User can get cluster by ID
        When User get cluster with id: "0"
        Then  Response is "200"
        And Response for list cluster by id is:"{u'status': u'Active', u'service_urls': {}, u'name': u'cluster-QA', u'base_image_id': u'd9342ba8-4c51-441c-8d5b-f9e14a901299', u'node_templates': {u'jt_nn.medium': 1, u'tt_dn.small': 1}, u'nodes': []}"


    Scenario: User can delete cluster with name "cluster-QA" by ID
        When User delete cluster with id: "0"
        Then  Response is "204"

    Scenario: User can not delete cluster with name "cluster-QA" by ID #No validation
        #When User delete cluster with id: "0"
        #Then  Response is "404"

    Scenario: User can get clusters, if all cluster is delete
        When  User see clusters
        Then  Response is "200"
        And Response list of list clusters:"[]"