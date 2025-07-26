"""
Immune system for the evolution framework.

This module provides pattern matching and threat detection capabilities
for the genomic analysis platform.
"""

import re
import time
from typing import Any, Dict, List, Optional, Pattern, Tuple
from dataclasses import dataclass


@dataclass
class ThreatPattern:
    """
    Represents a threat pattern for immune system detection.
    
    Attributes:
        pattern_id: Unique identifier for the pattern
        regex: Regular expression pattern for matching
        severity: Severity level (1-10, 10 being most severe)
        description: Human-readable description of the threat
        created_at: Timestamp when pattern was created
    """
    pattern_id: str
    regex: str
    severity: int
    description: str
    created_at: float


@dataclass
class ThreatDetection:
    """
    Represents a detected threat.
    
    Attributes:
        detection_id: Unique identifier for the detection
        pattern_id: ID of the pattern that matched
        matched_content: The content that matched the pattern
        severity: Severity level of the detected threat
        timestamp: When the threat was detected
        location: Where the threat was found
    """
    detection_id: str
    pattern_id: str
    matched_content: str
    severity: int
    timestamp: float
    location: str


class ImmuneSystem:
    """
    Immune system for detecting and responding to threats in genomic data.
    
    This class provides pattern matching capabilities to identify potential
    threats, anomalies, or suspicious patterns in genomic analysis data.
    """
    
    def __init__(self) -> None:
        """Initialize the immune system."""
        self.threat_patterns: Dict[str, ThreatPattern] = {}
        self.compiled_patterns: Dict[str, Pattern[str]] = {}
        self.detections: List[ThreatDetection] = []
        self.detection_count = 0
        self.max_detection_history = 1000
        
        # Initialize with default threat patterns
        self._initialize_default_patterns()
    
    def add_threat_pattern(self, pattern_id: str, regex: str, severity: int, 
                          description: str) -> bool:
        """
        Add a new threat pattern to the immune system.
        
        Args:
            pattern_id: Unique identifier for the pattern
            regex: Regular expression pattern for matching
            severity: Severity level (1-10)
            description: Description of what this pattern detects
            
        Returns:
            True if pattern was added successfully, False otherwise
        """
        try:
            # Validate the regex pattern
            compiled_pattern = re.compile(regex)
            
            # Create the threat pattern
            threat_pattern = ThreatPattern(
                pattern_id=pattern_id,
                regex=regex,
                severity=severity,
                description=description,
                created_at=time.time()
            )
            
            # Store the pattern and compiled version
            self.threat_patterns[pattern_id] = threat_pattern
            self.compiled_patterns[pattern_id] = compiled_pattern
            
            return True
            
        except re.error:
            return False
    
    def remove_threat_pattern(self, pattern_id: str) -> bool:
        """
        Remove a threat pattern from the immune system.
        
        Args:
            pattern_id: ID of the pattern to remove
            
        Returns:
            True if pattern was removed, False if not found
        """
        if pattern_id in self.threat_patterns:
            del self.threat_patterns[pattern_id]
            del self.compiled_patterns[pattern_id]
            return True
        return False
    
    def scan_content(self, content: str, location: str = "unknown") -> List[ThreatDetection]:
        """
        Scan content for threats using all registered patterns.
        
        Args:
            content: Content to scan for threats
            location: Description of where the content came from
            
        Returns:
            List of detected threats
        """
        detections = []
        
        for pattern_id, compiled_pattern in self.compiled_patterns.items():
            matches = compiled_pattern.finditer(content)
            
            for match in matches:
                detection = self._create_detection(
                    pattern_id=pattern_id,
                    matched_content=match.group(),
                    location=location
                )
                detections.append(detection)
                self._store_detection(detection)
        
        return detections
    
    def scan_data_dict(self, data: Dict[str, Any], location: str = "data_dict") -> List[ThreatDetection]:
        """
        Scan a dictionary of data for threats.
        
        Args:
            data: Dictionary to scan
            location: Description of the data source
            
        Returns:
            List of detected threats
        """
        detections = []
        
        # Convert dictionary to string representation for scanning
        content = str(data)
        detections.extend(self.scan_content(content, location))
        
        # Also scan individual string values
        for key, value in data.items():
            if isinstance(value, str):
                key_location = f"{location}.{key}"
                detections.extend(self.scan_content(value, key_location))
        
        return detections
    
    def get_pattern_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about threat patterns and detections.
        
        Returns:
            Dictionary containing statistics
        """
        total_patterns = len(self.threat_patterns)
        total_detections = len(self.detections)
        
        # Count detections by severity
        severity_counts = {}
        for detection in self.detections:
            severity = detection.severity
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Count detections by pattern
        pattern_counts = {}
        for detection in self.detections:
            pattern_id = detection.pattern_id
            pattern_counts[pattern_id] = pattern_counts.get(pattern_id, 0) + 1
        
        return {
            'total_patterns': total_patterns,
            'total_detections': total_detections,
            'detections_by_severity': severity_counts,
            'detections_by_pattern': pattern_counts,
            'most_active_pattern': max(pattern_counts.items(), key=lambda x: x[1])[0] if pattern_counts else None
        }
    
    def get_recent_detections(self, limit: int = 10) -> List[ThreatDetection]:
        """
        Get the most recent threat detections.
        
        Args:
            limit: Maximum number of detections to return
            
        Returns:
            List of recent detections
        """
        sorted_detections = sorted(self.detections, key=lambda x: x.timestamp, reverse=True)
        return sorted_detections[:limit]
    
    def clear_detections(self) -> None:
        """Clear all stored threat detections."""
        self.detections.clear()
        self.detection_count = 0
    
    def get_pattern_coverage(self) -> float:
        """
        Calculate pattern coverage (percentage of patterns that have detected threats).
        
        Returns:
            Coverage percentage (0.0 to 100.0)
        """
        if not self.threat_patterns:
            return 0.0
        
        active_patterns = set(detection.pattern_id for detection in self.detections)
        coverage = len(active_patterns) / len(self.threat_patterns) * 100.0
        
        return coverage
    
    def _initialize_default_patterns(self) -> None:
        """Initialize the immune system with default threat patterns."""
        default_patterns = [
            ("sql_injection", r"(?i)(union\s+select|drop\s+table|insert\s+into|delete\s+from)", 8, "SQL injection attempt"),
            ("xss_attack", r"(?i)(<script|javascript:|onload=|onerror=)", 7, "Cross-site scripting attempt"),
            ("path_traversal", r"(\.\.\/|\.\.\\)", 6, "Path traversal attempt"),
            ("suspicious_email", r"[a-zA-Z0-9._%+-]+@(?:tempmail|guerrillamail|10minutemail)", 4, "Suspicious email domain"),
            ("large_numbers", r"\b\d{16,}\b", 3, "Unusually large numbers"),
            ("genomic_anomaly", r"(?i)(mutation_count|variant_frequency):\s*[5-9]\d{2,}", 5, "Potential genomic data anomaly"),
            ("high_risk_gene", r"(?i)(BRCA[12]|TP53|MLH1|MSH2|MSH6)", 6, "High-risk gene variant detected")
        ]
        
        for pattern_id, regex, severity, description in default_patterns:
            self.add_threat_pattern(pattern_id, regex, severity, description)
    
    def _create_detection(self, pattern_id: str, matched_content: str, location: str) -> ThreatDetection:
        """
        Create a new threat detection.
        
        Args:
            pattern_id: ID of the pattern that matched
            matched_content: The content that was matched
            location: Where the threat was detected
            
        Returns:
            New ThreatDetection instance
        """
        self.detection_count += 1
        detection_id = f"det_{self.detection_count:06d}"
        
        threat_pattern = self.threat_patterns[pattern_id]
        
        return ThreatDetection(
            detection_id=detection_id,
            pattern_id=pattern_id,
            matched_content=matched_content,
            severity=threat_pattern.severity,
            timestamp=time.time(),
            location=location
        )
    
    def _store_detection(self, detection: ThreatDetection) -> None:
        """
        Store a threat detection in the history.
        
        Args:
            detection: Detection to store
        """
        self.detections.append(detection)
        
        # Keep only the most recent detections
        if len(self.detections) > self.max_detection_history:
            self.detections = self.detections[-self.max_detection_history:]