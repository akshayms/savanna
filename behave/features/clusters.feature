@tags @tag
Feature: Test of cluster section

    Scenario: User can get clusters if list is empty
        When  User see clusters
        Then  Response is "200"
        And Response list of list clusters:"[]"

    Scenario: User can create cluster
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
                "name": "qacluster-1",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When User create cluster
        Then  Response is "202"

    Scenario: User can get clusters, if list has only one cluster
        When  User see clusters
        Then  Response is "200"
        And Response list of list clusters:"[u'qacluster-1']"

    Scenario: User can create cluster
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
                "name": "qacluster-2",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When User create cluster
        Then  Response is "202"

    Scenario: User can get clusters, if list has two cluster
        When  User see clusters
        Then  Response is "200"
        And Response list of list clusters:"[u'qacluster-1', u'qacluster-2']"

    Scenario: User can get cluster by ID
        When User get cluster with id: "0"
        Then  Response is "200"
        And Response for list cluster by id is:"{u'status': u'Active', u'service_urls': {}, u'name': u'qacluster-1', u'base_image_id': u'd9342ba8-4c51-441c-8d5b-f9e14a901299', u'node_templates': {u'jt_nn.medium': 1, u'tt_dn.small': 1}, u'nodes': []}"

    Scenario: User can create cluster
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
                "name": "qacluster-3",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When User create cluster
        Then  Response is "202"

    Scenario: User can get clusters, if list has three cluster
        When  User see clusters
        Then  Response is "200"
        And Response list of list clusters:"[u'qacluster-1', u'qacluster-2', u'qacluster-3']"

    Scenario: User can delete cluster by ID
        When User delete cluster with id: "0"
        Then  Response is "204"

    Scenario: User can get clusters, if one cluster delete
        When  User see clusters
        Then  Response is "200"
        And Response list of list clusters:"[u'qacluster-2', u'qacluster-3']"

    Scenario: User can delete cluster by ID
        When User delete cluster with id: "2"
        Then  Response is "204"

    Scenario: User can get clusters, if one cluster delete
        When  User see clusters
        Then  Response is "200"
        And Response list of list clusters:"[u'qacluster-2']"

    Scenario: User can delete cluster by ID
        When User delete cluster with id: "1"
        Then  Response is "204"

    Scenario: User can get clusters, if all cluster is delete
        When  User see clusters
        Then  Response is "200"
        And Response list of list clusters:"[]"

#----------------------------------------------------------------------------------------------------


    Scenario: User can get clusters if list is empty
        When  User see clusters
        Then  Response is "200"
        And Response list of list clusters:"[]"

    Scenario: User can create cluster
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt.medium": 1,
                    "nn.medium": 1,
                    "tt_dn.small": 1
                },
                "name": "qacluster-1",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When User create cluster
        Then  Response is "202"

    Scenario: User can get clusters, if list has only one cluster
        When  User see clusters
        Then  Response is "200"
        And Response list of list clusters:"[u'qacluster-1']"

    Scenario: User can create cluster
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt.medium": 1,
                    "nn.medium": 1,
                    "tt_dn.small": 1
                },
                "name": "qacluster-2",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When User create cluster
        Then  Response is "202"

    Scenario: User can get clusters, if list has two cluster
        When  User see clusters
        Then  Response is "200"
        And Response list of list clusters:"[u'qacluster-1', u'qacluster-2']"

    Scenario: User can get cluster by ID
        When User get cluster with id: "0"
        Then  Response is "200"
        And Response for list cluster by id is:"{u'status': u'Active', u'service_urls': {}, u'name': u'qacluster-1', u'base_image_id': u'd9342ba8-4c51-441c-8d5b-f9e14a901299', u'node_templates': {u'jt_nn.medium': 1, u'tt_dn.small': 1}, u'nodes': []}"

    Scenario: User can create cluster
        Given cluster data
        """
        {
            "cluster":
            {
                "node_templates":
                {
                    "jt.medium": 1,
                    "nn.medium": 1,
                    "tt_dn.small": 1
                },
                "name": "qacluster-3",
                "base_image_id": "d9342ba8-4c51-441c-8d5b-f9e14a901299"
            }
        }
        """
        When User create cluster
        Then  Response is "202"

    Scenario: User can get clusters, if list has three cluster
        When  User see clusters
        Then  Response is "200"
        And Response list of list clusters:"[u'qacluster-1', u'qacluster-2', u'qacluster-3']"

    Scenario: User can delete cluster by ID
        When User delete cluster with id: "0"
        Then  Response is "204"

    Scenario: User can get clusters, if one cluster delete
        When  User see clusters
        Then  Response is "200"
        And Response list of list clusters:"[u'qacluster-2', u'qacluster-3']"

    Scenario: User can delete cluster by ID
        When User delete cluster with id: "2"
        Then  Response is "204"

    Scenario: User can get clusters, if one cluster delete
        When  User see clusters
        Then  Response is "200"
        And Response list of list clusters:"[u'qacluster-2']"

    Scenario: User can delete cluster by ID
        When User delete cluster with id: "1"
        Then  Response is "204"

    Scenario: User can get clusters, if all cluster is delete
        When  User see clusters
        Then  Response is "200"
        And Response list of list clusters:"[]"