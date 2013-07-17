# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


class UITestCase(unittest2.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://172.18.168.169:8080"
        self.verificationErrors = []
        self.accept_next_alert = True

    def _login(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("admin")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("swordfish")
        driver.find_element_by_xpath("//button[@type='submit']").click()

    def _create_ngt(self):
        driver = self.driver
        driver.get(self.base_url + "/savanna/nodegroup_templates/")
        driver.find_element_by_id("nodegroup_templates__action_create").click()
        for i in range(60):
            if self.is_element_present(
                    By.XPATH, "//*[@id='modal_wrapper']"
                              "/div/form/div[4]/input"):
                break
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_xpath("//*[@id='modal_wrapper']"
                                     "/div/form/div[4]/input").click()
        for i in range(60):
            if self.is_element_present(By.ID, "id_nodegroup_name"):
                break
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_id("id_nodegroup_name").clear()
        driver.find_element_by_id("id_nodegroup_name").send_keys("qa-master")
        driver.find_element_by_id("id_processes_0").click()
        driver.find_element_by_id("id_processes_4").click()
        driver.find_element_by_xpath("//*[@id='modal_wrapper']"
                                     "/div/form/div[4]/input").click()
        time.sleep(1)
        driver.refresh()
        driver.find_element_by_id("nodegroup_templates__action_create").click()
        for i in range(60):
            if self.is_element_present(By.XPATH, "//*[@id='modal_wrapper']"
                                                 "/div/form/div[4]/input"):
                    break
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_xpath("//input[@value='Create']").click()
        for i in range(60):
            if self.is_element_present(By.ID, "id_nodegroup_name"):
                    break
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_id("id_nodegroup_name").clear()
        driver.find_element_by_id("id_nodegroup_name").send_keys("qa-worker")
        driver.find_element_by_id("id_processes_1").click()
        driver.find_element_by_id("id_processes_3").click()
        driver.find_element_by_xpath("//input[@value='Create']").click()
        time.sleep(1)
        driver.refresh()

    def _create_cl_tmpl(self):
        driver = self.driver
        driver.get(self.base_url + "/savanna/cluster_templates/")
        driver.find_element_by_id("cluster_templates__action_create").click()
        for i in range(60):
            if self.is_element_present(By.XPATH, "//*[@id='modal_wrapper']"
                                                 "/div/form/div[4]/input"):
                    break
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_xpath("//input[@value='Create']").click()
        for i in range(60):
            if self.is_element_present(By.ID, "id_cluster_template_name"):
                    break
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_id("id_cluster_template_name").clear()
        driver.find_element_by_id("id_cluster_template_name").\
            send_keys("qa-cluster-template")
        driver.find_element_by_link_text("Node Groups").click()
        driver.find_element_by_xpath("//select[@id='template_id']"
                                     "/option[text()='qa-master']").click()
        driver.find_element_by_id("add_group_button").click()
        driver.find_element_by_xpath("//select[@id='template_id']"
                                     "/option[text()='qa-worker']").click()
        driver.find_element_by_id("add_group_button").click()
        driver.find_element_by_xpath("//input[@value='Create']").click()
        time.sleep(1)
        driver.refresh()

    def _create_cluster(self):
        driver = self.driver
        driver.get(self.base_url + "/savanna/")
        driver.find_element_by_link_text("Clusters").click()
        driver.find_element_by_id("clusters__action_create").click()
        for i in range(60):
            if self.is_element_present(By.XPATH, "//*[@id='modal_wrapper']"
                                                 "/div/form/div[4]/input"):
                    break
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_xpath("//input[@value='Create']").click()
        for i in range(60):
            if self.is_element_present(By.ID, "id_cluster_name"):
                    break
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_id("id_cluster_name").clear()
        driver.find_element_by_id("id_cluster_name").send_keys("qa-cluster")
        driver.find_element_by_xpath("//select[@id='id_keypair']"
                                     "/option[text()='vrovachev']").click()
        driver.find_element_by_xpath("//input[@value='Create']").click()
        time.sleep(1)
        driver.refresh()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True

    # def is_alert_present(self):
    #     try:
    #         self.driver.switch_to_alert()
    #     except NoAlertPresentException, e:
    #         return False
    #     return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)