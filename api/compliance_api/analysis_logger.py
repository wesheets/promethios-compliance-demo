"""
Analysis Logger Module for Promethios Compliance Demo

This module provides logging functionality for the backend analysis steps,
allowing the frontend to display real-time processing information.
"""

import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional

# Thread-safe log storage
_log_lock = threading.Lock()
_logs = []
_max_logs = 100  # Maximum number of logs to keep in memory

class AnalysisLogger:
    """
    Class for logging analysis steps and events in the Promethios Compliance Demo.
    Provides methods for logging different types of events and retrieving logs.
    """
    
    def __init__(self):
        """Initialize the AnalysisLogger."""
        pass
    
    def log_event(self, event_type: str, message: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log a general event.
        
        Args:
            event_type: Type of event (e.g., compliance_decision, explanation_request)
            message: Human-readable message describing the event
            details: Additional details about the event
            
        Returns:
            The created log entry
        """
        timestamp = datetime.now().isoformat()
        
        # Extract application_id and framework from details if available
        application_id = details.get("application_id", "system")
        framework = details.get("framework", "general")
        
        log_entry = {
            "timestamp": timestamp,
            "step_type": event_type,
            "application_id": application_id,
            "framework": framework,
            "message": message,
            "details": details
        }
        
        with _log_lock:
            _logs.append(log_entry)
            # Trim logs if they exceed the maximum
            if len(_logs) > _max_logs:
                _logs.pop(0)
        
        return log_entry
    
    def get_logs(self, log_type: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get logs with optional filtering.
        
        Args:
            log_type: Filter logs by step type/event type
            limit: Maximum number of logs to return
            
        Returns:
            List of log entries matching the filters
        """
        with _log_lock:
            filtered_logs = _logs.copy()
        
        # Apply filters
        if log_type:
            filtered_logs = [log for log in filtered_logs if log["step_type"] == log_type]
        
        # Sort by timestamp (newest first)
        filtered_logs.sort(key=lambda x: x["timestamp"], reverse=True)
        
        # Apply limit
        return filtered_logs[:limit]
    
    def log_data_quality_analysis(self, application_id: str, framework: str, completeness: float, consistency: float, accuracy: float) -> Dict[str, Any]:
        """
        Log a data quality analysis step.
        
        Args:
            application_id: ID of the application being analyzed
            framework: Regulatory framework being applied
            completeness: Data completeness score (0-1)
            consistency: Data consistency score (0-1)
            accuracy: Data accuracy score (0-1)
            
        Returns:
            The created log entry
        """
        details = {
            "completeness_score": round(completeness, 2),
            "consistency_score": round(consistency, 2),
            "accuracy_score": round(accuracy, 2),
            "overall_score": round((completeness + consistency + accuracy) / 3, 2),
            "analysis_time_ms": int(time.time() * 1000) % 1000  # Simulated analysis time
        }
        
        message = f"Data quality analysis for application {application_id}: Overall score {details['overall_score']}"
        return self.log_event("data_quality", message, {
            "application_id": application_id,
            "framework": framework,
            **details
        })
    
    def log_model_confidence_analysis(self, application_id: str, framework: str, prediction_certainty: float, model_robustness: float) -> Dict[str, Any]:
        """
        Log a model confidence analysis step.
        
        Args:
            application_id: ID of the application being analyzed
            framework: Regulatory framework being applied
            prediction_certainty: Certainty of model predictions (0-1)
            model_robustness: Robustness of the model (0-1)
            
        Returns:
            The created log entry
        """
        details = {
            "prediction_certainty": round(prediction_certainty, 2),
            "model_robustness": round(model_robustness, 2),
            "overall_confidence": round((prediction_certainty + model_robustness) / 2, 2),
            "analysis_time_ms": int(time.time() * 1000) % 1000  # Simulated analysis time
        }
        
        message = f"Model confidence analysis for application {application_id}: Overall confidence {details['overall_confidence']}"
        return self.log_event("model_confidence", message, {
            "application_id": application_id,
            "framework": framework,
            **details
        })
    
    def log_regulatory_alignment_analysis(self, application_id: str, framework: str, requirements_met: int, requirements_total: int) -> Dict[str, Any]:
        """
        Log a regulatory alignment analysis step.
        
        Args:
            application_id: ID of the application being analyzed
            framework: Regulatory framework being applied
            requirements_met: Number of requirements met
            requirements_total: Total number of requirements
            
        Returns:
            The created log entry
        """
        alignment_score = requirements_met / requirements_total if requirements_total > 0 else 0
        
        details = {
            "requirements_met": requirements_met,
            "requirements_total": requirements_total,
            "alignment_score": round(alignment_score, 2),
            "analysis_time_ms": int(time.time() * 1000) % 1000  # Simulated analysis time
        }
        
        message = f"Regulatory alignment analysis for application {application_id}: Score {details['alignment_score']}"
        return self.log_event("regulatory_alignment", message, {
            "application_id": application_id,
            "framework": framework,
            **details
        })
    
    def log_ethical_considerations_analysis(self, application_id: str, framework: str, fairness_score: float, bias_risk: float) -> Dict[str, Any]:
        """
        Log an ethical considerations analysis step.
        
        Args:
            application_id: ID of the application being analyzed
            framework: Regulatory framework being applied
            fairness_score: Fairness score (0-1)
            bias_risk: Risk of bias (0-1)
            
        Returns:
            The created log entry
        """
        details = {
            "fairness_score": round(fairness_score, 2),
            "bias_risk": round(bias_risk, 2),
            "ethical_score": round(fairness_score * (1 - bias_risk), 2),
            "analysis_time_ms": int(time.time() * 1000) % 1000  # Simulated analysis time
        }
        
        message = f"Ethical considerations analysis for application {application_id}: Ethical score {details['ethical_score']}"
        return self.log_event("ethical_considerations", message, {
            "application_id": application_id,
            "framework": framework,
            **details
        })
    
    def log_overall_compliance_decision(self, application_id: str, framework: str, compliant: bool, trust_score: float, explanation: str) -> Dict[str, Any]:
        """
        Log an overall compliance decision.
        
        Args:
            application_id: ID of the application being analyzed
            framework: Regulatory framework being applied
            compliant: Whether the application is compliant
            trust_score: Overall trust score (0-1)
            explanation: Explanation of the decision
            
        Returns:
            The created log entry
        """
        details = {
            "compliant": compliant,
            "trust_score": round(trust_score, 2),
            "explanation": explanation,
            "decision_time_ms": int(time.time() * 1000) % 1000  # Simulated decision time
        }
        
        status = "COMPLIANT" if compliant else "NON-COMPLIANT"
        message = f"Compliance decision for application {application_id}: {status} with trust score {details['trust_score']}"
        return self.log_event("compliance_decision", message, {
            "application_id": application_id,
            "framework": framework,
            **details
        })

# Keep the module-level functions for backward compatibility
def _add_log(step_type: str, application_id: str, framework: str, details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a log entry to the in-memory log store.
    
    Args:
        step_type: Type of analysis step (data_quality, model_confidence, etc.)
        application_id: ID of the application being analyzed
        framework: Regulatory framework being applied
        details: Detailed information about the analysis step
        
    Returns:
        The created log entry
    """
    timestamp = datetime.now().isoformat()
    
    log_entry = {
        "timestamp": timestamp,
        "step_type": step_type,
        "application_id": application_id,
        "framework": framework,
        "details": details
    }
    
    with _log_lock:
        _logs.append(log_entry)
        # Trim logs if they exceed the maximum
        if len(_logs) > _max_logs:
            _logs.pop(0)
    
    return log_entry

def get_logs(limit: int = 50, application_id: Optional[str] = None, step_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get logs with optional filtering.
    
    Args:
        limit: Maximum number of logs to return
        application_id: Filter logs by application ID
        step_type: Filter logs by step type
        
    Returns:
        List of log entries matching the filters
    """
    with _log_lock:
        filtered_logs = _logs.copy()
    
    # Apply filters
    if application_id:
        filtered_logs = [log for log in filtered_logs if log["application_id"] == application_id]
    
    if step_type:
        filtered_logs = [log for log in filtered_logs if log["step_type"] == step_type]
    
    # Sort by timestamp (newest first)
    filtered_logs.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Apply limit
    return filtered_logs[:limit]

def log_data_quality_analysis(application_id: str, framework: str, completeness: float, consistency: float, accuracy: float) -> Dict[str, Any]:
    """
    Log a data quality analysis step.
    
    Args:
        application_id: ID of the application being analyzed
        framework: Regulatory framework being applied
        completeness: Data completeness score (0-1)
        consistency: Data consistency score (0-1)
        accuracy: Data accuracy score (0-1)
        
    Returns:
        The created log entry
    """
    details = {
        "completeness_score": round(completeness, 2),
        "consistency_score": round(consistency, 2),
        "accuracy_score": round(accuracy, 2),
        "overall_score": round((completeness + consistency + accuracy) / 3, 2),
        "analysis_time_ms": int(time.time() * 1000) % 1000  # Simulated analysis time
    }
    
    return _add_log("data_quality", application_id, framework, details)

def log_model_confidence_analysis(application_id: str, framework: str, prediction_certainty: float, model_robustness: float) -> Dict[str, Any]:
    """
    Log a model confidence analysis step.
    
    Args:
        application_id: ID of the application being analyzed
        framework: Regulatory framework being applied
        prediction_certainty: Certainty of model predictions (0-1)
        model_robustness: Robustness of the model (0-1)
        
    Returns:
        The created log entry
    """
    details = {
        "prediction_certainty": round(prediction_certainty, 2),
        "model_robustness": round(model_robustness, 2),
        "overall_confidence": round((prediction_certainty + model_robustness) / 2, 2),
        "analysis_time_ms": int(time.time() * 1000) % 1000  # Simulated analysis time
    }
    
    return _add_log("model_confidence", application_id, framework, details)

def log_regulatory_alignment_analysis(application_id: str, framework: str, requirements_met: int, requirements_total: int) -> Dict[str, Any]:
    """
    Log a regulatory alignment analysis step.
    
    Args:
        application_id: ID of the application being analyzed
        framework: Regulatory framework being applied
        requirements_met: Number of requirements met
        requirements_total: Total number of requirements
        
    Returns:
        The created log entry
    """
    alignment_score = requirements_met / requirements_total if requirements_total > 0 else 0
    
    details = {
        "requirements_met": requirements_met,
        "requirements_total": requirements_total,
        "alignment_score": round(alignment_score, 2),
        "analysis_time_ms": int(time.time() * 1000) % 1000  # Simulated analysis time
    }
    
    return _add_log("regulatory_alignment", application_id, framework, details)

def log_ethical_considerations_analysis(application_id: str, framework: str, fairness_score: float, bias_risk: float) -> Dict[str, Any]:
    """
    Log an ethical considerations analysis step.
    
    Args:
        application_id: ID of the application being analyzed
        framework: Regulatory framework being applied
        fairness_score: Fairness score (0-1)
        bias_risk: Risk of bias (0-1)
        
    Returns:
        The created log entry
    """
    details = {
        "fairness_score": round(fairness_score, 2),
        "bias_risk": round(bias_risk, 2),
        "ethical_score": round(fairness_score * (1 - bias_risk), 2),
        "analysis_time_ms": int(time.time() * 1000) % 1000  # Simulated analysis time
    }
    
    return _add_log("ethical_considerations", application_id, framework, details)

def log_overall_compliance_decision(application_id: str, framework: str, compliant: bool, trust_score: float, explanation: str) -> Dict[str, Any]:
    """
    Log an overall compliance decision.
    
    Args:
        application_id: ID of the application being analyzed
        framework: Regulatory framework being applied
        compliant: Whether the application is compliant
        trust_score: Overall trust score (0-1)
        explanation: Explanation of the decision
        
    Returns:
        The created log entry
    """
    details = {
        "compliant": compliant,
        "trust_score": round(trust_score, 2),
        "explanation": explanation,
        "decision_time_ms": int(time.time() * 1000) % 1000  # Simulated decision time
    }
    
    return _add_log("compliance_decision", application_id, framework, details)
