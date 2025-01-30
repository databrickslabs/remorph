#import pytest
#from unittest.mock import patch, MagicMock
#from databricks.labs.remorph.assessments.configure_assessment import ConfigureAssessment
#from databricks.labs.blueprint.tui import MockPrompts
#
#CHOICES = sorted({"No", "Yes"})
#def test_configure_assessment_no_workspace():
#    prompts = MockPrompts(
#        {
#            r"Do you have an existing Databricks workspace?": str(CHOICES.index("No")),
#        }
#    )
#    with pytest.raises(SystemExit):
#        ConfigureAssessment(product_name = "remorph", prompts = prompts).run()
#
#@patch("webbrowser.open")
#def test_configure_assessment_without_profile(ws):
#    prompts = MockPrompts(
#        {
#            r"Do you have an existing Databricks workspace?": str(CHOICES.index("Yes")),
#            r"Please enter the Databricks workspace host": "http://localhost",
#            r"Confirm that you have created the profile": "no"
#        }
#    )
#
#    with pytest.raises(SystemExit):
#        ConfigureAssessment(product_name = "remorph", prompts = prompts).run()
#
#
#@patch("webbrowser.open")
#def test_configure_assessment_cred(ws):
#    prompts = MockPrompts(
#        {
#            r"Do you have an existing Databricks workspace?": str(CHOICES.index("Yes")),
#            r"Please enter the Databricks workspace host": "http://localhost",
#            r"Confirm that you have created the profile": "yes"
#        }
#    )
#
#
#    ConfigureAssessment(product_name = "remorph", prompts = prompts).run()








