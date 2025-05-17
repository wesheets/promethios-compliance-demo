"""
Timeline and Compliance History Module

This module provides functionality to track and visualize the compliance history
of loan applications over time.
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime

class ComplianceTimeline:
    """
    A class that manages the compliance history timeline for loan applications.
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize the compliance timeline manager.
        
        Args:
            storage_path: Optional path to a JSON file for storing timeline data
        """
        self.storage_path = storage_path
        self.timelines = {}
        
        # Load existing timelines if storage path is provided
        if storage_path:
            try:
                with open(storage_path, 'r') as f:
                    self.timelines = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                # Initialize empty timelines if file doesn't exist or is invalid
                self.timelines = {}
    
    def add_event(self, application_id: str, event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new event to an application's compliance timeline.
        
        Args:
            application_id: ID of the loan application
            event_type: Type of event (e.g., 'evaluation', 'remediation', 'verification')
            event_data: Dictionary containing event details
            
        Returns:
            The created event dictionary
        """
        # Create timeline for application if it doesn't exist
        if application_id not in self.timelines:
            self.timelines[application_id] = []
        
        # Create the event with timestamp
        timestamp = datetime.now().isoformat()
        event = {
            "id": f"{application_id}_{len(self.timelines[application_id])}",
            "timestamp": timestamp,
            "type": event_type,
            "data": event_data
        }
        
        # Add the event to the timeline
        self.timelines[application_id].append(event)
        
        # Save timelines if storage path is provided
        if self.storage_path:
            try:
                with open(self.storage_path, 'w') as f:
                    json.dump(self.timelines, f, indent=2)
            except Exception as e:
                print(f"Error saving timeline data: {str(e)}")
        
        return event
    
    def get_timeline(self, application_id: str) -> List[Dict[str, Any]]:
        """
        Get the compliance timeline for a specific application.
        
        Args:
            application_id: ID of the loan application
            
        Returns:
            List of event dictionaries in chronological order
        """
        return self.timelines.get(application_id, [])
    
    def get_latest_event(self, application_id: str, event_type: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get the latest event for a specific application, optionally filtered by type.
        
        Args:
            application_id: ID of the loan application
            event_type: Optional type of event to filter by
            
        Returns:
            Latest event dictionary or None if no events exist
        """
        timeline = self.timelines.get(application_id, [])
        
        if not timeline:
            return None
        
        # Filter by event type if specified
        if event_type:
            filtered_timeline = [event for event in timeline if event["type"] == event_type]
            if not filtered_timeline:
                return None
            return filtered_timeline[-1]
        
        # Return the latest event
        return timeline[-1]
    
    def get_compliance_history(self, application_id: str) -> List[Dict[str, Any]]:
        """
        Get the compliance evaluation history for a specific application.
        
        Args:
            application_id: ID of the loan application
            
        Returns:
            List of compliance evaluation events in chronological order
        """
        timeline = self.timelines.get(application_id, [])
        
        # Filter for evaluation events only
        evaluation_events = [event for event in timeline if event["type"] == "evaluation"]
        
        return evaluation_events
    
    def get_remediation_history(self, application_id: str) -> List[Dict[str, Any]]:
        """
        Get the remediation history for a specific application.
        
        Args:
            application_id: ID of the loan application
            
        Returns:
            List of remediation events in chronological order
        """
        timeline = self.timelines.get(application_id, [])
        
        # Filter for remediation events only
        remediation_events = [event for event in timeline if event["type"] == "remediation"]
        
        return remediation_events
    
    def get_compliance_trend(self, application_id: str) -> Dict[str, Any]:
        """
        Calculate the compliance score trend over time for a specific application.
        
        Args:
            application_id: ID of the loan application
            
        Returns:
            Dictionary with timestamps and compliance scores
        """
        evaluation_events = self.get_compliance_history(application_id)
        
        timestamps = []
        scores = []
        
        for event in evaluation_events:
            timestamp = event["timestamp"]
            score = event["data"].get("compliance_score", 0)
            
            timestamps.append(timestamp)
            scores.append(score)
        
        return {
            "timestamps": timestamps,
            "scores": scores
        }
    
    def get_trust_factor_trends(self, application_id: str) -> Dict[str, Any]:
        """
        Calculate the trust factor score trends over time for a specific application.
        
        Args:
            application_id: ID of the loan application
            
        Returns:
            Dictionary with factor names, timestamps, and score series
        """
        evaluation_events = self.get_compliance_history(application_id)
        
        # Initialize result structure
        result = {
            "timestamps": [],
            "factors": {}
        }
        
        for event in evaluation_events:
            timestamp = event["timestamp"]
            result["timestamps"].append(timestamp)
            
            # Extract trust factor scores
            trust_factors = event["data"].get("trust_factors", {}).get("factors", {})
            
            for factor_name, factor_info in trust_factors.items():
                score = factor_info.get("score", 0)
                
                # Initialize factor series if not exists
                if factor_name not in result["factors"]:
                    result["factors"][factor_name] = []
                
                result["factors"][factor_name].append(score)
        
        return result
