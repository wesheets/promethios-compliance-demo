"""
Unit tests for the Compliance Timeline module.

This module contains tests for the compliance history timeline functionality.
"""

import unittest
import sys
import os
import json
import tempfile
from datetime import datetime
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the module to test
from compliance_api.compliance_timeline import ComplianceTimeline

class TestComplianceTimeline(unittest.TestCase):
    """Tests for the ComplianceTimeline class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a timeline without persistent storage
        self.timeline = ComplianceTimeline()
        
        # Sample application ID for testing
        self.application_id = "app_123"
        
        # Sample event data for testing
        self.evaluation_event_data = {
            "is_compliant": False,
            "compliance_score": 65.0,
            "framework": "EU_AI_ACT",
            "primary_reason": "Insufficient data quality",
            "trust_factors": {
                "overall_score": 70.0,
                "factors": {
                    "data_quality": {"score": 60.0},
                    "model_confidence": {"score": 75.0},
                    "regulatory_alignment": {"score": 65.0},
                    "ethical_considerations": {"score": 80.0}
                }
            }
        }
        
        self.remediation_event_data = {
            "action": "Improve data quality",
            "description": "Verified employment information and resolved income data inconsistencies",
            "impact": "Data quality score improved from 60.0 to 85.0"
        }
        
        self.verification_event_data = {
            "verifier": "John Doe",
            "status": "Verified",
            "notes": "All documentation reviewed and approved"
        }
    
    def test_add_event(self):
        """Test adding events to the timeline."""
        # Add an evaluation event
        eval_event = self.timeline.add_event(
            self.application_id, "evaluation", self.evaluation_event_data
        )
        
        # Check that the event was added correctly
        self.assertIn(self.application_id, self.timeline.timelines)
        self.assertEqual(len(self.timeline.timelines[self.application_id]), 1)
        self.assertEqual(self.timeline.timelines[self.application_id][0], eval_event)
        
        # Check that the event has the expected fields
        self.assertIn("id", eval_event)
        self.assertIn("timestamp", eval_event)
        self.assertIn("type", eval_event)
        self.assertIn("data", eval_event)
        self.assertEqual(eval_event["type"], "evaluation")
        self.assertEqual(eval_event["data"], self.evaluation_event_data)
        
        # Add a remediation event
        remed_event = self.timeline.add_event(
            self.application_id, "remediation", self.remediation_event_data
        )
        
        # Check that the event was added correctly
        self.assertEqual(len(self.timeline.timelines[self.application_id]), 2)
        self.assertEqual(self.timeline.timelines[self.application_id][1], remed_event)
        
        # Add a verification event
        verif_event = self.timeline.add_event(
            self.application_id, "verification", self.verification_event_data
        )
        
        # Check that the event was added correctly
        self.assertEqual(len(self.timeline.timelines[self.application_id]), 3)
        self.assertEqual(self.timeline.timelines[self.application_id][2], verif_event)
    
    def test_get_timeline(self):
        """Test getting the timeline for an application."""
        # Add some events
        self.timeline.add_event(self.application_id, "evaluation", self.evaluation_event_data)
        self.timeline.add_event(self.application_id, "remediation", self.remediation_event_data)
        
        # Get the timeline
        timeline = self.timeline.get_timeline(self.application_id)
        
        # Check that the timeline contains the expected events
        self.assertEqual(len(timeline), 2)
        self.assertEqual(timeline[0]["type"], "evaluation")
        self.assertEqual(timeline[1]["type"], "remediation")
        
        # Check that getting a non-existent timeline returns an empty list
        self.assertEqual(self.timeline.get_timeline("non_existent"), [])
    
    def test_get_latest_event(self):
        """Test getting the latest event for an application."""
        # Add some events
        self.timeline.add_event(self.application_id, "evaluation", self.evaluation_event_data)
        self.timeline.add_event(self.application_id, "remediation", self.remediation_event_data)
        
        # Get the latest event
        latest = self.timeline.get_latest_event(self.application_id)
        
        # Check that the latest event is the remediation event
        self.assertEqual(latest["type"], "remediation")
        
        # Get the latest event of a specific type
        latest_eval = self.timeline.get_latest_event(self.application_id, "evaluation")
        
        # Check that the latest evaluation event is returned
        self.assertEqual(latest_eval["type"], "evaluation")
        
        # Check that getting a non-existent event returns None
        self.assertIsNone(self.timeline.get_latest_event("non_existent"))
        self.assertIsNone(self.timeline.get_latest_event(self.application_id, "non_existent"))
    
    def test_get_compliance_history(self):
        """Test getting the compliance evaluation history for an application."""
        # Add some events of different types
        self.timeline.add_event(self.application_id, "evaluation", self.evaluation_event_data)
        self.timeline.add_event(self.application_id, "remediation", self.remediation_event_data)
        self.timeline.add_event(self.application_id, "evaluation", self.evaluation_event_data)
        
        # Get the compliance history
        history = self.timeline.get_compliance_history(self.application_id)
        
        # Check that only evaluation events are returned
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["type"], "evaluation")
        self.assertEqual(history[1]["type"], "evaluation")
    
    def test_get_remediation_history(self):
        """Test getting the remediation history for an application."""
        # Add some events of different types
        self.timeline.add_event(self.application_id, "evaluation", self.evaluation_event_data)
        self.timeline.add_event(self.application_id, "remediation", self.remediation_event_data)
        self.timeline.add_event(self.application_id, "evaluation", self.evaluation_event_data)
        self.timeline.add_event(self.application_id, "remediation", self.remediation_event_data)
        
        # Get the remediation history
        history = self.timeline.get_remediation_history(self.application_id)
        
        # Check that only remediation events are returned
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["type"], "remediation")
        self.assertEqual(history[1]["type"], "remediation")
    
    def test_get_compliance_trend(self):
        """Test calculating the compliance score trend over time."""
        # Add some evaluation events with different scores
        self.timeline.add_event(self.application_id, "evaluation", {
            "compliance_score": 65.0,
            "framework": "EU_AI_ACT"
        })
        self.timeline.add_event(self.application_id, "remediation", self.remediation_event_data)
        self.timeline.add_event(self.application_id, "evaluation", {
            "compliance_score": 75.0,
            "framework": "EU_AI_ACT"
        })
        self.timeline.add_event(self.application_id, "remediation", self.remediation_event_data)
        self.timeline.add_event(self.application_id, "evaluation", {
            "compliance_score": 85.0,
            "framework": "EU_AI_ACT"
        })
        
        # Get the compliance trend
        trend = self.timeline.get_compliance_trend(self.application_id)
        
        # Check that the trend contains the expected data
        self.assertIn("timestamps", trend)
        self.assertIn("scores", trend)
        self.assertEqual(len(trend["timestamps"]), 3)
        self.assertEqual(len(trend["scores"]), 3)
        self.assertEqual(trend["scores"], [65.0, 75.0, 85.0])
    
    def test_get_trust_factor_trends(self):
        """Test calculating the trust factor score trends over time."""
        # Add some evaluation events with different trust factor scores
        self.timeline.add_event(self.application_id, "evaluation", {
            "trust_factors": {
                "factors": {
                    "data_quality": {"score": 60.0},
                    "model_confidence": {"score": 70.0}
                }
            }
        })
        self.timeline.add_event(self.application_id, "evaluation", {
            "trust_factors": {
                "factors": {
                    "data_quality": {"score": 70.0},
                    "model_confidence": {"score": 75.0}
                }
            }
        })
        self.timeline.add_event(self.application_id, "evaluation", {
            "trust_factors": {
                "factors": {
                    "data_quality": {"score": 80.0},
                    "model_confidence": {"score": 80.0}
                }
            }
        })
        
        # Get the trust factor trends
        trends = self.timeline.get_trust_factor_trends(self.application_id)
        
        # Check that the trends contain the expected data
        self.assertIn("timestamps", trends)
        self.assertIn("factors", trends)
        self.assertEqual(len(trends["timestamps"]), 3)
        self.assertIn("data_quality", trends["factors"])
        self.assertIn("model_confidence", trends["factors"])
        self.assertEqual(trends["factors"]["data_quality"], [60.0, 70.0, 80.0])
        self.assertEqual(trends["factors"]["model_confidence"], [70.0, 75.0, 80.0])
    
    def test_persistent_storage(self):
        """Test that timelines can be saved to and loaded from a file."""
        # Create a temporary file for storage
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp_path = temp.name
        
        try:
            # Create a timeline with persistent storage
            timeline = ComplianceTimeline(storage_path=temp_path)
            
            # Add some events
            timeline.add_event(self.application_id, "evaluation", self.evaluation_event_data)
            timeline.add_event(self.application_id, "remediation", self.remediation_event_data)
            
            # Create a new timeline instance that should load from the file
            new_timeline = ComplianceTimeline(storage_path=temp_path)
            
            # Check that the events were loaded correctly
            self.assertIn(self.application_id, new_timeline.timelines)
            self.assertEqual(len(new_timeline.timelines[self.application_id]), 2)
            self.assertEqual(new_timeline.timelines[self.application_id][0]["type"], "evaluation")
            self.assertEqual(new_timeline.timelines[self.application_id][1]["type"], "remediation")
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_persistent_storage_error_handling(self):
        """Test handling of errors when saving to or loading from a file."""
        # Create a timeline with an invalid storage path
        timeline = ComplianceTimeline(storage_path="/non/existent/directory/file.json")
        
        # Add an event (should not raise an error despite invalid path)
        event = timeline.add_event(self.application_id, "evaluation", self.evaluation_event_data)
        
        # Check that the event was added correctly in memory
        self.assertIn(self.application_id, timeline.timelines)
        self.assertEqual(len(timeline.timelines[self.application_id]), 1)
        self.assertEqual(timeline.timelines[self.application_id][0], event)

if __name__ == "__main__":
    unittest.main()
